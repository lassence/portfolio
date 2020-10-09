# Delete all .DS_Store files on MacOS

You can write a function in bash or zsh to delete all your [`.DS_Store`](https://en.wikipedia.org/wiki/.DS_Store) cache files from your home directory on Mac OS. 

Copy the following line to your `.bashrc` or `.zshrc` file, located at the root of your home directory:
```sh
alias cleards="find ~/ -type f -name '*.DS_Store' -ls -delete 2>/dev/null;"
```

Next time you log into your terminal, just type: `cleards`.
