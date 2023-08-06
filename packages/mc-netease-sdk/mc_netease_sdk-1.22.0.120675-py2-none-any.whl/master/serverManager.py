# -*- coding: utf-8 -*-

"""这里是master关于服务器管理的一些接口
"""


def GetAllServerStatus():
	"""
	获取所有服务器的状态。只有状态2表示服务器正常服务，其他状态表示服务器不能服务。

	Returns:
		dict           key:int类型，服务器id，value:int类型，服务器状态。服务器状态如下：<br/> 1:断开连接状态<br/>2:已连接状态<br/> 3:关服状态<br/>4:优雅关服状态<br/>6, 滚动更新中间状态，即将转换到状态7<br/>7 也是滚动更新中间状态，即将转换到状态1或2
	"""
	pass


def GetAllServersOnlineNum():
	"""
	获取所有服务器的在线人数。

	Returns:
		dict           key，int类型，表示服务器id，value，int类型，表示服务器在线人数
	"""
	pass


def GetConnectedLobbyAndGameIds():
	"""
	获取所有已经连接的lobby/game的服务器id列表。

	Returns:
		list           服务器id列表，服务器id是int类型。
	"""
	pass


def GetOneServerStatus(serverId):
	# type: (int) -> int
	"""
	获取服务器状态。只有状态2表示服务器正常服务，其他状态表示服务器不能服务。

	Args:
		serverId       int            服务器id

	Returns:
		int            服务器状态。服务器状态如下：<br/> 1:断开连接状态<br/>2:已连接状态<br/> 3:关服状态<br/>4:优雅关服状态<br/>6, 滚动更新中间状态，即将转换到状态7<br/>7 也是滚动更新中间状态，即将转换到状态1或2
	"""
	pass


def GetOnlineNumByServerId(serverId):
	# type: (int) -> int
	"""
	获取服务器(lobby/game/proxy)的在线人数。

	Args:
		serverId       int            服务器id

	Returns:
		int            在线人数
	"""
	pass


def GetServerProtocolVersion(serverId):
	# type: (int) -> int
	"""
	获取服务器的协议版本号。多协议版本引擎中（比如同时支持1.14客户端和1.15客户端），需要把客户端分配到相同协议版本的lobby/game中。

	Args:
		serverId       int            lobby/game服务器id

	Returns:
		int            协议版本
	"""
	pass


def GetTotalOnlineNum():
	"""
	获取总得在线人数。

	Returns:
		int            在线人数
	"""
	pass


def IsConnectedServer(serverId):
	# type: (int) -> bool
	"""
	master是否与lobby/game/proxy建立连接。

	Args:
		serverId       int            服务器id

	Returns:
		bool           True，已经建立连接;False未建立连接
	"""
	pass


def IsValidServer(serverId):
	# type: (int) -> bool
	"""
	服务器是否有效。一种用途：master将玩家分配到服务器之前，会检查服务器是否有效，避免把玩家分配到一个即将关闭的服务器中。

	Args:
		serverId       int            服务器id

	Returns:
		bool           True，master已经同服务器建立链接，且服务器正在提供服务，不是即将关闭的服务。
	"""
	pass


def StopServerByServerid(serverId, actType):
	# type: (int, int) -> None
	"""
	关闭某个服务器。

	Args:
		serverId       int            proxy/lobby/game服务器id
		actType        int            1:强制踢出所有玩家后关服;2:等待所有玩家退出后关服

	"""
	pass

