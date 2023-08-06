from hbshare.quant.load_data import load_funds_data, load_funds_alpha
from hbshare.quant.fund_perf import ret
import pandas as pd
import numpy as np
import pyecharts.options as opts
from datetime import datetime, timedelta
from pyecharts.charts import Line, Tab, Grid, Bar
from pyecharts.globals import ThemeType
import pymysql
from sqlalchemy import create_engine
from hbshare.quant.cons import index_underlying
from hbshare.quant.fut import wind_index_fut_amount, wind_com_fut_sec_index_amount, fin_fut_daily_k_by_contracts
from hbshare.quant.cons import sql_write_path_hb, HSJY_VIRTUAL_CONTRACT

pymysql.install_as_MySQLdb()


def nav_lines(
        fund_list, start_date, end_date, title='', zz=False, axis_cross=None,
        db_path=sql_write_path_hb['daily'], cal_path=sql_write_path_hb['work'], all_selected=True
):
    if axis_cross:
        axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    if zz:
        funds_data = load_funds_alpha(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path
        )['eav']
    else:
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path,
            # freq='',
            # fillna=False
        )

    web = Line(
        init_opts=opts.InitOpts(
            page_title=title,
            width='700px',
            height='500px',
            theme=ThemeType.CHALK
        )
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    ).add_xaxis(
        xaxis_data=funds_data['t_date'].tolist()
    )
    funds = funds_data.columns.tolist()

    funds.remove('t_date')
    for j in funds:
        nav_data = funds_data[j] / funds_data[funds_data[j] > 0][j].tolist()[0]
        web.add_yaxis(
            series_name=j,
            y_axis=nav_data.round(4).tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            is_selected=all_selected
        )

    web.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            is_scale=True,
            type_="category", boundary_gap=False
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        legend_opts=opts.LegendOpts(
            # type_='scroll',
            pos_top='5%'
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        title_opts=opts.TitleOpts(title=title),
        tooltip_opts=axis_cross
    )

    return web


def gen_grid(
        end_date, funds, zz=False, lookback_years=3, grid_width=1200, grid_height=500, pos_top=23, axis_cross=None,
        db_path=sql_write_path_hb['work'], cal_path=sql_write_path_hb['daily'], all_selected=True
):
    if axis_cross:
        axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    engine = create_engine(db_path)
    start_date = end_date - timedelta(days=365 * lookback_years + 7)
    start_date2 = end_date - timedelta(days=365 + 7)
    if len(funds) > 1:
        fund_list = pd.read_sql_query(
            'select * from fund_list where `name` in ' + str(tuple(funds)) + ' order by `name`', engine
        )
    else:
        fund_list = pd.read_sql_query(
            'select * from fund_list where `name`="' + str(funds[0]) + '"', engine
        )

    grid_nav = Grid(init_opts=opts.InitOpts(width=str(grid_width) + "px", height=str(grid_height) + "px"))

    web = nav_lines(
        fund_list=fund_list,
        start_date=start_date,
        end_date=end_date,
        zz=zz,
        db_path=db_path,
        cal_path=cal_path,
        all_selected=all_selected
    )

    web2 = nav_lines(
        fund_list=fund_list,
        start_date=start_date2,
        end_date=end_date,
        zz=zz,
        db_path=db_path,
        cal_path=cal_path,
        all_selected=all_selected
    )

    grid_nav.add(
        web.set_global_opts(
            title_opts=opts.TitleOpts(
                title='近' + str(lookback_years) + '年: '
                      + start_date.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_right="5%"
            ),
            tooltip_opts=axis_cross,
            legend_opts=opts.LegendOpts(
                pos_top="7%"
            )
        ),
        grid_opts=opts.GridOpts(pos_left='55%', pos_top=str(pos_top) + "%")
    ).add(
        web2.set_global_opts(
            title_opts=opts.TitleOpts(
                title='近一年: '
                      + start_date2.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_left="5%"
            ),
            tooltip_opts=axis_cross,
            legend_opts=opts.LegendOpts(
                pos_top="7%"
            )
        ),
        grid_opts=opts.GridOpts(pos_right='55%', pos_top=str(pos_top) + "%")
    )
    return grid_nav


