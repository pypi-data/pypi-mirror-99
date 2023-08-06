#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rule_engine/ast.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import collections
import collections.abc
import datetime
import decimal
import functools
import math
import operator
import re

from . import errors

import dateutil.parser

NoneType = type(None)

def _to_decimal(value):
	if isinstance(value, decimal.Decimal):
		return value
	return decimal.Decimal(repr(value))

def coerce_value(value, verify_type=True):
	"""
	Take a native Python *value* and convert it to a value of a data type which can be represented by a Rule Engine
	:py:class:`~.DataType`. This function is useful for converting native Python values at the engine boundaries such as
	when resolving a symbol from an object external to the engine.

	.. versionadded:: 2.0.0

	:param value: The value to convert.
	:param bool verify_type: Whether or not to verify the converted value's type.
	:return: The converted value.
	"""
	# ARRAY
	if isinstance(value, (list, range, tuple)):
		value = tuple(coerce_value(v, verify_type=verify_type) for v in value)
	# DATETIME
	elif isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
		value = datetime.datetime(value.year, value.month, value.day)
	# FLOAT
	elif isinstance(value, (float, int)) and not isinstance(value, bool):
		value = _to_decimal(value)
	# MAPPING
	elif isinstance(value, (dict, collections.OrderedDict)):
		value = collections.OrderedDict(
			(coerce_value(k, verify_type=verify_type), coerce_value(v, verify_type=verify_type)) for k, v in value.items()
		)
	if verify_type:
		DataType.from_value(value)  # use this to raise a TypeError, if the type is incompatible
	return value

def is_integer_number(value):
	"""
	Check whether *value* is an integer number (i.e. a whole, number). This can, for example, be used to check if a
	floating point number such as ``3.0`` can safely be converted to an integer without loss of information.

	.. versionadded:: 2.1.0

	:param value: The value to check. This value is a native Python type.
	:return: Whether or not the value is an integer number.
	:rtype: bool
	"""
	if not is_real_number(value):
		return False
	if math.floor(value) != value:
		return False
	return True

def is_natural_number(value):
	"""
	Check whether *value* is a natural number (i.e. a whole, non-negative number). This can, for example, be used to
	check if a floating point number such as ``3.0`` can safely be converted to an integer without loss of information.

	:param value: The value to check. This value is a native Python type.
	:return: Whether or not the value is a natural number.
	:rtype: bool
	"""
	if not is_integer_number(value):
		return False
	if value < 0:
		return False
	return True

def is_real_number(value):
	"""
	Check whether *value* is a real number (i.e. capable of being represented as a floating point value without loss of
	information as well as being finite). Despite being able to be represented as a float, ``NaN`` is not considered a
	real number for the purposes of this function.

	:param value: The value to check. This value is a native Python type.
	:return: Whether or not the value is a natural number.
	:rtype: bool
	"""
	if not is_numeric(value):
		return False
	if not math.isfinite(value):
		return False
	return True

def is_numeric(value):
	"""
	Check whether *value* is a numeric value (i.e. capable of being represented as a floating point value without loss
	of information).

	:param value: The value to check. This value is a native Python type.
	:return: Whether or not the value is numeric.
	:rtype: bool
	"""
	if not isinstance(value, (decimal.Decimal, float, int)):
		return False
	if isinstance(value, bool):
		return False
	return True

def _iterable_member_value_type(python_value):
	"""
	Take a native *python_value* and return the corresponding data type if type of each of its members are either the
	same or NULL. NULL is considered a special case to allow nullable-values. This by extension means that an iterable
	may not be defined as only capable of containing NULL values.

	:return: The data type of the sequence members. This will never be NULL, because that is considered a special case.
		It will either be UNSPECIFIED or one of the other types.
	"""
	subvalue_types = set()
	for subvalue in python_value:
		if isinstance(subvalue, ExpressionBase):
			subvalue_type = subvalue.result_type
		else:
			subvalue_type = DataType.from_value(subvalue)
		subvalue_types.add(subvalue_type)
	if DataType.NULL in subvalue_types:
		# treat NULL as a special case, allowing typed arrays to be a specified type *or* NULL
		# this however makes it impossible to define an array with a type of NULL
		subvalue_types.remove(DataType.NULL)
	if len(subvalue_types) == 1:
		subvalue_type = subvalue_types.pop()
	else:
		subvalue_type = DataType.UNDEFINED
	return subvalue_type

def _assert_is_integer_number(*values):
	if not all(map(is_integer_number, values)):
		raise errors.EvaluationError('data type mismatch (not an integer number)')

def _assert_is_natural_number(*values):
	if not all(map(is_natural_number, values)):
		raise errors.EvaluationError('data type mismatch (not a natural number)')

def _assert_is_numeric(*values):
	if not all(map(is_numeric, values)):
		raise errors.EvaluationError('data type mismatch (not a numeric value)')

def _is_reduced(*values):
	"""
	Check if the ast expression *value* is a literal expression and if it is a compound datatype, that all of it's
	members are reduced literals. A value that causes this to evaluate to True for is able to be evaluated without a
	*thing*.
	"""
	return all((isinstance(value, LiteralExpressionBase) and value.is_reduced) for value in values)

class _DataTypeDef(object):
	__slots__ = ('name', 'python_type', 'is_scalar')
	def __init__(self, name, python_type):
		self.name = name
		self.python_type = python_type
		self.is_scalar = True

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self.name == other.name

	def __hash__(self):
		return hash((self.python_type, self.is_scalar))

	def __repr__(self):
		return "<{} name={} python_type={} >".format(self.__class__.__name__, self.name,  self.python_type.__name__)

	@property
	def is_compound(self):
		return not self.is_scalar

