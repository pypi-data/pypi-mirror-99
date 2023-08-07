from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

from halo_app.app.context import HaloContext
from halo_app.domain.entity import AbsHaloAggregateRoot, AbsHaloEntity
from halo_app.domain.event import AbsHaloDomainEvent


class Item(AbsHaloAggregateRoot):

    def __init__(self, id: str,  data: str):
        super(Item, self).__init__(id)
        self.data = data
        self.events = []

class Detail(AbsHaloEntity):

    def __init__(self, id: str,  desc: str, qty:int):
        super(Item, self).__init__(id)
        self.desc = desc
        self.qty = qty
        self.events = []


    def add(self, context, something: str) -> str:
        try:
            self.qty += 1
            self.desc = something
            self.events.append(self.add_domain_event(context, something))
            return something
        except Exception:
            self.events.append(self.add_error_domain_event(context, something))
            return None



    def add_domain_event(self, context, something: str):
        class HaloDomainEvent(AbsHaloDomainEvent):
            def __init__(self, context: HaloContext, name: str,agg_root_id:str,something:str):
                super(HaloDomainEvent, self).__init__(context, name,agg_root_id)
                self.something = something

        return HaloDomainEvent(context, "good",self.agg_root_id,something)

    def add_error_domain_event(self, context, something: str):
        class HaloDomainEvent(AbsHaloDomainEvent):
            def __init__(self, context: HaloContext, name: str,agg_root_id:str,something:str):
                super(HaloDomainEvent, self).__init__(context, name,agg_root_id)
                self.something = something

        return HaloDomainEvent(context, "bad",self.agg_root_id,something)