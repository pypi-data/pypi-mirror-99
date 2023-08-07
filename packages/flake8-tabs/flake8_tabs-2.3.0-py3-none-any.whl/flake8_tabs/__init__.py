"""
Tab (or Spaces) indentation style checker for flake8
"""

__version__ = "2.3.0"

import collections
import itertools
import re
import tokenize
import typing as ty

import flake8.checker
import flake8.processor

from . import categorizer
from . import editorconfig


if ty.TYPE_CHECKING:
	import os


CATEGORY_NAMES = {
	categorizer.CategoryType.CALL: "call",
	categorizer.CategoryType.DEFN: "definition",
	categorizer.CategoryType.EXPR: "expression",
	categorizer.CategoryType.STMT: "statement",
}


T = ty.TypeVar("T")
U = ty.TypeVar("U")


def map_next(pred: ty.Callable[[T], U], *iterable, default: U = ...) -> U:
	try:
		val = next(itertools.chain.from_iterable(iterable))
	except StopIteration:
		if default is not Ellipsis:
			return default
		
		raise
	else:
		return pred(val)

def pairwise_fill(it: ty.Iterator[T], *, fill: U = None) \
    -> ty.Iterator[ty.Tuple[T, ty.Union[T, U]]]:
	"s -> (s0,s1), (s1,s2), (s2, s3), ..., (s_n-1, s_n), (s_n, None)"
	# Based on `pairwise` example at:
	# https://docs.python.org/3.9/library/itertools.html#itertools-recipes
	a, b = itertools.tee(itertools.chain(it, (fill,)))
	next(b, None)
	return zip(a, b)


class Indent(collections.namedtuple("Indent", ("tabs", "spaces"))):
	"""
	Convience class representing the combined indentation of tabs and spaces with vector-style math
	"""
	def __bool__(self):
		return self.tabs != 0 or self.spaces != 0
	
	@property
	def characters(self):
		return self.tabs + self.spaces
	
	def __pos__(self):
		return self
	
	def __neg__(self):
		return Indent(-self.tabs, -self.spaces)
	
	def __eq__(self, other):
		if other == 0:
			return self.tabs == 0 and self.spaces == 0
		
		return super().__eq__(other)
	
	def __add__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			if other == 0:
				return self
			
			return NotImplemented
		
		return Indent(self.tabs + other[0], self.spaces + other[1])
	
	def __radd__(self, other):
		if not isinstance(other, Indent):
			# Special case for adding to zero (makes `sum` work)
			if other == 0:
				return self
			
			return NotImplemented
		
		return other.__add__(self)
	
	def __sub__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			# Special case for adding to zero (makes `sum` work)
			if other == 0:
				return self.__pos__()
			
			return NotImplemented
		
		return Indent(self.tabs - other[0], self.spaces - other[1])
	
	def __rsub__(self, other):
		if not isinstance(other, Indent):
			if other == 0:
				return self.__neg__()
			
			return NotImplemented
		
		return other.__add__(self)
	
	def __mul__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			return NotImplemented
		
		return Indent(self.tabs * other[0], self.spaces * other[1])
	
	def __div__(self, other):
		if not isinstance(other, collections.abc.Sequence) or len(other) != 2:
			return NotImplemented
		
		return Indent(self.tabs / other[0], self.spaces / other[1])

Indent.null = Indent(0, 0)


