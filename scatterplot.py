import plotly.express as px
from dash import Output, Input, dcc, html
from sklearn.decomposition import PCA
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('./bank-additional-full.csv')
df.drop(df.select_dtypes('object').columns, axis=1, inplace=True)

pca = PCA(n_components=2)
res = pca.fit_transform(df)

df['x'] = res[:,0]
df['y'] = res[:,1]

graph = html.Div([
    dcc.Graph(id='graph', figure=px.scatter(df, x='x', y='y', hover_data=['age'])),
    dcc.Graph(id='graph2'),
])


# add callback for toggling the collapse on small screens
def create_callback(app):
    @app.callback(
        Output("graph2", "figure"),
        [Input("graph", "selectedData")],
    )
    def toggle_navbar_collapse(selected_data):
        if selected_data is not None:
            new_list = []
            for x in selected_data['points']:
                new_list.append(x['customdata'][0])
            return go.Figure(go.Box(x=new_list))
        return go.Figure(go.Box(x=[0,1,2]))
