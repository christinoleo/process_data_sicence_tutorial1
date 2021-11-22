import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="left",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        # dbc.Col(dbc.NavbarBrand("", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            html.Div(style={'padding-left': '50px'}),
            dbc.Button("Primary", color="primary", className="me-1", id='mybutton'),
        ]
    ),
    color="dark",
    dark=True,
)

app.layout = html.Div(children=[
    navbar,
    html.H1(id='mybuttondiv'),
    html.Div(style={'background-color':'purple', 'height': '500px'}),
    html.H1('Ola Rosling opens UN global goal meeting 2020'),
    html.Video(
            controls = True,
            id='movie_player',
            src="https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1920_18MG.mp4",
            autoPlay=False,
            style={'width':'80vw'}
        ),
])


# add callback for toggling the collapse on small screens
@app.callback(
    Output("mybuttondiv", "children"),
    Input("mybutton", "n_clicks"),
)
def toggle_navbar_collapse(n):
    if n is None:
        return "Not clicked."
    print('button pressed')
    return f'Hello {n}'


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
