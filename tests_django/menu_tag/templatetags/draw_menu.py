# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

from ..models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context='True')
def draw_menu(context, menu_slug):
    request = context['request']
    url = request.build_absolute_uri().split('?')[0]
    try:
        menu_obj = Menu.objects.get(slug=menu_slug)
    except Menu.DoesNotExist:
        return format_html(
            f'<ul id={menu_slug}>Menu {menu_slug} is absent in DB</ul>')

    item_slug = request.GET.get('item', None)

    def walk_items(item_list):
        item_iterator = iter(item_list)
        try:
            item = next(item_iterator)
            while True:
                try:
                    next_item = next(item_iterator)
                except StopIteration:
                    yield item, None
                    break
                if isinstance(next_item, list):
                    try:
                        iter(next_item)
                    except TypeError:
                        pass
                    else:
                        yield item, next_item
                        item = next(item_iterator)
                        continue
                yield item, None
                item = next_item
        except StopIteration:
            pass

    def list_formatter(item_list):
        output = []
        for item, children in walk_items(item_list):
            sublist = ''
            if children:
                sublist = f'<ul>{list_formatter(children)}</ul>'
            output.append(f'<li><a href="{url}?item={item.slug}">{item.title}</a>{sublist}</li>')
        output = ''.join(output)
        return output

    def item_branch(item_slug):
        branch = []
        sorry = None, branch
        if not item_slug:
            return sorry
        try:
            item = MenuItem.objects.get(slug=item_slug)
        except MenuItem.DoesNotExist:
            return sorry
        children = list(item.children.all()) if item.children.count() else []
        if not item.parent:
            if children:
                branch = [item, children]
            return item, branch
        item_with_siblings = list(item.parent.children.all())
        if children:
            if len(item_with_siblings) < 2:
                item_with_siblings = item.parent.children[0]
            item_pos = item_with_siblings.index(item) + 1
            item_with_siblings = item_with_siblings[:item_pos] + [children] + item_with_siblings[item_pos:]
        branch_temp = []
        while item.parent:
            item = item.parent
            branch_temp.insert(0, item)
        branch_temp.append(item_with_siblings)
        branch = []
        while branch_temp:
            elem = branch_temp.pop()
            branch = [elem, branch] if branch else elem
        return item, branch

    def menu_as_list(branch_item, branch_as_list):
        menu = list(menu_obj.menu_items.filter(parent=None))
        if not branch_item:
            return menu
        if not branch_as_list:
            branch_as_list = [branch_item]
        menu_countains_item = menu_obj.menu_items.filter(
            slug=item_slug).count()
        if menu_countains_item:
            branch_pos = menu.index(branch_item)
            menu.remove(branch_item)
            menu = menu[:branch_pos] + branch_as_list + menu[branch_pos:]
        return menu

    branch_item, branch_as_list = item_branch(item_slug)
    m = menu_as_list(branch_item, branch_as_list)
    if not m:
        m_html = f'The menu {menu_slug} does not contain items'
    else:
        m_html = list_formatter(m)
    m_html = f'<ul id="{menu_slug}">{m_html}</ul>'
    return format_html(m_html)
