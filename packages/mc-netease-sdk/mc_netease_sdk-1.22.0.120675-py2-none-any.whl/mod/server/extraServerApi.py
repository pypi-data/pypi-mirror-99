# -*- coding: utf-8 -*-

from typing import Tuple
from typing import Union
from typing import List
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from mod.server.system.serverSystem import ServerSystem
from typing import Type
from mod.common.component.baseComponent import BaseComponent
import mod.common.minecraftEnum as minecraftEnum

def RegisterComponent(nameSpace, name, clsPath):
    # type: (str, str, str) -> bool
    """
    用于将组件注册到引擎中
    """
    pass

def RegisterSystem(nameSpace, systemName, clsPath):
    # type: (str, str, str) -> ServerSystem
    """
    用于将系统注册到引擎中，引擎会创建一个该系统的实例，并在退出游戏时回收。系统可以执行我们引擎赋予的基本逻辑，例如监听事件、执行Tick函数、与客户端进行通讯等。
    """
    pass

def GetSystem(nameSpace, systemName):
    # type: (str, str) -> ServerSystem
    """
    获取已注册的系统
    """
    pass

def CreateComponent(entityId, nameSpace, name):
    # type: (Union[str,int], str, str) -> BaseComponent
    """
    给实体创建服务端组件
    """
    pass

def GetComponent(entityId, nameSpace, name):
    # type: (str, str, str) -> BaseComponent
    """
    获取实体的服务端组件。一般用来判断某个组件是否创建过，其他情况请使用CreateComponent
    """
    pass

def DestroyComponent(entityId, nameSpace, name):
    # type: (str, str, str) -> None
    """
    删除实体的服务端组件
    """
    pass

def GetEngineCompFactory():
    # type: () -> EngineCompFactoryServer
    """
    获取引擎组件的工厂，通过工厂可以创建服务端的引擎组件
    """
    pass

def GetMinecraftEnum():
    """
    用于获取枚举值文档中的枚举值
    """
    return minecraftEnum

def GetServerSystemCls():
    # type: () -> Type[ServerSystem]
    """
    用于获取服务器system基类。实现新的system时，需要继承该接口返回的类
    """
    pass

def GetComponentCls():
    # type: () -> Type[BaseComponent]
    """
    用于获取服务器component基类。实现新的component时，需要继承该接口返回的类
    """
    pass

def GetEngineNamespace():
    # type: () -> str
    """
    获取引擎事件的命名空间。监听引擎事件时，namespace传该接口返回的namespace
    """
    pass

def GetEngineSystemName():
    # type: () -> str
    """
    获取引擎系统名。监听引擎事件时，systemName传该接口返回的systemName
    """
    pass

def GetLevelId():
    # type: () -> str
    """
    获取levelId。某些组件需要levelId创建，可以用此接口获取levelId。其中level即为当前地图的游戏。
    """
    pass

def GetEngineActor():
    # type: () -> dict
    """
    获取所有实体。
    """
    pass

def GetPlayerList():
    # type: () -> List[str]
    """
    获取level中所有玩家的id列表
    """
    pass

def SetEntityLimit(num):
    # type: (int) -> bool
    """
    设置以玩家为中心，6个chunk范围内的最大实体数量，实体数量超过该值后将不再随机生成实体，不影响summon指令和sdk相关生成实体接口
    """
    pass

def GetEntityLimit():
    # type: () -> int
    """
    获取当前level最大实体数量（上限值，非现有值）
    """
    pass

def GetDirFromRot(rot):
    # type: (Tuple[float,float]) -> Tuple[float,float,float]
    """
    通过旋转角度获取朝向
    """
    pass

def StartProfile():
    # type: () -> bool
    """
    开始启动服务端脚本性能分析，启动后调用StopProfile即可在路径path生成函数性能火焰图，此接口只支持PC端。生成的火焰图可以用浏览器打开，推荐chrome浏览器。
    """
    pass

def StopProfile(fileName=None):
    # type: (str) -> bool
    """
    停止服务端脚本性能分析并生成火焰图，与StartProfile配合使用，此接口只支持PC端
    """
    pass

def StartMultiProfile():
    # type: () -> bool
    """
    开始启动服务端与客户端双端脚本性能分析，启动后调用StopMultiProfile即可在路径path生成函数性能火焰图。双端采集时数据误差较大，建议优先使用StartProfile单端版本，此接口只支持PC端
    """
    pass

def StopMultiProfile(fileName=None):
    # type: (str) -> bool
    """
    停止双端脚本性能分析并生成火焰图，与StartMultiProfile配合使用，此接口只支持PC端
    """
    pass

def StartRecordPacket():
    # type: () -> bool
    """
    开始启动服务端与客户端之间的引擎收发包统计，启动后调用StopRecordPacket即可获取两个函数调用之间引擎收发包的统计信息，仅支持租赁服与Apollo网络服环境（不支持单机环境）
    """
    pass

def StopRecordPacket():
    # type: () -> dict
    """
    停止服务端与客户端之间的引擎收发包统计并输出结果，与StartRecordPacket配合使用，输出结果为字典，key为网络包名，value字典中记录收发信息，具体见示例，仅支持租赁服与Apollo网络服环境（不支持单机环境）
    """
    pass

def StartRecordEvent():
    # type: () -> bool
    """
    开始启动服务端与客户端之间的脚本事件收发统计，启动后调用StopRecordEvent即可获取两个函数调用之间脚本事件收发的统计信息，仅支持租赁服与Apollo网络服环境（不支持单机环境）
    """
    pass

def StopRecordEvent():
    # type: () -> dict
    """
    停止服务端与客户端之间的脚本事件收发统计并输出结果，与StartRecordEvent配合使用，输出结果为字典，key为网络包名，value字典中记录收发信息，具体见示例，仅支持租赁服与Apollo网络服环境（不支持单机环境）
    """
    pass

def IsInServer():
    # type: () -> bool
    """
    获取当前游戏是否跑在服务器环境下
    """
    pass

def IsInApollo():
    # type: () -> bool
    """
    返回当前游戏Mod是否运行在Apollo网络服
    """
    pass

def AddEntityTickEventWhiteList(identifier):
    # type: (str) -> bool
    """
    添加实体类型到EntityTickServerEvent事件的触发白名单。
    """
    pass

def GetPlatform():
    # type: () -> int
    """
    获取脚本运行的平台
    """
    pass