_DATA_TYPE_UNDEFINED = _DataTypeDef('UNDEFINED', errors.UNDEFINED)
class _CollectionDataTypeDef(_DataTypeDef):
	__slots__ = ('value_type', 'value_type_nullable')
	def __init__(self, name, python_type, value_type=_DATA_TYPE_UNDEFINED, value_type_nullable=True):
		# check these three classes individually instead of using Collection which isn't available before Python v3.6
		if not issubclass(python_type, collections.abc.Container):
			raise TypeError('the specified python_type is not a container')
		if not issubclass(python_type, collections.abc.Iterable):
			raise TypeError('the specified python_type is not an iterable')
		if not issubclass(python_type, collections.abc.Sized):
			raise TypeError('the specified python_type is not a sized')
		super(_CollectionDataTypeDef, self).__init__(name, python_type)
		self.is_scalar = False
		self.value_type = value_type
		self.value_type_nullable = value_type_nullable

	def __call__(self, value_type, value_type_nullable=True):
		return self.__class__(
			self.name,
			self.python_type,
			value_type=value_type,
			value_type_nullable=value_type_nullable
		)

	def __repr__(self):
		return "<{} name={} python_type={} value_type={} >".format(
			self.__class__.__name__,
			self.name,
			self.python_type.__name__,
			self.value_type.name
		)

	def __eq__(self, other):
		if not super().__eq__(other):
			return False
		return all((
			self.value_type == other.value_type,
			self.value_type_nullable == other.value_type_nullable
		))

	def __hash__(self):
		return hash((self.python_type, self.is_scalar, hash((self.value_type, self.value_type_nullable))))

class _ArrayDataTypeDef(_CollectionDataTypeDef):
	pass

class _SetDataTypeDef(_CollectionDataTypeDef):
	pass

class _MappingDataTypeDef(_DataTypeDef):
	__slots__ = ('key_type', 'value_type', 'value_type_nullable')
	def __init__(self, name, python_type, key_type=_DATA_TYPE_UNDEFINED, value_type=_DATA_TYPE_UNDEFINED, value_type_nullable=True):
		if not issubclass(python_type, collections.abc.Mapping):
			raise TypeError('the specified python_type is not a mapping')
		super(_MappingDataTypeDef, self).__init__(name, python_type)
		self.is_scalar = False
		# ARRAY is the only compound data type that can be used as a mapping key, this is because ARRAY's are backed by
		# Python tuple's while SET and MAPPING objects are set and dict instances, respectively which are not hashable.
		if key_type.is_compound and not isinstance(key_type, DataType.ARRAY.__class__):
			raise errors.EngineError("the {} data type may not be used for mapping keys".format(key_type.name))
		self.key_type = key_type
		self.value_type = value_type
		self.value_type_nullable = value_type_nullable

	def __call__(self, key_type, value_type=_DATA_TYPE_UNDEFINED, value_type_nullable=True):
		return self.__class__(
			self.name,
			self.python_type,
			key_type=key_type,
			value_type=value_type,
			value_type_nullable=value_type_nullable
		)

	def __repr__(self):
		return "<{} name={} python_type={} key_type={} value_type={} >".format(
			self.__class__.__name__,
			self.name,
			self.python_type.__name__,
			self.key_type.name,
			self.value_type.name
		)

	def __eq__(self, other):
		if not super().__eq__(other):
			return False
		return all((
			self.key_type == other.key_type,
			self.value_type == other.value_type,
			self.value_type_nullable == other.value_type_nullable
		))

	def __hash__(self):
		return hash((self.python_type, self.is_scalar, hash((self.key_type, self.value_type, self.value_type_nullable))))

class DataTypeMeta(type):
	def __new__(metacls, cls, bases, classdict):
		data_type = super().__new__(metacls, cls, bases, classdict)
		data_type._member_map_ = collections.OrderedDict()
		for key, value in classdict.items():
			if not isinstance(value, _DataTypeDef):
				continue
			data_type._member_map_[key] = value
		return data_type

	def __contains__(self, item):
		return item in self._member_map_

	def __getitem__(cls, item):
		return cls._member_map_[item]

	def __iter__(cls):
		yield from cls._member_map_

	def __len__(cls):
		return len(cls._member_map_)

