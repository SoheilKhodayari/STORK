from ._base import PayloadStrategy

#====================================================================== 
# Blacklist
#====================================================================== 
from ._blacklist_payloads import SlashToBackslashPayload
from ._blacklist_payloads import EscapeDoubleslashPayload
from ._blacklist_payloads import NoSlashesPayload

from ._blacklist_payloads import UnicodeDotPayload

from ._blacklist_payloads import ChangeSchemePayload

from ._blacklist_payloads import EncodeSpecialsPayload
from ._blacklist_payloads import EncodeKeepSlashPayload


#====================================================================== 
# Whitelist
#====================================================================== 
from ._whitelist_payloads import PrependWhitelistPayload
from ._whitelist_payloads import PrependAuthenticationPayload
from ._whitelist_payloads import DirectoryPayload


#====================================================================== 
# IP
#====================================================================== 
from ._ip_payloads import ToIP4OctPayload
from ._ip_payloads import ToIP4DotlessOctPayload

from ._ip_payloads import ToIP4DecPayload
from ._ip_payloads import ToIP4DotlessDecPayload

from ._ip_payloads import ToIP4HexPayload
from ._ip_payloads import ToIP4DotlessHexPayload

from ._ip_payloads import ToNipDashPayload
from ._ip_payloads import ToNipDotPayload


#====================================================================== 
# Misc
#====================================================================== 
from ._misc_payloads import IdentityPayload


class PayloadFactory:

    def __init__(self):
        self._payload_strats = {}

        # Misc
        self.register_strategy(IdentityPayload)

        # Blacklist payloads
        self.register_strategy(SlashToBackslashPayload)
        self.register_strategy(EscapeDoubleslashPayload)
        self.register_strategy(NoSlashesPayload)
        self.register_strategy(UnicodeDotPayload)
        self.register_strategy(ChangeSchemePayload)
        self.register_strategy(EncodeSpecialsPayload)
        # self.register_strategy(EncodeKeepSlashPayload)

        # Whitelist payloads
        self.register_strategy(PrependWhitelistPayload)
        self.register_strategy(PrependAuthenticationPayload)
        self.register_strategy(DirectoryPayload)

        # IP payloads
        # self.register_strategy(ToIP4OctPayload)
        # self.register_strategy(ToIP4DotlessOctPayload)
        self.register_strategy(ToIP4DecPayload)
        self.register_strategy(ToIP4DotlessDecPayload)
        # self.register_strategy(ToIP4HexPayload)
        # self.register_strategy(ToIP4DotlessHexPayload)
        # self.register_strategy(ToNipDashPayload)
        # self.register_strategy(ToNipDotPayload)

    def register_strategy(self, payload_strategy_cls):
        name = payload_strategy_cls.__name__
        self._payload_strats[name] = payload_strategy_cls

    def unregister_strategy(self, payload_strategy_cls):
        name = payload_strategy_cls.__name__
        del self._payload_strats[name]


    def list_strategies(self):
        return list(self._payload_strats.keys())

    def create_by_name(self, strat_name, add_tracking=False,  **kwargs):
        if strat_name in self._payload_strats:
            return self._payload_strats[strat_name](add_tracking, **kwargs)
        raise Exception(f"No payload strategy with name {strat_name} registered")
