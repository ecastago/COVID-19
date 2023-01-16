import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from client import Client

departamentos_colombia = ['AMAZONAS','ANTIOQUIA','ARAUCA','ATLANTICO','BOLIVAR','BOYACA','BOGOTA','CALDAS','CAQUETA', 
                          'CASANARE','CAUCA','CESAR','CHOCO','CORDOBA','CUNDINAMARCA','GUAINIA','GUAVIARE', 
                          'HUILA','GUAJIRA','MAGDALENA','NARIÑO','NORTE SANTANDER','PUTUMAYO','QUINDIO', 
                          'RISARALDA','SAN ANDRÉS','PROVIDENCIA','SANTANDER','STA MARTA D.E.','SUCRE','TOLIMA','VALLE','VAUPES','VICHADA'
                          ]

app = dash.Dash(__name__, title='Covid-19 Analisis and Visualization by Esteban Castaño G.')
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Bienvenido al Sistema de Consultas Covid-19 en Colombia",
                    style={
                        "textAlign":"center",
                    }
                ),
                html.Em(
                    children="Esteban Castaño Gómez",

                )
            ]
        ),
        html.Div(
            children=[
                html.H3("Numero de Casos:"),
                dcc.Input(
                    id='numero_consultas',
                    placeholder="Numero de consultas",
                    type="number",
                    min=0,
                    max=200000,
                    value=10,
                    style={
                        "textAlign":"center"
                    }
                ),
                html.H3("Seleccione Departamento Deseado:"),
                dcc.Dropdown(
                    id="departamento",
                    options=[{"label":i, "value":i} for i in departamentos_colombia]
                ),
                html.Button(
                    id='submit', 
                    n_clicks=0, 
                    children='Submit'
                )
            ],
            style={
                    'border': '1px solid black',
                    'padding': '10px',
                    'textAlign': 'center',
                    'display': 'grid',
                    'justifyContent': 'space-around',
                    'justifyItems': 'stretch',
                    'width': '50%',
                    'position': 'relative',
                    'left': '25%',
                    'right': '25%',
            }
        ),
        html.Div(
            children=[
                dash_table.DataTable(
                    id='table',
                    page_size=15,
                    filter_action="native",
                    sort_mode="multi",
                    sort_action="native"
                )
            ],
            style={
                "textAlign":"center",
                'position': 'relative',
                'left': '5%',
                'right': '10%',
                'width': '80%',
                'margin': '40px'
            }
        )
    ]
)

@app.callback(
    [Output('table', 'data'),
    Output('table', 'columns')],
    Input('submit', 'n_clicks'),
    State('numero_consultas', 'value'),
    State('departamento', 'value')
)
def update_output(n_clicks, numero_consultas, departamento):
            
    client = Client(numero_consultas,departamento)
    
    columns = [{"name": i, "id": i} for i in ["ciudad_municipio_nom","departamento_nom","edad","tipo_recuperacion","estado","pais_viajo_1_nom"]]
    data = client.df.to_dict('records')

    return data, columns

if __name__ == '__main__':
    app.run_server(port=4050, debug=True)