class DataType(metaclass=DataTypeMeta):
	"""
	A collection of constants representing the different supported data types. There are three ways to compare data
	types. All three are effectively the same when dealing with scalars.

	Equality checking
	  .. code-block::

	    dt == DataType.TYPE
	  This is the most explicit form of testing and when dealing with compound data types, it recursively checks that
	  all of the member types are also equal.

	Class checking
	  .. code-block::

	    isinstance(dt, DataType.TYPE.__class__)
	  This checks that the data types are the same but when dealing with compound data types, the member types are
	  ignored.

	Compatibility checking
	  .. code-block::

	    DataType.is_compatible(dt, DataType.TYPE)
	  This checks that the types are compatible without any kind of conversion. When dealing with compound data types,
	  this ensures that the member types are either the same or :py:attr:`~.UNDEFINED`.
	"""
	ARRAY = _ArrayDataTypeDef('ARRAY', tuple)
	"""
	.. py:function:: __call__(value_type, value_type_nullable=True)
	
	:param value_type: The type of the array members.
	:param bool value_type_nullable: Whether or not array members are allowed to be :py:attr:`.NULL`.
	"""
	BOOLEAN = _DataTypeDef('BOOLEAN', bool)
	DATETIME = _DataTypeDef('DATETIME', datetime.datetime)
	FLOAT = _DataTypeDef('FLOAT', decimal.Decimal)
	MAPPING = _MappingDataTypeDef('MAPPING', dict)
	"""
	.. py:function:: __call__(key_type, value_type, value_type_nullable=True)
	
	:param key_type: The type of the mapping keys.
	:param value_type: The type of the mapping values.
	:param bool value_type_nullable: Whether or not mapping values are allowed to be :py:attr:`.NULL`.
	"""
	NULL = _DataTypeDef('NULL', NoneType)
	SET = _SetDataTypeDef('SET', set)
	"""
	.. py:function:: __call__(value_type, value_type_nullable=True)

	:param value_type: The type of the set members.
	:param bool value_type_nullable: Whether or not set members are allowed to be :py:attr:`.NULL`.
	"""
	STRING = _DataTypeDef('STRING', str)
	UNDEFINED = _DATA_TYPE_UNDEFINED
	"""
	Undefined values. This constant can be used to indicate that a particular symbol is valid, but it's data type is
	currently unknown.
	"""
	@classmethod
	def from_name(cls, name):
		"""
		Get the data type from its name.

		.. versionadded:: 2.0.0

		:param str name: The name of the data type to retrieve.
		:return: One of the constants.
		"""
		if not isinstance(name, str):
			raise TypeError('from_name argument 1 must be str, not ' + type(name).__name__)
		dt = getattr(cls, name, None)
		if not isinstance(dt, _DataTypeDef):
			raise ValueError("can not map name {0!r} to a compatible data type".format(name))
		return dt

	@classmethod
	def from_type(cls, python_type):
		"""
		Get the supported data type constant for the specified Python type. If the type can not be mapped to a supported
		data type, then a :py:exc:`ValueError` exception will be raised. This function will not return
		:py:attr:`.UNDEFINED`.

		:param type python_type: The native Python type to retrieve the corresponding type constant for.
		:return: One of the constants.
		"""
		if not isinstance(python_type, type):
			raise TypeError('from_type argument 1 must be type, not ' + type(python_type).__name__)
		if python_type in (list, range, tuple):
			return cls.ARRAY
		elif python_type is bool:
			return cls.BOOLEAN
		elif python_type is datetime.date or python_type is datetime.datetime:
			return cls.DATETIME
		elif python_type in (decimal.Decimal, float, int):
			return cls.FLOAT
		elif python_type is dict:
			return cls.MAPPING
		elif python_type is NoneType:
			return cls.NULL
		elif python_type is set:
			return cls.SET
		elif python_type is str:
			return cls.STRING
		raise ValueError("can not map python type {0!r} to a compatible data type".format(python_type.__name__))

	@classmethod
	def from_value(cls, python_value):
		"""
		Get the supported data type constant for the specified Python value. If the value can not be mapped to a
		supported data type, then a :py:exc:`TypeError` exception will be raised. This function will not return
		:py:attr:`.UNDEFINED`.

		:param python_value: The native Python value to retrieve the corresponding data type constant for.
		:return: One of the constants.
		"""
		if isinstance(python_value, bool):
			return cls.BOOLEAN
		elif isinstance(python_value, (datetime.date, datetime.datetime)):
			return cls.DATETIME
		elif isinstance(python_value, (decimal.Decimal, float, int)):
			return cls.FLOAT
		elif python_value is None:
			return cls.NULL
		elif isinstance(python_value, (set,)):
			return cls.SET(value_type=_iterable_member_value_type(python_value))
		elif isinstance(python_value, (str,)):
			return cls.STRING
		elif isinstance(python_value, collections.abc.Mapping):
			return cls.MAPPING(
				key_type=_iterable_member_value_type(python_value.keys()),
				value_type=_iterable_member_value_type(python_value.values())
			)
		elif isinstance(python_value, collections.abc.Sequence):
			return cls.ARRAY(value_type=_iterable_member_value_type(python_value))
		raise TypeError("can not map python type {0!r} to a compatible data type".format(type(python_value).__name__))

	@classmethod
	def is_compatible(cls, dt1, dt2):
		"""
		Check if two data type definitions are compatible without any kind of conversion. This evaluates to ``True``
		when one or both are :py:attr:`.UNDEFINED` or both types are the same. In the case of compound data types (such
		as :py:attr:`.ARRAY`) the member types are checked recursively in the same manner.

		.. versionadded:: 2.1.0

		:param dt1: The first data type to compare.
		:param dt2: The second data type to compare.
		:return: Whether or not the two types are compatible.
		:rtype: bool
		"""
		if not (cls.is_definition(dt1) and cls.is_definition(dt2)):
			raise TypeError('argument is not a data type definition')
		if dt1 is _DATA_TYPE_UNDEFINED or dt2 is _DATA_TYPE_UNDEFINED:
			return True
		if dt1.is_scalar and dt2.is_scalar:
			return dt1 == dt2
		elif dt1.is_compound and dt2.is_compound:
			if isinstance(dt1, DataType.ARRAY.__class__) and isinstance(dt2, DataType.ARRAY.__class__):
				return cls.is_compatible(dt1.value_type, dt2.value_type)
			elif isinstance(dt1, DataType.MAPPING.__class__) and isinstance(dt2, DataType.MAPPING.__class__):
				if not cls.is_compatible(dt1.key_type, dt2.key_type):
					return False
				if not cls.is_compatible(dt1.value_type, dt2.value_type):
					return False
				return True
			elif isinstance(dt1, DataType.SET.__class__) and isinstance(dt2, DataType.SET.__class__):
				return cls.is_compatible(dt1.value_type, dt2.value_type)
		return False

	@classmethod
	def is_definition(cls, value):
		"""
		Check if *value* is a data type definition.

		.. versionadded:: 2.1.0

		:param value: The value to check.
		:return: ``True`` if *value* is a data type definition.
		:rtype: bool
		"""
		return isinstance(value, _DataTypeDef)

class ASTNodeBase(object):
	def to_graphviz(self, digraph):
		digraph.node(str(id(self)), self.__class__.__name__)

################################################################################
# Base Expression Classes
################################################################################
class ExpressionBase(ASTNodeBase):
	__slots__ = ('context',)
	result_type = DataType.UNDEFINED
	"""The data type of the result of successful evaluation."""
	def __repr__(self):
		return "<{0} >".format(self.__class__.__name__)

	def evaluate(self, thing):
		"""
		Evaluate this AST node and all applicable children nodes.

		:param thing: The object to use for symbol resolution.
		:return: The result of the evaluation as a native Python type.
		"""
		raise NotImplementedError()

	def reduce(self):
		"""
		Reduce this expression into a smaller subset of nodes. If the expression can not be reduced, then return an
		instance of itself, otherwise return a reduced :py:class:`.ExpressionBase` to replace it.

		:return: Either a reduced version of this node or itself.
		:rtype: :py:class:`.ExpressionBase`
		"""
		return self

