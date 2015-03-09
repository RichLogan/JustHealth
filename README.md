# How to Win Life

## Add a Change

    $ git add fileName
    $ git commit -m "Commit Message"
    $ git push

Try and keep commits as logical groupings of files. If you have edited a number of files for one thing, and a nmber for others then don't commit all files at once, do a commit for each set of similar files.

## Use descriptive commit messages
Explain quickly what you've done and what it changes. Link to issues.

Note: You can refer to Issues in commit messages using #issueNumber, e.g "Added section to ChangeManagement as per #1" and they will link automatically. A commit message such as "Resolves #1" or "Fixes #1" will automatically close the issue.

## Log tasks and bugs as issues

Label, assign and use milestones properly

## Use git properly

    $ git status
You can use this to work out what state you working directory is in. It will show you've changed that you haven't added, what's been added but not committed, and in what state your working directory is in compared to master.
* * *
    $ git pull
Remember to do this in order to pull down other peoples changes.
* * *

## Branches
Remember to use branches! A branch should be created for each feature. All code on the master branch should be deployable at any time.

A branch is a copy of the Master code at the point where it was created, and any changes to that branch do NOT effect Master. This means you are free to work without worrying about breaking anything on Master.

To switch to a branch you use:

    $ git checkout branchName

To create a new branch you can use:

    $ git checkout -b branchName

and you will switch to the new branch automatically.

You then add and commit as normal, but when it comes to push rather than the usual push origin master it would be:

    $ git push origin branchName

When you have completed working on your feature and it is ready to be merged into Master, you simply switch back to Master:

    $ git checkout Master

and merge your branch

    $ git merge branchName

If your branch only changes files that have not been changed since the branch was created, everything will be fine. If it changes a file that has been changed since the branch was made then there will be a conflict. This is not as scary as it sounds. It will edit the conflicted files to show both versions. You simply have to go in and change it to what it should be and recommit :)

For example, imagine there is a file with one word on Master and the word is Person.

1. I create a Branch to work on it.
2. Steve then also creates a branch, changes Person to Steve and then commits and merges to Master. The word on Master now says Steve, but on my branch it will still say Person.
3. I change my Person to Rich and commit and try to merge.It will tell me there is a conflict and my file will change from just having the word Rich to looking like this:<div>
<<<<<<< HEAD
</div>
<div>
Steve
</div>
<div>
=======
</div>
<div>
Rich
</div>
<div>
>>>>>>> master
</div>

4. I will have to go in and decide whether it should actually say Steve or Rich and replace all of that (all lines and arrows) with what I want (Just Steve or Rich or both or something completely different), then re-add/commit/push. Re-adding a file marks that commit as fixed.

## Users
Account Type    Username    Password
Carer           emma123     hello
Patient         chutchinson hello1
