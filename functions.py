from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import math


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
                 horz_shft=0.5, tkn_per_block=0.5, blocks_per_yr=2628000.0, user_ip_tkn=1.0, user_pwripor=1.0):
    user_pwrup = vrt_shft + base_boost + math.log(horz_shft + (user_pwripor / user_ip_tkn), log_base)
    pool_base_pwrup = vrt_shft + base_boost + math.log(horz_shft + (pwripor_stk / ip_tkn_stk), log_base)
    base_pool_pwrup = pool_base_pwrup * ip_tkn_stk
    agg_pwrup = base_pool_pwrup + user_pwrup * user_ip_tkn
    comp_multiplier = tkn_per_block / agg_pwrup
    user_apr_usd = user_ip_tkn * user_pwrup * comp_multiplier * blocks_per_yr * ipor_prc
    return user_apr_usd



