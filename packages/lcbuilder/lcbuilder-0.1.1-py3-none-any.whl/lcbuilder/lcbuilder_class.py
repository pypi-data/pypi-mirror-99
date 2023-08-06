from lcbuilder.objectinfo.InputObjectInfo import InputObjectInfo
from lcbuilder.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo
from lcbuilder.objectinfo.ObjectInfo import ObjectInfo
from lcbuilder.objectinfo.preparer.MissionFfiLightcurveBuilder import MissionFfiLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionInputLightcurveBuilder import MissionInputLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionLightcurveBuilder import MissionLightcurveBuilder


class LcBuilder:
    def __init__(self) -> None:
        self.lightcurve_builders = {InputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionInputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionObjectInfo: MissionLightcurveBuilder(),
                                    MissionFfiIdObjectInfo: MissionFfiLightcurveBuilder(),
                                    MissionFfiCoordsObjectInfo: MissionFfiLightcurveBuilder()}

    def build(self, object_info: ObjectInfo, object_dir: str):
        return self.lightcurve_builders[type(object_info)].build(object_info, object_dir)
