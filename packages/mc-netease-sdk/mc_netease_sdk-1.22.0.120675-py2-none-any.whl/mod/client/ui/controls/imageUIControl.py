# -*- coding: utf-8 -*-

from mod.client.ui.controls.baseUIControl import BaseUIControl
from typing import Tuple

class ImageUIControl(BaseUIControl):
    def SetSprite(self, texturePath):
        # type: (str) -> None
        """
        给图片控件换指定贴图
        """
        pass

    def SetSpriteColor(self, color):
        # type: (Tuple[float,float,float]) -> None
        """
        设置图片颜色
        """
        pass

    def SetSpriteGray(self, gray):
        # type: (bool) -> None
        """
        给图片控件置灰，比直接SetSprite一张灰图片效率要高
        """
        pass

    def SetSpriteUV(self, uv):
        # type: (Tuple[float,float]) -> None
        """
        设置图片的起始uv，与json中的"uv"属性作用一致
        """
        pass

    def SetSpriteUVSize(self, uvSize):
        # type: (Tuple[float,float]) -> None
        """
        设置图片的uv大小，与json中的"uv_size"属性作用一致
        """
        pass

    def SetSpriteClipRatio(self, clipRatio):
        # type: (float) -> None
        """
        设置图片的裁剪区域比例（不改变控件尺寸）。可以配合image控件的clip_ratio属性控制方向。
        """
        pass

