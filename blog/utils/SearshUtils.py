from flask_paginate import Pagination, get_page_parameter
from flask import request
from blog.models.BookModel import Book
from blog import cfg
def get_pagination(items):
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = cfg.ITEMS_PER_PAGE
        # تحديد بداية ونهاية العناصر لهذه الصفحة
        start = (page - 1) * per_page
        end = start + per_page
 
        pagination = Pagination(page=page, total=len(items), per_page=per_page, css_framework='bootstrap4')
        return start, end, pagination