class LiteralExpressionBase(ExpressionBase):
	"""A base class for representing literal values from the grammar text."""
	__slots__ = ('value',)
	is_reduced = True
	def __init__(self, context, value):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param value: The native Python value.
		"""
		self.context = context
		if not isinstance(value, self.result_type.python_type) and self.result_type.is_scalar:
			raise TypeError("__init__ argument 2 must be {}, not {}".format(self.result_type.python_type.__name__, type(value).__name__))
		self.value = value

	def __repr__(self):
		return "<{0} value={1!r} >".format(self.__class__.__name__, self.value)

	@classmethod
	def from_value(cls, context, value):
		"""
		Create a Literal Expression instance to represent the specified *value*.

		.. versionadded:: 2.0.0

		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param value: The value to represent as a Literal Expression.
		:return: A subclass of :py:class:`~.LiteralExpressionBase` specific to the type of *value*.
		"""
		datatype = DataType.from_value(value)
		for subclass in cls.__subclasses__():
			if subclass.__name__.startswith('_'):
				continue
			if DataType.is_compatible(subclass.result_type, datatype):
				break
		else:
			raise errors.EngineError("can not create literal expression from python value: {!r}".format(value))
		if datatype.is_compound:
			if isinstance(datatype, _CollectionDataTypeDef):
				value = datatype.python_type(cls.from_value(context, v) for v in value)
			elif isinstance(datatype, DataType.MAPPING.__class__):
				value = tuple((cls.from_value(context, k), cls.from_value(context, v)) for k, v in value.items())
		else:
			value = coerce_value(value)
		return subclass(context, value)

	def evaluate(self, thing):
		return self.value

	def to_graphviz(self, digraph, *args, **kwargs):
		if self.result_type.is_compound:
			digraph.node(str(id(self)), self.__class__.__name__)
		else:
			digraph.node(str(id(self)), "{}\nvalue={!r}".format(self.__class__.__name__, self.value))

################################################################################
# Literal Expressions
################################################################################
class _CollectionMixin(object):
	def evaluate(self, thing):
		return self.result_type.python_type(member.evaluate(thing) for member in self.value)

	@property
	def is_reduced(self):
		return _is_reduced(*self.value)

	def to_graphviz(self, digraph, *args, **kwargs):
		super(_CollectionMixin, self).to_graphviz(digraph, *args, **kwargs)
		for member in self.value:
			member.to_graphviz(digraph, *args, **kwargs)
			digraph.edge(str(id(self)), str(id(member)))

class ArrayExpression(_CollectionMixin, LiteralExpressionBase):
	"""Literal array expressions containing 0 or more sub-expressions."""
	result_type = DataType.ARRAY
	def __init__(self, *args, **kwargs):
		super(ArrayExpression, self).__init__(*args, **kwargs)
		self.result_type = DataType.ARRAY(value_type=_iterable_member_value_type(self.value))

class BooleanExpression(LiteralExpressionBase):
	"""Literal boolean expressions representing True or False."""
	result_type = DataType.BOOLEAN

class DatetimeExpression(LiteralExpressionBase):
	"""
	Literal datetime expressions representing a specific point in time. This expression type always evaluates to true.
	"""
	result_type = DataType.DATETIME
	@classmethod
	def from_string(cls, context, string):
		try:
			dt = dateutil.parser.isoparse(string)
		except ValueError:
			raise errors.DatetimeSyntaxError('invalid datetime', string)
		if dt.tzinfo is None:
			dt = dt.replace(tzinfo=context.default_timezone)
		return cls(context, dt)

class FloatExpression(LiteralExpressionBase):
	"""Literal float expressions representing numerical values."""
	result_type = DataType.FLOAT
	def __init__(self, context, value, **kwargs):
		value = _to_decimal(value)
		super(FloatExpression, self).__init__(context, value, **kwargs)

class MappingExpression(LiteralExpressionBase):
	"""Literal mapping expression representing a set of associations between keys and values."""
	result_type = DataType.MAPPING
	def __init__(self, context, value, **kwargs):
		if isinstance(value, dict):
			value = tuple(value.items())
		super(MappingExpression, self).__init__(context, value, **kwargs)
		self.result_type = DataType.MAPPING(
			key_type=_iterable_member_value_type(key for key, _ in self.value),
			value_type=_iterable_member_value_type(value for _, value in self.value)
		)

	def evaluate(self, thing):
		mapping = collections.OrderedDict()
		for key, value in self.value:
			key = key.evaluate(thing)
			key_type = DataType.from_value(key)
			if key_type.is_compound and not isinstance(key_type, DataType.ARRAY.__class__):
				raise errors.EngineError("the {} data type may not be used for mapping keys".format(key_type.name))
			mapping[key] = value
		# defer value evaluation to avoid evaluating values of duplicate keys
		for key, value in mapping.items():
			mapping[key] = value.evaluate(thing)
		return mapping

	@property
	def is_reduced(self):
		return all(_is_reduced(key, value) for key, value in self.value)

class NullExpression(LiteralExpressionBase):
	"""Literal null expressions representing null values. This expression type always evaluates to false."""
	result_type = DataType.NULL
	def __init__(self, context, value=None):
		# all of the literal expressions take a value
		if value is not None:
			raise TypeError('value must be None')
		super(NullExpression, self).__init__(context, value=None)

class SetExpression(_CollectionMixin, LiteralExpressionBase):
	"""Literal set expressions containing 0 or more sub-expressions."""
	result_type = DataType.SET
	def __init__(self, *args, **kwargs):
		super(SetExpression, self).__init__(*args, **kwargs)
		self.result_type = DataType.SET(value_type=_iterable_member_value_type(self.value))

class StringExpression(LiteralExpressionBase):
	"""Literal string expressions representing an array of characters."""
	result_type = DataType.STRING

################################################################################
# Left-Operator-Right Expressions
################################################################################
class LeftOperatorRightExpressionBase(ExpressionBase):
	"""
	A base class for representing complex expressions composed of a left side and a right side, separated by an
	operator.
	"""
	compatible_types = (DataType.ARRAY, DataType.BOOLEAN, DataType.DATETIME, DataType.FLOAT, DataType.MAPPING, DataType.NULL, DataType.SET, DataType.STRING)
	"""
	A tuple containing the compatible data types that the left and right expressions must return. This can for example
	be used to indicate that arithmetic operations are compatible with :py:attr:`~.DataType.FLOAT` but not
	:py:attr:`~.DataType.STRING` values.
	"""
	result_type = DataType.BOOLEAN
	def __init__(self, context, type_, left, right):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param str type_: The grammar type of operator at the center of the expression. Subclasses must define operator
			methods to handle evaluation based on this value.
		:param left: The expression to the left of the operator.
		:type left: :py:class:`.ExpressionBase`
		:param right: The expression to the right of the operator.
		:type right: :py:class:`.ExpressionBase`
		"""
		self.context = context
		type_ = type_.lower()
		self.type = type_
		self._evaluator = getattr(self, '_op_' + type_, None)
		if self._evaluator is None:
			raise errors.EngineError('unsupported operator: ' + type_)
		self._assert_type_is_compatible(left)
		self.left = left
		self._assert_type_is_compatible(right)
		self.right = right

	def _assert_type_is_compatible(self, value):
		if value.result_type == DataType.UNDEFINED:
			return
		if any(DataType.is_compatible(dt, value.result_type) for dt in self.compatible_types):
			return
		raise errors.EvaluationError('data type mismatch')

	def __repr__(self):
		return "<{} type={!r} >".format(self.__class__.__name__, self.type)

	def evaluate(self, thing):
		return self._evaluator(thing)

	def reduce(self):
		if not _is_reduced(self.left, self.right):
			return self
		return LiteralExpressionBase.from_value(self.context, self.evaluate(None))

	def to_graphviz(self, digraph, *args, **kwargs):
		digraph.node(str(id(self)), "{}\ntype={!r}".format(self.__class__.__name__, self.type))
		self.left.to_graphviz(digraph, *args, **kwargs)
		self.right.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.left)), label='left')
		digraph.edge(str(id(self)), str(id(self.right)), label='right')

