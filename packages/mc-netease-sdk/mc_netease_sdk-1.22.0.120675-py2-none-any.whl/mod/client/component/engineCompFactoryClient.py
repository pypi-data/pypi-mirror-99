# -*- coding: utf-8 -*-

from mod.client.component.skyRenderCompClient import SkyRenderCompClient
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.client.component.cameraCompClient import CameraComponentClient
from mod.client.component.itemCompClient import ItemCompClient
from typing import Union
from mod.client.component.attrCompClient import AttrCompClient
from mod.client.component.chunkSourceCompClient import ChunkSourceCompClient
from mod.client.component.particleSkeletonBindComp import ParticleSkeletonBindComp
from mod.client.component.playerViewCompClient import PlayerViewCompClient
from mod.client.component.queryVariableCompClient import QueryVariableComponentClient
from mod.client.component.particleEntityBindComp import ParticleEntityBindComp
from mod.client.component.virtualWorldCompClient import VirtualWorldCompClient
from mod.client.component.engineTypeCompClient import EngineTypeComponentClient
from mod.client.component.frameAniControlComp import FrameAniControlComp
from mod.client.component.actorMotionCompClient import ActorMotionComponentClient
from mod.client.component.frameAniSkeletonBindComp import FrameAniSkeletonBindComp
from mod.client.component.healthCompClient import HealthComponentClient
from mod.client.component.audioCustomCompClient import AudioCustomComponentClient
from mod.client.component.posCompClient import PosComponentClient
from mod.client.component.particleTransComp import ParticleTransComp
from mod.client.component.blockInfoCompClient import BlockInfoComponentClient
from mod.client.component.recipeCompClient import RecipeCompClient
from mod.client.component.blockUseEventWhiteListCompClient import BlockUseEventWhiteListComponentClient
from mod.client.component.modelCompClient import ModelComponentClient
from mod.client.component.nameCompClient import NameComponentClient
from mod.client.component.gameCompClient import GameComponentClient
from mod.client.component.configCompClient import ConfigCompClient
from mod.client.component.playerCompClient import PlayerCompClient
from mod.client.component.fogCompClient import FogCompClient
from mod.client.component.textBoardCompClient import TextBoardComponentClient
from mod.client.component.actorCollidableCompClient import ActorCollidableCompClient
from mod.client.component.auxValueCompClient import AuxValueComponentClient
from mod.client.component.brightnessCompClient import BrightnessCompClient
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.operationCompClient import OperationCompClient
from mod.client.component.textNotifyCompClient import TextNotifyComponet
from mod.client.component.rotCompClient import RotComponentClient
from mod.client.component.audioSystemCompClient import AudioSystemCompClient
from mod.client.component.particleControlComp import ParticleControlComp
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from mod.client.component.playerAnimCompClient import PlayerAnimCompClient

