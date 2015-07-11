##Pagination plugin for Obraz.  
This plugin creates 'page.paginator' variable for using in 'index.html' template ( every paginated page is a copy of 'index.html' file).  
Use [Jekyll docs](http://jekyllrb.com/docs/pagination/) for understanding how to use plugin.

Small tip: in Jekyll's templates we have global variable * **'paginator'** * in this plugin we have * **'page.paginator'** * variable.  
Edited copy/paste from Jekyll docs:  
```htmldjango
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
```

Configuration in `_config.yml`:  
```yml
    paginate: posts_per_page
    paginate_path: path_for_paginated_pages
```

Requirements:  
* [Obraz](http://obraz.pirx.ru/) == 0.9.x
