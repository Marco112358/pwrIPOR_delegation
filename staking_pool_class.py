import math

class staking_pool:
    def __init__(self, ip_tkn_stk=None, pwrIPOR_stk=None, ipor_prc=None, vrt_shft=1.0, base_boost=0.4, log_base=2.0,
                 horz_shft=0.5, tkn_per_block=0.5, blocks_per_yr=2628000.0, ):
        self.ip_tkn_stk = ip_tkn_stk
        self.pwrIPOR_stk = pwrIPOR_stk
        self.ipor_prc = ipor_prc
        self.vrt_shft = vrt_shft
        self.base_boost = base_boost
        self.log_base = log_base
        self.horz_shft = horz_shft
        self.tkn_per_block = tkn_per_block
        self.blocks_per_yr = blocks_per_yr
        self.pool_base_pwrup = self.pool_base_pwrup_fnc
        self.base_pool_pwrup = self.base_pool_pwrup_fnc

    def pool_base_pwrup_fnc(self):
        self.pool_base_pwrup = self.vrt_shft + self.base_boost + \
                               math.log(self.horz_shft + (self.pwrIPOR_stk / self.ip_tkn_stk), self.log_base)

    def base_pool_pwrup_fnc(self):
        self.base_pool_pwrup = self.pool_base_pwrup * self.ip_tkn_stk
