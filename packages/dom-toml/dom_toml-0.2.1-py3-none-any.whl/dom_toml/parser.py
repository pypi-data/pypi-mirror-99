#!/usr/bin/env python3
#
#  parser.py
"""
Abstract base class for TOML configuration parsers.

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Tuple, Type, Union

# 3rd party
import toml

__all__ = ["AbstractConfigParser", "BadConfigError", "construct_path"]

TOML_TYPES = Any


class BadConfigError(ValueError):
	"""
	Indicates an error in the TOML configuration.
	"""


def construct_path(path: Iterable[str]) -> str:
	"""
	Construct a dotted path to a key.

	:param path: The path elements.
	"""

	return '.'.join([toml.dumps({elem: 0})[:-5] for elem in path])


class AbstractConfigParser(ABC):
	"""
	Abstract base class for TOML configuration parsers.
	"""

	@staticmethod
	def assert_type(
			obj: Any,
			expected_type: Union[Type, Tuple[Type, ...]],
			path: Iterable[str],
			what: str = "type",
			) -> None:
		"""
		Assert that ``obj`` is of type ``expected_type``, otherwise raise an error with a helpful message.

		:param obj: The object to check the type of.
		:param expected_type: The expected type.
		:param path: The elements of the path to ``obj`` in the TOML mapping.
		:param what: What ``obj`` is, e.g. ``'type'``, ``'value type'``.

		.. seealso:: :meth:`~.assert_value_type` and :meth:`~.assert_indexed_type`
		"""

		if not isinstance(obj, expected_type):
			name = construct_path(path)
			raise TypeError(f"Invalid {what} for {name!r}: expected {expected_type!r}, got {type(obj)!r}")

	@staticmethod
	def assert_indexed_type(
			obj: Any,
			expected_type: Union[Type, Tuple[Type, ...]],
			path: Iterable[str],
			idx: int = 0,
			) -> None:
		"""
		Assert that ``obj`` is of type ``expected_type``, otherwise raise an error with a helpful message.

		:param obj: The object to check the type of.
		:param expected_type: The expected type.
		:param path: The elements of the path to ``obj`` in the TOML mapping.
		:param idx: The index of ``obj`` in the array.

		.. seealso:: :meth:`~.assert_type`, and :meth:`~.assert_value_type`
		"""

		if not isinstance(obj, expected_type):
			name = construct_path(path) + f"[{idx}]"
			raise TypeError(f"Invalid type for {name!r}: expected {expected_type!r}, got {type(obj)!r}")

	def assert_value_type(
			self,
			obj: Any,
			expected_type: Union[Type, Tuple[Type, ...]],
			path: Iterable[str],
			):
		"""
		Assert that the value ``obj`` is of type ``expected_type``, otherwise raise an error with a helpful message.

		:param obj: The object to check the type of.
		:param expected_type: The expected type.
		:param path: The elements of the path to ``obj`` in the TOML mapping.

		.. seealso:: :meth:`~.assert_type` and :meth:`~.assert_indexed_type`
		"""

		self.assert_type(obj, expected_type, path, "value type")

	@property
	@abstractmethod
	def keys(self) -> List[str]:  # pragma: no cover
		"""
		The keys to parse from the TOML file.
		"""

		raise NotImplementedError

	def parse(self, config: Dict[str, TOML_TYPES]) -> Dict[str, TOML_TYPES]:
		r"""
		Parse the TOML configuration.

		This function iterates over the list of keys given in :attr:`~.keys`.
		For each key, it searches for a method on the class called :file:`parse_{<key>}`.

		* If the method exists, that method is called, passing the value as the only argument.
		  The value returned from that method is included in the parsed configuration.
		  The signature of those methods is:

		  .. parsed-literal::

			def visit_<key>(
				self,
				config: :class:`typing.Dict`\[:class:`str`\, :py:obj:`typing.Any`\],
				) -> :py:obj:`typing.Any`\:

		* If the method doesn't exist, the value is included in the parsed configuration unchanged.

		* Missing keys are ignored. Override this function in a subclass if you need that behaviour.

		Once all keys have been parsed the configuration is returned.

		:param config:
		"""

		parsed_config = {}

		for key in self.keys:
			if key not in config:
				# Ignore absent values
				pass

			elif hasattr(self, f"parse_{key.replace('-', '_')}"):
				parsed_config[key] = getattr(self, f"parse_{key.replace('-', '_')}")(config)

			elif key in config:
				parsed_config[key] = config[key]

		return parsed_config
