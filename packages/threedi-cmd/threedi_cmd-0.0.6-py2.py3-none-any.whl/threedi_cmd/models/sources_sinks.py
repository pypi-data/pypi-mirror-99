from pathlib import Path
from .base import EventWrapper
from typing import Dict
from openapi_client import SimulationsApi
from openapi_client.models import (
    ConstantSourcesSinks,
    TimeseriesSourcesSinks,
    LizardRasterSourcesSinks,
    LizardTimeseriesSourcesSinks,
    Upload,
    FileTimeseriesSourcesSinks,
    FileRasterSourcesSinks,
    NetCDFRasterSourcesSinks,
    NetCDFTimeseriesSourcesSinks,
)

from threedi_cmd.models.waitfor import WaitForProcessedFileWrapper


class ConstantSourcesSinksWrapper(EventWrapper):
    api_class = SimulationsApi
    model = ConstantSourcesSinks
    api_path: str = "sources_sinks_constant"
    scenario_name = "constantsourcessinks"


class SourcesSinksTimeseriesWrapper(EventWrapper):
    api_class = SimulationsApi
    model = TimeseriesSourcesSinks
    api_path: str = "sources_sinks_timeseries"
    scenario_name = "timeseriessourcessinks"


class SourcesSinksRasterLizardWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LizardRasterSourcesSinks
    api_path: str = "sources_sinks_rasters_lizard"
    scenario_name = "sourcessinksrasterlizard"


class SourcesSinksTimeseriesLizardWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LizardTimeseriesSourcesSinks
    api_path: str = "sources_sinks_timeseries_lizard"
    scenario_name = "sourcessinkstimeserieslizard"


class WaitForSourcesSinksTimeseriesFileWrapper(WaitForProcessedFileWrapper):
    api_class = SimulationsApi
    model = FileTimeseriesSourcesSinks
    scenario_name = "waitforsourcessinkstimeseriesfile"


class WaitForSourcesSinksTimeseriesNetCDFWrapper(
    WaitForSourcesSinksTimeseriesFileWrapper
):
    model = NetCDFTimeseriesSourcesSinks
    websocket_model_name = "NetCDFTimeseriesSourcesSinks"
    scenario_name = "waitforsourcessinkstimeseriesnetcdf"


class SourcesSinksTimeseriesNetCDFWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Upload
    api_path: str = "sources_sinks_timeseries_netcdf"
    scenario_name = "sourcessinkstimeseriesnetcdf"
    filepath: Path = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 10,
        }
        wait_for_validation = WaitForSourcesSinksTimeseriesNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


class WaitForSourcesSinksRasterFileWrapper(WaitForProcessedFileWrapper):
    api_class = SimulationsApi
    model = FileRasterSourcesSinks
    scenario_name = "waitforsourcessinksrasterfile"


class WaitForSourcesSinksRasterNetCDFWrapper(
    WaitForSourcesSinksRasterFileWrapper
):
    model = NetCDFRasterSourcesSinks
    websocket_model_name = "NetCDFRasterSourcesSinks"
    scenario_name = "waitforsourcessinksrasternetcdf"


class SourcesSinksRasterNetCDFWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Upload
    api_path: str = "sources_sinks_rasters_netcdf"
    scenario_name = "sourcessinksrasternetcdf"
    filepath = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 10,
        }
        wait_for_validation = WaitForSourcesSinksRasterNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


WRAPPERS = [
    ConstantSourcesSinksWrapper,
    SourcesSinksTimeseriesWrapper,
    SourcesSinksRasterLizardWrapper,
    SourcesSinksTimeseriesLizardWrapper,
    SourcesSinksTimeseriesNetCDFWrapper,
    WaitForSourcesSinksTimeseriesNetCDFWrapper,
    SourcesSinksRasterNetCDFWrapper,
    WaitForSourcesSinksTimeseriesNetCDFWrapper,
]
