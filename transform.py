#!/usr/bin/python
# coding: utf-8
from __future__ import print_function
import os
import sys
import time

profix = '''\
title: {title}
date: {date}
categories:
tags:
---
'''

more_tag = '\n<!--more-->\n'

cur_dir = os.path.dirname(__file__)
post_dir = os.path.join(cur_dir, 'source/_posts')
essay_dir = os.path.join(cur_dir, 'source/_essays')
draft_dir = os.path.join(cur_dir, 'source/_drafts')

def _count_word(text):
    num = 0
    for i in text:
        if i not in ' \n!"#$%&amp;()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~':
            num = num +1
    return num


def _format(fname):
    fsrc = os.path.join(draft_dir, fname)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cache, tmp, line = [], '', ''
    mark = False

    with open(fsrc, 'r') as src:
        line = src.readline()
        if '#' in line:
            title = line.lstrip('# ').rstrip('\n')
            cache.append(profix.format(title=title, date=date))
        elif 'title' in line:
            return
        while 1:
            line = src.readline()
            if line == '\n':
                cache.append(line)
            elif '>' in line:
                cache.append(line)
                cache.append(more_tag)
                mark = True
                break
            else:
                break

        content = src.read()

        if mark:
            num = _count_word(content.decode('utf-8'))
            rtime = int(num/500)
            tag = '\n** 本文%s字  %s分钟读完 **\n\n' % (num, rtime)
            cache.append(tag)

        cache.append(content)
        tmp = ''.join(cache)

    if mark:
        fdst = os.path.join(essay_dir, fname)
    else:
        fdst = os.path.join(post_dir, fname)

    print("Transform {0} --> {1}".format(fsrc, fdst))

    with open(fdst, 'w') as dst:
        dst.write(tmp)

    # print("Remove {0}".format(fsrc))
    # os.remove(src)
    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        title = sys.argv[1]
        fname = "%s.md" % title
        _format(fname)
    else:
        fnames = os.listdir(draft_dir)
        for fname in fnames:
            if fname.endswith('.md'):
                _format(fname)


