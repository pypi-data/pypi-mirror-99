from pathlib import Path
import logging

import typer

from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.threedimodel_config import AggregationIni
from threedi_settings.api_models import OpenAPINumericalSettings
from threedi_settings.api_models import OpenAPITimeStepSettings
from threedi_settings.api_models import OpenAPIGeneralSettings
from threedi_settings.api_models import OpenAPIAggregationSettings
from threedi_settings.api_models import OpenAPISimulationSettings

logger = logging.getLogger(__name__)


settings_app = typer.Typer()


@settings_app.command()
def import_settings(
    simulation_id: int,
    ini_file: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        writable=False,
        resolve_path=True,
        help="Legacy model settings ini file.",
    ),
):
    """
    "Create API V3 settings resources from legacy model ini file"
    """
    model_ini = ThreedimodelIni(ini_file)
    aggr_ini = AggregationIni(ini_file)
    OpenAPINumericalSettings(simulation_id, model_ini.as_dict()).create()
    OpenAPITimeStepSettings(simulation_id, model_ini.as_dict()).create()
    OpenAPIGeneralSettings(simulation_id, model_ini.as_dict()).create()
    OpenAPIAggregationSettings(simulation_id, aggr_ini.as_dict()).create()
    sim_settings = OpenAPISimulationSettings(simulation_id)
    resp = sim_settings.retrieve()
    print(resp)


if __name__ == "__main__":
    settings_app()
