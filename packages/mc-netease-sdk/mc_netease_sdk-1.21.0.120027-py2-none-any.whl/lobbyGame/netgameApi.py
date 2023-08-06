# -*- coding: utf-8 -*-

"""这里是lobbygame的一些通用的接口
"""


def ChangeAllPerformanceSwitch(isDisable, extra):
	# type: (bool, list) -> None
	"""
	整体关闭/打开预定义的游戏原生逻辑，所有的逻辑默认状态均为【开】（也就是is_disable=False），
	只有当调用此接口关闭之后，才会进入到【关】的状态，关闭这类原生逻辑能够提
	高服务器的性能，承载更高的同时在线人数，同时也会使一些生存服的玩法失效。另外，强烈建议在服务
	器初始化时调用此接口，同时不要在服务器运行中途修改

	Args:
		is_disable     bool           True代表【关】，False代表【开】
		extra          list           剔除掉不需要改变开关状态的具体功能的枚举值列表。默认为空

	"""
	pass


def ChangePerformanceSwitch(key, isDisable):
	# type: (int, bool) -> None
	"""
	关闭/打开某个游戏原生逻辑，所有的逻辑默认状态均为【开】（也就是is_disable=False），
	只有当调用此接口关闭之后，才会进入到【关】的状态，关闭这类原生逻辑能够提高服务器的性能，
	承载更高的同时在线人数，同时也会使一些生存服的玩法失效。另外，强烈建议在服务器初始化时调用此接口，同时不要在服务器运行中途修改

	Args:
		key            int            具体功能的枚举值，详情见备注
		isDisable      bool           True代表【关】，False代表【开】

	"""
	pass


def CheckMasterExist():
	"""
	检查服务器是否与master建立连接

	Returns:
		bool           是否与master建立连接
	"""
	pass


def DelForbidDragonEggTeleportField(fid):
	# type: (int) -> bool
	"""
	删除禁止龙蛋传送的地图区域

	Args:
		fid            int            区域的唯一ID，必须大于等于0

	Returns:
		bool           是否成功删除（对应fid无法找到返回删除失败）
	"""
	pass


def DelForbidFlowField(fid):
	# type: (int) -> bool
	"""
	删除地图区域，不同的ID的区域边界会阻挡流体的流动

	Args:
		fid            int            区域的唯一ID，必须大于等于0

	Returns:
		bool           是否成功删除（对应fid无法找到返回删除失败）
	"""
	pass


def GetCommonConfig():
	"""
	获取公共配置netgame_common.json中内容，将该文件内容映射为一个dict，注意该配置不是实时更新，可能遗漏部分服务器配置

	Returns:
		dict           配置内容
	"""
	pass


def GetConnectingProxyIdOfPlayer(playerId):
	# type: (str) -> int
	"""
	获取玩家客户端连接的proxy服务器id

	Args:
		playerId       str            玩家id

	Returns:
		int            proxy服务器id
	"""
	pass


def GetMongoConfig():
	"""
	获取mongo数据库的连接参数，对应netgame_common.json中mongo配置

	Returns:
		tuple          (exist, host, user, password, database, port).exist：bool,是否存在mongo数据库配置; host：str, mongo数据库的地址;user：str,mongo数据库的访问用户; port：int, mongo数据库的端口; password：str,mongo数据库的访问密码;database：str,mongo数据库的数据库名
	"""
	pass


def GetMysqlConfig():
	"""
	获取mysql数据库的连接参数，对应netgame_common.json中mysql配置

	Returns:
		tuple          (exist, host, user, password, database, port).exist：bool,是否存在mysql数据库配置; host：string, mysql数据库的地址;user：string,mysql数据库的访问用户; port：int, mysql数据库的端口; password：string,mysql数据库的访问密码;database：string,mysql数据库的数据库名
	"""
	pass


def GetOnlinePlayerNum():
	"""
	获取当前服务器的在线人数

	Returns:
		int            当前服务器在线人数
	"""
	pass


def GetPlayerIdByUid(uid):
	"""
	根据玩家uid获取玩家ID（也即playerId）。若玩家不在这个lobby/game，则返回为空字符

	Returns:
		str            玩家id，也即玩家的playerId
	"""
	pass


def GetPlayerLockResult(id, success):
	# type: (int, bool) -> None
	"""
	不建议开发者使用，把获取玩家在线锁结果告知给引擎层

	Args:
		id             int            对应【ServerGetPlayerLockEvent】事件的传入唯一ID
		success        bool           是否成功

	"""
	pass


