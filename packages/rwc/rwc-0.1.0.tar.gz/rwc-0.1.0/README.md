# rwc

A reStructuredText and Markdown wordcounter,
designed for long-form writing.

rwc looks for reStructuredText and Markdown files
in the directory (or directories) passed on the command line,
renders them to HTML,
strips away everything but the text from that rendered HTML,
and does per-file word counts on that text,
outputting the count per file
as well as a total for the directory.

## Usage

```shell
$ ls
test-one.md test-two.rst test-three.rst

$ rwc .
test-one.md: 10 words
test-two.rst: 10 words
test-three.rst: 23 words
-----
total: 43 words
```

## License

rwc is licensed under the MIT License.
See [the LICENSE file](./LICENSE).
