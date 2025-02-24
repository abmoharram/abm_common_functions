#!/bin/bash

# Check if a commit message is provided
if [ -z "$1" ]; then
    echo "Error: No commit message provided."
    echo "Usage: ./p2r.sh \"Your commit message\""
    exit 1
fi

ruff check
ruff format
sleep 1
# Run Git commands
git add .
git commit -m "$1"
git push

# Success message
echo "✅ Changes pushed successfully!"
