---
title: Git 笔记
date: 2016-05-30 20:06:12
tags: Git
categories: 工具
---

Recording some usefull but easy to forget git commands

# user setting

    git config --global user.name "Your username"
    git config --global user.email "Your email"

without "--global" if just this time.

# modify comment for last commit

    git commit --amend

# additinally add after commit

    git commit -m <"XXXXX">
    git add <some_forgotten_files>
    git commit --amend

# delete

    git rm <file>           # del both working dir and staged snapshot
    git rm -f <file>        # after add, del both working dir and staged snapshot
    git rm --cached <file>  # keep file in working dir, but del in staged snapshot

# diff

    git diff                # working dir vs staged snapshot
    git diff --cached       # staged snapshot vs commit history

# branch

    git branch <name>       # create new branch
    git checkout <name>     # switch branch
    git checkout -b <name>  # create and switch to new branch
    git branch              # show all local branch
    git branch -d <name>    # del local branch
    git push <remote_name> :<remote_branch_name>  # del remote branch