def GetPlayerNickname(playerId):
	# type: (str) -> str
	"""
	获取玩家的昵称。

	Args:
		playerId       str            玩家id

	Returns:
		str            昵称
	"""
	pass


def GetPlayerUid(playerId):
	# type: (str) -> int
	"""
	获取玩家的uid

	Args:
		playerId       str            玩家id

	Returns:
		int            玩家的uid；玩家的唯一标识
	"""
	pass


def GetRedisConfig():
	"""
	获取redis数据库的连接参数，对应netgame_common.json中redis配置

	Returns:
		tuple          (exist, host, port, password).exist：bool,是否存在redis配置; host：str, redis数据库的地址;port：int, redis数据库的端口; password：str,redis数据库的访问密码
	"""
	pass


def GetServerId():
	"""
	获取服务器id

	Returns:
		int            服务器id，对应netgame_common.json中配置的serverid
	"""
	pass


def GetUidIsSilent(uid):
	"""
	根据玩家uid获取是否被禁言

	Returns:
		int            0:全局禁言，1:普通禁言，2:没有被禁言
	"""
	pass


def IsServiceConnected(serviceId):
	"""
	检查服务器是否与某个service建立连接

	Returns:
		bool           是否与service建立连接
	"""
	pass


def IsShowDebugLog():
	"""
	当前服务器是否打印debug等级的日志

	Returns:
		bool           True，打印debug log，否则不打印debug log
	"""
	pass


def NotifyClientToOpenShopUi(playerId):
	# type: (str) -> None
	"""
	通知客户端打开商城界面

	Args:
		playerId       str            玩家id

	"""
	pass


def QueryPlayerDataResult(dbCallIndex, success, dataStr):
	# type: (int, bool, str) -> None
	"""
	不建议开发者使用，把mc地图中玩家存档字符串告知引擎。需要在queryPlayerDataEvent事件的监听函数中调用本api

	Args:
		dbCallIndex    int            对应【queryPlayerDataEvent】事件的传入唯一ID
		success        bool           是否成功
		dataStr        str            mc地图中玩家存档字符串。

	"""
	pass


def ReleasePlayerLockResult(id, success):
	# type: (int, bool) -> None
	"""
	不建议开发者使用，把释放玩家在线锁结果告知给引擎层

	Args:
		id             int            对应【ServerReleasePlayerLockEvent/ServerReleasePlayerLockOnShutDownEvent】事件传入的唯一ID
		success        bool           是否成功

	"""
	pass


def SavePlayerDataResult(dbCallIndex, success):
	# type: (int, bool) -> None
	"""
	不建议开发者使用，把玩家数据存档状态告知引擎。mod中需要把玩家数据保存到mysql/mongo中。在savePlayerDataOnShutDownEvent/savePlayerDataEvent事件的监听函数中调用本api

	Args:
		dbCallIndex    int            【savePlayerDataEvent/savePlayerDataOnShutDownEvent】事件中传入唯一ID
		success        bool           存档是否成功

	"""
	pass


def SetAutoRespawn(autoRespawn, internalSeconds, minY, x, y, z):
	# type: (bool, int, int, int, int, int) -> None
	"""
	设置是否启用自动重生逻辑

	Args:
		autoRespawn    bool           是否启用自动重生逻辑
		internalSecondsint            每隔多少秒，检查是否满足自动重生条件
		minY           int            高度低于多少，就会触发自动重生逻辑
		x              int            自动重生逻辑触发后，重生点的坐标
		y              int            自动重生逻辑触发后，重生点的坐标
		z              int            自动重生逻辑触发后，重生点的坐标

	"""
	pass


def SetCityMode(isCityMode):
	# type: (bool) -> None
	"""
	设置游戏为主城模式：包括有无法改变地形，不切换日夜，不改变天气，不刷新生物等限制

	Args:
		isCityMode     bool           是否为主城模式

	"""
	pass


def SetEnableLimitArea(limit, x, y, z, offsetX, offsetZ):
	# type: (bool, int, int, int, int, int) -> None
	"""
	设置地图最大区域，超过区域的地形不再生成

	Args:
		limit          bool           是否启用地区区域限制
		x              int            地图区域的中心点
		y              int            地图区域的中心点
		z              int            地图区域的中心点
		offsetX        int            地图区域在x方向和z方向的最大偏移
		offsetZ        int            地图区域在x方向和z方向的最大偏移

	"""
	pass


