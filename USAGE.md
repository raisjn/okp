# CPY basics

okp is a CPY processor that translates [CPY](https://github.com/vrsperanza/CPY)
code into cpp. The original CPY processor is written in C++, while okp is
implemented in python. okp also has a few extensions to make code look more
pythonic.


~~~~~
usage: okp [-h] [-ni] [-r] [-ri] [-o EXENAME] [-d DIR] [-v] [-p] [-k] [-c]
           [-for] [-rof] [-t]
           [files [files ...]]

Process .cpy files into C++

positional arguments:
  files                 list of files to process and compile

optional arguments:
  -h, --help            show this help message and exit
  -ni, --disable-implication
                        disables variable implication
  -r, --run             invoke executable after compiling it
  -ri, --run-with-stdin
                        invoke executable after compiling it and pass stdin to
                        it
  -o EXENAME, --output EXENAME
                        set the name of the executable file
  -d DIR, --dir DIR     output source files to this directory. implies -k
  -v, --verbose
  -p, --print           print translated C++ source code
  -k, --keep-dir        keep compilation directory around
  -c, -ne, --no-exe     compile .o files only (no main)
  -for, --enable-for    enable for loop shorthand
  -rof, --enable-rof    enable rof loop shorthand
  -t, --transpile       don't compile code, only transpile
  -sh, --single-header  transpile into a single header file
~~~~~

**NOTE**: any lines that start with `\`` will be ignored by the okp processor
and treated as raw c++. Surrounding multiple lines of code with triple
backticks will also treat those lines as raw c++.

## Bugs

If there are any bugs or problems with okp's processing, please open an issue
to get it resolved ASAP. Parsing a language is tricky and okp is not a full
language parser


## Sugar

### Indentation based blocks

In CPY, indentation is used instead of curly brackets. Instead of writing:

~~~~~
int main() {
  return 0
}

you write:

int main(): // the colon is optional
  return 0
~~~~~

### Optional parentheses

You can leave out parentheses in most `for` and `while` loops as well as
`switch` statements, so `for i = 0; i < 10; i++:` is valid, as is `while True:`

### Function argument type coalescing

Multiple arguments of the same type can be coalesced in function declarations, so `def foo(int a, b, c)` will mark `a`, `b` and `c` as integers.

### Function type inference

if a function definition is missing its type annotation, the function is annotated as `auto`. So `def main()` turns into `auto main()`, while `int main()` will stay `int main()`.

### Variable type inference

When a variable is seen for the first time in its lexical scope it will be
annotated with `auto`. Lexical scope is determined by indentation level. A
child block inherits its parents scope. See the `known` keyword for more
details.

### Variable destructuring

`return a,b` and `a,b = foo()` are both valid. `return a,b` turns a,b into a tuple, while `a,b = foo()` uses `std:tie` to assign a,b to the results of foo().

### Automatic semi-colons

okp automatically adds semi-colons to the end of lines when necessary (and
sometimes even when not necessary)

### Automatic #includes

When certain keywords are used, okp will automatically import the appropriate
module. The supported modules are iostream, vector, tuple, queue, dequeue, map,
unordered\_map and cstdio.

### Automatic header file creation

When a .cpy file is encountered by okp, it generates two files: a .cpp file and
a .h file. The .h file contains the functions and classes from the .cpp file,
so its possible to use one .cpy file from another. To do so, you would use the
line `#include foo.h` or `import foo`

### Ignoring cpp code

Sometimes you might want to mix .cpy and .cpp code in the same file. There are
two ways of doing this: one is to prepend `$` to the beginning of a line of cpp
code, the other is to surround a block of cpp code with triple backticks

### Joining multi-line statements

okp uses the backslash character at the end of lines to indicate that two lines
should be joined. okp will automatically join lines inside parentheses but will
not join lines inside curly braces.


~~~~~~
a = foo(
  1,
  2,
  3
)

becomes

a = foo(1,2,3);
~~~~~~~

but

~~~~~~~
a = foo({
  1,
  2,
  3
})
~~~~~~~

will not be joined (and lead to an okp induced syntax error) because the lines
are inside an open bracket.

to join lines inside curly braces, a % sign can be added to the opening brace
and all lines up to the corresponding closing brace will be joined into one
line.

~~~~~~
a = { \
  .foo=1, \
  .bar=2, \
  .baz=3, \
}

a = %{
  .foo=1,
  .bar=2,
  .baz=3
}

both become

a = { .foo=1, .bar=2, .baz=3 }
~~~~~~


## Keywords

### block (okp extension)

To manually create blocks or insert curly brackets, the `block` keyword can be used.

~~~~~
block:
  foo = 10

translates to

/* block: */ {
  auto foo = 10; };
~~~~~

### def (okp extension)

`def` can be used to mark a function but is optional. It's purely decoration
because `main():` works the same as `def main():`

### for and rof

When the -for is used, for loop shortening is enabled. `for x 0 10` turns into
`for x = 0; x < 10; x++`. `for x a b c` turns into `for x = a; x < b; x += c`.

When the -rof flag is set, reverse for loop shortening is turned on: `rof a b
c` turns into `for x = a; x > b; x -= c`. Like the `for` shoretening syntax,
The `c` parameter is optional

### io shorthand

`!!` and `puts` are io keywords that translate into cout statements.  `?` and
`??` translate into cin statements. They are not recommended for usage but are
implemented for compartibility with CPY's implementation.


### known

okp supports automatic lexical scoping of variables. If a variable is seen for the first time, then it will be prefixed with `auto`. For example:

~~~~~
def main():
  foo = 10
  print foo

turns into

auto main():
  auto foo = 10
  cout << foo
~~~~~

To disable the auto prefixing of a variable, the `known` keyword can be used, like:

~~~~~
def main():
  known foo = 10

will translate to:

auto main():
  foo = 10
~~~~~

The known keyword is useful in advanced situations or where the lexical scoping
fails.

### pass (okp extension)

`pass` gets translated into `(void)0`. Its mostly useful as a placeholder line

### print (okp extension)

In okp dialect, `print a,b,c` gets translated into cout << a << b << c << endl.
If the line ends with a comma, the endl is not added

### raw_input (okp extension)

In okp dialect, `raw_input a,b,c` gets translated into `cin >> a >> b >> c`.

### self (okp extension)

`self.` gets translated into `this->` to make the code look more pythonic

### static initialization

if the `-ig` flag is used, it's possible to declare and initializes static
variables inline at the namespace level, like: `static int foo = 1`. it's also
possible to declare and initialize variables like `extern int foo = 1` at the
class level.
