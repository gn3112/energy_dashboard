import dash
import plotly.graph_objects as go

from app.layouts.content import layout

from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import pytz
from dash import html

from app.api.api_historian import API_Historian
import pandas as pd

from app.config.config import Config
from app.utils.colors import *

h = API_Historian()
config = Config()


def init_callbacks(app):
    from app.utils.load_info import load_info
    _, devices_info = load_info()
    
    devices_info_pd = pd.DataFrame(devices_info)
    processes = devices_info_pd['process'].unique().tolist()

    color_dict = generate_colors(["total"] + processes)

    @app.callback(
        Output('live_time', 'children'),
        [Input('time_interval', 'n_intervals')])
    def update_time(n):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return str(time)
    
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        return layout

    @app.callback(
    Output('kpi1', 'figure'),
    Output('kpi2', 'figure'),
    Output('kpi3', 'figure'),
    Output('kpi4', 'figure'),
    Input('time_interval_content', 'n_intervals'))
    def update_kpis(n):
        
        # Define datetimes
        actual_datetime = datetime.now()

        today_midnight_datetime = datetime(
            year=actual_datetime.year, 
            month=actual_datetime.month, 
            day=actual_datetime.day, 
            hour=0,
            minute=0,
            second=0)

        yesterday_midnight_datetime = today_midnight_datetime - timedelta(hours=24)

        # Get data from source
        data_last_24hrs = h.get_aggregate_over_period(yesterday_midnight_datetime, today_midnight_datetime, "all_measurements")
        data_today = h.get_aggregate_over_period(today_midnight_datetime, actual_datetime, "all_measurements")

        data_realtime_power = h.get_data_multi(today_midnight_datetime, actual_datetime, 1, ["realtime_power"])[0][-1] #Last value

        # Create figures and layouts

        # First KPI: Today consumption
        kp1_fig = go.Figure()

        kp1_fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = data_today['value']*24, # 24hours for period
            title = {"text": "Elec. cons. {}Wh/day<br>".format(config.DISPLAY_UNIT),'font': {'size':15}},
            number = {'font': {'size':35}},
            delta = {'reference': data_last_24hrs['value']*24 , 'relative': True, "valueformat": ".1%"}, # 24hours for period
            # domain = {'x': [0.6, 1], 'y': [0, 1]}
        ))
        kp1_fig.update_layout(
                # margin={"t":6, "r": 5, "l": 5, "b": 1},
                plot_bgcolor="#F7F9F9",
                paper_bgcolor="#F7F9F9",
        )

        # Second KPI: Realtime power
        kp2_fig = go.Figure()
        kp2_fig = go.Figure(go.Indicator(
            mode = "number+gauge",
            value = data_realtime_power,
            title = {'text': "Elec. cons. {}W<br>".format(config.DISPLAY_UNIT),'font': {'size':15}},
            number = {'font': {'size':25}},
            gauge = {'axis': {'range': [None, 1500]}},
            domain = {'x': [0, 1], 'y': [0.05, 0.75]}
        ))
        kp2_fig.update_layout(
            margin={"t":1, "r": 5, "l": 5, "b": 1},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9",
        )

        #Third KPI: Monthly average daily consumption
        kp3_fig = go.Figure()
        kp3_fig = go.Figure(go.Indicator(
            mode = "number",
            value = 5,
            title = {'text': "Elec. cons. {}Wh/month<br>".format(config.DISPLAY_UNIT),'font': {'size':15}},
            number = {'font': {'size':25}},
            gauge = {'axis': {'range': [None, 1500]}},
            domain = {'x': [0, 1], 'y': [0.05, 0.75]}
        ))
        kp3_fig.update_layout(
            margin={"t":1, "r": 5, "l": 5, "b": 1},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9",
        )
        
        # Fourth KPI: Energy per unit of production
        kp4_fig = go.Figure()
        kp4_fig = go.Figure(go.Indicator(
            mode = "number",
            value = 5,
            title = {'text': "Ratio cons. output {}Wh/unit<br>".format(config.DISPLAY_UNIT),'font': {'size':15}},
            number = {'font': {'size':25}},
            gauge = {'axis': {'range': [None, 1500]}},
            domain = {'x': [0, 1], 'y': [0.05, 0.75]}
        ))
        kp4_fig.update_layout(
            margin={"t":1, "r": 5, "l": 5, "b": 1},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9",
        )

        return kp1_fig, kp2_fig, kp3_fig, kp4_fig

    @app.callback(
    dash.dependencies.Output('power_graph', 'figure'),
    dash.dependencies.Input('elec_groups', 'value'),
    dash.dependencies.Input("sensor_type", 'value'),
    dash.dependencies.Input("day_slider", "value"))
    def line_plot_power(groups, measurements, days):

        """ Figure place holder """
        fig = go.Figure()
        fig.update_layout(
            # xaxis_title="Timestamp",
            yaxis_title="{}W".format(config.DISPLAY_UNIT),
            legend_title="Legend",
            margin={"t":30, "r": 20, "l": 5, "b": 4},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9",
        )

        if not groups or not measurements:
            return fig

        """ Data query and processing """
        now = datetime.now(tz=pytz.timezone(config.TIMEZONE))

        sensor_groups = {0:{'sensors': config.APPARENT_POWER_SENSORS, 'name': "Apparent Power"},
            1:{'sensors': config.ACTIVE_POWER_SENSORS, 'name': "Active Power"}}

        result = {}
        tags = []
        for group in groups:
            for measurement in measurements:
                tags += [f"{group}_{sensor}" for sensor in sensor_groups[measurement]["sensors"]]

        data = h.get_data_multi(now - timedelta(hours=days*24), now, 1 if days*24 < 24 else int(round(days)), tags)

        if not data:
            return fig

        if not "timestamp" in list(result.keys()):
            result["timestamp"] = data["timestamps"]

        for group in groups:
            for measurement in measurements:
                data_reformatted = [data[tags.index(f"{group}_{sensor_no}")] for sensor_no in sensor_groups[measurement]["sensors"]]
                result[f"{group}_{measurement}"] = [sum(x) for x in zip(*data_reformatted)]

        columns = list(result.keys())

        df = pd.DataFrame(data=result, columns=columns)
        df.sort_values(by="timestamp")

        columns.remove("timestamp")

        serial_to_name = {device["tag"]: device["name"] for device in devices_info}

        """ Adding trace to existing figure """
        for measurement in columns:
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df[measurement],
                name=f"{serial_to_name[measurement[:-2]]} {sensor_groups[int(measurement[-1])]['name']}"
            ))

        fig.update_yaxes(range=[0, max(df[measurement]) * 1.2])
        
        return fig

    @app.callback(
    dash.dependencies.Output('overall_process', 'figure'),
    dash.dependencies.Output('datetime_feedback', 'children'),
    dash.dependencies.State("start_date", 'value'),
    dash.dependencies.State("end_date", 'value'),
    dash.dependencies.State('elec_groups', 'value'),
    dash.dependencies.Input('button', 'n_clicks'))
    def pie_chart_processes(start_date, end_date, elec_groups, n_clicks):    

        """ Figure place holder """
        fig = go.Figure()
        fig.update_layout(
            margin={"t":14, "r": 15, "l": 5, "b": 5},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9"
        )

        """ Data query and processing """
        sensors = config.ACTIVE_POWER_SENSORS
        datetime_past = datetime.strptime(start_date,"%Y-%m-%dT%H:%M") 
        datetime_now = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")

        """ Catching error in datetime entry"""
        if datetime_past > datetime_now or datetime_now >= datetime.now():
            return fig, html.A("Incorrect datetime range", style={"color": "red"})
        
        result = {}

        for group in processes:
            serials = []
            for device in devices_info:
                if device["process"] == group:
                    serials.append(device["tag"])
            tags = [f"{serial}_{sensor}" for serial in serials for sensor in sensors]
            data = h.get_data_multi(datetime_past, datetime_now, 1, tags, "ROWCOUNT")
            if not data:
                return fig, None

            del data["timestamps"]
        
            i = 0
            hours = (datetime_now - datetime_past).total_seconds() / 3600
            result[group] = sum([j[0] if j[0] else 0 for j in data.values()]) * hours 

        values = list(result.values())
        values_percentage = [round(group_value/sum(values)*100,1) for group_value in values]

        """ Adding trace to existing figure """
        colors = [get_color(process, color_dict) for process in processes]
        fig.add_trace(go.Pie(labels=list(result.keys()), 
                             values=values_percentage, 
                             hole=.3, 
                             marker=dict(colors=colors)
                             ))
        return fig, None
 
    @app.callback(
    dash.dependencies.Output('comparison_plot', 'figure'),
    dash.dependencies.State("start_date", 'value'),
    dash.dependencies.State("end_date", 'value'),
    dash.dependencies.State("input1", "value"),
    dash.dependencies.Input('button', 'n_clicks'))
    def bar_plot_measurements(start_date, end_date, input1, n_clicks):

        """ Figure place holder """
        fig = go.Figure()
        fig.update_layout(
            xaxis_title="{}Wh".format(config.DISPLAY_UNIT),
            showlegend=False,
            margin={"t":25, "r": 15, "l": 5, "b": 5},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9",
        )

        if not input1:
            input1 = 1
        else:
            fig.update_xaxes(
                title="k€",
            )
            input1 = float(input1)*config.KWH_PRICE

        """ Data query and processing """
        start_date = datetime.strptime(start_date,"%Y-%m-%dT%H:%M") 
        end_date = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")

        """ Catching error in datetime entry"""
        if start_date > end_date or end_date >= datetime.now():
            return fig

        sensors = config.ACTIVE_POWER_SENSORS

        tags = [f"{device['tag']}_{sensor}" for device in devices_info for sensor in sensors]
        data = h.get_data_multi(start_date, end_date, 1, tags, "ROWCOUNT")
        if not data:
            return fig

        del data["timestamps"]
        
        i = 0
        hours = (end_date - start_date).total_seconds() / 3600
        
        names = []
        values = []
        labels = []
        for device in devices_info:
            names.append(device['name'])
            if None not in [data[j][0] for j in range(i,i+3)]:          
                values.append(sum([data[j][0] for j in range(i,i+3)]) * hours * input1)
            else:
                values.append(0)

            labels.append(device['process'])
            i += 3
        
        df = pd.DataFrame({'y': values,
                           'x': names,
                           'label': labels})
        df = df.sort_values('label')
        df = df.sort_values('x')

        """ Adding trace to existing figure """
        n = 0
        all_x = []
        all_label = []
        for label, label_df in df.groupby('label'):
            if n != 0: 
                x = [i + 1 for i in list(range(n,n+len(label_df.y)))]
            else:
                x = list(range(n,len(label_df.y)))
            n = x[-1] + 1
            fig.add_trace(go.Bar(
                    y=label_df.x,
                    x=label_df.y,
                    name=label,
                    orientation="h",
                    marker={'color': color_dict[label]},
            ))
        fig.update_layout(
            yaxis = dict(
            {'categoryorder':'total descending'},
            tickfont = dict(size=9)),
            barmode='stack')
            
        return fig

    @app.callback(
    dash.dependencies.Output('sankey_diagram', 'figure'),
    dash.dependencies.State("start_date", 'value'),
    dash.dependencies.State("end_date", 'value'),
    dash.dependencies.Input('button', 'n_clicks'))
    def sankey_diagram(start_date, end_date, n_clicks):

        """ Figure place holder """
        fig = go.Figure()
        fig.update_layout(
            margin={"t":5, "r": 10, "l": 10, "b": 5},
            plot_bgcolor="#F7F9F9",
            paper_bgcolor="#F7F9F9"
        )

        """ Data query and processing """
        start_date = datetime.strptime(start_date,"%Y-%m-%dT%H:%M") 
        end_date = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")

        """ Catching error in datetime entry"""
        if start_date > end_date or end_date >= datetime.now():
            return fig
            
        hours = (end_date - start_date).total_seconds() / 3600

        # Defining dataframe for measurements (used later to insert value column)
        measurements_df = pd.DataFrame(devices_info)
        measurements_df.sort_index(inplace=True)

        measurement_tags = measurements_df['tag'].to_list()

        # Get all measurements values
        sensors = config.ACTIVE_POWER_SENSORS

        tags = [f"{tag}_{sensor}" for tag in measurement_tags for sensor in sensors]
        data = h.get_data_multi(start_date, end_date, 1, tags, "ROWCOUNT")
        
        if not data:
            return fig

        del data["timestamps"]
        
        # Creating values list from data
        i = 0
        measurements_value = []

        for _ in measurement_tags:
            if None not in [data[j][0] for j in range(i,i+3)]:
                measurements_value.append(sum([data[j][0] for j in range(i,i+3)]) * hours)
            else:
                measurements_value.append(0)
            i += 3
        
        # Add values to existing dataframe
        measurements_df['value'] = measurements_value
        
        # Creating labels list
        labels = ["total"] + list(measurements_df['process'].unique()) + list(measurements_df['name'])

        # Creating colors list
        colors = []
        for label in labels:
            if label not in list(color_dict.keys()):
                colors.append(get_color(devices_info_pd[devices_info_pd['name'] == label]['process'].values[0], color_dict))
            else:
                colors.append(get_color(label, color_dict))

        # Creating source / target / value lists
        source = []
        target = []
        value = []
        for process in measurements_df['process'].unique():
            source.append(labels.index('total'))
            target.append(labels.index(process))
            value.append(measurements_df[measurements_df['process'] == process]['value'].sum())
            for measurement in measurements_df[measurements_df['process'] == process]['name'].to_list():
                source.append(labels.index(process))
                target.append(labels.index(measurement))
                value.append(measurements_df[measurements_df['name'] == measurement]['value'].sum())


        """ Adding trace to existing figure """

        fig.add_trace(go.Sankey(
            valueformat = ".0f",
            valuesuffix = '{}Wh'.format(config.DISPLAY_UNIT),
            arrangement='snap',
            node = dict(
                pad = 15,
                thickness = 15,
                line = dict(color = "black", width = 0.5),
                label = labels,
                # x = [0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                # y = [0.5, 0.15, 0.9, 0.8, 0.7, 0.3, 0.1, 0.5],
                color = colors
            ),
            link = dict(
                source = source,
                target = target,
                value = value,
                # color = color
        )))

        return fig