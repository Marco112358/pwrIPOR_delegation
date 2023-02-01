import functions as fn
import pandas as pd
import numpy as np
from scipy.optimize import minimize

## USER Parameters ##
user_ip_usdc = 2000.0
user_ip_usdt = 3000.0
user_ip_dai = 1500.0
user_pwripor = 1000.0

user_ip_tkns = [user_ip_usdc, user_ip_usdt, user_ip_dai]

## Global Parameters ##
vrt_shft = 1.0
base_boost = 0.4
log_base = 2.0
horz_shft = 0.5
tkn_per_block = 0.5
blocks_per_yr = 365 * 24 * 60 * 60 / 12
lm_stats_url = 'https://api.ipor.io/monitor/liquidity-mining-statistics'
tkns = ['ipUSDC', 'ipUSDT', 'ipDAI']

## NEEDED API INPUTS ##
pools_df = fn.data_import(lm_stats_url)
stkd_amts = []
deleg_amts = []
for i, tkn in enumerate(tkns):
    stkd_amts.append(float(pools_df.loc[tkn, 'stakedIpTokenAmount']))
    deleg_amts.append(float(pools_df.loc[tkn, 'delegatedPwIporAmount']))
ipor_prc = fn.get_price('ipor', 'usd')


def objective(x, sign=-1.0):
    user_pwripor_list = np.multiply(x, user_pwripor)
    new_pwripor_list = deleg_amts + user_pwripor_list
    user_apr = []
    for t in np.arange(0, len(tkns)):
        if user_ip_tkns[t] == 0:
            apr = 0.0
        else:
            apr = fn.staking_pool(stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                                  horz_shft, tkn_per_block, blocks_per_yr, user_ip_tkns[t], user_pwripor_list[t])
        user_apr.append(apr)
    return sign * np.sum([user_apr])


def constraint1(x):
    return 1 - np.sum(x)


x0 = [1 / 3, 1 / 3, 1 / 3]
b1 = (0, 1)
b2 = (0, 1)
b3 = (0, 1)
bnds = (b1, b2, b3)

con1 = {'type': 'ineq', 'fun': constraint1}
cons = [con1]
sol = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=cons)

max_delegation_strat = sol.x

## Running final output ##
user_pwripor_list = np.multiply(max_delegation_strat, user_pwripor)
new_pwripor_list = deleg_amts + user_pwripor_list
user_apr_list = []
for t in np.arange(0, len(tkns)):
    apr = fn.staking_pool(stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                          horz_shft, tkn_per_block, blocks_per_yr, user_ip_tkns[t], user_pwripor_list[t])
    user_apr_list.append(apr)

## Format the Tables for output
user_delegation = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_delegation.iloc[0, :] = max_delegation_strat
user_aprs = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_aprs.iloc[0, :] = user_apr_list
user_tot_aprs = np.sum(user_aprs, axis=1)[0]

print('You should allocate your pwrIPOR tokens using this delegation strategy:')
print(user_delegation)
print('This would give you the following expected aprs in USD')
print(user_aprs)
print('With the total apr in USD across all staking pools of:')
print(user_tot_aprs)
