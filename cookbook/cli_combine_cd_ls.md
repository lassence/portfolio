# Combine 'cd' & 'ls' into a single command

When working in the Terminal, I find it useful to have a single command for moving to another directory (`cd`) and displaying the content of this directory (`ls`).

Here is how to combine these two steps into a single function named `cs`:

```sh
function cs () {
    cd "$@" && ls -laFGh
}
```