def chart_index_fut_basis_wind(
        index_code, start_date, end_date,
        sql_path=sql_write_path_hb['daily'], table='futures_wind',
        grid_width=1200, grid_height=400, zoom_left=90, zoom_right=100,
        chart_pos_left=10, chart_pos_right=20
):
    engine = create_engine(sql_path)

    data_raw = pd.read_sql_query(
        'select * from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` in (\'IC\') order by `t_date`',
        engine
    )

    data_00 = data_raw[data_raw['symbol'] == index_code + '00.CFE'].reset_index(drop=True)
    data_01 = data_raw[data_raw['symbol'] == index_code + '01.CFE'].reset_index(drop=True)
    data_02 = data_raw[data_raw['symbol'] == index_code + '02.CFE'].reset_index(drop=True)
    data_03 = data_raw[data_raw['symbol'] == index_code + '03.CFE'].reset_index(drop=True)

    data_00['remain'] = (data_00['delist_date'] - data_00['t_date']).map(lambda x: x.days)
    data_00['basis'] = round(data_00['basis'] / data_00['underlying'] / data_00['remain'] * 365 * 100, 2)

    data_01['remain'] = (data_01['delist_date'] - data_01['t_date']).map(lambda x: x.days)
    data_01['basis'] = round(data_01['basis'] / data_01['underlying'] / data_01['remain'] * 365 * 100, 2)

    data_02['remain'] = (data_02['delist_date'] - data_02['t_date']).map(lambda x: x.days)
    data_02['basis'] = round(data_02['basis'] / data_02['underlying'] / data_02['remain'] * 365 * 100, 2)

    data_03['remain'] = (data_03['delist_date'] - data_03['t_date']).map(lambda x: x.days)
    data_03['basis'] = round(data_03['basis'] / data_03['underlying'] / data_03['remain'] * 365 * 100, 2)

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=data_00['t_date'].tolist()
    ).add_yaxis(
        series_name=index_underlying[index_code],
        y_axis=data_00['underlying'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name=index_code + '当月',
        y_axis=data_00['close'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name=index_code + '次月',
        y_axis=data_01['close'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name=index_code + '季月',
        y_axis=data_02['close'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name=index_code + '次季',
        y_axis=data_03['close'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='基差',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_='dataMin',
        )
        # ).extend_axis(
        #     yaxis=opts.AxisOpts(
        #         name='成交额',
        #         axislabel_opts=opts.LabelOpts(formatter="{value} 亿元"),
        #         position="right",
        #         offset=80
        #         # interval=5
        #         )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=data_raw['t_date'][len(data_raw) - 1]
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=zoom_left, range_end=zoom_right),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ]
    )

    web2 = Line().add_xaxis(
        xaxis_data=data_00['t_date'].tolist()
    ).add_yaxis(
        series_name='当月基差',
        y_axis=data_00['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        is_selected=False,
    ).add_yaxis(
        series_name='次月基差',
        y_axis=data_01['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1
    ).add_yaxis(
        series_name='季月基差',
        y_axis=data_02['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1
    ).add_yaxis(
        series_name='次季基差',
        y_axis=data_03['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1
    )

    web.overlap(web2)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right=str(chart_pos_right) + "%",
                pos_left=str(chart_pos_left) + "%",
            ),
            is_control_axis_index=True
        )
    )
    return grid


def chart_index_fut_basis(
        index_code, start_date, end_date,
        grid_width=1200, grid_height=400, zoom_left=90, zoom_right=100,
        chart_pos_left=10, chart_pos_right=20
):
    fut_data = fin_fut_daily_k_by_contracts(
        contract_list=HSJY_VIRTUAL_CONTRACT['FINANCE'][index_code].values(),
        start_date=start_date,
        end_date=end_date
    )


def chart_fut_amount_wind(
        start_date=datetime(2010, 1, 1).date(), end_date=datetime.now().date(),
        db_path=sql_write_path_hb['daily'], grid_width=1200, grid_height=600, freq='W'
):
    com_data = wind_com_fut_sec_index_amount(start_date=start_date, end_date=end_date, db_path=db_path, freq=freq)
    index_data = wind_index_fut_amount(start_date=start_date, end_date=end_date, db_path=db_path, freq=freq)

    data = com_data.merge(index_data, on='t_date')

    columns = data.columns.tolist()
    columns.pop(columns.index('t_date'))

    data = data.set_index(data['t_date'])[columns]
    data = data.dropna(axis=0, how='all')

    web = Line(
    ).add_xaxis(
        xaxis_data=data.index.tolist()
    )

    codes = data.columns.tolist()
    data['all'] = data[codes].apply(lambda x: x.sum(), axis=1)
    for i in codes:
        web.add_yaxis(
            series_name=i,
            y_axis=data[i].tolist(),
            stack='总量',
            label_opts=opts.LabelOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(title="每周期货成交额(日均) " + data.index.tolist()[-1].strftime('%Y-%m-%d')),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axislabel_opts=opts.LabelOpts(formatter="{value} 亿元"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=0,
                range_end=100,
                # is_show=False,
                type_="inside",
                # xaxis_index=[0, 1],
            ),
            opts.DataZoomOpts(
            #     is_show=True,
            #     xaxis_index=[0, 1],
            #     type_="slider",
            #     pos_top="90%",
            #     range_start=98,
            #     range_end=100,
            ),
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )
    # web2.set_global_opts(
    #     legend_opts=opts.LegendOpts(
    #         pos_top="7%",
    #         pos_left='10%',
    #         pos_right='20%'
    #     )
    # )
    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(grid_width) + "px",
                height=str(grid_height) + "px"
            ),
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right="20%",
                pos_left="10%",
                pos_top='20%',
                # pos_bottom='50%'
            ),
            # is_control_axis_index=True
        # ).add(
        #     web2, grid_opts=opts.GridOpts(
        #         pos_right="20%",
        #         pos_left="10%",
        #         pos_top='55%',
        #         pos_bottom='15%'
        #     ),
        )
    )

    return grid