class FileChecker(flake8.checker.FileChecker):
	"""
	Blacklist some `pycodestyle` checks that our plugin will implement instead
	"""
	
	BLACKLIST = frozenset({
		# E101 indentation contains mixed spaces and tabs
		#  – Incorrectly reports cases of using tabs for indentation but spaces for alignment
		#    (We have our own checks for cases where the two are mixed, which is still an error.)
		"pycodestyle.tabs_or_spaces",
		
		# E121 continuation line under-indented for hanging indent
		# E122 continuation line missing indentation or outdented
		# E123 closing bracket does not match indentation of opening bracket’s line
		# E126 continuation line over-indented for hanging indent
		# E127 continuation line over-indented for visual indent
		# E128 continuation line under-indented for visual indent
		#  – We handle these ourselves: That's what this checker is about after all
		# E124 closing bracket does not match visual indentation
		# E125 continuation line with same indent as next logical line
		# E129 visually indented line with same indent as next logical line
		# E131 continuation line unaligned for hanging indent
		# E133 closing bracket is missing indentation
		#  – These aren't handled yet but cannot be disabled separately
		"pycodestyle.continued_indentation",
		
		# W191 indentation contains tabs
		#  – Not applicable since we love tabs 🙂️
		"pycodestyle.tabs_obsolete",
		
		# W291 trailing whitespace
		# W293 blank line contains whitespace
		#  – Implemented by `BlankLinesChecker` with more options and saner defaults
		"pycodestyle.trailing_whitespace",
	})
	
	def __init__(self, filename, checks, options):
		if not Config["use-pycodestyle-indent"]:
			for checks_type in checks:
				checks[checks_type] = list(filter(
					lambda c: c["name"] not in self.BLACKLIST,
					checks[checks_type]
				))
		super().__init__(filename, checks, options)

def expand_indent(line):
	r"""Return the amount of indentation (patched function for `flake8`)
	
	Tabs are expanded to the next multiple of the current tab size.
	
	>>> expand_indent('    ')
	4
	>>> expand_indent('\t')
	4
	>>> expand_indent('   \t')
	4
	>>> expand_indent('    \t')
	8
	"""
	if "\t" not in line:
		return len(line) - len(line.lstrip())
	
	# XXX: Technically this should consider the per-file indent configuration as
	#      well, but its only for pretty-printing and we don't have the filepath
	config = {
		"indent-size": Config["indent-size"],
	}
	
	result = 0
	for char in line:
		if char == "\t":
			result  = result // config["indent-size"] * config["indent-size"]
			result += config["indent-size"]
		elif char == " ":
			result += 1
		else:
			break
	return result

def patch_flake8():
	flake8.checker.FileChecker = FileChecker
	flake8.processor.expand_indent = expand_indent


# Support for `__class_getitem__` was added in Python 3.7
class ClassGetItemPolyfill(type):
	def __getitem__(self, name: str) -> ty.Union[bool, int, str]:
		return self.__class_getitem__(name)


