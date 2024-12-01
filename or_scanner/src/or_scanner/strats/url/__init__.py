from ._base import URLStrategy

from ._qkey_id import QKeyId
from ._qkey_single import QKeySingle

from ._path_id import PathId
from ._path_single import PathSingle

from ._url_id import URLId
from ._url_single import URLSingle

from ._param_pollution_id import ParamPollutionId


class URLFactory:

    def __init__(self):
        self._url_strats = {}

        self.register_strategy(QKeyId)
        self.register_strategy(QKeySingle)

        self.register_strategy(PathId)
        self.register_strategy(PathSingle)

        self.register_strategy(URLId)
        self.register_strategy(URLSingle)

        # self.register_strategy(ParamPollutionId)


    def register_strategy(self, url_strategy_cls):
        name = url_strategy_cls.__name__
        self._url_strats[name] = url_strategy_cls

    def unregister_strategy(self, url_strategy_cls):
        name = url_strategy_cls.__name__
        del self._url_strats[name]


    def list_strategies(self):
        return list(self._url_strats.keys())

    def create_by_name(self, strat_name, **kwargs):
        if strat_name in self._url_strats:
            return self._url_strats[strat_name](**kwargs)
        raise Exception(f"No url strategy with name {strat_name} registered")


