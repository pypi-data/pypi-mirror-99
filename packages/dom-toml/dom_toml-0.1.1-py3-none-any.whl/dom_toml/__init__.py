#!/usr/bin/env python3
#
#  __init__.py
"""
Dom's custom encoder for Tom's Obvious, Minimal Language.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on https://github.com/uiri/toml
#  MIT Licensed
#  Copyright 2013-2019 William Pearson
#  Copyright 2015-2016 Julien Enselme
#  Copyright 2016 Google Inc.
#  Copyright 2017 Samuel Vasko
#  Copyright 2017 Nate Prewitt
#  Copyright 2017 Jack Evans
#  Copyright 2019 Filippo Broggini
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
import re
from typing import Any, Mapping, MutableMapping, Type, TypeVar, Union

# 3rd party
import toml
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from toml.decoder import InlineTableDict

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["TomlEncoder", "dumps", "loads", "dump", "load", "_M"]

_M = TypeVar("_M", bound=MutableMapping[str, Any])

_section_disallowed_re = re.compile(r'^[A-Za-z0-9_-]+$')


class TomlEncoder(toml.TomlEncoder):
	"""
	Customised TOML encoder which wraps long lists onto multiple lines
	and adds a blank line before arrays of tables.
	"""  # noqa: D400

	# The maximum width of the list **value**, after which it will be wrapped.
	max_width: int = 100

	def dump_list(self, v):  # noqa: D102
		single_line = super().dump_list(v)

		if len(single_line) <= self.max_width:
			return single_line

		retval = StringList(['['])

		with retval.with_indent("    ", 1):
			for u in v:
				retval.append(f"{str(self.dump_value(u))},")

		retval.append(']')

		return str(retval)

	def dump_sections(self, o, sup):  # noqa: D102
		retstr = ''

		if sup != '' and sup[-1] != '.':
			sup += '.'

		arraystr = StringList()
		arraystr.indent_type = ' ' * 4

		retdict = self._dict()  # type: ignore

		for section in o:
			section = str(section)
			qsection = section

			if not _section_disallowed_re.match(section):
				qsection = _dump_str(section)

			if not isinstance(o[section], dict):
				arrayoftables = False

				if isinstance(o[section], list):
					for a in o[section]:
						if isinstance(a, dict):
							arrayoftables = True

				if arrayoftables:
					for a in o[section]:
						arraytabstr = '\n'

						# if arraystr:
						arraystr.blankline(ensure_single=True)

						arraystr.append(f"[[{sup}{qsection}]]")

						s, d = self.dump_sections(a, sup + qsection)

						if s:
							if s[0] == '[':
								arraytabstr += s
							else:
								arraystr.append(s)

						while d:  # pragma: no cover
							newd = self._dict()  # type: ignore

							for dsec in d:
								s1, d1 = self.dump_sections(d[dsec], f"{sup}{qsection}.{dsec}")

								if s1:
									arraytabstr += f'[{sup}{qsection}.{dsec}]\n{s1}'

								for s1 in d1:
									newd[f"{dsec}.{s1}"] = d1[s1]

							d = newd

						arraystr.append(arraytabstr)
				else:
					if o[section] is not None:
						retstr += f"{qsection} = {self.dump_value(o[section])}\n"

			elif self.preserve and isinstance(o[section], InlineTableDict):
				retstr += f"{qsection} = {self.dump_inline_table(o[section])}"

			else:
				retdict[qsection] = o[section]

		retstr += str(arraystr)

		return retstr.lstrip(), retdict


def dumps(
		data: Mapping[str, Any],
		encoder: Union[Type[toml.TomlEncoder], toml.TomlEncoder, None] = None,
		) -> str:
	"""
	Convert ``data`` to a TOML string.

	:param data:
	:param encoder: The :class:`toml.TomlEncoder` to use for constructing the output string.

	:returns: A string containing the ``TOML`` corresponding to ``data``.
	"""

	if isinstance(encoder, type):
		encoder = encoder()

	return toml.dumps(data, encoder=encoder)


def dump(
		data: Mapping[str, Any],
		filename: PathLike,
		encoder: Union[Type[toml.TomlEncoder], toml.TomlEncoder, None] = None,
		) -> str:
	"""
	Writes out ``data`` as TOML to the given file.

	:param data:
	:param filename: The filename to write to.
	:param encoder: The :class:`toml.TomlEncoder` to use for constructing the output string.

	:returns: A string containing the ``TOML`` corresponding to ``data``.
	"""

	filename = PathPlus(filename)
	as_toml = dumps(data, encoder=encoder)
	filename.write_clean(as_toml)
	return as_toml


def loads(
		s,
		dict_: Type[_M] = dict,  # type: ignore
		decoder: Union[Type[toml.TomlDecoder], toml.TomlDecoder, None] = None,
		) -> _M:
	r"""
	Parse the given string as TOML.

	:param s:
	:param dict\_: The class of the returned data.
	:param decoder: The :class:`toml.TomlEncoder` to use for constructing the output string.

	:returns: A mapping containing the ``TOML`` data.
	"""

	if isinstance(decoder, type):
		decoder = decoder()

	return toml.loads(  # type: ignore
			s,
			_dict=dict_,
			decoder=decoder,
			)


def load(
		filename: PathLike,
		dict_: Type[_M] = dict,  # type: ignore
		decoder: Union[Type[toml.TomlDecoder], toml.TomlDecoder, None] = None,
		) -> _M:
	r"""
	Parse TOML from the given file.

	:param filename: The filename to read from to.
	:param dict\_: The class of the returned data.
	:param decoder: The :class:`toml.TomlEncoder` to use for constructing the output string.

	:returns: A mapping containing the ``TOML`` data.
	"""

	filename = PathPlus(filename)

	return loads(
			filename.read_text(),
			dict_=dict_,
			decoder=decoder,
			)


def _dump_str(v):  # pragma: no cover
	if v[0] == 'u':
		v = v[1:]
	singlequote = v.startswith("'")
	if singlequote or v.startswith('"'):
		v = v[1:-1]
	if singlequote:
		v = v.replace("\\'", "'")
		v = v.replace('"', '\\"')
	v = v.split("\\x")

	# print([x.encode("UTF-8") for x in v])
	[x.encode("UTF-8") for x in v]

	while len(v) > 1:
		i = -1
		if not v[0]:
			v = v[1:]
		v[0] = v[0].replace("\\\\", '\\')
		# No, I don't know why != works and == breaks
		joinx = v[0][i] != '\\'
		while v[0][:i] and v[0][i] == '\\':
			joinx = not joinx
			i -= 1
		if joinx:
			joiner = 'x'
		else:
			joiner = "u00"
		v = [v[0] + joiner + v[1]] + v[2:]
	return str('"' + v[0] + '"')


# Fix unicode characters on PyPy
toml.encoder._dump_str = _dump_str  # type: ignore