def SetForbidDragonEggTeleportField(fid, dimensionId, minPos, maxPos, priority, isForbid):
	# type: (int, int, tuple(int), tuple(int), int, bool) -> bool
	"""
	设置禁止龙蛋传送的地图区域

	Args:
		fid            int            区域的唯一ID，必须大于等于0
		dimensionId    int            区域所在的维度
		minPos         tuple(int)     长方体区域的x，y，z值最小的点，x，y，z为方块的坐标，而不是像素坐标
		maxPos         tuple(int)     长方体区域的x，y，z值最大的点，x，y，z为方块的坐标，而不是像素坐标
		priority       int            区域的优先级，缺损时默认值为0，当一个点位于多个区域包围时，最终会以优先级最高的区域为准
		isForbid       bool           是否禁止龙蛋传送，为了处理嵌套区域之间的权限冲突，只要是独立的区域都需要设置是否禁止龙蛋传送

	Returns:
		bool           是否成功设置
	"""
	pass


def SetForbidFlowField(fid, dimensionId, minPos, maxPos, priority, isForbid):
	# type: (int, int, tuple(int), tuple(int), int, bool) -> bool
	"""
	设置地图区域，不同的ID的区域边界会阻挡流体的流动

	Args:
		fid            int            区域的唯一ID，必须大于等于0
		dimensionId    int            区域所在的维度
		minPos         tuple(int)     长方体区域的x，y，z值最小的点，x，y，z为方块的坐标，而不是像素坐标
		maxPos         tuple(int)     长方体区域的x，y，z值最大的点，x，y，z为方块的坐标，而不是像素坐标
		priority       int            区域的优先级，缺损时默认值为0，当一个点位于多个区域包围时，最终会以优先级最高的区域为准
		isForbid       bool           是否禁止流体流动，为了处理嵌套区域之间的权限冲突，只要是独立的区域都需要设置是否禁止流体流动

	Returns:
		bool           是否设置成功
	"""
	pass


def SetGracefulShutdownOk():
	"""
	不建议开发者使用，设置脚本层的优雅关机逻辑已经执行完毕，引擎可以开始优雅关机了

	"""
	pass


def SetLevelGameType(mode):
	# type: (int) -> None
	"""
	强制设置游戏的玩法模式

	Args:
		mode           int            0生存模式，1创造模式，2冒险模式

	"""
	pass


def SetShutdownOk():
	"""
	不建议开发者使用，设置脚本层的强制关机逻辑已经执行完毕，引擎可以开始强制关机了

	"""
	pass


def SetUseDatabaseSave(bUseDatabase, dbName, internalSaveSecond):
	# type: (bool, str, int) -> None
	"""
	设置是否使用数据库定时存档。定时存档会定时触发savePlayerDataEvent事件

	Args:
		bUseDatabase   bool           是否使用数据库
		dbName         str            30个字符内的英文字符串，建议使用项目英文名
		internalSaveSecondint            触发定时存档的时间间隔，单位秒

	"""
	pass


def ShieldPlayerJoinText(bShield):
	# type: (bool) -> None
	"""
	是否屏蔽客户端左上角 “xxx 加入了游戏”的提示

	Args:
		bShield        bool           True，不显示提示；False，显示提示

	"""
	pass


def ShutdownServer():
	"""
	强制关机

	"""
	pass


def TransferToOtherServer(playerId, typeName, transferParam):
	# type: (str, str, str) -> None
	"""
	玩家转移到指定类型的服务器，假如同类服务器有多个，就根据负载均衡选择一个

	Args:
		playerId       str            玩家id
		typeName       str            目标服务器的类型，netgame_commom.json中配置的type,比如lobby，game
		transferParam  str            切服传入参数，默认空字符串。当玩家跳转到目标服务器触发AddServerPlayerEvent事件时，AddServerPlayerEvent事件会携带这个参数

	"""
	pass


def TransferToOtherServerById(playerId, serverId, transferParam):
	# type: (str, str, str) -> None
	"""
	玩家迁移到指定服务器id的服务器

	Args:
		playerId       str            玩家id
		serverId       str            目标服务器id，对应netgame_common.json中配置的serverid
		transferParam  str            切服传入参数，默认空字符串。当玩家跳转到目标服务器触发AddServerPlayerEvent事件时，AddServerPlayerEvent事件会携带这个参数

	"""
	pass


def TryToKickoutPlayer(playerId, message):
	# type: (str, str) -> None
	"""
	把玩家踢下线，message中的文字会显示在客户端的断线提示中

	Args:
		playerId       str            玩家对象的entityId
		message        str            踢掉玩家的理由，默认为空

	"""
	pass

