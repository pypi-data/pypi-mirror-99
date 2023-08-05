# coding: utf-8
from core.basic_models.scenarios.base_scenario import scenario_factory
from core.descriptions.smart_updatable_lazy_descriptions import SmartUpdatableLazyDescriptions


class ScenariosDescriptions(SmartUpdatableLazyDescriptions):
    def __init__(self, items):
        super(ScenariosDescriptions, self).__init__(scenario_factory, items, ordered=True)
