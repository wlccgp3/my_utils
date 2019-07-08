#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from IPython.display import publish_display_data
from IPython.core.interactiveshell import InteractiveShell
from .tools import MagicList


formater = InteractiveShell.instance().display_formatter.format

__all__ = ['custom_display']


def custom_display(*objs, title='', symbol=':'):
    title_list = MagicList(title.split(';'))
    symbol_list = MagicList(symbol.split(';'))

    format_dict = {}
    html = []
    plain = []

    length = len(objs)
    plain_top_px = 5
    symbol_left_px = 5  # 连接符边距
    symbol_top_px = plain_top_px + 5  # 连接符号上高度
    title_bottom_px = 2  # 标题下划线厚度

    for index, obj in enumerate(objs):
        sym = symbol_list.get(index, symbol)
        tit = title_list.get(index, title)
        if not tit:
            symbol_top_px = plain_top_px + 2
            title_bottom_px = 0
        format_dict, md_dict = formater(obj)
        text_plain = format_dict.get('text/plain')
        text_plain = text_plain.replace('Name', '\nName').replace(', dtype', ',\ndtype').replace(', Length', ',\nLength')

        text_html = format_dict.get(
            'text/html',
            '<div><pre style="text-align:left;margin-top:{0}px;">{1}</pre></div>'.format(plain_top_px, text_plain)  # text_plain嵌入html显示
        )

        html.append(text_html.replace('<div>',
            '<div style="display:inline-block;vertical-align:top;text-align:center;">\n'  # 更改div显示方式
            '<pre style="border-bottom:{}px solid">{}</pre>'.format(title_bottom_px, tit))  # 标题底部下划线
        )

        if index + 1 < length:  # web页面展示用，表格连接符，刚好比objs要少一个
            html.append(
                '<pre style="display:inline-block;position:relative;top:{0}px;'
                'margin-left:{1}px;margin-right:{1}px;">{2}</pre>'.format(symbol_top_px, symbol_left_px, sym)
            )

        plain.append(text_plain)
        if index + 1 < length:  # 终端打印时用
            plain.append('-'*10)

    format_dict.update({
        'text/html': '\n'.join(html),
        'text/plain': '\n'.join(plain),
    })
    publish_display_data(data=format_dict)


if __name__ == '__main__':
    pass

