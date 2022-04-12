import dash
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from Rover import Rover

# Graph rover
sim_rover = Rover(0, 0, 0)
# Output rover
output_rover = Rover(0, 0, 0)
# List of instructions
instruction_list = []
# Checkpoints list
checkpoints = []
bearing_markers = ["triangle-up", "triangle-right", "triangle-down", "triangle-left"]

X = deque(maxlen=1)
X.append(sim_rover.get_x())

Y = deque(maxlen=1)
Y.append(sim_rover.get_y())

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# App layout
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('MARS ROVER SIMULATION'),
                                 html.P('Visualising rover movement on MARS plateau'),
                                 html.P('Insert instructions below : '),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[dcc.Textarea(id='text_instructions',
                                                            value='',
                                                            style={'width': '100%', 'height': 200},)],
                                     style={'color': '#FFFFFF'}),
                                 html.Button('Print output', id='update_position', n_clicks=0),
                                 html.Button('Simulate', id='simulate', n_clicks=0, style={'margin-left': '5vh'},),
                                 html.Button('Reset', id='reset_position', n_clicks=0, style={'margin-left': '5vh'},),
                                 html.P('Output : ', style={'margin-top': '10vh'},),
                                 html.P('', id='output_positions'),
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='live-graph', animate=False, style={'width': '124vh', 'height': '100vh'}),
                                 dcc.Interval(
                                            id='graph-update',
                                            interval=250,
                                            n_intervals=0
                                        ),
                             ])
                              ])
        ]

)


# Callback for rover position update
@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')],
    State('text_instructions', 'value')
)
def update_graph_scatter(n, value):
    if len(instruction_list) > 0:
        # Execute next move
        line = instruction_list[0]
        sim_rover.single_move(line[0])
        instruction_list[0] = line[1:]
        if len(instruction_list[0]) == 0:
            instruction_list.pop(0)
            # Add checkpoint
            checkpoints.append(plotly.graph_objs.Scatter(
                x=[sim_rover.get_x()],
                y=[sim_rover.get_y()],
                name='Checkpoint : ' + str(len(checkpoints)+1),
                mode='markers',
                marker_symbol=bearing_markers[sim_rover.get_direction()],
                marker=dict(size=20))
            )
    # Update graph data
    X.append(sim_rover.get_x())
    Y.append(sim_rover.get_y())

    # Add potential checkpoints
    current_rover = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Rover',
        mode='markers',
        marker_symbol=bearing_markers[sim_rover.get_direction()],
        marker=dict(size=20)
    )
    data = [current_rover]
    for checkpoint in checkpoints:
        data.append(checkpoint)

    return {'data': data,
            'layout': go.Layout(xaxis=dict(range=[-2, 50], dtick=2), yaxis=dict(range=[-1, 25], dtick=1), )}


# Callback for output calculation
@app.callback(
    Output('output_positions', 'children'),
    Input('update_position', 'n_clicks'),
    State('text_instructions', 'value')
)
def update_output_position(n_clicks, value):
    # Update instruction list for graph plotting
    positions = output_rover.execute(value)
    result = []
    for p in positions:
        result.append(p)
        result.append(html.Br())
    result.pop()
    return result


# Callback for to reset rover
@app.callback(
    Output('text_instructions', 'value'),
    Input('reset_position', 'n_clicks')
)
def reset_position(n_clicks):
    global instruction_list, checkpoints
    instruction_list = []
    checkpoints = []
    output_rover.set_x(0)
    output_rover.set_y(0)
    output_rover.set_direction(0)
    sim_rover.set_x(0)
    sim_rover.set_y(0)
    sim_rover.set_direction(0)
    return ""


# Callback for output calculation
@app.callback(
    Output('simulate', 'n_clicks'),
    Input('simulate', 'n_clicks'),
    State('text_instructions', 'value')
)
def update_instructions(n_clicks, value):
    global instruction_list
    instruction_list = value.splitlines()
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)