class Config(metaclass=ClassGetItemPolyfill):
	"""
	Registers the configuration options for the other checkers
	"""
	name: str    = "flake8-tabs"
	version: str = __version__
	
	
	OPTIONS: ty.Final[
		ty.Dict[
			str,  # Field name
			ty.Tuple[
				ty.Union[bool, int, str],  # Default value
				ty.Optional[str],          # EditorConfig option name
			]
		]
	] = {
		# Master switch for the `IndentationChecker` module
		"use-flake8-tabs": (
			False,
			None,
		),
		
		"use-pycodestyle-indent": (
			True,  # + Special default code
			None,
		),
		
		"blank-lines-indent": (
			"keep",
			"trim_trailing_whitespace",  # + Special mapping code
		),
		
		"indent-style": (
			"keep",
			"indent_style",
		),
		
		# Indentation size: Used when requiring further indentation after we already have alignment
		"indent-size": (
			4,
			"indent_size",
		),
		
		# Indentation tabs: The number of tabs, when indenting, to require for the
		#                   first level of indentation of functions calls,
		#                   function/class definitions and other expressions/statements
		
		"indent-levels-call": (
			1,
			None,
		),
		
		"indent-levels-defn": (
			2,  # PEP-8 requires indentation to be distinguishable
			None,
		),
		
		"indent-levels-expr": (
			1,
			None,
		),
		
		# Continuation line style: Which indentation style to allow on continuation lines
		#  * “aligned” means that follow-up lines should be indented by the exact
		#    number of extra spaces required to align them if the previous line's
		#    final opening brace
		#  * “hanging” means that follow-up lines should be indented by a tab
		#  * “both” chooses the allowed indentation style based on whether the
		#    first lines contains any relevant values after the final opening brace
		"continuation-style": (
			"both",
			None,
		),
	}
	
	_option_values: ty.Dict[str, ty.Optional[ty.Union[bool, int, str]]] = {}
	
	
	@classmethod
	def add_options(cls, option_manager):
		# Patch support for indent-size and the use-pycodestyle-indent options into flake8
		patch_flake8()
		
		
		# Indentation style: Tabs or spaces?
		option_manager.add_option(
			"--indent-style", type="choice", metavar="STYLE", parse_from_config=True,
			choices=("tab", "space", "keep"),
			help=(f"The indentation style to enforce on newly opened blocks "
			      f"(Default: `{cls.OPTIONS['indent-style'][1]}` from .editorconfig "
			      f"or {cls.OPTIONS['indent-style'][0]!r})"),
		)
		
		
		# Indentation style options
		option_manager.add_option(
			"--blank-lines-indent", type="choice", metavar="MODE", parse_from_config=True,
			choices=("maybe", "always", "never"),
			help=(f"Whether there should be, properly aligned, indentation in blank lines; "
			      f"\"always\" forces this, \"never\" disallows this (Default: Depends on "
			      f"`{cls.OPTIONS['blank-lines-indent'][1]}` from .editorconfig or "
			      f"{cls.OPTIONS['blank-lines-indent'][0]!r})")
		)
		
		# Patcher options
		option_manager.add_option(
			"--use-flake8-tabs", action="store_true", parse_from_config=True, default=None,
			help=("Use flake8-tabs instead for indentation checking? "
			      "Enabling this will disable PyCodeStyle's indentation checks "
			      "unless you override that behaviour; by default only minimal "
			      "checking will be performed")
		)
		option_manager.add_option(
			"--use-pycodestyle-indent", action="store_true", parse_from_config=True, default=None,
			help=("Force the use of PyCodeStyle's indentation checks even if "
			      "flake8-tabs is enabled")
		)
		
		# First-indentation tab number options
		option_manager.add_option(
			"--indent-tabs-call", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_call",
			help=(f"Number of tabs to indent on the first level of indentation within a function/"
			      f"method call (Default: {cls.OPTIONS['indent-levels-call'][0]!r})")
		)
		option_manager.add_option(
			"--indent-tabs-def", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_defn",
			help=(f"Number of tabs to indent on the first level of indentation within a class/"
			      f"function definition (Default: {cls.OPTIONS['indent-levels-defn'][0]!r})")
		)
		option_manager.add_option(
			"--indent-tabs-expr", type="int", metavar="n", parse_from_config=True,
			dest="indent_levels_expr",
			help=(f"Number of tabs to indent on the first level of indentation within an "
			      f"expression (Default: {cls.OPTIONS['indent-levels-expr'][0]!r})")
		)
		
		
		# More rigid style enforcing options
		option_manager.add_option(
			"--continuation-style", type="choice", metavar="STYLE", parse_from_config=True,
			choices=("aligned", "hanging", "both"),
			help=(f"Restrict the allowed continuation line style to either "
			      f"\"hanging\" or \"aligned\"; see the documentation for what "
			      f"this means (Default: {cls.OPTIONS['continuation-style'][0]!r})")
		)
		
		# Prevent conflict with other plugins registering `--tab-width` as well
		for option in option_manager.options:
			if option.dest == "tab_width":
				return
		
		option_manager.add_option(
			"--tab-width", type="int", metavar="n", parse_from_config=True,
			dest="indent_size",
			help=(f"Number of spaces per tab character for line length checking "
			      f"(Default: `{cls.OPTIONS['indent-size'][1]}` from .editorconfig or "
			      f"{cls.OPTIONS['indent-size'][0]!r})"),
		)
	
	@classmethod
	def parse_options(cls, option_manager, options, extra_args):
		for option_name in cls.OPTIONS.keys():
			cls._option_values[option_name] = getattr(options, option_name.replace("-", "_"))
	
	@classmethod
	def _get_field(cls, field: str, filepath: ty.Union[bytes, str, "os.PathLike", None] = None) \
	    -> ty.Union[bool, int, str]:
		(default, ec_name) = cls.OPTIONS[field]
		
		value: ty.Union[str, int, bool, None] = cls._option_values.get(field)
		if value is not None:
			return value
		
		if ec_name is not None and filepath is not None:
			# While this branch may be run several times in this loop, the
			# result of `query_filepath` is LRU cached so we only read the
			# relevant configuration files at most once per filepath
			#
			# Using an LRU cache on the function has the benefit that it
			# also caches the results between different calls to this
			# function (like when the different checkers of this module
			# are called one after another).
			value = editorconfig.query_filepath(filepath).get(ec_name)
			
			if value is not None:
				# EditorConfig value of some fields requires mapping to obtain
				# the equivalent configuration value
				if field == "blank-lines-indent":
					# `value` here is actually “trim_trailing_whitespace”
					return "never" if value else "always"
				
				return value
		
		# Special default values
		if field == "use-pycodestyle-indent":
			return not cls._get_field("use-flake8-tabs", filepath)
		
		return default
	
	
	@classmethod
	def __class_getitem__(cls, field: str):
		return cls._get_field(field)
	
	
	@classmethod
	def with_filepath(cls, filepath: ty.Union[bytes, str, "os.PathLike"], *fields: str) \
	    -> ty.Dict[str, ty.Union[bool, int, str]]:
		result: ty.Dict[str, ty.Union[str, int, bool]] = {}
		for field in fields:
			result[field] = cls._get_field(field, filepath)
		return result
	
	def __init__(self, filename: str) -> None:
		pass


