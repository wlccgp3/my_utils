#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from io import BytesIO
from reportlab.lib import colors
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Path
from fontTools.pens.reportLabPen import ReportLabPen
from reportlab.graphics.shapes import Group, Drawing

__all__ = ['MagicFont']


class MagicFont(object):
    """字体文件处理

    import matplotlib.pyplot as plt

    font_path = '/Users/miles/Documents/data/font/HanYiWangChuanTiao-2.ttf'
    data_mapping = MagicFont(font_path, limit=range(0x4e00, 0x9fa6)).to_pil_iter()
    for ucode, data in data_mapping:
        print(ucode, chr(ucode))
        plt.imshow(data)
        plt.show()
    """
    def __init__(self, font_path, limit=None, fill=100):
        if isinstance(font_path, bytes):
            font_path = BytesIO(font_path)

        self.font_data = TTFont(font_path)
        self.limit = limit
        self.fill = fill

    def to_pil_iter(self, resize=None):
        gs = self.font_data.getGlyphSet()
        cmap = self.font_data.getBestCmap()
        ucodes = cmap.keys()
        if self.limit:
            ucodes = self.limit

        for ucode in ucodes:
            g = gs[cmap.get(ucode)]
            if not hasattr(g._glyph, 'coordinates'):
                continue

            w = g._glyph.xMax - g._glyph.xMin + self.fill
            h = g._glyph.yMax - g._glyph.yMin + self.fill
            l, t = g._glyph.xMin - self.fill/2, g._glyph.yMin - self.fill/2
            pen = ReportLabPen(gs, Path(fillColor=colors.black))
            g.draw(pen)
            g = Group(pen.path)
            g.translate(-l, -t)
            d = Drawing(w, h)
            d.add(g)

            data = renderPM.drawToPIL(d)
            if resize:
                data = data.resize(resize)

            yield ucode, data

    def to_pil(self, resize=None):
        font_mapping = {}
        for ucode, data in self.to_pil_iter(resize):
            font_mapping.update({ucode: data})
        return font_mapping

    def to_img_iter(self, resize=None, fmt='png'):
        for ucode, data in self.to_pil_iter(resize):
            b = BytesIO()
            data.save(b, format=fmt)
            yield ucode, b.getvalue()

    def to_img(self, resize=None, fmt='png'):
        font_mapping = {}
        for ucode, data in self.to_img_iter(resize, fmt):
            font_mapping.update({ucode: data})
        return font_mapping

    def to_file(self, dir_path, resize=None, fmt='png'):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        if os.path.isdir(dir_path):
            for ucode, data in self.to_pil_iter(resize):
                file_path = os.path.join(dir_path, '{}.png'.format(ucode))
                data.save(file_path, format=fmt)
