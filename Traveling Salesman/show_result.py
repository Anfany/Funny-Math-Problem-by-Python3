# -*- coding：utf-8 -*-
# &Author  AnFany

#  根据利用遗传算法得到的结果，进行展示


from pyecharts import GeoLines, Style
from pyecharts_snapshot.main import make_a_snapshot


style = Style(
    title_pos="center",
    width=410,
    height=280,
    background_color="#d8e3e7",
    title_text_size=12,
    subtitle_text_size=9,
    title_color='#134567',
    subtitle_color='#134567'
)

style_geo = style.add(
    is_label_show=True,
    label_formatter="{b}",
    is_legend_show=True,
    label_text_size=6,
    label_text_color='#c02c38',
    line_width=1,
    label_pos="inside",
    label_color=['#000000', '#e2e1e4'],
    geo_effect_symbolsize=0,
    line_opacity=0.6,
    geo_normal_color="#e2e1e4",
    symbol_size=0,
    border_color='#7a7374',
)


def create_charts(data_path, path_html, path_png, length):
    charts = GeoLines("TSP问题：以全国34市百度地图驾车距离为例)", '路径：%.3fkm' % (length / 1000), **style.init_style)
    charts.add('', data_path, **style_geo)
    charts.render(path_html)
    make_a_snapshot(path_html, path_png)
    return print('绘图完毕')
