# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from collections import defaultdict
from configparser import ConfigParser
import functools
from pathlib import Path
import logging
from typing import Dict, List, Optional

try:
    from openapi_client.models import GeneralSettings
    from openapi_client.models import TimeStepSettings
    from openapi_client.models import NumericalSettings
    from openapi_client.models import AggregationSettings
    from openapi_client import SimulationsApi
    from openapi_client import ApiException
    from threedi_api_client import ThreediApiClient
    from openapi_client.models import SimulationSettingsOverview
except ImportError:
    msg = "You need to install the extra 'api' (e.g. 'pip install threedi-settings[api]') to be able to use the threedi-settings http module"  # noqa
    raise ImportError(msg)

from threedi_settings.mappings import (
    general_settings_map,
    time_step_settings_map,
    numerical_settings_map,
    aggregation_settings_map,
)
from threedi_settings.models import NumericalConfig, TimeStepConfig, GeneralSimulationConfig, AggregationConfig, SimulationConfig
from threedi_settings.threedimodel_config import ThreedimodelIni

logger = logging.getLogger(__name__)
import os


api_config = {
    "API_HOST": os.environ.get("API_HOST"),
    "API_USERNAME": os.environ.get("API_USERNAME"),
    "API_PASSWORD": os.environ.get("API_PASSWORD")
}


class OpenApiSimulationClient:
    def __init__(
        self, simulation_id: int
    ):
        self.simulation_id = simulation_id
        _api_client = ThreediApiClient(config=api_config)
        self.api_client = SimulationsApi(_api_client)


class BaseOpenAPI(ABC, OpenApiSimulationClient):
    def __init__(
        self, simulation_id: int, config_dict, openapi_model, mapping
    ):
        super().__init__(simulation_id)
        self.config_dict = config_dict
        self.model = openapi_model
        self.mapping = mapping

    @functools.cached_property
    def instance(self):
        data = {}
        exclude = {
            "url", "id",
        }
        for name in self.model.openapi_types.keys():
            if name.lower() in exclude:
                continue
            if name == "simulation_id":
                data[name] = self.simulation_id
                continue
            old_field_info, new_field_info = self.mapping[name]
            ini_value = self.config_dict[old_field_info.name]
            try:
                ini_value = old_field_info.type(ini_value)
                if new_field_info.type != old_field_info.type:
                    try:
                        ini_value = new_field_info.type(ini_value)
                    except Exception:
                        raise
            except ValueError as err:
                logger.warning(f"{err} --> {ini_value} --> {old_field_info}")
                ini_value = new_field_info.default
            data[name] = ini_value
        return self.model(**data)

    @property
    @abstractmethod
    def create_method_name(self) -> str:
        ...

    def create(self):
        try:
            create = getattr(self.api_client, self.create_method_name)
        except AttributeError:
            raise AttributeError(
                f"Create method '{self.create_method_name}' unknown"
            )
        try:
            resp = create(self.simulation_id, self.instance)
        except ApiException as err:
            logger.error(
                "Could not create resource %s. Server response: %s",
                self.model.__name__,
                err,
            )
            return
        logger.info(
            "Successfully created resource %s. Server response: %s ",
            self.model.__name__,
            resp,
        )
        return resp


class OpenAPIGeneralSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config):
        super().__init__(
            simulation_id, config, GeneralSettings, general_settings_map
        )

    @property
    def create_method_name(self):
        return "simulations_settings_general_create"


class OpenAPITimeStepSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config):
        super().__init__(
            simulation_id, config, TimeStepSettings, time_step_settings_map
        )

    @property
    def create_method_name(self):
        return "simulations_settings_time_step_create"


class OpenAPINumericalSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config):
        super().__init__(
            simulation_id, config, NumericalSettings, numerical_settings_map
        )

    @property
    def create_method_name(self):
        return "simulations_settings_numerical_create"


