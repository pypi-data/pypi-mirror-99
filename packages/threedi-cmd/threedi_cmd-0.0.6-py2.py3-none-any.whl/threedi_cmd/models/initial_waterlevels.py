from typing import Dict
from openapi_client import SimulationsApi
from openapi_client import ThreedimodelsApi
from openapi_client.models import (
    OneDWaterLevel,
    TwoDWaterLevel,
    GroundWaterLevel,
    OneDWaterLevelPredefined,
    TwoDWaterRaster,
    GroundWaterRaster,
)
from .base import InitialWrapper


class OneDWaterLevelWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = OneDWaterLevel
    base_path = "simulations_initial"
    api_path = "1d_water_level_constant"
    scenario_name = "1dwaterlevelconstant"


class OneDWaterLevelPredefinedWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = OneDWaterLevelPredefined
    base_path = "simulations_initial"
    api_path = "1d_water_level_predefined"
    scenario_name = "1dwaterlevelpredefined"


class TwoDWaterLevelWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = TwoDWaterLevel
    base_path = "simulations_initial"
    api_path = "2d_water_level_constant"
    scenario_name = "2dwaterlevelconstant"


class TwoDWaterLevelRasterError(Exception):
    pass


class TwoDWaterLevelRasterWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = TwoDWaterRaster
    base_path = "simulations_initial"
    api_path = "2d_water_level_raster"
    scenario_name = "2dwaterlevelraster"
    lookup: str = None

    # initial_waterlevel__source_raster__type
    def initialize_instance(self, data: Dict):
        self.lookup = data.pop("initial_waterlevel__source_raster__type", None)
        if self.lookup is None and "initial_waterlevel" not in data:
            raise TwoDWaterLevelRasterError(
                f"Please proved either "
                f"`initial_waterlevel__source_raster__type` "
                f"or `initial_waterlevel`"
                f"for the TwoDWaterLevelRaster: {data}"
            )

        if self.lookup is not None:
            # Try to lookup/find the raster.
            api = ThreedimodelsApi(self._api_client)
            res = api.threedimodels_rasters_list(
                self.simulation.threedimodel, type=self.lookup
            )
            if res.count != 1:
                raise TwoDWaterLevelRasterError(
                    f"Could not find "
                    f"initial_waterlevel__source_raster__type, raster_list "
                    f"response whas {res}"
                )

            raster = res.results[0]

            # Now find the initial waterlevel related to this
            # raster
            res = api.threedimodels_initial_waterlevels_list(
                self.simulation.threedimodel
            )

            # Search through initial waterlevel options
            # for the correct one
            found = [
                x
                for x in res.results
                if int(x.source_raster_id) == int(raster.id)
            ]

            if len(found) != 1:
                raise TwoDWaterLevelRasterError(
                    f"Could not find "
                    f"initial_waterlevel__source_raster__type, "
                    f"initial_waterlevels list"
                    f"response was {res}"
                )

            # Set initial_waterlevel
            data["initial_waterlevel"] = res.results[0].id

        super().initialize_instance(data)


class GroundWaterLevelWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = GroundWaterLevel
    base_path = "simulations_initial"
    api_path = "groundwater_level_constant"
    scenario_name = "groundwaterlevelconstant"


class GroundWaterLevelRasterWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = GroundWaterRaster
    base_path = "simulations_initial"
    api_path = "groundwater_level_raster"
    scenario_name = "groundwaterlevelraster"


WRAPPERS = [
    OneDWaterLevelWrapper,
    OneDWaterLevelPredefinedWrapper,
    TwoDWaterLevelWrapper,
    TwoDWaterLevelRasterWrapper,
    GroundWaterLevelWrapper,
    GroundWaterLevelRasterWrapper,
]
