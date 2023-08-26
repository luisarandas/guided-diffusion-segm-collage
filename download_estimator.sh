#!/bin/bash

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git and try again."
    exit 1
fi

mkdir -p libs
cd libs
git clone https://github.com/xuebinqin/DIS.git
echo "Repository downloaded successfully to libs/DIS!"
