import functools
import pathlib
import typing as ty

import editorconfig
import editorconfig.ini


if ty.TYPE_CHECKING:
	import os


MAX_CONFIG_SEARCH_DEPTH: int = 25
STOP_CONFIG_SEARCH_ON_DIRS: ty.Tuple[str, ...] = (".git", ".hg")

_STR_BOOLEAN_MAPPING = {
	"y": True,
	"yes": True,
	"t": True,
	"on": True,
	"1": True,
	"true": True,
	"n": False,
	"no": False,
	"f": False,
	"off": False,
	"0": False,
	"false": False,
}


@functools.lru_cache(maxsize=1)
def query_filepath(filepath: ty.Union[bytes, str, "os.PathLike"]):
	filepath = pathlib.Path(filepath).absolute()
	handler = editorconfig.EditorConfigHandler(filepath)
	
	# Reimplement `handler.get_configuration` using private APIs, stopping when reaching a VCS root
	#
	# Inspired by https://github.com/PyCQA/isort/blob/a07bdf3cf7484dfb7570b4eec076fc0bc483b79a/isort/settings.py  # noqa: E501
	try:
		handler.check_assertions()
		
		search_directory = filepath.parent
		for _ in range(MAX_CONFIG_SEARCH_DEPTH):
			parser = editorconfig.ini.EditorConfigParser(filepath)
			parser.read(search_directory / handler.conf_filename)
			
			# Merge new EditorConfig file's options into current options
			old_options = handler.options
			handler.options = parser.options
			if old_options:
				handler.options.update(old_options)
			
			# Stop parsing if parsed file has a `root = true` option
			if parser.root_file:
				break
			
			# Stop when hitting VCS root
			hit_stop_dir = False
			for stop_dirname in STOP_CONFIG_SEARCH_ON_DIRS:
				if (search_directory / stop_dirname).is_dir():
					hit_stop_dir = True
					break
			if hit_stop_dir:
				break
			
			# Stop when hitting file system root
			if search_directory.parent == search_directory:
				break
			
			# Try next directory
			search_directory = search_directory.parent
		
		handler.preprocess_values()
		
		# Fix up value types that shouldn't be `str`
		for key in ("insert_final_newline", "trim_trailing_whitespace"):
			if key not in handler.options:
				continue
			
			try:
				value_str = str(handler.options[key]).lower()
				handler.options[key] = _STR_BOOLEAN_MAPPING[value_str]
			except KeyError:
				del handler.options[key]
		
		for key in ("indent_size", "max_line_length", "tab_width"):
			if key not in handler.options:
				continue
			
			try:
				handler.options[key] = int(handler.options[key])
			except ValueError:
				del handler.options[key]
		
		return handler.options
	except editorconfig.EditorConfigError:
		return {}
