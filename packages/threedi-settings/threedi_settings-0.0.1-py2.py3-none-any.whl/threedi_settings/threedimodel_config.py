# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from pathlib import Path
import logging
from configparser import ConfigParser
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class ThreedimodelIni:
    """
    Physical schema that describes how the model data is
    represented and stored
    """

    def __init__(self, config_file: Path):
        """
        :param config_file: configuration ini file
        """
        self.config_file = config_file
        assert (
            self.config_file.exists() and not self.config_file.is_dir()
        ), f"{self.config_file} does not exist or is a dir"

        self.config = ConfigParser()
        with open(self.config_file, "r") as ini_file:
            self.config.read_file(ini_file)

    @property
    def model_root(self) -> Path:
        return self.config_file.parent

    def as_dict(self, flat: bool = True) -> Dict:
        d = {}
        sections = self.config.sections()

        for section in sections:
            options = self.config.options(section)
            temp_dict = {}
            for option in options:
                if not flat:
                    temp_dict[option] = self.config.get(section, option)
                    d[section] = temp_dict
                    continue
                d[option] = self.config.get(section, option)
        return d


class AggregationIni(ThreedimodelIni):
    """
    Physical schema that describes how the model data is
    represented and stored
    """

    def __init__(self, config_file: Path):
        """
        :param config_file: configuration ini file
        """
        super().__init__(config_file=config_file)
        self.aggregation = ConfigParser()
        if self.aggregation_ini:
            with open(self.aggregation_ini, "r") as aggr_file:
                self.aggregation.read_file(aggr_file)

    @property
    def aggregation_ini(self) -> Optional[Path]:
        if not self.config["output"]["aggregation_settings"]:
            return
        return self.model_root / self.config["output"]["aggregation_settings"]

    @property
    def model_root(self) -> Path:
        return self.config_file.parent

    def as_dict(self) -> Dict:
        sections_dict = {}

        # get sections and iterate over each
        sections = self.aggregation.sections()

        for section in sections:
            options = self.aggregation.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = self.aggregation.get(section, option)

            sections_dict[section] = temp_dict

        return sections_dict
