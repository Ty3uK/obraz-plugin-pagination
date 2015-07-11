# -*- coding: utf-8 -*-

# Copyright (c) 2015 Maksim Karelov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Pagination plugin for Obraz.

This plugin creates 'page.paginator' variable for using in 'index.html' template ( every paginated page is a copy of 'index.html' file).
Use Jekyll docs for understand how to use plugin: http://jekyllrb.com/docs/pagination/

Small tip: in Jekyll's templates we have global variable 'paginator', in this plugin we have 'page.paginator' variable.
Edited copy/paste from Jekyll docs:

<!-- Pagination links -->
<div class="pagination">
    {% if page.paginator.previous_page %}
        <a href="{{ page.paginator.previous_page_path }}" class="previous">Previous</a>
    {% else %}
        <span class="previous">Previous</span>
    {% endif %}
    <span class="page_number ">Page: {{ page.paginator.page }} of {{ page.paginator.total_pages }}</span>
    {% if paginator.next_page %}
        <a href="{{ page.paginator.next_page_path }}" class="next">Next</a>
    {% else %}
        <span class="next ">Next</span>
    {% endif %}
</div>

Configuration in `_config.yml`:
    paginate: posts_per_page
    paginate_path: path_for_paginated_pages

Requirements:

* Obraz == 0.9.x
"""

from __future__ import division
import obraz
from math import ceil
from copy import copy

# Set default value of pagination variable
PAGINATE_DEFAULT = 0
# Set default value of pagination_path variable
PAGINATE_PATH_DEFAULT = "/blog/page{num}/"


@obraz.processor
def process_paginator_pages(site):
    print("Generating pagination...")
    paginate = site.get("paginate", PAGINATE_DEFAULT)
    paginate_path = site.get("paginate_path", PAGINATE_PATH_DEFAULT)
    pages = site.get("pages", [])

    posts = sorted(site.get("posts", []), key = lambda x: x['date'].strftime('%d.%m.%Y'), reverse = True)

    posts_count = len(posts)
    pages_count = int(ceil(posts_count / paginate))

    base_page = {}

    paginator_default = {
        'page': 1,
        'per_page': paginate,
        'posts': [],
        'total_posts': len(posts),
        'total_pages': pages_count,
        'previous_page': None,
        'previous_page_path': None,
        'next_page': None,
        'next_page_path': None
    }

    for page in pages:
        if page['path'] == "index.html":
            base_page = page
            base_page['paginator'] = paginator_default
            break

    pagination_pages = [base_page]

    for index in range(1, pages_count + 1):
        if index > 1:
            temp_page = copy(base_page)

            temp_page['paginator'] = copy(paginator_default)
            temp_page['url'] = paginate_path.format(num = index)
            temp_page['path'] = paginate_path.format(num = index)
            temp_page['paginator']['page'] = index

            pagination_pages.append(temp_page)

    current_page = 1
    current_page_posts = []

    for post in posts:
        current_page_posts.append(post)

        if len(current_page_posts) == paginate:
            pagination_page = current_page - 1
            pagination_pages[pagination_page]['paginator']['posts'] = copy(current_page_posts)
            current_page_posts = list()

            if current_page < pages_count:
                pagination_pages[pagination_page]['paginator']['next_page'] = current_page + 1
                pagination_pages[pagination_page]['paginator']['next_page_path'] = paginate_path.format(num = current_page + 1)
            if current_page > 1:
                pagination_pages[pagination_page]['paginator']['previous_page'] = current_page - 1
                pagination_pages[pagination_page]['paginator']['previous_page_path'] = paginate_path.format(num = current_page - 1) if (pagination_page) > 1 else '/'

            current_page += 1

    if posts_count < paginate:
        pagination_pages[0]['paginator']['posts'] = copy(current_page_posts)

    site['pages'] = pagination_pages