class EngineCompFactoryClient(object):
    def CreateActorCollidable(self, entityId):
        # type: (Union[str,int]) -> ActorCollidableCompClient
        """
        创建actorCollidable组件
        """
        pass

    def CreateActorMotion(self, entityId):
        # type: (Union[str,int]) -> ActorMotionComponentClient
        """
        创建actorMotion组件
        """
        pass

    def CreateActorRender(self, entityId):
        # type: (Union[str,int]) -> ActorRenderCompClient
        """
        创建actorRender组件
        """
        pass

    def CreateAttr(self, entityId):
        # type: (str) -> AttrCompClient
        """
        创建实体属性组件
        """
        pass

    def CreateAuxValue(self, entityId):
        # type: (Union[str,int]) -> AuxValueComponentClient
        """
        创建auxValue组件
        """
        pass

    def CreateBlockInfo(self, entityId):
        # type: (Union[str,int]) -> BlockInfoComponentClient
        """
        创建blockInfo组件
        """
        pass

    def CreateBlockUseEventWhiteList(self, entityId):
        # type: (Union[str,int]) -> BlockUseEventWhiteListComponentClient
        """
        创建blockUseEventWhiteList组件
        """
        pass

    def CreateBrightness(self, entityId):
        # type: (Union[str,int]) -> BrightnessCompClient
        """
        创建brightness组件
        """
        pass

    def CreateCamera(self, entityId):
        # type: (Union[str,int]) -> CameraComponentClient
        """
        创建camera组件
        """
        pass

    def CreateChunkSource(self, entityId):
        # type: (Union[str,int]) -> ChunkSourceCompClient
        """
        创建chunkSource组件
        """
        pass

    def CreateConfigClient(self, levelId):
        # type: (str) -> ConfigCompClient
        """
        创建config组件
        """
        pass

    def CreateCustomAudio(self, entityId):
        # type: (Union[str,int]) -> AudioCustomComponentClient
        """
        创建customAudio组件
        """
        pass

    def CreateEngineType(self, entityId):
        # type: (Union[str,int]) -> EngineTypeComponentClient
        """
        创建engineType组件
        """
        pass

    def CreateFog(self, entityId):
        # type: (Union[str,int]) -> FogCompClient
        """
        创建fog组件
        """
        pass

    def CreateFrameAniControl(self, entityId):
        # type: (Union[str,int]) -> FrameAniControlComp
        """
        创建frameAniControl组件
        """
        pass

    def CreateFrameAniEntityBind(self, entityId):
        # type: (Union[str,int]) -> FrameAniEntityBindComp
        """
        创建frameAniEntityBind组件
        """
        pass

    def CreateFrameAniSkeletonBind(self, entityId):
        # type: (Union[str,int]) -> FrameAniSkeletonBindComp
        """
        创建frameAniSkeletonBind组件
        """
        pass

    def CreateFrameAniTrans(self, entityId):
        # type: (Union[str,int]) -> FrameAniTransComp
        """
        创建frameAniTrans组件
        """
        pass

    def CreateGame(self, entityId):
        # type: (Union[str,int]) -> GameComponentClient
        """
        创建game组件
        """
        pass

    def CreateHealth(self, entityId):
        # type: (Union[str,int]) -> HealthComponentClient
        """
        创建health组件
        """
        pass

    def CreateItem(self, entityId):
        # type: (Union[str,int]) -> ItemCompClient
        """
        创建item组件
        """
        pass

    def CreateModAttr(self, entityId):
        # type: (Union[str,int]) -> ModAttrComponentClient
        """
        创建modAttr组件
        """
        pass

    def CreateModel(self, entityId):
        # type: (Union[str,int]) -> ModelComponentClient
        """
        创建model组件
        """
        pass

    def CreateName(self, entityId):
        # type: (Union[str,int]) -> NameComponentClient
        """
        创建name组件
        """
        pass

    def CreateOperation(self, entityId):
        # type: (Union[str,int]) -> OperationCompClient
        """
        创建operation组件
        """
        pass

    def CreateParticleControl(self, entityId):
        # type: (Union[str,int]) -> ParticleControlComp
        """
        创建particleControl组件
        """
        pass

    def CreateParticleEntityBind(self, entityId):
        # type: (Union[str,int]) -> ParticleEntityBindComp
        """
        创建particleEntityBind组件
        """
        pass

    def CreateParticleSkeletonBind(self, entityId):
        # type: (Union[str,int]) -> ParticleSkeletonBindComp
        """
        创建particleSkeletonBind组件
        """
        pass

    def CreateParticleTrans(self, entityId):
        # type: (Union[str,int]) -> ParticleTransComp
        """
        创建particleTrans组件
        """
        pass

    def CreatePlayer(self, entityId):
        # type: (Union[str,int]) -> PlayerCompClient
        """
        创建player组件
        """
        pass

    def CreatePlayerAnim(self, playerId):
        # type: (str) -> PlayerAnimCompClient
        """
        创建玩家动画组件
        """
        pass

    def CreatePlayerView(self, entityId):
        # type: (Union[str,int]) -> PlayerViewCompClient
        """
        创建playerView组件
        """
        pass

    def CreatePos(self, entityId):
        # type: (Union[str,int]) -> PosComponentClient
        """
        创建pos组件
        """
        pass

    def CreateQueryVariable(self, entityId):
        # type: (Union[str,int]) -> QueryVariableComponentClient
        """
        创建queryVariable组件
        """
        pass

    def CreateRecipe(self, entityId):
        # type: (Union[str,int]) -> RecipeCompClient
        """
        创建recipe组件
        """
        pass

    def CreateRot(self, entityId):
        # type: (Union[str,int]) -> RotComponentClient
        """
        创建rot组件
        """
        pass

    def CreateSkyRender(self, entityId):
        # type: (Union[str,int]) -> SkyRenderCompClient
        """
        创建skyRender组件
        """
        pass

    def CreateSystemAudio(self, entityId):
        # type: (Union[str,int]) -> AudioSystemCompClient
        """
        创建systemAudio组件
        """
        pass

    def CreateTextBoard(self, entityId):
        # type: (Union[str,int]) -> TextBoardComponentClient
        """
        创建textBoard组件
        """
        pass

    def CreateTextNotifyClient(self, entityId):
        # type: (Union[str,int]) -> TextNotifyComponet
        """
        创建textNotifyClient组件
        """
        pass

    def CreateVirtualWorld(self, levelId):
        # type: (str) -> VirtualWorldCompClient
        """
        创建virtualWorld组件实例组件
        """
        pass

