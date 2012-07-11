#!/bin/bash
#
# git-svn-diff originally by (http://mojodna.net/2009/02/24/my-work-git-workflow.html)
# modified by mike@mikepearce.net
# modified by aconway@[redacted] - handle diffs that introduce new files
# modified by t.broyer@ltgt.net - fixes diffs that introduce new files
# modified by m@rkj.me - fix sed syntax issue in OS X
#
# Generate an SVN-compatible diff against the tip of the tracking branch

# Get the tracking branch (if we're on a branch)
TRACKING_BRANCH=`git svn info | grep URL | sed -e 's/.*\/branches\///'`

# If the tracking branch has 'URL' at the beginning, then the sed wasn't successful and
# we'll fall back to the svn-remote config option
if [[ "$TRACKING_BRANCH" =~ URL.* ]]
then
        TRACKING_BRANCH=`git config --get svn-remote.svn.fetch | sed -e 's/.*:refs\/remotes\///'`
fi

# Get the highest revision number
REV=`git svn find-rev $(git rev-list --date-order --max-count=1 $TRACKING_BRANCH)`

# Then do the diff from the highest revision on the current branch 
# and masssage into SVN format
git diff --no-prefix $(git rev-list --date-order --max-count=1 $TRACKING_BRANCH) $* |
sed -e "/--- \/dev\/null/{ N; s|^--- /dev/null\n+++ \(.*\)|---\1	(revision 0)\n+++\1	(revision 0)|;}" \
    -e "s/^--- .*/&	(revision $REV)/" \
    -e "s/^+++ .*/&	(working copy)/" \
    -e "s/^diff --git [^[:space:]]*/Index:/" \
    -e "s/^index.*/===================================================================/"