def format_violation(code: int, message: str):
	return f"ET{code} (flake8-tabs) {message}"

def format_warning(code: int, message: str):
	return f"WT{code} (flake8-tabs) {message}"


class BlankLinesChecker:
	"""
	Checks indentation in blank lines to match the next line if there happens to be any
	"""
	name    = "flake8-tabs"
	version = __version__
	
	
	REGEXP = re.compile(r"([ \t\v]*).*?([ \t\v]*)([\r\x0C]*\n?)$")
	
	
	def __new__(cls, physical_line, lines, line_number, filename):
		# Look up per-file attributes from EditorConfig
		config = Config.with_filepath(filename, "blank-lines-indent")
		
		indent, trailing, crlf = cls.REGEXP.match(physical_line).groups()
		if len(physical_line) - len(crlf) < 1:  # Totally blank line
			if config["blank-lines-indent"] != "always":
				return  # Otherwise check whether the next non-blank line is also unindented
		elif len(indent) + len(crlf) == len(physical_line):
			if config["blank-lines-indent"] == "never":  # Cannot have indented blank line in this mode
				return (0, format_warning(
					293,
					"blank line contains whitespace, but option "
					"blank-lines-indent=never does not permit this"
				))
		else:
			# Not a blank line with whitespace
			if len(trailing) > 0:
				return (len(physical_line) - len(trailing) - len(crlf), format_warning(
					291,
					"trailing whitespace"
				))
			return
		
		# Confusingly using `lines[line_number]` does not yield the current line
		# but the line *after* that, so use the following variable to make it
		# more obvious what is happening in the following code
		line_idx = line_number - 1
		
		# Scan for previous non-blank line
		expected_indent_prev = ""
		for idx in range(line_idx - 1, -1, -1):
			line_indent, _, line_crlf = cls.REGEXP.match(lines[idx]).groups()
			if len(line_indent) + len(line_crlf) != len(lines[idx]):
				expected_indent_prev = line_indent
				break
		
		# Scan for next non-blank line
		expected_indent_next = ""
		for idx in range(line_idx + 1, len(lines), +1):
			line_indent, _, line_crlf = cls.REGEXP.match(lines[idx]).groups()
			if len(line_indent) + len(line_crlf) != len(lines[idx]):
				expected_indent_next = line_indent
				break
		
		# Choose the shorter indentation of the two
		if expand_indent(expected_indent_prev) < expand_indent(expected_indent_next):
			expected_indent = expected_indent_prev
		else:
			expected_indent = expected_indent_next
		
		# Compare the two indents
		if indent != expected_indent:
			return (0, format_warning(
				293,
				"blank line contains unaligned whitespace"
			))
	
	def __init__(self, physical_line, lines, line_number, filename):
		pass


