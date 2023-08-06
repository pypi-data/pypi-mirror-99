# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class ActorRenderCompClient(BaseComponent):
    def GetNotRenderAtAll(self):
        # type: () -> bool
        """
        获取实体是否不渲染
        """
        pass

    def SetNotRenderAtAll(self, notRender):
        # type: (bool) -> bool
        """
        设置是否关闭实体渲染
        """
        pass

    def AddPlayerRenderMaterial(self, materialKey, materialName):
        # type: (str, str) -> bool
        """
        增加玩家渲染需要的材质
        """
        pass

    def AddPlayerRenderController(self, renderControllerName, condition=''):
        # type: (str, str) -> bool
        """
        增加玩家渲染控制器
        """
        pass

    def RemovePlayerRenderController(self, renderControllerName):
        # type: (str) -> bool
        """
        删除玩家渲染控制器
        """
        pass

    def RemovePlayerGeometry(self, geometryKey):
        # type: (str) -> bool
        """
        删除玩家渲染几何体
        """
        pass

    def AddPlayerGeometry(self, geometryKey, geometryName):
        # type: (str, str) -> bool
        """
        增加玩家渲染几何体
        """
        pass

    def AddPlayerTexture(self, geometryKey, geometryName):
        # type: (str, str) -> bool
        """
        增加玩家渲染贴图
        """
        pass

    def AddPlayerAnimation(self, animationKey, animationName):
        # type: (str, str) -> bool
        """
        增加玩家渲染动画
        """
        pass

    def AddPlayerAnimationController(self, animationControllerKey, animationControllerName):
        # type: (str, str) -> bool
        """
        增加玩家渲染动画控制器
        """
        pass

    def RemovePlayerAnimationController(self, animationControllKey):
        # type: (str) -> bool
        """
        移除玩家渲染动画控制器
        """
        pass

    def RebuildPlayerRender(self):
        # type: () -> bool
        """
        重建玩家的数据渲染器
        """
        pass

    def AddActorRenderMaterial(self, actorIdentifier, materialKey, materialName):
        # type: (str, str, str) -> bool
        """
        增加生物渲染需要的材质
        """
        pass

    def AddActorRenderController(self, actorIdentifier, renderControllerName, condition=''):
        # type: (str, str, str) -> bool
        """
        增加生物渲染控制器
        """
        pass

    def RemoveActorRenderController(self, actorIdentifier, renderControllerName):
        # type: (str, str) -> bool
        """
        删除生物渲染控制器
        """
        pass

    def RebuildActorRender(self, actorIdentifier):
        # type: (str) -> bool
        """
        重建生物的数据渲染器（该接口不支持玩家，玩家请使用RebuildPlayerRender）
        """
        pass

    def ChangeArmorTextures(self, armorIdentifier, texturesDict, uiIconTexture):
        # type: (str, dict, str) -> bool
        """
        修改盔甲在场景中显示和在UI中显示的贴图
        """
        pass

