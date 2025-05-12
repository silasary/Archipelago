#!/bin/bash

# Define the branch name
BRANCH="sims4"

# Check the first argument to decide which action to perform
if [ "$1" == "sync" ]; then
    # Switch upstream to sims4/main for syncing
    git branch --set-upstream-to=sims4/main $BRANCH
    echo "Upstream set to sims4/main for syncing"
elif [ "$1" == "work" ]; then
    # Switch upstream to origin/patch-2 for local work
    git branch --set-upstream-to=origin/$BRANCH $BRANCH
    echo "Upstream set to origin/sims4 for local work"
else
    echo "Usage: $0 [sync|work]"
    exit 1
fi
