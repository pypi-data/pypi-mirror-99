# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

from halo_app.classes import AbsBaseClass


class AbsInfraService(AbsBaseClass):
    pass


class AbsMailService(AbsBaseClass):
    def send(self,item)->bool:
        pass