def chart_fin_fut_amt(product, start_date=None, end_date=None, grid_width=1200, grid_height=600):
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()

    fut_data = fin_fut_daily_k_by_contracts(
        contract_list=HSJY_VIRTUAL_CONTRACT['FINANCE'][product].values(),
        start_date=start_date,
        end_date=end_date
    )
    transaction_data = pd.DataFrame(fut_data['data'])
    transaction_data['TRADINGDAY'] = pd.to_datetime(transaction_data['TRADINGDAY']).dt.date.tolist()
    transaction_data = transaction_data.groupby(by='TRADINGDAY').sum()[
        ['TurnoverVolume'.upper(), 'TurnoverValue'.upper(), 'OpenInterest'.upper()]
    ].reset_index()

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='成交量',
        y_axis=list(transaction_data['TurnoverVolume'.upper()].values / 10000),
        linestyle_opts=opts.LineStyleOpts(
            # color="red",
            width=1,
            # type_="dashed"
        ),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='持仓量',
            axislabel_opts=opts.LabelOpts(formatter="{value} 万手"),
            position="right",
            # interval=5
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='成交额',
            axislabel_opts=opts.LabelOpts(formatter="{value} 亿元"),
            position="right",
            offset=80
            # interval=5
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=product + ' ' + transaction_data['TRADINGDAY'][len(transaction_data) - 1].strftime('%Y-%m-%d')
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 万手")),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ]
    )

    web2 = Line().add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='持仓量',
        y_axis=list(transaction_data['OpenInterest'.upper()].values / 10000),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1
    )

    web3 = Line().add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='成交额',
        y_axis=list(transaction_data['TurnoverValue'.upper()].values / 100000000),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2
    )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(pos_right="20%", pos_left="10%"),
            is_control_axis_index=True
        )
    )

    return grid