class ArithmeticExpression(LeftOperatorRightExpressionBase):
	"""A class for representing arithmetic expressions from the grammar text such as addition and subtraction."""
	compatible_types = (DataType.FLOAT,)
	result_type = DataType.FLOAT
	def __op_arithmetic(self, op, thing):
		left_value = self.left.evaluate(thing)
		_assert_is_numeric(left_value)
		right_value = self.right.evaluate(thing)
		_assert_is_numeric(right_value)
		return op(left_value, right_value)

	_op_add  = functools.partialmethod(__op_arithmetic, operator.add)
	_op_sub  = functools.partialmethod(__op_arithmetic, operator.sub)
	_op_fdiv = functools.partialmethod(__op_arithmetic, operator.floordiv)
	_op_tdiv = functools.partialmethod(__op_arithmetic, operator.truediv)
	_op_mod  = functools.partialmethod(__op_arithmetic, operator.mod)
	_op_mul  = functools.partialmethod(__op_arithmetic, operator.mul)
	_op_pow  = functools.partialmethod(__op_arithmetic, math.pow)

class BitwiseExpression(LeftOperatorRightExpressionBase):
	"""
	A class for representing bitwise arithmetic expressions from the grammar text such as XOR and shifting operations.
	"""
	compatible_types = (DataType.FLOAT, DataType.SET)
	result_type = DataType.UNDEFINED
	def __init__(self, *args, **kwargs):
		super(BitwiseExpression, self).__init__(*args, **kwargs)
		# don't use DataType.is_compatible, because for sets the member type isn't important
		if self.left.result_type != DataType.UNDEFINED and self.right.result_type != DataType.UNDEFINED:
			if self.left.result_type.__class__ != self.right.result_type.__class__:
				raise errors.EvaluationError('data type mismatch')
		if self.left.result_type == DataType.FLOAT:
			if _is_reduced(self.left):
				_assert_is_natural_number(self.left.evaluate(None))
			self.result_type = DataType.FLOAT
		if self.right.result_type == DataType.FLOAT:
			if _is_reduced(self.right):
				_assert_is_natural_number(self.right.evaluate(None))
			self.result_type = DataType.FLOAT
		if isinstance(self.left.result_type, DataType.SET.__class__) or isinstance(self.right.result_type, DataType.SET.__class__):
			self.result_type = DataType.SET  # this discards the member type info

	def _op_bitwise(self, op, thing):
		left = self.left.evaluate(thing)
		if DataType.from_value(left) == DataType.FLOAT:
			return self._op_bitwise_float(op, thing, left)
		elif isinstance(DataType.from_value(left), DataType.SET.__class__):
			return self._op_bitwise_set(op, thing, left)
		raise errors.EvaluationError('data type mismatch')

	def _op_bitwise_float(self, op, thing, left):
		_assert_is_natural_number(left)
		right = self.right.evaluate(thing)
		_assert_is_natural_number(right)
		return _to_decimal(op(int(left), int(right)))

	def _op_bitwise_set(self, op, thing, left):
		right = self.right.evaluate(thing)
		if not DataType.is_compatible(DataType.from_value(right), DataType.SET):
			raise errors.EvaluationError('data type mismatch')
		return op(left, right)

	_op_bwand = functools.partialmethod(_op_bitwise, operator.and_)
	_op_bwor  = functools.partialmethod(_op_bitwise, operator.or_)
	_op_bwxor = functools.partialmethod(_op_bitwise, operator.xor)

class BitwiseShiftExpression(BitwiseExpression):
	compatible_types = (DataType.FLOAT,)
	result_type = DataType.FLOAT
	def _op_bitwise_shift(self, *args, **kwargs):
		return self._op_bitwise(*args, **kwargs)
	_op_bwlsh = functools.partialmethod(_op_bitwise_shift, operator.lshift)
	_op_bwrsh = functools.partialmethod(_op_bitwise_shift, operator.rshift)

class LogicExpression(LeftOperatorRightExpressionBase):
	"""A class for representing logical expressions from the grammar text such as "and" and "or"."""
	def _op_and(self, thing):
		return bool(self.left.evaluate(thing) and self.right.evaluate(thing))

	def _op_or(self, thing):
		return bool(self.left.evaluate(thing) or self.right.evaluate(thing))

################################################################################
# Left-Operator-Right Comparison Expressions
################################################################################
class ComparisonExpression(LeftOperatorRightExpressionBase):
	"""A class for representing comparison expressions from the grammar text such as equality checks."""
	def _op_eq(self, thing):
		left_value = self.left.evaluate(thing)
		right_value = self.right.evaluate(thing)
		if type(left_value) is not type(right_value):
			return False
		return operator.eq(left_value, right_value)

	def _op_ne(self, thing):
		left_value = self.left.evaluate(thing)
		right_value = self.right.evaluate(thing)
		if type(left_value) is not type(right_value):
			return True
		return operator.ne(left_value, right_value)

