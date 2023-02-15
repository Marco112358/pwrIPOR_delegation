from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import math
import requests
from web3 import Web3


def cg_pull(ticker='btc', curr='usd', days='max', intv='daily'):
    cg = CoinGeckoAPI()
    out = cg.get_coin_market_chart_by_id(id=ticker, vs_currency=curr, days=days, interval=intv)
    df = pd.DataFrame(data=out)
    df[['date', 'price']] = pd.DataFrame(df.prices.tolist(), index=df.index)
    df[['date']] = df[['date']] / 1000
    df['datetime'] = [datetime.fromtimestamp(x) for x in df['date']]
    df_out = df[['datetime', 'price']]
    return df_out


def get_price(ticker='ipor', curr='usd', days='max', intv='daily'):
    cg = CoinGeckoAPI()
    out = cg.get_price(ids=ticker, vs_currencies=curr)
    df = pd.DataFrame(data=out)
    val = df[ticker][0]
    return val


def staking_pool(ip_tkn_stk=None, pwripor_stk=None, ipor_prc=None, vrt_shft=1.0, base_boost=0.4, log_base=2.0,
                 horz_shft=0.5, tkn_per_block=0.5, blocks_per_yr=2628000.0, user_ip_tkn=1.0, user_pwripor=1.0,
                 ratio_scalar=2.0):
    user_pwrup = vrt_shft + base_boost + math.log(horz_shft + (ratio_scalar * (user_pwripor / user_ip_tkn)), log_base)
    pool_base_pwrup = vrt_shft + base_boost + math.log(horz_shft + (ratio_scalar * (pwripor_stk / ip_tkn_stk)), log_base)
    base_pool_pwrup = pool_base_pwrup * ip_tkn_stk
    agg_pwrup = base_pool_pwrup  # + user_pwrup * user_ip_tkn
    comp_multiplier = tkn_per_block / agg_pwrup
    user_apr_usd = user_ip_tkn * user_pwrup * comp_multiplier * blocks_per_yr * ipor_prc
    return user_apr_usd


def data_import(url='https://api.ipor.io/monitor/liquidity-mining-statistics'):
    lm_stats_dict = requests.get(url).json()
    pools_list = []
    for pool_info in lm_stats_dict['pools']:
        pools_list.append([pool_info['ipToken'], pool_info['delegatedPwIporAmount'], pool_info['stakedIpTokenAmount']])
    pools_df = pd.DataFrame(data=pools_list, columns=['ipToken', 'delegatedPwIporAmount', 'stakedIpTokenAmount'])
    pools_df = pools_df.set_index('ipToken', drop=True)
    return pools_df


def get_exch_rt(API_KEY="19817a3526604af0aff145aada226a17",
                url="https://mainnet.infura.io/v3/19817a3526604af0aff145aada226a17", scalar=1000000000000000000,
                address=None, abi=None):
    w3 = Web3(Web3.HTTPProvider(url))
    # Get abi from etherscan > contract > code > scroll down to Contract ABI section and copy
    contract = w3.eth.contract(address=address, abi=abi)
    exch_rt = contract.functions.calculateExchangeRate().call() / scalar
    return exch_rt
