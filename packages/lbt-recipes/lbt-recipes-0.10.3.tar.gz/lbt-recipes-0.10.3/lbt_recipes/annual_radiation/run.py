import sys
import luigi
import os
import time
from multiprocessing import freeze_support
from queenbee_local import local_scheduler, _copy_artifacts, update_params, parse_input_args

import flow.main as annual_radiation_workerbee


_recipe_default_inputs = {   'model': None,
    'north': 0.0,
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'sensor_count': 200,
    'sensor_grid': '*',
    'wea': None}


class LetAnnualRadiationFly(luigi.WrapperTask):
    # global parameters
    _input_params = luigi.DictParameter()

    def requires(self):
        yield [annual_radiation_workerbee._Main_9da8e0c2Orchestrator(_input_params=self._input_params)]


def start(project_folder, user_values, workers):
    freeze_support()

    input_params = update_params(_recipe_default_inputs, user_values)

    if 'simulation_folder' not in input_params or not input_params['simulation_folder']:
        if 'simulation_id' not in input_params or not input_params['simulation_id']:
            simulation_id = 'annual_radiation_%d' % int(round(time.time(), 2) * 100)
        else:
            simulation_id = input_params['simulation_id']

        simulation_folder = os.path.join(project_folder, simulation_id)
        input_params['simulation_folder'] = simulation_folder
    else:
        simulation_folder = input_params['simulation_folder']

    # copy project folder content to simulation folder
    artifacts = ['model', 'wea']
    optional_artifacts = []
    for artifact in artifacts:
        value = input_params[artifact]
        if value is None:
            if artifact in optional_artifacts:
                continue
            raise ValueError('None value for required artifact input: %s' % artifact)
        from_ = os.path.join(project_folder, input_params[artifact])
        to_ = os.path.join(simulation_folder, input_params[artifact])
        _copy_artifacts(from_, to_)

    luigi.build(
        [LetAnnualRadiationFly(_input_params=input_params)],
        local_scheduler=local_scheduler(),
        workers=workers
    )


if __name__ == '__main__':
    project_folder, user_values, workers = parse_input_args(sys.argv)
    start(project_folder, user_values, workers)