class ArithmeticComparisonExpression(ComparisonExpression):
	"""
	A class for representing arithmetic comparison expressions from the grammar text such as less-than-or-equal-to and
	greater-than.
	"""
	compatible_types = (DataType.ARRAY, DataType.BOOLEAN, DataType.DATETIME, DataType.FLOAT, DataType.NULL, DataType.STRING)
	def __init__(self, *args, **kwargs):
		super(ArithmeticComparisonExpression, self).__init__(*args, **kwargs)
		if self.left.result_type != DataType.UNDEFINED and self.right.result_type != DataType.UNDEFINED:
			if self.left.result_type != self.right.result_type:
				raise errors.EvaluationError('data type mismatch')

	def __op_arithmetic(self, op, thing):
		left_value = self.left.evaluate(thing)
		right_value = self.right.evaluate(thing)
		return self.__op_arithmetic_values(op, left_value, right_value)

	def __op_arithmetic_arrays(self, op, left_value, right_value):
		for subleft_value, subright_value in zip(left_value, right_value):
			if self.__op_arithmetic_values(operator.ne, subleft_value, subright_value):
				return self.__op_arithmetic_values(op, subleft_value, subright_value)
		if len(left_value) != len(right_value):
			return self.__op_arithmetic_values(op, len(left_value), len(right_value))
		return op in (operator.ge, operator.le)

	def __op_arithmetic_values(self, op, left_value, right_value):
		if left_value is None and right_value is None:
			return op in (operator.ge, operator.le)
		elif isinstance(left_value, tuple) and isinstance(right_value, tuple):
			return self.__op_arithmetic_arrays(op, left_value, right_value)
		elif type(left_value) is not type(right_value):
			raise errors.EvaluationError('data type mismatch')
		return op(left_value, right_value)

	_op_ge = functools.partialmethod(__op_arithmetic, operator.ge)
	_op_gt = functools.partialmethod(__op_arithmetic, operator.gt)
	_op_le = functools.partialmethod(__op_arithmetic, operator.le)
	_op_lt = functools.partialmethod(__op_arithmetic, operator.lt)

class FuzzyComparisonExpression(ComparisonExpression):
	"""
	A class for representing regular expression comparison expressions from the grammar text such as search and does not
	match.
	"""
	compatible_types = (DataType.NULL, DataType.STRING)
	def __init__(self, *args, **kwargs):
		super(FuzzyComparisonExpression, self).__init__(*args, **kwargs)
		if isinstance(self.right, StringExpression):
			self._right = self._compile_regex(self.right.evaluate(None))

	def _compile_regex(self, regex):
		try:
			result = re.compile(regex, flags=self.context.regex_flags)
		except re.error as error:
			raise errors.RegexSyntaxError('invalid regular expression', error=error, value=regex) from None
		return result

	def __op_regex(self, regex_function, modifier, thing):
		left = self.left.evaluate(thing)
		if not isinstance(left, str) and left is not None:
			raise errors.EvaluationError('data type mismatch')
		if isinstance(self.right, StringExpression):
			regex = self._right
		else:
			regex = self.right.evaluate(thing)
			if isinstance(regex, str):
				regex = self._compile_regex(regex)
			elif regex is not None:
				raise errors.EvaluationError('data type mismatch')
		if left is None or regex is None:
			return not modifier(left, regex)
		match = getattr(regex, regex_function)(left)
		if match is not None:
			self.context._tls['regex.groups'] = coerce_value(match.groups())
		return modifier(match, None)

	_op_eq_fzm = functools.partialmethod(__op_regex, 'match', operator.is_not)
	_op_eq_fzs = functools.partialmethod(__op_regex, 'search', operator.is_not)
	_op_ne_fzm = functools.partialmethod(__op_regex, 'match', operator.is_)
	_op_ne_fzs = functools.partialmethod(__op_regex, 'search', operator.is_)

################################################################################
# Miscellaneous Expressions
################################################################################
class ContainsExpression(ExpressionBase):
	"""An expression used to test whether an item exists within a container."""
	__slots__ = ('container', 'member')
	result_type = DataType.BOOLEAN
	def __init__(self, context, container, member):
		if container.result_type == DataType.STRING:
			if member.result_type != DataType.UNDEFINED and member.result_type != DataType.STRING:
				raise errors.EvaluationError('data type mismatch')
		elif container.result_type != DataType.UNDEFINED and container.result_type.is_scalar:
			raise errors.EvaluationError('data type mismatch')
		self.context = context
		self.member = member
		self.container = container

	def __repr__(self):
		return "<{0} container={1!r} member={2!r} >".format(self.__class__.__name__, self.container, self.member)

	def evaluate(self, thing):
		container_value = self.container.evaluate(thing)
		member_value = self.member.evaluate(thing)
		if DataType.from_value(container_value) == DataType.STRING:
			if DataType.from_value(member_value) != DataType.STRING:
				raise errors.EvaluationError('data type mismatch')
		return bool(member_value in container_value)

	def reduce(self):
		if not _is_reduced(self.container, self.member):
			return self
		return BooleanExpression(self.context, self.evaluate(None))


	def to_graphviz(self, digraph, *args, **kwargs):
		super(ContainsExpression, self).to_graphviz(digraph, *args, **kwargs)
		self.container.to_graphviz(digraph, *args, **kwargs)
		self.member.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.container)), label='container')
		digraph.edge(str(id(self)), str(id(self.member)), label='member')

