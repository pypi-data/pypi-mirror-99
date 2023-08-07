import enum
import tokenize
import typing as ty


# List of keywords in Python as of Python 3.9.2
# See: https://docs.python.org/3/reference/lexical_analysis.html#keywords (update as needed)
KEYWORDS = frozenset({
	"False", "None", "True", "and", "as", "assert", "async", "await", "break",
	"class", "continue", "def", "del", "elif", "else", "except", "finally",
	"for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
	"not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
})

# List of keywords introducing a statement when placed at start of line
KEYWORDS_STATEMENT = frozenset({
	"assert", "async", "break", "class", "continue", "def", "del", "elif",
	"else", "except", "finally", "for", "from", "global", "if", "import",
	"nonlocal", "pass", "raise", "return", "try", "while", "with",
})

# List of keywords that start a new definition (function or class)
KEYWORDS_DEFINITION = frozenset({"def", "class"})

# List of opening and closing brackets
TOKS_BRACKET_OPEN = frozenset({tokenize.LPAR, tokenize.LSQB, tokenize.LBRACE})
TOKS_BRACKET_CLOSE = frozenset({tokenize.RPAR, tokenize.RSQB, tokenize.RBRACE})

# List of tokens ending a logical input line
TOKS_LLINE_END = frozenset({tokenize.NEWLINE, tokenize.ENDMARKER})


class CategoryType(enum.Enum):
	CALL = enum.auto()
	DEFN = enum.auto()
	EXPR = enum.auto()
	STMT = enum.auto()


class TokenType(enum.Enum):
	TEXT      = enum.auto()
	COMMENT   = enum.auto()
	KEYWORD   = enum.auto()
	END_LLINE = enum.auto()
	END_PLINE = enum.auto()
	
	INDENT = enum.auto()
	DEDENT = enum.auto()
	
	BRACKET_OPEN  = enum.auto()
	BRACKET_CLOSE = enum.auto()


class Token(ty.NamedTuple):
	type: TokenType
	string: str
	start: ty.Tuple[int, int]
	end: ty.Tuple[int, int]
	line: str
	category: CategoryType
	
	@classmethod
	def with_tokenize_token(
			cls,
			type: TokenType,
			token_info: tokenize.TokenInfo,
			category: CategoryType = None,
	) -> "Token":
		return cls(
			type,
			token_info.string,
			token_info.start,
			token_info.end,
			token_info.line,
			category,
		)


