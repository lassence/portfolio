# Squash and reorder commits in Git

You can reorder and squash (merge together) commits in Git using the powerful `rebase` function.

## Rebase

To start a rebase over the last 10 commits, type:

```sh
git rebase -i HEAD~10
```

You will have to edit a file, where you can proceed to multiple changes in the branch history.

To *reorder commits*, cut the corresponding line (Ctrl-K) and paste it (Ctrl-U) on its new place in history.

To *squash commits together*, replace the `pick` prefix with `s` for all commits that should be squashed with the line above.

When you are satisfied, save (Ctrl-O) and quit (Ctrl-X). For squashes, you will be prompted to confirm or amend commit messages.

## Force push to the remote repository

You can check that the history was rearranged as expected with:

```sh
git log -10
```

If you are satisfied, you need to force push the branch to the remote repository. *Warning*: there is no going back after this point. Once rewritten on your local repository and pushed to remote, you cannot recover the old history.

Assuming you are working on `master` branch, type:

```sh
git push --force origin master
```

## Force pull on another local repository

In case you have other machines with the repository locally, you have to reset it to the new version with:

```sh
git fetch
git reset --hard origin/master
```