class GetAttributeExpression(ExpressionBase):
	"""A class representing an expression in which *name* is retrieved as an attribute of *object*."""
	__slots__ = ('name', 'object', 'safe')
	def __init__(self, context, object_, name, safe=False):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param object_: The parent object from which to retrieve the attribute.
		:param str name: The name of the attribute to retrieve.
		:param bool safe: Whether or not the safe version should be invoked.

		.. versionchanged:: 2.4.0
			Added the *safe* parameter.
		"""
		self.context = context
		self.object = object_
		if self.object.result_type != DataType.UNDEFINED:
			if not (self.object.result_type == DataType.NULL and safe):
				self.result_type = context.resolve_attribute_type(self.object.result_type, name)
		self.name = name
		self.safe = safe

	def __repr__(self):
		return "<{0} name={1!r} >".format(self.__class__.__name__, self.name)

	def evaluate(self, thing):
		resolved_obj = self.object.evaluate(thing)
		if resolved_obj is None and self.safe:
			return resolved_obj

		try:
			value = self.context.resolve_attribute(thing, resolved_obj, self.name)
		except errors.AttributeResolutionError:
			pass
		else:
			return coerce_value(value, verify_type=False)

		try:
			value = self.context.resolve(resolved_obj, self.name)
		except errors.SymbolResolutionError:
			default_value = self.context.default_value
			if default_value is errors.UNDEFINED:
				raise errors.AttributeResolutionError(self.name, resolved_obj, thing=thing) from None
			value = default_value
		return coerce_value(value, verify_type=False)

	def reduce(self):
		if not _is_reduced(self.object):
			return self
		return LiteralExpressionBase.from_value(self.context, self.evaluate(None))

	def to_graphviz(self, digraph, *args, **kwargs):
		digraph.node(str(id(self)), "{}\nname={!r}".format(self.__class__.__name__, self.name))
		self.object.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.object)))

class GetItemExpression(ExpressionBase):
	"""A class representing an expression in which an *item* is retrieved from a container *object*."""
	__slots__ = ('container', 'item', 'safe')
	def __init__(self, context, container, item, safe=False):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param container: The container object from which to retrieve the item.
		:param str item: The item to retrieve from the container.
		:param bool safe: Whether or not the safe version should be invoked.

		.. versionchanged:: 2.4.0
			Added the *safe* parameter.
		"""
		self.context = context
		self.container = container
		if container.result_type == DataType.STRING:
			if not DataType.is_compatible(item.result_type, DataType.FLOAT):
				raise errors.EvaluationError('data type mismatch (not an integer number)')
			self.result_type = DataType.STRING
		# check against __class__ so the parent class is dynamic in case it changes in the future, what we're doing here
		# is explicitly checking if result_type is an array with out checking the value_type
		elif isinstance(container.result_type, DataType.ARRAY.__class__):
			if not DataType.is_compatible(item.result_type, DataType.FLOAT):
				raise errors.EvaluationError('data type mismatch (not an integer number)')
			self.result_type = container.result_type.value_type
		elif isinstance(container.result_type, DataType.MAPPING.__class__):
			if not (safe or DataType.is_compatible(item.result_type, container.result_type.key_type)):
				raise errors.LookupError(errors.UNDEFINED, errors.UNDEFINED)
			self.result_type = container.result_type.value_type
		elif isinstance(container.result_type, DataType.SET.__class__):
			raise errors.EvaluationError('data type mismatch (container is a set)')
		elif container.result_type != DataType.UNDEFINED:
			if not (container.result_type == DataType.NULL and safe):
				raise errors.EvaluationError('data type mismatch')
		self.item = item
		self.safe = safe

	def __repr__(self):
		return "<{0} container={1!r} item={2!r} >".format(self.__class__.__name__, self.container, self.item)

	def evaluate(self, thing):
		resolved_obj = self.container.evaluate(thing)
		if resolved_obj is None:
			if self.safe:
				return resolved_obj
			raise errors.EvaluationError('data type mismatch (container is null)')

		resolved_item = self.item.evaluate(thing)
		if isinstance(resolved_obj, (str, tuple)):
			_assert_is_integer_number(resolved_item)
			resolved_item = int(resolved_item)
		try:
			value = operator.getitem(resolved_obj, resolved_item)
		except (IndexError, KeyError):
			if self.safe:
				return None
			raise errors.LookupError(resolved_obj, resolved_item)
		return coerce_value(value, verify_type=False)

	def reduce(self):
		if isinstance(self.container.result_type, DataType.MAPPING.__class__):
			if self.safe and not DataType.is_compatible(self.item.result_type, self.container.result_type.key_type):
				return NullExpression(self.context)
		if _is_reduced(self.container, self.item):
			return LiteralExpressionBase.from_value(self.context, self.evaluate(None))
		return self

	def to_graphviz(self, digraph, *args, **kwargs):
		super(GetItemExpression, self).to_graphviz(digraph, *args, **kwargs)
		self.container.to_graphviz(digraph, *args, **kwargs)
		self.item.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.container)), label='container')
		digraph.edge(str(id(self)), str(id(self.item)), label='item')

class GetSliceExpression(ExpressionBase):
	"""A class representing an expression in which a range of items is retrieved from a container *object*."""
	__slots__ = ('container', 'start', 'stop', 'safe')
	def __init__(self, context, container, start=None, stop=None, safe=False):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param container: The container object from which to retrieve the item.
		:param start: The expression that represents the starting index of the slice.
		:param stop: The expression that represents the stopping index of the slice.
		:param bool safe: Whether or not the safe version should be invoked.

		.. versionchanged:: 2.4.0
			Added the *safe* parameter.
		"""
		self.context = context
		self.container = container
		if container.result_type == DataType.STRING:
			self.result_type = DataType.STRING
		# check against __class__ so the parent class is dynamic in case it changes in the future, what we're doing here
		# is explicitly checking if result_type is an array with out checking the value_type
		elif isinstance(container.result_type, DataType.ARRAY.__class__):
			self.result_type = container.result_type
		elif isinstance(container.result_type, DataType.SET.__class__):
			raise errors.EvaluationError('data type mismatch (container is a set)')
		elif container.result_type != DataType.UNDEFINED:
			if not (container.result_type == DataType.NULL and safe):
				raise errors.EvaluationError('data type mismatch')
		self.start = start or LiteralExpressionBase.from_value(context, 0)
		self.stop = stop or LiteralExpressionBase.from_value(context, None)
		self.safe = safe

	def __repr__(self):
		return "<{0} container={1!r} start={2!r} stop={3!r} >".format(self.__class__.__name__, self.container, self.start, self.stop)

	def evaluate(self, thing):
		resolved_obj = self.container.evaluate(thing)
		if resolved_obj is None:
			if self.safe:
				return resolved_obj
			raise errors.EvaluationError('data type mismatch')

		resolved_start = self.start.evaluate(thing)
		if resolved_start is not None:
			_assert_is_integer_number(resolved_start)
			resolved_start = int(resolved_start)
		resolved_stop = self.stop.evaluate(thing)
		if resolved_stop is not None:
			_assert_is_integer_number(resolved_stop)
			resolved_stop = int(resolved_stop)
		value = operator.getitem(resolved_obj, slice(resolved_start, resolved_stop))
		return coerce_value(value, verify_type=False)

	def reduce(self):
		if not _is_reduced(self.container, self.start, self.stop):
			return self
		return LiteralExpressionBase.from_value(self.context, self.evaluate(None))

	def to_graphviz(self, digraph, *args, **kwargs):
		super(GetSliceExpression, self).to_graphviz(digraph, *args, **kwargs)
		self.container.to_graphviz(digraph, *args, **kwargs)
		self.start.to_graphviz(digraph, *args, **kwargs)
		self.stop.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.container)), label='container')
		digraph.edge(str(id(self)), str(id(self.start)), label='start')
		digraph.edge(str(id(self)), str(id(self.stop)), label='stop')

class SymbolExpression(ExpressionBase):
	"""
	A class representing a symbol name to be resolved at evaluation time with the help of a
	:py:class:`~rule_engine.engine.Context` object.
	"""
	__slots__ = ('name', 'result_type', 'scope')
	def __init__(self, context, name, scope=None):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param str name: The name of the symbol. This will be resolved with a given context object on the specified
			*thing*.
		:param str scope: The optional scope to use while resolving the symbol.
		"""
		context.symbols.add(name)
		self.context = context
		self.name = name
		type_hint = context.resolve_type(name, scope=scope)
		if type_hint is not None:
			self.result_type = type_hint
		self.scope = scope

	def __repr__(self):
		return "<{0} name={1!r} >".format(self.__class__.__name__, self.name)

	def evaluate(self, thing):
		try:
			value = self.context.resolve(thing, self.name, scope=self.scope)
		except errors.SymbolResolutionError:
			default_value = self.context.default_value
			if default_value is errors.UNDEFINED:
				raise
			value = default_value
		value = coerce_value(value, verify_type=False)
		if isinstance(value, datetime.datetime) and value.tzinfo is None:
			value = value.replace(tzinfo=self.context.default_timezone)

		# if the expected result type is undefined, return the value
		if self.result_type == DataType.UNDEFINED:
			return value

		# use DataType.from_value to raise a TypeError if value is not of a
		# compatible data type
		value_type = DataType.from_value(value)

		# if the type is the expected result type, return the value
		if DataType.is_compatible(value_type, self.result_type):
			if self.result_type.is_scalar:
				return value
			if self.result_type.value_type == DataType.UNDEFINED:
				return value
			if self.result_type.value_type != DataType.NULL and not self.result_type.value_type_nullable and any(v is None for v in value):
				raise errors.SymbolTypeError(self.name, is_value=value, is_type=value_type, expected_type=self.result_type)
			if self.result_type.value_type == value_type.value_type:
				return value

		# if the type is null, return the value (treat null as a special case)
		if value_type == DataType.NULL:
			return value

		raise errors.SymbolTypeError(self.name, is_value=value, is_type=value_type, expected_type=self.result_type)

	def to_graphviz(self, digraph, *args, **kwargs):
		digraph.node(str(id(self)), "{}\nname={!r}".format(self.__class__.__name__, self.name))

