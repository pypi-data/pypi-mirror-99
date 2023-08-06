import logging
from typing import Optional, Dict
from configparser import ConfigParser
from pathlib import Path

from threedi_settings.mappings import (
    general_settings_map,
    time_step_settings_map,
    numerical_settings_map,
    aggregation_settings_map,
)
from threedi_settings.models import SimulationConfig
from threedi_settings.threedimodel_config import ThreedimodelIni

logger = logging.getLogger(__name__)


class SimulationConfigWriter:

    def __init__(
        self,
        simulation_config: SimulationConfig,
        ini_file_path: Path,
        aggregation_file_path: Path,
        legacy_ini_file_path: Optional[Path]
    ):
        self.simulation_config = simulation_config
        self.aggr_config = ConfigParser()
        self.ini_output_file = ini_file_path
        self.aggregation_file_path = aggregation_file_path
        self.legacy_conf = None
        if legacy_ini_file_path:
            legacy_ini = ThreedimodelIni(legacy_ini_file_path)
            self.config = legacy_ini.config
        else:
            self.config = ConfigParser()

    def to_ini(self):
        self._add(general_settings_map, self.simulation_config.general_config)
        self._add(time_step_settings_map, self.simulation_config.time_step_config)
        self._add(numerical_settings_map, self.simulation_config.numerical_config)
        with self.ini_output_file.open("w") as configfile:
            self.config.write(configfile)
        if not self.simulation_config.aggregation_config:
            logger.debug("No aggregation settings defined for simulation %s ",
                         self.simulation_config.sim_uid)
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
        for i, entry in enumerate(
            self.simulation_config.aggregation_config, start=1
        ):
            for attr_name, mapping in aggregation_settings_map.items():
                value = getattr(entry, attr_name)
                old_field_info, _ = mapping
                if str(i) not in self.aggr_config:
                    self.aggr_config[str(i)] = {}
                self.aggr_config[str(i)][old_field_info.name] = f"{value}"