class OpenAPIAggregationSettings(OpenApiSimulationClient):
    def __init__(self, simulation_id: int, config: Dict):
        super().__init__(simulation_id)
        self.config_dict = config
        self.model = AggregationSettings
        self.mapping = aggregation_settings_map

    @property
    def create_method_name(self):
        return "simulations_settings_aggregation_create"

    @functools.cached_property
    def instances(self) -> List:
        _instances = []
        data = defaultdict(str)
        exclude = {
            "url",
            "name",
        }
        for k, d in self.config_dict.items():
            for name in self.model.openapi_types.keys():
                if name.lower() in exclude:
                    continue
                if name == "simulation_id":
                    data[name] = self.simulation_id
                    continue
                old_field_info, new_field_info = self.mapping[name]
                ini_value = d[old_field_info.name]
                try:
                    ini_value = old_field_info.type(ini_value)
                    if new_field_info.type != old_field_info.type:
                        try:
                            ini_value = new_field_info.type(ini_value)
                        except Exception:
                            raise
                except ValueError as err:
                    logger.warning(f"{err} --> {ini_value} --> {old_field_info}")
                    ini_value = new_field_info.default
                data[name] = ini_value
            _instances.append(self.model(**data))
        return _instances

    def create(self):
        try:
            create = getattr(self.api_client, self.create_method_name)
        except AttributeError:
            raise AttributeError(
                f"Create method '{self.create_method_name}' unknown"
            )
        responses = []
        for instance in self.instances:
            try:
                resp = create(self.simulation_id, instance)
            except ApiException as err:
                logger.error(
                    "Could not create resource %s. Server response: %s",
                    self.model.__name__,
                    err,
                )
                continue
            logger.info(
                "Successfully created resource %s. Server response: %s ",
                self.model.__name__,
                resp,
            )
            responses.append(resp)
        return responses


class OpenAPISimulationSettings(OpenApiSimulationClient):

    def __init__(self, simulation_id):
        super().__init__(simulation_id)
        self._simulation_config = None

    def retrieve(self) -> SimulationSettingsOverview:
        try:
            return self.api_client.simulations_settings_overview(self.simulation_id)
        except ApiException as err:
            logger.error("Could not retrieve settings information for simulation %s", self.simulation_id)
            return

    @property
    def simulation_config(self):
        if self._simulation_config:
            return self._simulation_config

        resp = self.retrieve()
        if not resp:
            return

        attr_names = [
            "general_settings", "time_step_settings", "numerical_settings"
        ]
        d = {}
        uid = ""
        sim_uid = ""
        for name in attr_names:
            tmp_d = getattr(resp, name).to_dict()
            uid = str(tmp_d.pop("id"))
            sim_uid = str(tmp_d.pop("simulation_id"))
            d[name] = tmp_d

        general_settings = GeneralSimulationConfig(
            uid=uid, sim_uid=sim_uid, **d["general_settings"]
        )
        time_step_settings = TimeStepConfig(
            uid=uid, sim_uid=sim_uid, **d["time_step_settings"]

        )
        numerical_settings = NumericalConfig(
            uid=uid, sim_uid=sim_uid, **d["numerical_settings"]
        )
        self._simulation_config = SimulationConfig(
            uid=uid, sim_uid=sim_uid,
            general_config=general_settings,
            time_step_config=time_step_settings,
            numerical_config=numerical_settings
        )
        return self._simulation_config


class OpenAPISimulationSettingsWriter(OpenAPISimulationSettings):

    def __init__(
        self,
        simulation_id: int,
        ini_file_path: Path,
        aggregation_file_path: Path,
        legacy_ini_file_path: Optional[Path]
    ):
        super().__init__(simulation_id)
        self.aggr_config = ConfigParser()
        self.ini_output_file = ini_file_path
        self.aggregation_file_path = aggregation_file_path
        self.legacy_conf = None
        if legacy_ini_file_path:
            legacy_ini = ThreedimodelIni(legacy_ini_file_path)
            self.config = legacy_ini.config
        else:
            self.config = ConfigParser()

    @functools.cached_property
    def settings(self):
        resp = self.retrieve()
        if not resp:
            return
        return resp

    def to_ini(self):
        if not self.settings:
            logger.error("Cannot create ini file, could not fetch data from API")
            return
        self._add(general_settings_map, self.settings.general_settings)
        self._add(time_step_settings_map, self.settings.time_step_settings)
        self._add(numerical_settings_map, self.settings.numerical_settings)
        with self.ini_output_file.open("w") as configfile:
            self.config.write(configfile)
        if not self.settings.aggregation_settings:
            logger.debug("No aggregation settings defined for simulation %s ", self.simulation_id)
            return
        self._add_aggregations()
        with self.aggregation_file_path.open("w") as aggregation_file:
            self.aggr_config.write(aggregation_file)

    def _add(self, settings_map: Dict, sub_setting):
        for attr_name, mapping in settings_map.items():
            value = getattr(sub_setting, attr_name)
            old_field_info, _ = mapping
            if old_field_info.ini_section not in self.config:
                self.config[old_field_info.ini_section] = {}
            self.config[old_field_info.ini_section][old_field_info.name] = f"{value}"

    def _add_aggregations(self):
        for i, entry in enumerate(self.settings.aggregation_settings, start=1):
            for attr_name, mapping in aggregation_settings_map.items():
                value = getattr(entry, attr_name)
                old_field_info, _ = mapping
                if str(i) not in self.aggr_config:
                    self.aggr_config[str(i)] = {}
                self.aggr_config[str(i)][old_field_info.name] = f"{value}"