class IndentationChecker:
	"""
	Checks indentation within braces with a “tabs for indentation, spaces
	for alignment” kind of mindset
	"""
	name    = "flake8-tabs"
	version = __version__
	
	
	@classmethod
	def _parse_line_indent(cls, line, *, allow_both: bool = True):
		"""
		Count number of tabs at start of line followed by number of spaces at start of line
		"""
		tabs   = 0
		spaces = 0
		expect_tab = True
		for char in line:
			if expect_tab and char == '\t':
				tabs += 1
			elif expect_tab and char == ' ':
				if not allow_both and tabs > 0:
					raise ValueError("Mixed tabs and spaces in indentation")
				spaces += 1
				expect_tab = False
			elif not expect_tab and char == ' ':
				spaces += 1
			elif not expect_tab and char == '\t':
				raise ValueError("Mixed tabs and spaces in indentation")
			else:
				break
		return Indent(tabs, spaces)
	
	@classmethod
	def _categorize_and_group_tokens_by_physical_line(
			cls, tokens: ty.Iterable[tokenize.TokenInfo]
	) -> ty.Generator[ty.Tuple[ty.List[categorizer.Token], ty.Optional[str]], ty.Any, None]:
		line_tokens = []
		
		ctokens = categorizer.Categorizer.process_all(tokens)
		for token, next_token in pairwise_fill(ctokens):
			line_tokens.append(token)
			if token.type in (categorizer.TokenType.END_PLINE,
			                  categorizer.TokenType.END_LLINE):
				yield (line_tokens[:], next_token.line if next_token is not None else None)
				line_tokens.clear()
		
		assert len(line_tokens) == 0
	
	def __init__(self, logical_line: str, line_number: int, noqa: bool, previous_indent_level: int,
	             tokens: ty.Iterable[tokenize.TokenInfo], filename: str) -> None:
		self.messages = []
		
		# We only care about non-empty non-noqa-marked lines
		if len(tokens) < 1 or noqa:
			return
		
		# Look up per-file attributes from EditorConfig
		config_fields = ("indent-style",)
		if Config["use-flake8-tabs"]:
			config_fields += (
				"continuation-style",
				"indent-levels-call",
				"indent-levels-defn",
				"indent-levels-expr",
				"indent-size",
			)
		
		config = Config.with_filepath(filename, *config_fields)
		
		# If we receive an INDENT token as first token here and the previous
		# line is reported to have had no indentation then we are seeing the
		# very first indentation of some code block here. This is a great place
		# to check if the block's entire indentation matches the expected
		# indentation style without producing an error for every single
		# mismatching logical line.
		if config["indent-style"] != "keep" and \
		   tokens[0].type == tokenize.INDENT and previous_indent_level == 0:
			block_indent = tokens[0].line[tokens[0].start[1]:tokens[0].end[1]]
			
			if config["indent-style"] == "tab" and not all(c == "\t" for c in block_indent):
				self.messages.append((tokens[0].start, format_warning(
					191,
					"indentation contains spaces, but option indent-style=tab requires tabs"
				)))
			elif config["indent-style"] == "space" and not all(c == " " for c in block_indent):
				self.messages.append((tokens[0].start, format_warning(
					191,
					"indentation contains tabs, but option indent-style=space requires spaces"
				)))
		
		# Don't run main part of checker unless enabled
		if not Config["use-flake8-tabs"]:
			return
		
		# Assume first line to be correctly indented
		try:
			first_indent = self._parse_line_indent(tokens[0].line, allow_both=False)
		except ValueError:  # mixed tabs and spaces – report error and abort this logical line
			self.messages.append((tokens[0].start, format_violation(
				101, "indentation contains mixed spaces and tabs"
			)))
			return
		
		# Indentation stack: Keeps track of the indentation `(tabs, spaces)`
		#                    caused by each brace
		# Item 0 represents the base indentation we got above, item 1 represents
		# indentation gained because of continuation lines
		indent_stack = [first_indent, Indent.null]
		
		# Indentation gained by adding up the length of all initial keywords
		#
		# Needed to determine the expected indention of continuation lines if
		# there are no brackets open after the first line.
		keyword_indent: ty.Optional[Indent] = None
		
		open_brackets: int = 0
		for ltokens, next_line in self._categorize_and_group_tokens_by_physical_line(tokens):
			# Convenience aliases for current physical line
			line_category = ltokens[0].category
			line_start    = ltokens[0].start
			line_text     = ltokens[0].line
			
			# Determine current physical line indentation
			try:
				line_indent = self._parse_line_indent(line_text)
			except ValueError:  # mixed tabs and spaces – report error and abort this logical line
				self.messages.append((line_start, format_violation(
					101, "indentation contains mixed spaces and tabs"
				)))
				return
			
			# Skip blank lines within expressions (no opinion on those)
			if len(line_text.strip()) < 1:
				continue
			
			# Determine number of characters in initial keywords on first line
			if keyword_indent is None:
				keyword_indent = Indent.null
				for token, next_token in pairwise_fill(ltokens):
					if token.type in (
						categorizer.TokenType.INDENT,
						categorizer.TokenType.DEDENT,
					):
						continue
					
					if token.type is not categorizer.TokenType.KEYWORD:
						break
					
					# Add up length of token and any whitespace between this token
					# and the next one
					keyword_indent += Indent(
						0,
						((next_token.start[1] - token.start[1])
						 if next_token is not None
						 else token.end[1] - token.start[1])
					)
				
				# Fallback for continuation lines without initial keywords such as
				# variable assignments
				#
				# Fixes GL/ntninja/flake8-tabs#5.
				if keyword_indent == Indent.null:
					keyword_indent = Indent(1, 0)
			
			# Calculate expected indentation for the current line
			#
			# While indentation is mostly determined by the contents of the
			# preceding line some adjustments for initial closing brackets
			# on the current line are applied before considering the value
			# final and comparing to the line's actual indentation.
			line_expected_indent: Indent = sum(indent_stack)
			
			# Check if line ends with an opening bracket
			#
			# Depending on whether the lines ends with an opening bracket we'll
			# either expect the following line to be indented with spaces to align
			# with each opened bracket, or expect it to be indented with a single
			# tab for the outermost opened bracket.
			line_ends_with_bracket: bool = map_next(
				lambda t: t.type is categorizer.TokenType.BRACKET_OPEN,
				itertools.dropwhile(
					# Skip end-of-line tokens
					lambda t: t.type in (
						categorizer.TokenType.COMMENT,
						categorizer.TokenType.END_LLINE,
						categorizer.TokenType.END_PLINE,
					),
					reversed(ltokens),
				),
				default=False
			)
			next_line_indent_hanging = (line_ends_with_bracket is True)
			
			# Issue warning if opened bracket implies non-allowed indentation
			# style on next line
			if next_line_indent_hanging and config["continuation-style"] == "aligned":
				self.messages.append((line_start, format_violation(
					113,
					"use of hanging indentation, but option continuation-style=aligned "
					"does not permit this"
				)))
			
			if not next_line_indent_hanging and config["continuation-style"] == "hanging":
				self.messages.append((line_start, format_violation(
					113,
					"use of alignment as indentation, but option continuation-style=hanging "
					"does not permit this"
				)))
			
			# Determine indentation closed by initial closing brackets
			#
			# Unlike other closed brackets, brackets closed at the start of line
			# also decrease the expected indentation on the current line and not
			# just subsequent lines.
			line_initial_closing_brackets: int = sum(1 for _ in itertools.takewhile(
				lambda t: t.type is categorizer.TokenType.BRACKET_CLOSE,
				ltokens,
			))
			line_initial_dedent: Indent = \
				sum(indent_stack[(len(indent_stack) - line_initial_closing_brackets):])
			
			line_expected_indent -= line_initial_dedent
			
			# Calculate expected indentation for next line
			if next_line_indent_hanging:
				# Choose expected number of tabs for indentation on the following
				# lines based on the innermost active category
				indent_tabs = config["indent-levels-expr"]
				if ltokens[-1].category is categorizer.CategoryType.CALL:
					indent_tabs = config["indent-levels-call"]
				elif ltokens[-1].category is categorizer.CategoryType.DEFN:
					indent_tabs = config["indent-levels-defn"]
				
				# Parse indentation of the following line (if any), for cases where we
				# really and truly cannot predict which indentation it should have
				# and therefor need to peak at what is actually there
				next_indent = Indent.null
				try:
					if next_line is not None:
						next_indent = self._parse_line_indent(next_line)
				except ValueError:
					pass
				
				newly_opened_brackets: int = line_initial_closing_brackets
				for token in ltokens:
					if token.type is categorizer.TokenType.BRACKET_OPEN:
						newly_opened_brackets += 1
						
						# Record single added level of indentation on first opened
						# bracket on this line
						if newly_opened_brackets == 1:
							# Apply indentation as spaces or tabs depending on whether
							# the current indentation already contains any spaces
							#
							# This ensures that that we don't create any weird tab/
							# spaces hybrid structures that would look bad if
							# [editor tab width] != config["indent-size"].
							#
							# In order to also support spaces-indented documents we
							# also check whether the current line contains any
							# indentation at all and if that isn't the case we
							# fall back to analyzing the indentation of the next line
							# of the document instead: If it only starts with spaces,
							# we also expect spaces-based indentation, otherwise we
							# expect tabs.
							indent_with_tabs: bool = True
							if sum(indent_stack).characters > 0:
								indent_with_tabs = (sum(indent_stack).spaces < 1)
							elif next_indent.characters > 0:
								indent_with_tabs = (next_indent.tabs > 0)
							
							indent_stack.append(
								Indent(indent_tabs, 0)
								if indent_with_tabs
								else Indent(0, indent_tabs * config["indent-size"])
							)
						else:
							indent_stack.append(Indent.null)
					elif token.type is categorizer.TokenType.BRACKET_CLOSE:
						newly_opened_brackets -= 1
						
						# Pop the indentation added by a previous opening bracket
						#
						# If we have more closing brackets than opening brackets on
						# this line this may also pop brackets added on previous lines.
						indent_stack.pop()
				open_brackets += newly_opened_brackets
			else:
				for token in ltokens:
					if token.type is categorizer.TokenType.BRACKET_OPEN:
						open_brackets += 1
						
						# Record alignment indentation added by the opened bracket
						#
						# Brackets on the same line will be popped again from the stack
						# leaving only those that actually matter when computing the
						# amount of hanging indent added by each bracket. By using
						# `sum(indent_stack).characters` here these previously popped
						# brackets will not be considered when determining the number
						# of characters/spaces added by this opening bracket.
						indent_stack.append(
							Indent(0, token.end[1] - sum(indent_stack).characters)
						)
					elif token.type is categorizer.TokenType.BRACKET_CLOSE:
						open_brackets -= 1
						
						# Pop the indentation added by a previous opening bracket
						#
						# If we have more closing brackets than opening brackets on
						# this line this may also pop brackets added on previous lines.
						indent_stack.pop()
			
			
			# +-----------------------------------------------+ #
			# | Compare found indentation with expected value | #
			# +-----------------------------------------------+ #
			
			# If there are no open braces after the end of the current line,
			# expect the next line to be indented by the size of any leading
			# keyword (useful for `assert`, `with`, …)
			if sum(indent_stack) == first_indent:
				indent_stack[1] = keyword_indent
			
			# Compare settings on current line
			if line_indent != line_expected_indent:
				# Find error code similar to `pycodestyle`
				code = 112
				if line_indent == first_indent:
					code = 122
				elif line_expected_indent.spaces == line_indent.spaces == 0:
					if line_indent.tabs < line_expected_indent.tabs:
						code = 121
					else:
						code = 126
				else:
					if line_indent.spaces > line_expected_indent.spaces:
						code = 127
					else:
						code = 128
				
				# Generate and store error message
				if line_expected_indent.spaces == line_indent.spaces:
					self.messages.append((line_start, format_violation(
						code,
						f"unexpected number of tabs at start of "
						f"{CATEGORY_NAMES[line_category]} line (expected "
						f"{line_expected_indent.tabs}, got {line_indent.tabs})"
					)))
				elif line_expected_indent.tabs == line_indent.tabs:
					self.messages.append((line_start, format_violation(
						code,
						f"unexpected number of spaces at start of "
						f"{CATEGORY_NAMES[line_category]} line (expected "
						f"{line_expected_indent.spaces}, got {line_indent.spaces})"
					)))
				else:
					self.messages.append((line_start, format_violation(
						code,
						f"unexpected number of tabs and spaces at start of "
						f"{CATEGORY_NAMES[line_category]} line " +  # noqa: W504
						"(expected {0.tabs} tabs and {0.spaces} spaces, "
						"got {1.tabs} tabs and {1.spaces} spaces)".format(
							line_expected_indent, line_indent,
						)
					)))
	
	def __iter__(self):
		return iter(self.messages)
