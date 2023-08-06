# -*- coding: utf-8 -*-

from mod.client.ui.controls.baseUIControl import BaseUIControl

class MiniMapUIControl(BaseUIControl):
    def ZoomIn(self, value=0.05):
        # type: (float) -> bool
        """
        放大地图
        """
        pass

    def ZoomOut(self, value=0.05):
        # type: (float) -> bool
        """
        缩小地图
        """
        pass

    def ZoomReset(self):
        # type: () -> bool
        """
        恢复地图放缩大小为默认值
        """
        pass

    def SetHighestY(self, highestY):
        # type: (int) -> bool
        """
        设置绘制地图的最大高度
        """
        pass

