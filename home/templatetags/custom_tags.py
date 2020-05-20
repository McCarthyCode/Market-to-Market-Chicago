from django import template
from html import entities

from home.models import NewsItem

register = template.Library()

@register.simple_tag
def render_news_item(request, item):
    assert isinstance(item, NewsItem)

    html = str(item.render(request).content, 'utf-8')

    skip = {ord(x) for x in '<>"&;'}
    translation_table = {
        key: '&{};'.format(value)
        for key, value in entities.codepoint2name.items() if key not in skip
    }

    return html.translate(translation_table)

@register.simple_tag
def render_category_item(request, item):
    assert isinstance(item, NewsItem)

    html = str(item.render_category(request).content, 'utf-8')

    skip = {ord(x) for x in '<>"&;'}
    translation_table = {
        key: '&{};'.format(value)
        for key, value in entities.codepoint2name.items() if key not in skip
    }

    return html.translate(translation_table)

@register.filter
def modulo(num, val):
    return num % val
