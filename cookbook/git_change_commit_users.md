# Change author and email address on past Git commits

## Only change the latest commit

If you want to change only the last commit, you can do it easily with `--amend`:

```sh
# Amend last commit username and email
git commit --amend --author="Lara Croft<lara@croft.org>" --no-edit
```

## Change multiple previous commits

In case you want to change multiple previous commits information, you will need to use `git rebase`.

Let's say you want to go 10 commits back. Initiate a rebase with:

```sh
# Initiate rebase
git rebase -i HEAD~10
```

At each commit, git will pause to let you change the information. Then you will resume the rebasing process.

```sh
# Amend commit username and email
git commit --amend --author="Lara Croft<lara@croft.org>" --no-edit

# Continue rebasing
git rebase --continue 
```

## Change all commits in a row

Note: this method should be considered carefully, as it rewrites history for all repository collaborators, by creating new commit objects. Hence, anyone working on the repository will need to fetch the rewritten history. More info on [GitHub](https://help.github.com/en/github/using-git/changing-author-info).

This method is useful if you need to change username and email address for a large number of commits, and rebasing + amending each commit is impractical.

First, create a backup of your repository, in case you need to recover the original history.

Then, if you want to change *all* commits, regardless of their author:

```sh
git filter-branch --env-filter '
CORRECT_NAME="Correct Name"
CORRECT_EMAIL="correct-email@example.com"

export GIT_AUTHOR_NAME="$CORRECT_NAME"
export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
' --tag-name-filter cat -- --branches --tags
```

If you only want to rewrite commits that were issued by a *specific email address*:

```sh
git filter-branch --env-filter '

OLD_EMAIL="old-email@example.com"
CORRECT_NAME="Correct Name"
CORRECT_EMAIL="correct-email@example.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
export GIT_COMMITTER_NAME="$CORRECT_NAME"
export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
export GIT_AUTHOR_NAME="$CORRECT_NAME"
export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

## Set the right username and email for future commits

If you committed with the wrong username and/or email address by mistake, you may want to make sure that this will not happen again. 

You can either change the git username and email *locally* (for a specific repository), or *globally* (for all repositories on your computer).

```sh
# Check current parameters
git config user.name
git config user.email
```

```sh
# Set local parameters
git config user.name "Lara Croft"
git config user.email "lara@croft.org"
```

```sh
# Set global parameters
git config --global user.name "Lara Croft"
git config --global user.email "lara@croft.org"
```
