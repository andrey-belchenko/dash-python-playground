import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};Server=192.168.0.115;Database=Ilim.DataMart;UID=conteq;Password=conteq;Trusted_Connection=yes')


df1 = pd.read_sql("SELECT top 10 * FROM [data].[DimProject]",conn)
df2 = pd.read_sql("""  with a as (
  select format(a.[Date],'yyyy') [Date], a.CompletedWorkActualCost [Value] from [data].FactEVA a 
  )
  select [Date],Sum([Value]) as [Value] from a group by [Date] having sum([Value])>0 order by [Date]""",conn)


app = dash.Dash(__name__)
# fig = go.Figure(data=[go.Scatter(x= df2["Date"],y= df2["Value"])])
fig={
            "data": [
                {
                    "x": df2["Date"],
                    "y": df2["Value"],
                    "type": "linear"
                    # ,"marker": {"color": colors},
                }
            ]
          
            ,
            "layout": {
                "xaxis": {"automargin": True,  "tickvals":df2["Date"]},
                "yaxis": {
                    "automargin": True,
                    "title": {"text": "YYYYY"}
                },
                "height": 250,
                "margin": {"t": 10, "l": 10, "r": 10},
            },
        }
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"id":"ProjectName","name":"ProjectName"}
        ],
        data=df1.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_filter ={'textAlign': 'left'},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10
    ),
    dcc.Graph(
        id="graph",
        # figure={
        #     "data": [
        #         {
        #             "x": df2["Date"],
        #             "y": df2["Value"],
        #             "type": "linear"
        #             # ,"marker": {"color": colors},
        #         }
        #     ]
          
        #     ,
        #     "layout": {
        #         "xaxis": {"automargin": True,  "tickvals":df2["Date"]},
        #         "yaxis": {
        #             "automargin": True,
        #             "title": {"text": "YYYYY"}
        #         },
        #         "height": 250,
        #         "margin": {"t": 10, "l": 10, "r": 10},
        #     },
        # }
        figure=fig
    )
    # ,
    # html.Div(id='datatable-interactivity-container')
])

# @app.callback(
#     Output('datatable-interactivity', 'style_data_conditional'),
#     Input('datatable-interactivity', 'selected_columns')
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]

# @app.callback(
#     Output('datatable-interactivity-container', "children"),
#     Input('datatable-interactivity', "derived_virtual_data"),
#     Input('datatable-interactivity', "derived_virtual_selected_rows"))
# def update_graphs(rows, derived_virtual_selected_rows):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     if derived_virtual_selected_rows is None:
#         derived_virtual_selected_rows = []

#     dff = df if rows is None else pd.DataFrame(rows)

#     colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
#               for i in range(len(dff))]

#     return [
#         dcc.Graph(
#             id=column,
#             figure={
#                 "data": [
#                     {
#                         "x": dff["country"],
#                         "y": dff[column],
#                         "type": "bar",
#                         "marker": {"color": colors},
#                     }
#                 ],
#                 "layout": {
#                     "xaxis": {"automargin": True},
#                     "yaxis": {
#                         "automargin": True,
#                         "title": {"text": column}
#                     },
#                     "height": 250,
#                     "margin": {"t": 10, "l": 10, "r": 10},
#                 },
#             },
#         )
#         # check if column exists - user may have deleted it
#         # If `column.deletable=False`, then you don't
#         # need to do this check.
#         for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
#     ]


if __name__ == '__main__':
    app.run_server(debug=True)
