#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Steve Sun'
SITENAME = u'Way2Steve'
SITEURL = 'http://www.v2steve.com'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh_CN'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_DATE_FORMAT = '%Y-%m-%d(%a)'

# Blogroll
LINKS = (
            ('aboutMe', 'http://v2steve.com/'),
        )

# Social widget
SOCIAL = (
            ('github', 'http://github.com/sundiontheway/'),
            ('weibo', 'http://weibo.com/smartdie'),
         )

DEFAULT_PAGINATION = 10

THEME = "./mytheme/pelican-svbtle/"
