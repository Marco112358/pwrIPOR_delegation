import functions as fn
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import time

start_time = time.time()

## USER Parameters ##
user_ipusdc = 1000
user_ipusdt = 0
user_ipdai = 250
user_pwripor = 500
change = -1000

## Global Parameters ##
vrt_shft = 1.4
base_boost = 0.4
log_base = 2.0
horz_shft = 0.5
ratio_scalar = 2.0
tkn_per_block = 0.5
blocks_per_yr = 365 * 24 * 60 * 60 / 12
lm_stats_url = 'https://api.ipor.io/monitor/liquidity-mining-statistics'
tkns = ['ipUSDC', 'ipUSDT', 'ipDAI']

## Parameters of Eth Mainnet Pulls ##
scalar = 1000000000000000000
API_KEY = "19817a3526604af0aff145aada226a17"
url = "https://mainnet.infura.io/v3/19817a3526604af0aff145aada226a17"
ipUSDC_address = '0xC52569b5A349A7055E9192dBdd271F1Bd8133277'
ipUSDT_address = '0x33C5A44fd6E76Fc2b50a9187CfeaC336A74324AC'
ipDAI_address = '0x086d4daab14741b195deE65aFF050ba184B65045'
# Get abi from etherscan > contract > code > scroll down to Contract ABI section and copy, if proxy need to go to other address
abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"address","name":"appointed","type":"address"},{"indexed":false,"internalType":"bool","name":"status","type":"bool"}],"name":"AppointedToRebalanceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"appointedOwner","type":"address"}],"name":"AppointedToTransferOwnership","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"uint256","name":"oldAutoRebalanceThresholdInThousands","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"newAutoRebalanceThresholdInThousands","type":"uint256"}],"name":"AutoRebalanceThresholdChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"address","name":"oldCharlieTreasury","type":"address"},{"indexed":true,"internalType":"address","name":"newCharlieTreasury","type":"address"}],"name":"CharlieTreasuryChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"address","name":"oldCharlieTreasuryManager","type":"address"},{"indexed":true,"internalType":"address","name":"newCharlieTreasuryManager","type":"address"}],"name":"CharlieTreasuryManagerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"uint256","name":"oldMaxLiquidityPoolBalance","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"newMaxLiquidityPoolBalance","type":"uint256"}],"name":"MaxLiquidityPoolBalanceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"uint256","name":"oldMaxLpAccountContribution","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"newMaxLpAccountContribution","type":"uint256"}],"name":"MaxLpAccountContributionChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"exchangeRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"assetAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ipTokenAmount","type":"uint256"}],"name":"ProvideLiquidity","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"exchangeRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"assetAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ipTokenAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"redeemFee","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"redeemAmount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"address","name":"oldTreasury","type":"address"},{"indexed":true,"internalType":"address","name":"newTreasury","type":"address"}],"name":"TreasuryChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"changedBy","type":"address"},{"indexed":true,"internalType":"address","name":"oldTreasuryManager","type":"address"},{"indexed":true,"internalType":"address","name":"newTreasuryManager","type":"address"}],"name":"TreasuryManagerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[{"internalType":"address","name":"appointed","type":"address"}],"name":"addAppointedToRebalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"calculateExchangeRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"confirmTransferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"assetAmount","type":"uint256"}],"name":"depositToStanley","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAsset","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAutoRebalanceThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCharlieTreasury","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCharlieTreasuryManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIpToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMaxLiquidityPoolBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMaxLpAccountContribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMilton","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMiltonStanleyBalanceRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMiltonStorage","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRedeemFeeRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getRedeemLpMaxUtilizationRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getStanley","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTreasury","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTreasuryManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVersion","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bool","name":"paused","type":"bool"},{"internalType":"address","name":"initAsset","type":"address"},{"internalType":"address","name":"ipToken","type":"address"},{"internalType":"address","name":"milton","type":"address"},{"internalType":"address","name":"miltonStorage","type":"address"},{"internalType":"address","name":"stanley","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"appointed","type":"address"}],"name":"isAppointedToRebalance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"assetAmount","type":"uint256"}],"name":"provideLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rebalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"ipTokenAmount","type":"uint256"}],"name":"redeem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"appointed","type":"address"}],"name":"removeAppointedToRebalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newAutoRebalanceThreshold","type":"uint256"}],"name":"setAutoRebalanceThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newCharlieTreasury","type":"address"}],"name":"setCharlieTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newCharlieTreasuryManager","type":"address"}],"name":"setCharlieTreasuryManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxLiquidityPoolBalance","type":"uint256"}],"name":"setMaxLiquidityPoolBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxLpAccountContribution","type":"uint256"}],"name":"setMaxLpAccountContribution","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newRatio","type":"uint256"}],"name":"setMiltonStanleyBalanceRatio","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newTreasury","type":"address"}],"name":"setTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newTreasuryManager","type":"address"}],"name":"setTreasuryManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"appointedOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"assetAmount","type":"uint256"}],"name":"transferToCharlieTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"assetAmount","type":"uint256"}],"name":"transferToTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"withdrawAllFromStanley","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"assetAmount","type":"uint256"}],"name":"withdrawFromStanley","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