class Statement(ASTNodeBase):
	"""A class representing the top level statement of the grammar text."""
	__slots__ = ('context', 'expression')
	def __init__(self, context, expression):
		"""
		:param context: The context to use for evaluating the statement.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param expression: The top level expression of the statement.
		:type expression: :py:class:`~.ExpressionBase`
		"""
		self.context = context
		self.expression = expression

	def evaluate(self, thing):
		return self.expression.evaluate(thing)

	def to_graphviz(self, digraph, *args, **kwargs):
		super(Statement, self).to_graphviz(digraph, *args, **kwargs)
		self.expression.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.expression)))

class TernaryExpression(ExpressionBase):
	"""
	A class for representing ternary expressions from the grammar text. These involve evaluating :py:attr:`.condition`
	before evaluating either :py:attr:`.case_true` or :py:attr:`.case_false` based on the results.
	"""
	def __init__(self, context, condition, case_true, case_false):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param condition: The condition expression whose evaluation determines whether the *case_true* or *case_false*
			expression is evaluated.
		:param case_true: The expression that's evaluated when *condition* is True.
		:param case_false:The expression that's evaluated when *condition* is False.
		"""
		self.context = context
		self.condition = condition
		self.case_true = case_true
		self.case_false = case_false
		if self.case_true.result_type == self.case_false.result_type:
			self.result_type = self.case_true.result_type
		elif isinstance(self.case_true.result_type, DataType.ARRAY.__class__) and isinstance(self.case_false.result_type, DataType.ARRAY.__class__):
			self.result_type = DataType.ARRAY

	def evaluate(self, thing):
		case = (self.case_true if self.condition.evaluate(thing) else self.case_false)
		return case.evaluate(thing)

	def reduce(self):
		if _is_reduced(self.condition):
			reduced_condition = bool(self.condition.value)
		else:
			reduced_condition = self.condition.reduce()
			if reduced_condition is self.condition:
				return self
		return self.case_true.reduce() if reduced_condition else self.case_false.reduce()

	def to_graphviz(self, digraph, *args, **kwargs):
		super(TernaryExpression, self).to_graphviz(digraph, *args, **kwargs)
		self.condition.to_graphviz(digraph, *args, **kwargs)
		self.case_true.to_graphviz(digraph, *args, **kwargs)
		self.case_false.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.condition)), label='condition')
		digraph.edge(str(id(self)), str(id(self.case_true)), label='true case')
		digraph.edge(str(id(self)), str(id(self.case_false)), label='false case')

class UnaryExpression(ExpressionBase):
	"""
	A class for representing unary expressions from the grammar text. These involve a single operator on the left side.
	"""
	def __init__(self, context, type_, right):
		"""
		:param context: The context to use for evaluating the expression.
		:type context: :py:class:`~rule_engine.engine.Context`
		:param str type_: The grammar type of operator to the left of the expression.
		:param right: The expression to the right of the operator.
		:type right: :py:class:`~.ExpressionBase`
		"""
		self.context = context
		type_ = type_.lower()
		self.type = type_
		self._evaluator = getattr(self, '_op_' + type_)
		self.result_type = {
			'not':    DataType.BOOLEAN,
			'uminus': DataType.FLOAT
		}[type_]
		self.right = right

	def __repr__(self):
		return "<{} type={!r} >".format(self.__class__.__name__, self.type)

	def evaluate(self, thing):
		return self._evaluator(thing)

	def __op(self, op, thing):
		return op(self.right.evaluate(thing))

	_op_not = functools.partialmethod(__op, operator.not_)

	def __op_arithmetic(self, op, thing):
		right = self.right.evaluate(thing)
		_assert_is_numeric(right)
		return op(right)

	_op_uminus = functools.partialmethod(__op_arithmetic, operator.neg)

	def reduce(self):
		type_ = self.type.lower()
		if not _is_reduced(self.right):
			return self
		if type_ == 'not':
			return BooleanExpression(self.context, self.evaluate(None))
		elif type_ == 'uminus':
			if not isinstance(self.right, (FloatExpression,)):
				raise errors.EvaluationError('data type mismatch (not a float expression)')
			return FloatExpression(self.context, self.evaluate(None))

	def to_graphviz(self, digraph, *args, **kwargs):
		digraph.node(str(id(self)), "{}\ntype={!r}".format(self.__class__.__name__, self.type.lower()))
		self.right.to_graphviz(digraph, *args, **kwargs)
		digraph.edge(str(id(self)), str(id(self.right)))
