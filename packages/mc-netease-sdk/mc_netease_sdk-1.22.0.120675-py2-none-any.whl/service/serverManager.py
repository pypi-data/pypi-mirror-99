# -*- coding: utf-8 -*-

"""这里是service的一些服务的管理接口
"""


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


def GetServersStatus():
	"""
	获取所有lobby/game服务器的状态。只有状态1表示服务器正常服务，其他状态表示服务器不能服务。

	Returns:
		dict           key:int, 服务器id，value:int 服务器状态。服务器状态如下：<br/>1:准备状态<br/>2:停止状态 <br/>3:准备状态
	"""
	pass


def IsConnectedServer(serverId):
	# type: (int) -> bool
	"""
	service是否与lobby/game/proxy建立连接。

	Args:
		serverId       int            服务器id

	Returns:
		bool           True，已经建立连接;False未建立连接
	"""
	pass

