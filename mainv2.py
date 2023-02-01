import functions as fn
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import time

start_time = time.time()

## NEED TO API THESE EXCHANGE RATES ##
ipusdc_prc = 1.0383
ipusdt_prc = 1.0431
ipdai_prc = 1.0406
## USER Parameters ##
user_ipusdc = 2000.0
user_ipusdt = 0.0
user_ipdai = 0.0
user_pwripor = 1000.0
change = 100

ip_prcs = [ipusdc_prc, ipusdt_prc, ipdai_prc]  # Will need to update if add new tokens
user_ip_tkns = [user_ipusdc, user_ipusdt, user_ipdai]  # Will need to update if add new tokens
no_tkns = len(user_ip_tkns)

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


## FIGURE OUT A WAY TO ADD TO X, X[0-2] = pcts, X[3-5] = new iptkns, X[6] = new pwripor
## HAVE TO ADD BOUNDARIES
## HAVE TO ADD CONSTRAINTS
## HAVE TO UPDATE LISTS
def objective(x, sign=-1.0):
    pwr_pct = x[:no_tkns]
    ip_tkns = x[no_tkns:-1]
    pw_tkn = x[-1]
    user_pwripor_list = np.multiply(pwr_pct, pw_tkn)
    new_pwripor_list = deleg_amts + user_pwripor_list
    user_apr = []
    for t in np.arange(0, no_tkns):
        if user_ip_tkns[t] == 0:
            apr = 0.0
        else:
            apr = fn.staking_pool(stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                                  horz_shft, tkn_per_block, blocks_per_yr, ip_tkns[t], user_pwripor_list[t])
        user_apr.append(apr)
    return sign * np.sum([user_apr])


def constraint1(x):
    pwr_pct = x[:no_tkns]
    return 1 - np.sum(pwr_pct)


def constraint2(x):
    ip_tkns = x[no_tkns:-1]
    pw_tkn = x[-1]
    ip_val_chng = np.sum(np.multiply(np.subtract(ip_tkns, user_ip_tkns), ip_prcs))
    pw_val_chng = np.multiply(np.subtract(pw_tkn, user_pwripor), ipor_prc)
    return change - ip_val_chng - pw_val_chng


pwr_pct0 = [1 / 3, 1 / 3, 1 / 3]
ip_tkns0 = user_ip_tkns
pw_tkn0 = [user_pwripor]
x0 = pwr_pct0 + ip_tkns0 + pw_tkn0
b1 = (0, 1)
b2 = (0, 1)
b3 = (0, 1)
bnds = [b1, b2, b3]
for t in np.arange(0, no_tkns):
    b = (min(user_ip_tkns[t], user_ip_tkns[t] + (change / ip_prcs[t])),
         max(user_ip_tkns[t], user_ip_tkns[t] + (change / ip_prcs[t])))
    bnds.append(b)
    # bnds = bnds + b

b = (min(user_pwripor, user_pwripor + (change / ipor_prc)), max(user_pwripor, user_pwripor + (change / ipor_prc)))
bnds.append(b)
# bnds = bnds + b


con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
cons = [con1, con2]
sol = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=cons)

## Running final output ##
new_pwr_pct = sol.x[:no_tkns]
new_ip_tkns = sol.x[no_tkns:-1]
new_pw_tkn = sol.x[-1]
user_pwripor_list = np.multiply(new_pwr_pct, new_pw_tkn)
new_pwripor_list = deleg_amts + user_pwripor_list
user_apr_list = []
for t in np.arange(0, no_tkns):
    if user_ip_tkns[t] == 0:
        apr = 0.0
    else:
        apr = fn.staking_pool(stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                              horz_shft, tkn_per_block, blocks_per_yr, new_ip_tkns[t], user_pwripor_list[t])
    user_apr_list.append(apr)

## Format the Tables for output and print
user_delegation = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_delegation.iloc[0, :] = new_pwr_pct
user_aprs = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_aprs.iloc[0, :] = user_apr_list
user_tot_aprs = np.sum(user_aprs, axis=1)[0]
user_iptkns_df = pd.DataFrame(index=['ipTkn Amounts'], columns=['USDC', 'USDT', 'DAI'])
user_iptkns_df.iloc[0, :] = new_ip_tkns
user_iptkns_chng = pd.DataFrame(index=['ipTkn Amounts'], columns=['USDC', 'USDT', 'DAI'])
user_iptkns_chng.iloc[0, :] = np.subtract(new_ip_tkns, user_ip_tkns)
cost = np.sum(np.multiply(np.subtract(new_ip_tkns, user_ip_tkns), ip_prcs)) \
       + np.multiply(np.subtract(new_pw_tkn, user_pwripor), ipor_prc)
print('You should buy/sell ' + str((new_pw_tkn - user_pwripor)) + ' more pwrIPOR')
print('For a total of ' + str(new_pw_tkn) + ' pwrIPOR')
print('You should buy/sell the following amounts of ipTokens')
print(user_iptkns_chng)
print('For a total amout of ipTkns')
print(user_iptkns_df)
print('You should allocate your pwrIPOR tokens using this delegation strategy:')
print(user_delegation)
print('This would give you the following expected aprs in USD')
print(user_aprs)
print('With the total apr in USD across all staking pools of:')
print(user_tot_aprs)
print('This would cost a total of ' + str(cost))
print('This optimization took ' + str(time.time() - start_time) + ' seconds to run')

