You need to create a django application which implements a tree menu.

It is necessary to observe the following conditions:

1. The menu is implemented via template tag.
2. Everything that is above the selected item is expanded. First nesting level under the selected item is also expanded.
3. Stored in the database.
4. Can be edited in the standard Django admin panel.
5. The active menu item is determined based on the URL of the current page.
6. There can be several menus on one page. They should differ by name.
7. When you click on the menu, you navigate to the URL specified in the menu. URL can be specified either explicitly or through the Django's named url system.
8. Try to draw each menu with exactly 1 query to the database

You need a django-app, which allows you to add a menu (one or more) to the database using the admin panel, and draw a menu on any desired page by specifying its name:

`{% draw_menu 'main_menu' %}`

(where "main_menu" is the name of a menu)

You should use only Django and Python's standard library for this task, with no additional 3rd-party libraries.

[Решение](https://github.com/mxmaslin/Test-tasks/blob/master/solutions/python/passport_validator.py "Решение задания на валидацию паспорта")