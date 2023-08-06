# -*- coding: utf-8 -*-

from typing import Union
from typing import List
from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class ChunkSourceCompServer(BaseComponent):
    def SetAddArea(self, key, dimensionId, minPos, maxPos):
        # type: (str, int, Tuple[int,int,int], Tuple[int,int,int]) -> bool
        """
        设置区块的常加载
        """
        pass

    def DeleteArea(self, key):
        # type: (str) -> bool
        """
        删除一个常加载区域
        """
        pass

    def DeleteAllArea(self):
        # type: () -> int
        """
        删除所有常加载区域
        """
        pass

    def GetAllAreaKeys(self):
        # type: () -> List[str]
        """
        获取所有常加载区域名称列表
        """
        pass

    def CheckChunkState(self, dimension, pos):
        # type: (int, Tuple[int,int,int]) -> bool
        """
        判断指定位置的chunk是否加载完成
        """
        pass

    def AddChunkPosWhiteList(self, dimension, pos):
        # type: (int, Tuple[int,int]) -> bool
        """
        为某区块加载完成、准备卸载事件添加监听
        """
        pass

    def RemoveChunkPosWhiteList(self, dimension, pos):
        # type: (int, Tuple[int,int]) -> bool
        """
        移除对某区块加载完成、准备卸载事件的监听
        """
        pass

    def GetChunkMinPos(self, chunkPos):
        # type: (Tuple[int,int]) -> Union[None,Tuple[int,int,int]]
        """
        获取某区块最小点的坐标
        """
        pass

    def GetChunkMaxPos(self, chunkPos):
        # type: (Tuple[int,int]) -> Union[None,Tuple[int,int,int]]
        """
        获取某区块最大点的坐标
        """
        pass

    def GetChunkMobNum(self, dimension, chunkPos):
        # type: (int, Tuple[int,int]) -> int
        """
        获取某区块中的生物数量（不包括玩家，但包括盔甲架）
        """
        pass

    def GetChunkPosFromBlockPos(self, blockPos):
        # type: (Tuple[int,int,int]) -> Union[None,Tuple[int,int]]
        """
        通过方块坐标获得该方块所在区块坐标
        """
        pass

    def IsChunkGenerated(self, dimensionId, chunkPos):
        # type: (int, Tuple[int,int]) -> bool
        """
        获取某个区块是否生成过。
        """
        pass

