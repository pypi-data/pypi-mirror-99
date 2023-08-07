# Tab (and Spaces) Style Checker for flake8 _(flake8-tabs)_

[![PyPI](https://img.shields.io/pypi/v/flake8-tabs.svg?label=PyPI&style=flat-square)](https://pypi.org/project/flake8-tabs/
)[![License](https://img.shields.io/pypi/l/flake8-tabs.svg?label=License&style=flat-square&color=red)](https://gitlab.com/ntninja/flake8-tabs/blob/master/LICENSE.md
)[![Download Statistics](https://img.shields.io/pypi/dm/flake8-tabs.svg?label=Downloads&style=flat-square)](https://pypistats.org/packages/flake8-tabs
)[![Standard-readme compliant](https://img.shields.io/badge/Readme%20Style-Standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Like tabs? So do I!

This module provides a smart indentation checking module for the awesome
[`flake8`](https://flake8.readthedocs.io/) style checker suite, featuring
[`pycodestyle`](https://pycodestyle.readthedocs.io/),
[`pyflakes`](https://github.com/PyCQA/pyflakes) and
[`mccabe`](https://github.com/pycqa/mccabe)
by default as well as a minimalist plugin architecture.

When enabled *flake8-tabs* will disable *pycodestyle*'s “tabs_or_spaces”, “continued_indentation”,
“tabs_obsolete” and “trailing_whitespace” checkers by default. Replacing them by its own more
flexible checkers, that allow for the “tabs for indentation, spaces for alignment” paradgime to be
applied to your source code – or simply getting a better indentation checker for your spaces based
source code.

## Table of Contents

  * [Install](#install)
  * [Usage](#usage)
    * [Configuration options](#configuration-options)
  * [Reported Error Codes](#reported-error-codes)
  * [Alternatives](#alternatives)
  * [Contributing](#contributing)
    * [Setting up a local development environment](#setting-up-a-local-development-environment)
  * [License](#license)

## Install

For interactive use (`flake8` command) install using [pip](https://pip.pypa.io/) 19.1+:

```
$ pip install flake8-tabs
```

Or, if `flake8` was installed via [pipx](https://pipxproject.github.io/pipx/) add it that program's virtual environment instead:

```
$ pipx inject flake8 flake8-tabs
```

For adding *flake8-tabs* to your regular linting checks simply ensure that is mentioned in your
development `requirements.txt`, [tox](tox.readthedocs.io/) configuration or wherever your linting
dependencies are stored in your project. There is no way in *flake8* to enforce that a certain
linter is run when invoking the `flake8` command, but you can use `flake8 --help` to view the list
of plugins detected and active (last line of output).

There should be no issues when using this plugin with *flake8* forks like
[flake9](https://pypi.org/project/flake9/) or [flakehell](https://flakehell.readthedocs.io/), but
this has not been tested. Feedback welcome!

## Usage

By default installing *flake8-tabs* will only enable the blank line indentation checker. To enable
*flake8-tabs* for your project proper, you will need to set the
[`use-flake8-tabs`](#use-flake8-tabs) option mentioned below to *true*.

All of the following options are specified using *flake8*'s configuration system. See the relevant
sections on [invoking](https://flake8.pycqa.org/en/latest/user/invocation.html) and
[configuring](https://flake8.pycqa.org/en/latest/user/configuration.html) *flake8* for details on
how and where these options may be used.

### Configuration options

Some of the below options will attempt to use read their defaults from the repository's
[.editorconfig](https://editorconfig.org/) file if one is found. Adding an EditorConfig file
to your project is highly recommended as it will ensure that
[many code editors](https://editorconfig.org/#pre-installed) will automatically set their
editing preferences based on your project's expectations. By using these values by default
*flake8-tabs* saves you from duplicating this configuration between that file and your linter.

All other option defaults, as well as all ultimate defaults tend to reflect recommendations from
[PEP-8](https://www.python.org/dev/peps/pep-0008/).

**Note**: In the following, *indenting* refers to the practice of adding new levels of indentation
(usually using tab key whether you're using tabs or not) on a separate line, while *aligning*
refers to the practice of adding spacing in front of the elements on the following line to make
them visually match the elements on the previous line. *Indentation* may refer to any of the above.

#### `use-flake8-tabs`

 * Default: *false*
 * Allowed values: *true*, *false*

Enable *flake8-tabs* for indentation checking and, by default, disable the all conflicting checkers
from *pycodestyle* (see next option). Without setting this to *true*, or passing `--use-flake8-tabs`
on the command-line, only *flake8-tabs*'s blank line indentation checking will be enabled. While this
flag is disabled it is guaranteed no errors will be reported where *pycodestyle* will not report
one as well. While further checks may be enabled at some point that do not require use of this
flag, they will not ever break this guarantee.

This way you can selectively disable errors from *pycodestyle* and incrementally depend on the
smarter checkers in *flake8-tabs*.

#### `use-pycodestyle-indent`

 * Default: *false* if `use-flake8-tabs` is *true* otherwise *true*
 * Allowed values: *true*, *false*

If *false* indentation style checks from *pycodestyle* will be disabled, see the description of
the previous option for details.

#### `indent-style`

 * Default: `indent_style` property of [.editorconfig](https://editorconfig.org/) or *"keep"* if unset / not found
 * Allowed values: *"tab"*, *"space"*, *"keep"*

The indentation style to expect in newly indented code blocks. By default *flake8-tabs* will simply
analyze what is already there and only ensure that no inconsistent mixture of both tabs and spaces
in the same code block happens. This allows different files, and even different code blocks in the
same file, to use different indentation styles; generally you'll want to pick one and stick with it.

#### `tab-width`

 * Default: `indent_size` property of [.editorconfig](https://editorconfig.org/) or *4* if unset / not found
 * Allowed values: Any integer >= 1

The expected size of each tab in spaces. This is not really specific to this plugin, but used to
properly calculate the required additional spaced indentation when indenting within an aligned
section.

Internally this value is also used to monkeypatch *flake8*'s pretty printing function to expand tabs
to this number of spaces instead of its hard-coded default of 8 spaces per tab.

#### `blank-lines-indent`

 * Default depends on `trim_trailing_whitespace` property of [.editorconfig](https://editorconfig.org/):
    * *"never"* if *true*
    * *"always"* if *false*
    * *"maybe"* if unset / not found
 * Allowed values: *"maybe"*, *"always"*, *"never"*

Whether to allow properly aligned indentation in blank lines. The default value will allow both
aligned indentation and no indentation. *"always"* will require blank lines to contain indentation,
*"never"* will prohibit it.

By properly aligned indentation we mean indentation that has the same value as the indentation of
the next block of source code:

```py
# This is OK (matching indent):
def main():
↹	# … snip …
↹	do_something()
↹	
↹	do_something_else()
↹	# … snip …

# This is not OK (unmatching indent):
def main():
↹	while True:
↹	↹	# … snip …
↹	↹	do_something()
↹	
↹	↹	do_something_else()
↹	↹	# … snip …

# This is by default OK as well (unindented):
def main():
↹	while True:
↹	↹	# … snip …
↹	↹	do_something()

↹	↹	do_something_else()
↹	↹	# … snip …
```

Note that this checker does not ensure that the blank line indentation style is consistent within
a document when set to *"maybe"*, so the following will pass by default but may not be what you
want:

```py
def main():
↹	while True:
↹	↹	# … snip …
↹	↹	do_something()

↹	↹	do_something_else()
↹	↹	
↹	↹	do_more()
↹	↹	# … snip …
```

Please open an issue if ensuring consistent per-document blank line indentation is something you
need.

#### `continuation-style`

 * Default: *"both"*
 * Allowed values: *"aligned"*, *"hanging"*, *"both"*

By default *flake8-tabs* allows lines following the initial line belonging to the same
statement (“continuation lines”) to either align to the innermost opened bracket of the
preceeding line or use 1–2 levels of indenting (see the next set of options) depending on
whether the previous line ended with an opening bracket or not:

```py
# Example for aligned indentation (OK with continuation-style=aligned|both):
def foo_bar(x: int,
␣␣␣␣␣␣␣␣␣␣␣␣y: int) -> str:  # The “y” matches up with the “x” above
↹	return f"{x}, {y}"

# Same code with hanging indentation (OK with continuation-style=hanging|both):
def foo_bar(  # This line ends with an opening bracket
↹	↹	x: int,
↹	↹	y: int,
) -> str:
↹	return f"{x}, {y}"
```

This option can be used to restrict the allowed continuation style to only one of the above
(PEP-8 allows both with semantics very similar to the ones mentioned above). In particular,
setting `continuation-style` to *"hanging"* will ensure that *flake8-tabs* will never allow
a line to contain both spaces and tabs at the same time.


#### Indenting Tab Counts

When using hanging indentation on a continuation line, the following options may be used to
configurate the number of tabs expected on the continuation line. These options are not very
useful if `continuation-style` is set to *"aligned"*.

(Note that a tab here may also refer to an equivalent number of spaces based on the configured
tab width.)

##### `indent-tabs-call`

 * Default: *1*
 * Allowed values: Any integer >= 1

The number of tabs to add when adding the first level of indentation using indenting within a
function or method call:

```py
# Example with: indent-tabs-call=3
x = long_function_name(
↹	↹	↹	{  # First level gets 3 levels of indenting
↹	↹	↹	↹	"name": "value"  # Next level is indented as usual
↹	↹	↹	},
↹	↹	↹	param2, param3
)
```

Usually you should leave this at *1* (PEP-8) but some teams may prefer a value of *2* to function
calls more easily distinguishable from blocks.

##### `indent-tabs-def`

 * Default: *2*
 * Allowed values: Any integer >= 1

The number of tabs to add when adding the first level of indentation using indenting within a
class of method definition:

```py
# Example with the default of: indent-tabs-def=2
def main(
↹	↹	param1, param2, param3,
↹	↹	param4):
↹	initialize_something()
)
```

Notice in the example above how an indent level of *1* would make the elements of the parameter
list hard to distingish from the first statement. Hence PEP-8 recommends either indenting twice
or using alignment instead.

##### `indent-tabs-expr`

 * Default: *1*
 * Allowed values: Any integer >= 1

The number of tabs to add when adding the first level of indentation using indenting within any
other kind of construct (such as a tuple, set, dict, …).


## Reported Error Codes

All error codes were borrowed from *pycodestyle*. You can detect that they were generated by
*flake8-tabs* by them being followed by the word `(flake8-tabs)` as well as the extra `T` added
after the initial severity letter.


| Error Code | Meaning                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------ |
| ET101      | Mixed block of tabs and spaces detected where there as a least one tab *following* a space       |
| ET121, ET122, ET123, ET126, ET127, ET128 | Identation did not match what was expected (somewhat configurable) |
| WT291      | Extranous whitespace detected on end of line                                                     |
| WT293      | Whitespace that was not aligned with the surrounding source detected (configurable)              |

Also note that, due to the way we disable the relevant checkers from *pycodestyle* the following
error codes **do not have an equivalent** in this plugin: E124, E125, E129, E131, E133.


## Alternatives

  * [flake8-expandtab](https://pypi.org/project/flake8-expandtab/) replaces all tabs in the input
    document with a configurable number of spaces before it is passed to *pycodestyle*
     * *Comment*: While its code is a lot simpler, this approach does not prevent inappropriate
       mixing of tabs and spaces on the same line. It will silently allow documents that will
       look broken when viewed with a different tab width setting and will even fail to detect
       documents that are invalid Python due to unparsable mixed spaces/tabs usage.

       That said, it was the primary inspiration for developing this checker in the first place.


## Contributing

As usual, contributions to the project are welcome!

**Please report issues and feature requests** at
[https://gitlab.com/ntninja/flake8-tabs/-/issues/](https://gitlab.com/ntninja/flake8-tabs/-/issues/)
(requires GitLab.com account) after verifying that it hasn't already been reported. In cases where
you believe that *flake8-tabs* is incorrectly reporting a violation or should report a violation
that it is currently not, please include a minimum affected code sample and any reported violations
you are currently seeing.

If you cannot or don't want to create a GitLab.com account, feel free to instead contact me via email
at alexander-f8t@ninetailed.ninja instead. However, please use GitLab instead if you can as it helps
me keep things organized.

**Code and documentation contributions** are of course also welcome. If your new to forking and merge
requests on GitLab [this short guide](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html)
should come in handy. If you need help with anything, feel free to open an issue and I'll try to
guide you through the process if needed.

As with reporting issues you may also contact me via email with patches if using GitLab.com is not
possible for you. Again, using GitLab.com is strongly preferred however.

### Setting up a local development environment

*flake8-tabs* uses [PDM](https://pdm.fming.dev/) for its Python project management needs. Please
refer to its [installation instructions](https://pdm.fming.dev/#installation) before continuting.
(Using the [pipx](https://pipxproject.github.io/pipx/) based installation method on Linux is
highly recommended: As of March 2021, the virtualenv preloading packages shipped with some distros
may cause weird version-conflict related errors in the author's experience.)

After installing PDM, prepare the development environment using:

```
$ pdm install --dev
```

Your locally modified version of *flake8-tabs* may now be invoked using `pdm run`:

```
$ pdm run flake8 […]
```

You can also run your modified version from another directory (such as a project of yours where
*flake8-tabs* exhibits some bad behaviour) using the `-p` option of `pdm run`:

```
~/path/to/your/project$ pdm run -p ~/path/to/flake8-tabs flake8 […]
```

## License

This project is licensed under the GNU Lesser General Public License version 3.0 or (at your option) any later version.

For the full license, please consult the [LICENSE.md](https://gitlab.com/ntninja/flake8-tabs/LICENSE.md) file distributed along with this project.

Copyright owners are:

  * 2017–2021 Alexander Schlarb
  * 2020 Peter Linss