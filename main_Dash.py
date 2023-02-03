from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from optimizer import optimizer
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    " Input ipUSDC Amount ",
    dcc.Input(id='ipUSDC', value='0.01', type='number'),
    " Input ipUSDT Amount ",
    dcc.Input(id='ipUSDT', value='0.01', type='number'),
    " Input ipDAI Amount ",
    dcc.Input(id='ipDAI', value='0.01', type='number'),
    " Input pwrIPOR Amount ",
    dcc.Input(id='pwrIPOR', value='0.01', type='number'),
    " Input USDC to buy/sell ",
    dcc.Input(id='change', value='100.0', type='number'),
    html.Table([
        html.Tr([html.Td('pwrIPOR Change'), html.Td(id='pwrIPOR_chng')]),
        html.Tr([html.Td('pwrIPOR Total'), html.Td(id='pwrIPOR_total')]),
        html.Tr([html.Td('pwrIPOR Cost'), html.Td(id='pwrIPOR_cost')]),
        html.Tr([html.Td('Total Cost'), html.Td(id='total_cost')]),
    ]),
])


@app.callback(
    Output('pwrIPOR_chng', 'children'),
    Output('pwrIPOR_total', 'children'),
    Output('pwrIPOR_cost', 'children'),
    Output('total_cost', 'children'),
    Input('ipUSDC', 'value'),
    Input('ipUSDT', 'value'),
    Input('ipDAI', 'value'),
    Input('pwrIPOR', 'value'),
    Input('change', 'value'))
def update_output_div(input_value, input_value2, input_value3, input_value4, input_value5):
    ## USER Parameters ##
    user_ipusdc = float(input_value)
    user_ipusdt = float(input_value2)
    user_ipdai = float(input_value3)
    user_pwripor = float(input_value4)
    change = float(input_value5)

    pwripor_final, pwrtk_chng, ipor_cost_final, total_cost_final = optimizer(user_ipusdc, user_ipusdt, user_ipdai, user_pwripor, change)

    ## Will have to strip out all of the ip tokens individually
    return pwrtk_chng, pwripor_final, ipor_cost_final, total_cost_final


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
