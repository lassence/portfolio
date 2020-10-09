# Batch convert files encoding in Terminal

On Mac OS X and Linux, you can convert files encoding in batch with `iconv`.

## Check encoding of a file

Mac OS X: `file -I file.txt`

Linux: `file -i file.txt`

## Convert files to new encoding 

For example, to convert all `.html` files from ISO-8859-1 to UTF-8, and save them with the same name.

On Mac OS X:

```sh
find . -name "*.html" \
-exec sh -c "iconv -f ISO-8859-1 -t UTF-8 {} > {}.utf8" \; \
-exec mv "{}".utf8 "{}" \;
```

On Linux:

```sh
find . -name "*.html" \
-exec sh -c "iconv -f ISO-8859-1 -t UTF-8 {} -o {}" \;
```