def chart_freq_dist(
        funds, end_date, lookback_year, grid_width=1200, grid_height=600, pos_top=20, interval=0.5,
        dtype='', fillna=False, freq='w',
        db_path=sql_write_path_hb['work'], cal_path=sql_write_path_hb['daily']
):
    date_end = end_date
    date_start = date_end - timedelta(days=365 * lookback_year)
    table = 'fund_list'

    fund_list = pd.read_sql_query(
        'select * from ' + table + ' where `name` in ' + str(tuple(funds)), create_engine(db_path)
    )

    if dtype.lower() != 'alpha':
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=date_start,
            end_date=date_end,
            fillna=fillna,
            db_path=db_path,
            cal_db_path=cal_path,
            freq=freq
        )
    else:
        funds_data = load_funds_alpha(
            fund_list=fund_list,
            first_date=date_start,
            end_date=date_end,
            fillna=fillna,
            db_path=db_path,
            cal_db_path=cal_path,
            freq=freq
        )

    ret_df = ret(data_df=funds_data)
    ret_data = ret_df[funds]
    ret_values = np.reshape(ret_data.values, (1, ret_data.values.shape[0] * ret_data.values.shape[1]))
    ret_values = ret_values[~np.isnan(ret_values)] * 100
    ret_floor = np.floor(min(ret_values)) - 1
    ret_ceil = np.ceil(max(ret_values))
    ret_space = np.linspace(start=ret_floor, stop=ret_ceil, num=int((ret_ceil - ret_floor) / interval + 1))
    dist_df = pd.DataFrame({'zone': ret_space})
    dist_df['label'] = dist_df['zone'].apply(lambda x: str(x) + '% ~ ' + str(x + interval) + '%')
    for i in funds:
        dist_df[i] = 0
        for j in range(1, len(ret_df)):
            fund_ret = ret_df[i][j] * 100
            if np.isnan(fund_ret):
                continue
            fund_ret_index = sum(ret_space <= fund_ret) - 1

            dist_df.loc[fund_ret_index, i] += 1

    web = Bar(
    ).add_xaxis(
        xaxis_data=dist_df['label'].tolist()
    )
    for i in funds:
        web.add_yaxis(
            series_name=i,
            y_axis=dist_df[i].tolist(),
            stack='总量',
            label_opts=opts.LabelOpts(is_show=False),
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(
            title='近' + str(lookback_year) + '年产品周收益分布（平均周收益：' + str(np.mean(ret_values).round(2))
                  + '%）' + funds_data['t_date'].tolist()[-1].strftime('%Y-%m-%d')
        ),
        tooltip_opts=opts.TooltipOpts(
            # trigger="axis", axis_pointer_type="cross"
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        # datazoom_opts=[
        #     opts.DataZoomOpts(
        #         range_start=0,
        #         range_end=100,
        #         # is_show=False,
        #         type_="inside",
        #         # xaxis_index=[0, 1],
        #     ),
        #     opts.DataZoomOpts(
        #         #     is_show=True,
        #         #     xaxis_index=[0, 1],
        #         #     type_="slider",
        #         #     pos_top="90%",
        #         #     range_start=98,
        #         #     range_end=100,
        #     ),
        # ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='5%',
            pos_right='5%'
        )
    )
    # web2.set_global_opts(
    #     legend_opts=opts.LegendOpts(
    #         pos_top="7%",
    #         pos_left='10%',
    #         pos_right='20%'
    #     )
    # )
    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(grid_width) + "px",
                height=str(grid_height) + "px"
            ),
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right="10%",
                pos_left="10%",
                pos_top=str(pos_top) + '%',
                # pos_bottom='50%'
            ),
            # is_control_axis_index=True
            # ).add(
            #     web2, grid_opts=opts.GridOpts(
            #         pos_right="20%",
            #         pos_left="10%",
            #         pos_top='55%',
            #         pos_bottom='15%'
            #     ),
        )
    )
    return grid


# def chart_ret_with_index(
#         funds, end_date, lookback_year, grid_width=1200, grid_height=600, interval=0.5,
#         dtype='', fillna=False, freq='w',
#         db_path=sql_write_path_hb['work'], cal_path=sql_write_path_hb['daily'], *kwargs
# )
