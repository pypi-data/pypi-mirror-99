# -*- coding: utf-8 -*-

from typing import Tuple

class RotComponentClient(object):
    def GetRot(self):
        # type: () -> Tuple[float,float]
        """
        获取实体角度
        """
        pass

    def SetRot(self, rot):
        # type: (Tuple[float,float]) -> bool
        """
        设置实体的角度
        """
        pass

    def GetBodyRot(self):
        # type: () -> float
        """
        支持获取实体的身体角度
        """
        pass

