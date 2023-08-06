import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from hbshare.rm_associated.util.config import style_name


def draw_picture(df, r_square):
    colors = ['#5793f3', '#d14a61']

    factor_order = style_name + ['SPECIFIC']
    df = df.reindex(factor_order)

    x_data = [x.upper() for x in df.index.tolist()]
    factor_exposure = df['exposure'].round(3).tolist()
    factor_return = df['annual_return'].round(2).tolist()

    exposure_limit = int(np.max(np.abs(factor_exposure)) + 1)
    return_limit = int(np.max(np.abs(factor_return)) / 5 + 1) * 5

    bar = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
        .add_xaxis(
            xaxis_data=x_data)
        .add_yaxis(
            series_name='因子暴露',
            y_axis=factor_exposure,
            label_opts=opts.LabelOpts(is_show=False),
            color=colors[0])
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="因子收益",
                type_="value",
                min_=-return_limit,
                max_=return_limit,
                split_number=6,
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                axistick_opts=opts.AxisTickOpts(is_show=True)))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="风格暴露及收益贡献", subtitle="回归R2：{}%".format((r_square * 100).round(2)), pos_left="center"),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts={"interval": "0"},
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")),
            yaxis_opts=opts.AxisOpts(
                name="因子暴露",
                type_="value",
                min_=-exposure_limit,
                max_=exposure_limit,
                split_number=6,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ))
    )

    bar2 = (
        Bar()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="因子收益",
            yaxis_index=1,
            y_axis=factor_return,
            label_opts=opts.LabelOpts(is_show=False))
    )

    return bar.overlap(bar2)


# x_data = df.index.tolist()
# factor_exposure = df['exposure'].round(3).tolist()
# factor_return = df['annual_return'].round(2).tolist()
# exposure_limit = 0.2
# # return_limit = int(np.max(np.abs(factor_return)) / 5 + 1) * 5
# return_limit = 6
# bar = (
#     Bar(init_opts=opts.InitOpts(width='1200px', height='600px', theme=ThemeType.WESTEROS))
#         .add_xaxis(
#         xaxis_data=x_data)
#         .add_yaxis(
#         series_name='因子暴露',
#         y_axis=factor_exposure,
#         label_opts=opts.LabelOpts(is_show=False),
#         color=colors[0])
#         .extend_axis(
#         yaxis=opts.AxisOpts(
#             name="因子收益",
#             type_="value",
#             min_=-return_limit,
#             max_=return_limit,
#             split_number=6,
#             axislabel_opts=opts.LabelOpts(formatter="{value} %"),
#             axistick_opts=opts.AxisTickOpts(is_show=True)))
#         .set_global_opts(
#         title_opts=opts.TitleOpts(
#             title="行业暴露及收益归因", subtitle="行业因子总收益：{}%".format(df['annual_return'].sum().round(2)), pos_left="center"),
#         tooltip_opts=opts.TooltipOpts(
#             is_show=True, trigger="axis", axis_pointer_type="cross"),
#         legend_opts=opts.LegendOpts(pos_left="800", pos_top="top"),
#         xaxis_opts=opts.AxisOpts(
#             type_="category",
#             axislabel_opts={"interval": "0", "rotate": 90},
#             axistick_opts=opts.AxisTickOpts(is_show=True),
#             axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")),
#         yaxis_opts=opts.AxisOpts(
#             name="因子暴露",
#             type_="value",
#             min_=-exposure_limit,
#             max_=exposure_limit,
#             split_number=6,
#             axistick_opts=opts.AxisTickOpts(is_show=True),
#             splitline_opts=opts.SplitLineOpts(is_show=True),
#         ))
# )
# bar2 = (
#     Bar()
#         .add_xaxis(xaxis_data=x_data)
#         .add_yaxis(
#         series_name="因子收益",
#         yaxis_index=1,
#         y_axis=factor_return,
#         label_opts=opts.LabelOpts(is_show=False))
# )
# bar.overlap(bar2)
# bar.render("D:\\kevin\\线下产品归因\\泰暘持仓归因_行业.html")