class Categorizer:
	"""Simplifies and enriches a token stream by assigning indentation categories
	
	The assigned categories are:
	
	 * ``DEFN`` – Function or class definition
	 * ``CALL`` – Function, method or class call
	   (lexical non-keyword name followed by an opening parenthese)
	 * ``STMT`` – Arbitrary statement that is not also a definition
	 * ``EXPR`` – Arbitrary expression that is not also a call or statement
	
	Additionally some metadata, such as reliable logical and physical end-of-line
	markers are reported and unlike :mod:`tokenize`, continuation lines
	(backslash followed by newline) are reported as physical line endings instead
	of being silently ignored."""
	_categories: ty.List[CategoryType]
	_category_curr: CategoryType
	_category_next: CategoryType
	_prev_token: ty.Optional[tokenize.TokenInfo]
	
	def __init__(self) -> None:
		self.reset()
	
	def reset(self) -> None:
		# A note on the relationship between `_categories`, `_categories_curr`
		# and `_category_next`:
		#
		#  * `_categories` represents the “category stack” and `_category_next`
		#    is the currently queued value to be pushed onto this stack:
		#     * When opening a bracket the current value of `_category_next`
		#       is pushed onto `_categories` and becomes the new `_category_curr`
		#     * When closing a bracket the top-most value in `_categories` is
		#       popped into `_category_next` and `_category_curr` is set to the
		#       new `_categories[-1]` value
		#  * `_category_curr` is the currently active category value and is
		#    reported to the caller with every reported token
		#
		# In general `_categories[-1]` and `_category_curr` should match, the
		# only current exception is when parsing the regular name token followed
		# by an opening parenthese of a function call. In this case, the values
		# of `_category_curr` and `_category_next` will be `CategoryType.CALL`
		# to prepare the category state for the upcoming function call, while
		# ensure that the category of the surrounding context is restored after
		# the function call's closing parenthese is encountered.
		#
		# Additionally, whenever an opening bracket is encountered the value of
		# `_category_next` is set to `EXPR`, so that the next opening bracket
		# within the opened bracket will be considered an arbitrary expression
		# category (tuple, dict/set, list) unless a function call is detected
		# first.
		self._categories    = [CategoryType.STMT]
		self._category_curr = CategoryType.STMT
		self._category_next = CategoryType.STMT
		
		self._prev_token = None
	
	def push(self, token: tokenize.TokenInfo) -> ty.Generator[Token, ty.Any, None]:
		if token.exact_type == tokenize.ENCODING:
			# This token is for information only and does not actually correspond
			# to any source code
			return
		
		if self._prev_token is not None:
			yield from self._parse(self._prev_token, token)
			
			# Fix up for missing physical line notifications on continuation lines
			if self._prev_token.end[0] < token.start[0] and \
			   self._prev_token.exact_type != tokenize.NL:
				string = self._prev_token.line[self._prev_token.end[1]:].lstrip()
				yield Token(
					TokenType.END_PLINE,
					string,
					(self._prev_token.end[0], len(self._prev_token.line) - len(string)),
					(self._prev_token.end[0], len(self._prev_token.line)),
					self._prev_token.line,
					self._category_curr
				)
		
		if token.type in TOKS_LLINE_END:
			# Emit end of logical line token
			yield Token.with_tokenize_token(
				TokenType.END_LLINE, token, self._category_curr
			)
			
			# Reset categorization logic after every logical line
			self.reset()
		else:
			self._prev_token = token
	
	def close(self) -> ty.Generator[Token, ty.Any, None]:
		if self._prev_token is not None:
			yield from self._parse(self._prev_token, tokenize.TokenInfo(
				tokenize.ENDMARKER,
				"",
				self._prev_token.end,
				self._prev_token.end,
				self._prev_token.line,
			))
		
		self.reset()
	
	@classmethod
	def process_all(cls, tokens: ty.Iterable[tokenize.TokenInfo]) \
	    -> ty.Generator[Token, ty.Any, None]:
		instance = cls()
		
		for token in tokens:
			yield from instance.push(token)
		
		yield from instance.close()
	
	def _parse(self, token: tokenize.TokenInfo, next_token: tokenize.TokenInfo) \
	    -> ty.Generator[Token, ty.Any, None]:
		res_token_type: TokenType = TokenType.TEXT
		
		# Distinguish keywords from other names (why doesn't `tokenize` do this!?)
		is_keyword = (token.type == tokenize.NAME and token.string in KEYWORDS)
		
		if is_keyword:
			# Disambiguate between arbitrary statements and function/class
			# definitions
			if self._category_curr is CategoryType.STMT:
				if token.string in KEYWORDS_DEFINITION:
					self._categories[-1] = self._category_curr = \
						self._category_next = CategoryType.DEFN
				elif token.string == "async" \
				     and next_token.type == tokenize.NAME \
				     and next_token.string in KEYWORDS_DEFINITION:
					self._categories[-1] = self._category_curr = \
						self._category_next = CategoryType.DEFN
			
			res_token_type = TokenType.KEYWORD
		elif token.exact_type == tokenize.NAME:
			# Detect function calls in expressions/statements
			#
			# Idea: Non-keyword name that is not part of a definition and followed
			# by an opening parenthese is a function call.
			if self._category_curr != CategoryType.DEFN \
			   and next_token.exact_type == tokenize.LPAR:
				self._category_curr = self._category_next = CategoryType.CALL
		elif token.exact_type in TOKS_BRACKET_OPEN:
			# Perform steps described in `__init__` to switch to new category state
			self._categories.append(self._category_next)
			self._category_curr = self._category_next
			self._category_next = CategoryType.EXPR
			
			res_token_type = TokenType.BRACKET_OPEN
		elif token.exact_type in TOKS_BRACKET_CLOSE:
			# Perform steps described in `__init__` to restore category state
			self._category_next = self._categories.pop()
			self._category_curr = self._categories[-1]
			
			res_token_type = TokenType.BRACKET_CLOSE
		elif token.exact_type == tokenize.COMMENT:
			res_token_type = TokenType.COMMENT
		elif token.exact_type == tokenize.NL:
			res_token_type = TokenType.END_PLINE
		elif token.exact_type == tokenize.INDENT:
			res_token_type = TokenType.INDENT
		elif token.exact_type == tokenize.DEDENT:
			res_token_type = TokenType.DEDENT
		
		yield Token.with_tokenize_token(
			res_token_type, token, self._category_curr
		)


if __name__ == "__main__":
	import pathlib
	
	__dirpath__ = pathlib.Path(__file__).parent
	
	with open(__dirpath__ / ".." / "tests" / "ok.py", "rb") as f:
		tokenizer = tokenize.tokenize(f.readline)
		for token in Categorizer.process_all(tokenizer):
			span = f"{token.start[0]},{token.start[1]}-{token.end[0]},{token.end[1]}:"
			print(f"{span:20}{token.type.name:15}{token.category.name:6}{token.string!r}")
