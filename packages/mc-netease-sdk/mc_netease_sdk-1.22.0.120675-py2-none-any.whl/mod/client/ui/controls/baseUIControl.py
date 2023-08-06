# -*- coding: utf-8 -*-

from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from typing import Tuple
from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.buttonUIControl import ButtonUIControl

class BaseUIControl(object):
    def SetPosition(self, pos):
        # type: (Tuple[float,float]) -> None
        """
        设置控件相对父节点的坐标
        """
        pass

    def GetPosition(self):
        # type: () -> Tuple[float,float]
        """
        获取控件相对父节点的坐标
        """
        pass

    def SetSize(self, size, resizeChildren=False):
        # type: (Tuple[float,float], bool) -> None
        """
        设置控件的大小
        """
        pass

    def GetSize(self):
        # type: () -> Tuple[float,float]
        """
        获取控件的大小
        """
        pass

    def SetVisible(self, visible, forceUpdtae=True):
        # type: (bool, bool) -> None
        """
        根据控件路径选择是否显示某控件
        """
        pass

    def GetVisible(self):
        # type: () -> bool
        """
        根据控件路径返回某控件是否已显示
        """
        pass

    def SetTouchEnable(self, enable):
        # type: (bool) -> None
        """
        设置控件是否可点击交互
        """
        pass

    def SetAlpha(self, alpha):
        # type: (float) -> None
        """
        设置节点的透明度，仅对image和label控件生效
        """
        pass

    def SetLayer(self, layer, syncRefresh=True, forceUpdtae=True):
        # type: (int, bool, bool) -> None
        """
        设置控件节点的层级
        """
        pass

    def GetChildByName(self, childName):
        # type: (str) -> BaseUIControl
        """
        根据子控件的名称获取BaseUIControl实例
        """
        pass

    def GetChildByPath(self, childPath):
        # type: (str) -> BaseUIControl
        """
        根据相对路径获取BaseUIControl实例
        """
        pass

    def asLabel(self):
        # type: () -> LabelUIControl
        """
        将当前BaseUIControl转换为LabelUIControl实例，如当前控件非Label类型则返回None
        """
        pass

    def asButton(self):
        # type: () -> ButtonUIControl
        """
        将当前BaseUIControl转换为ButtonUIControl实例，如当前控件非button类型则返回None
        """
        pass

    def asImage(self):
        # type: () -> ImageUIControl
        """
        将当前BaseUIControl转换为ImageUIControl实例，如当前控件非image类型则返回None
        """
        pass

    def asGrid(self):
        # type: () -> GridUIControl
        """
        将当前BaseUIControl转换为GridUIControl实例，如当前控件非grid类型则返回None
        """
        pass

    def asScrollView(self):
        # type: () -> ScrollViewUIControl
        """
        将当前BaseUIControl转换为ScrollViewUIControl实例，如当前控件非scrollview类型则返回None
        """
        pass

    def asSwitchToggle(self):
        # type: () -> SwitchToggleUIControl
        """
        将当前BaseUIControl转换为SwitchToggleUIControl实例，如当前控件非panel类型则返回None
        """
        pass

    def asTextEditBox(self):
        # type: () -> TextEditBoxUIControl
        """
        将当前BaseUIControl转换为TextEditBoxUIControl实例，如当前控件非editbox类型则返回None
        """
        pass

    def asProgressBar(self, fillImagePath='/filled_progress_bar'):
        # type: (str) -> ProgressBarUIControl
        """
        将当前BaseUIControl转换为TextEditBoxUIControl实例，如当前控件非panel类型则返回None
        """
        pass

    def asNeteasePaperDoll(self):
        # type: () -> NeteasePaperDollUIControl
        """
        将当前BaseUIControl转换为NeteasePaperDollUIControl实例，如当前控件非custom类型则返回None
        """
        pass

    def asMiniMap(self):
        # type: () -> MiniMapUIControl
        """
        将当前BaseUIControl转换为MiniMapUIControl实例，如当前控件非小地图类型则返回None
        """
        pass

