#!/usr/bin/python2.7
# coding: utf-8
from __future__ import print_function
import commands

def run(dr, fname, title):
    path = '%s/%s' % (dr, fname)
    gen_post = 'hexo new post {title} -p {path}'.format(title=title, path=path)
    code, out = commands.getstatusoutput(gen_post)
    if code == 0:
        fpath = out.split('Created: ')[1]
        code, out = commands.getstatusoutput('open %s' % fpath)


def main():
    dr = raw_input("目录？(blog) ")
    if not dr:
        dr = 'blog'
    fname = raw_input("文件名？(blog) ")
    if not fname:
        fname = 'default'
    title = raw_input("标题？(blog) ")
    if not title:
        title = fname

    run(dr, fname, title)
    print('完成')


if __name__ == "__main__":
    main()
