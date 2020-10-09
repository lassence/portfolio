# Manage multiple Git accounts locally

When working on the same machine with multiple projects linked to different GitHub/GitLab/BitBucket/etc. accounts, you may need to handle multiple usernames, email addresses, and SSH keys.

## Usernames and emails

A manual solution can be to set the username and email address for each repository. However if you have numerous projects, it can be tedious and error-prone.

A more systemic solution is to manage your identities in a configuration file.

1. Create or edit a file named `.gitconfig` in your Home directory.
2. Since Git 2.13 you can use [conditional includes](https://git-scm.com/docs/git-config#_conditional_includes), which link to different config files based on the projects directories. For instance:

 ```ini
# Default credentials
[user]
    name = my_username
    email = me@email.com

# Work credentials
[includeIf "gitdir:~/work/"]
    path = ~/work.gitconfig

# Side projects credentials
[includeIf "gitdir:~/side-projects/"]
    path = ~/side.gitconfig
```

3. For each custom credential, create a `.gitconfig` file with the relevant parameters. For example, in `~/work.gitconfig`:

```ini
[user]
    name = work_username
    email = me@corporate.com
```
Beyond username and email, you can specify any additional git parameter in these files.

## SSH keys

First, generate one SSH key per Git account, and add them to their GitHub/GitLab/BitBucket accounts. You can refer to this [tutorial](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

Your multiple SSH keys will be handled in a file named `~/.ssh/config`. Create or edit the file, and write one entry per account, like this:

```sh
# Personal GitHub
Host github.com   # Default GitHub host name
   HostName github.com
   User git
   IdentityFile ~/.ssh/id_rsa

# Work Github
Host github.com-work   # Alias host for your work GitHub account
   HostName github.com
   User git
   IdentityFile ~/.ssh/work

# Personal GitLab
Host gitlab.com   # No need for an alias if you only use one GitLab account
   HostName gitlab.com
   User git
   IdentityFile ~/.ssh/gitlab
```

If you have multiple accounts by the same Git provider (like GitHub in this example), you need a different **Host** name for each account. In the above example, we replaced `Host github.com` with `Host github.com-work` for the GitHub work account.

Finally, you will have to change the **remote URL** with the alias **Host** name in the relevant repositories. For the GitHub work account in this example:  

1. When cloning a repository,  
replace `git clone git@github.com:user/repo.git`  
with `git clone git@github.com-work:user/repo.git`

2. For an existing repository on your machine,  
update the remote address with `git remote set-url origin git@github.com-work:user/repo.git`,  
and check the change with `git remote -v`.
