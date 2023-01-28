import functions as fn
import pandas as pd
import numpy as np
from scipy.optimize import minimize

## USER Parameters ##
user_ip_usdc = 2000.0
user_ip_usdt = 3000.0
user_ip_dai = 1500.0
user_pwripor = 1000.0

## Global Parameters ##
vrt_shft = 1.0
base_boost = 0.4
log_base = 2.0
horz_shft = 0.5
tkn_per_block = 0.5
blocks_per_yr = 365 * 24 * 60 * 60 / 12

## NEEDED API INPUTS ##
ip_usdc_stk = 2542989.0
pwripor_stk_usdc = 57358.0
ip_usdt_stk = 2374886.0
pwripor_stk_usdt = 49054.0
ip_dai_stk = 2139505.0
pwripor_stk_dai = 43283.0
ipor_prc = fn.get_price('ipor', 'usd')


def objective(x, sign=-1.0):
    user_usdc_apr = fn.staking_pool(ip_usdc_stk, pwripor_stk_usdc, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                                    tkn_per_block, blocks_per_yr, user_ip_usdc, user_pwripor * x[0])
    user_usdt_apr = fn.staking_pool(ip_usdt_stk, pwripor_stk_usdt, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                                    tkn_per_block, blocks_per_yr, user_ip_usdt, user_pwripor * x[1])
    user_dai_apr = fn.staking_pool(ip_dai_stk, pwripor_stk_dai, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                                   tkn_per_block, blocks_per_yr, user_ip_dai, user_pwripor * x[2])
    return sign * np.sum([user_usdc_apr, user_usdt_apr, user_dai_apr])


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
user_delegation = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_delegation.iloc[0, :] = max_delegation_strat
user_usdc_apr = fn.staking_pool(ip_usdc_stk, pwripor_stk_usdc, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                                tkn_per_block, blocks_per_yr, user_ip_usdc,
                                user_pwripor * user_delegation.loc[:, 'USDC'][0])
user_usdt_apr = fn.staking_pool(ip_usdt_stk, pwripor_stk_usdt, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                                tkn_per_block, blocks_per_yr, user_ip_usdt,
                                user_pwripor * user_delegation.loc[:, 'USDT'][0])
user_dai_apr = fn.staking_pool(ip_dai_stk, pwripor_stk_dai, ipor_prc, vrt_shft, base_boost, log_base, horz_shft,
                               tkn_per_block, blocks_per_yr, user_ip_dai,
                               user_pwripor * user_delegation.loc[:, 'DAI'][0])

user_aprs = pd.DataFrame(index=['pct'], columns=['USDC', 'USDT', 'DAI'])
user_aprs.iloc[0, :] = [user_usdc_apr, user_usdt_apr, user_dai_apr]
user_tot_aprs = np.sum(user_aprs, axis=1)[0]

print('You should allocate your pwrIPOR tokens using this delegation strategy:')
print(user_delegation)
print('This would give you the following expected aprs in USD')
print(user_aprs)
print('With the total apr in USD across all staking pools of:')
print(user_tot_aprs)
