from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from optimizer import optimizer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    " Input ipUSDC Amount ",
    dcc.Input(id='ipUSDC', value='0.01', type='number'),
    html.Br(),
    " Input ipUSDT Amount ",
    dcc.Input(id='ipUSDT', value='0.01', type='number'),
    html.Br(),
    " Input ipDAI Amount ",
    dcc.Input(id='ipDAI', value='0.01', type='number'),
    html.Br(),
    " Input pwrIPOR Amount ",
    dcc.Input(id='pwrIPOR', value='0.01', type='number'),
    html.Br(),
    " Input USDC to buy/sell ",
    dcc.Input(id='change', value='100.0', type='number'),
    html.Br(),
    html.Table([
        html.Tr([html.Td('pwrIPOR Change'), html.Td(id='pwrIPOR_chng')]),
        html.Tr([html.Td('ipUSDC Change'), html.Td(id='ipUSDC_chng')]),
        html.Tr([html.Td('ipUSDT Change'), html.Td(id='ipUSDT_chng')]),
        html.Tr([html.Td('ipDAI Change'), html.Td(id='ipDAI_chng')]),
        html.Tr([html.Td('pwrIPOR Total'), html.Td(id='pwrIPOR_total')]),
        html.Tr([html.Td('ipUSDC Total'), html.Td(id='ipUSDC_total')]),
        html.Tr([html.Td('ipUSDT Total'), html.Td(id='ipUSDT_total')]),
        html.Tr([html.Td('ipDAI Total'), html.Td(id='ipDAI_total')]),
        html.Tr([html.Td('ipUSDC Delegation %'), html.Td(id='ipUSDC_deleg')]),
        html.Tr([html.Td('ipUSDT Delegation %'), html.Td(id='ipUSDT_deleg')]),
        html.Tr([html.Td('ipDAI Delegation %'), html.Td(id='ipDAI_deleg')]),
        html.Tr([html.Td('ipUSDC APR From Emmissions in USD'), html.Td(id='ipUSDC_apr')]),
        html.Tr([html.Td('ipUSDT APR From Emmissions in USD'), html.Td(id='ipUSDT_apr')]),
        html.Tr([html.Td('ipDAI APR From Emmissions in USD'), html.Td(id='ipDAI_apr')]),
        html.Tr([html.Td('Total APR From Emmissions in USD'), html.Td(id='total_apr')]),
        html.Tr([html.Td('pwrIPOR Cost'), html.Td(id='pwrIPOR_cost')]),
        html.Tr([html.Td('All ipTokens Cost'), html.Td(id='ipTkns_cost')]),
        html.Tr([html.Td('Total Cost'), html.Td(id='total_cost')]),
    ]),
])


@app.callback(
    Output('pwrIPOR_chng', 'children'),
    Output('ipUSDC_chng', 'children'),
    Output('ipUSDT_chng', 'children'),
    Output('ipDAI_chng', 'children'),
    Output('pwrIPOR_total', 'children'),
    Output('ipUSDC_total', 'children'),
    Output('ipUSDT_total', 'children'),
    Output('ipDAI_total', 'children'),
    Output('ipUSDC_deleg', 'children'),
    Output('ipUSDT_deleg', 'children'),
    Output('ipDAI_deleg', 'children'),
    Output('ipUSDC_apr', 'children'),
    Output('ipUSDT_apr', 'children'),
    Output('ipDAI_apr', 'children'),
    Output('total_apr', 'children'),
    Output('pwrIPOR_cost', 'children'),
    Output('ipTkns_cost', 'children'),
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

    pwripor_final, pwrtk_chng, ipor_cost_final, iptkn_cost_final, total_cost_final, ipUSDC_chng, ipUSDT_chng, \
    ipDAI_chng, ipUSDC_final, ipUSDT_final, ipDAI_final, ipUSDC_deleg, ipUSDT_deleg, ipDAI_deleg, ipUSDC_apr, \
    ipUSDT_apr, ipDAI_apr, apr_final = optimizer(user_ipusdc, user_ipusdt, user_ipdai, user_pwripor, change)

    ## Will have to strip out all of the ip tokens individually
    return pwrtk_chng, ipUSDC_chng, ipUSDT_chng, ipDAI_chng, pwripor_final, ipUSDC_final, ipUSDT_final, ipDAI_final, \
           ipUSDC_deleg, ipUSDT_deleg, ipDAI_deleg, ipUSDC_apr, ipUSDT_apr, ipDAI_apr, apr_final, ipor_cost_final, \
           iptkn_cost_final, total_cost_final


if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
