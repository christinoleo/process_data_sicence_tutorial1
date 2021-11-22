import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash import Output, Input

from preprocessing import df, campaign_cols, aggregate_vols

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
dcc.Dropdown(
        id='demo-dropdown',
        options=[
            dict(label=x, value=x) for x in df.columns
        ],
        value='age'
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id='graph',
    )
])


@app.callback(
    Output('graph', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
    from sklearn.metrics import silhouette_score

    model = KMeans(n_clusters=10)
    # model = DBSCAN()
    ndf = pd.get_dummies(df)
    ndf = ndf.drop(campaign_cols, axis=1)
    ndf = ndf.drop(aggregate_vols, axis=1)
    prediction = model.fit_predict(ndf)
    print(silhouette_score(ndf, prediction))

    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca_df = pd.DataFrame(pca.fit_transform(ndf))
    pca_df['cluster'] = prediction
    pca_all_df = pd.concat([pca_df, ndf], axis=1)

    return px.scatter_3d(pca_all_df, x=0, y=1, z=value, color='cluster', )


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)