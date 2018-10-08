#!/bin/bash

work_dir=`dirname $0`
cd "$work_dir"
echo " Working Directory: $work_dir "

case "$1" in
  "transfer")
    python script/transfer.py
    ;;
  "new")
    hexo new post "$2"
  "run")
    hexo clean && hexo g
    hexo s
    ;;
  "d")
    hexo clean && hexo g
    hexo d
    exit 0
    ;;
  *)
    hexo clean && hexo g
    exit 0
   ;;
esac