## Put Imports and Parameters into Lists and get no. of tokens ##
ip_contracts = [ipUSDC_address, ipUSDT_address, ipDAI_address]  # Will need to update if add new tokens
user_ip_tkns = [user_ipusdc, user_ipusdt, user_ipdai]  # Will need to update if add new tokens
no_tkns = len(user_ip_tkns)

## NEEDED API INPUTS ##
pools_df = fn.data_import(lm_stats_url)
stkd_amts = []
deleg_amts = []
ip_prcs = []
for i, tkn in enumerate(tkns):
    stkd_amts.append(float(pools_df.loc[tkn, 'stakedIpTokenAmount']))
    deleg_amts.append(float(pools_df.loc[tkn, 'delegatedPwIporAmount']))
    ## Pull ipToken exchange rates from the Liquidity Pool Contracts (Joseph)
    ip_prcs.append(fn.get_exch_rt(API_KEY, url, scalar, ip_contracts[i], abi))
ipor_prc = fn.get_price('ipor', 'usd')

## Optimizer ##
def objective(x, sign=-1.0):
    pwr_pct = x[:no_tkns]
    ip_tkns = x[no_tkns:-1]
    pw_tkn = x[-1]
    user_pwripor_list = np.multiply(pwr_pct, pw_tkn)
    new_pwripor_list = deleg_amts + user_pwripor_list
    new_stkd_amts = stkd_amts + ip_tkns
    user_apr = []
    for t in np.arange(0, no_tkns):
        if user_ip_tkns[t] == 0:
            apr = 0.0
        else:
            apr = fn.staking_pool(new_stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                                  horz_shft, tkn_per_block, blocks_per_yr, ip_tkns[t], user_pwripor_list[t], ratio_scalar)
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
bnds = [b1, b1, b1]
for t in np.arange(0, no_tkns):
    b = (max(0, min(user_ip_tkns[t], user_ip_tkns[t] + (change / ip_prcs[t]))),
         max(user_ip_tkns[t], user_ip_tkns[t] + (change / ip_prcs[t])))
    # b = (0, user_ip_tkns[t] + (change / ip_prcs[t]))
    bnds.append(b)

b = (max(0, min(user_pwripor, user_pwripor + (change / ipor_prc))),
     max(user_pwripor, user_pwripor + (change / ipor_prc)))
# b = (0, user_pwripor + (change / ipor_prc))
bnds.append(b)

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
new_stkd_amts = stkd_amts + new_ip_tkns
user_apr_list = []
for t in np.arange(0, no_tkns):
    if user_ip_tkns[t] == 0:
        apr = 0.0
    else:
        apr = fn.staking_pool(new_stkd_amts[t], new_pwripor_list[t], ipor_prc, vrt_shft, base_boost, log_base,
                              horz_shft, tkn_per_block, blocks_per_yr, new_ip_tkns[t], user_pwripor_list[t], ratio_scalar)
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
iptokn_cost = np.sum(np.multiply(np.subtract(new_ip_tkns, user_ip_tkns), ip_prcs))
ipor_cost = np.multiply(np.subtract(new_pw_tkn, user_pwripor), ipor_prc)
total_cost = iptokn_cost + ipor_cost

print('You should buy/sell ' + str(round((new_pw_tkn - user_pwripor), 2)) + ' more pwrIPOR')
print('For a final total of ' + str(round(new_pw_tkn, 2)) + ' pwrIPOR')
print('Cost to purchase (or amount received) pwrIPOR is ' + str(round(ipor_cost, 2)))
print('You should buy/sell the following amounts of ipTokens')
print(user_iptkns_chng)
print('For a final total amount of ipTkns')
print(user_iptkns_df)
print('Cost to purchase (or amount received)  ipTokens is ' + str(round(iptokn_cost, 2)))
print('You should allocate your pwrIPOR tokens using this delegation strategy:')
print(user_delegation)
print('This would give you the following expected aprs in USD')
print(user_aprs)
print('With the total apr in USD across all staking pools of:')
print(round(user_tot_aprs, 2))
print('This would cost a total of ' + str(round(total_cost, 2)))
print('This optimization took ' + str(round(time.time() - start_time, 2)) + ' seconds to run')

