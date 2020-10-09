# Find files matching pattern in Terminal

Here is a one-liner to find all files matching a pattern, in a folder and its subfolders.

For example on Mac OS X, to find all files which name contains a parenthesis with a number, like `(1)`:

```sh
find . -regex ".([1-9])."
```

And to delete the matching files and folders:

```sh
find . -regex ".([1-9])." -exec rm -rf {} ;
```
