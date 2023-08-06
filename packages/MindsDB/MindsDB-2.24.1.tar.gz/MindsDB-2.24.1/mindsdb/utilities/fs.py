import inspect
import os
from pathlib import Path
import shutil
import pickle


def create_directory(path):
    path = Path(path)
    path.mkdir(mode=0o777, exist_ok=True, parents=True)


def get_paths():
    this_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    mindsdb_path = os.path.abspath(Path(this_file_path).parent.parent)

    tuples = [
        (
            f'{mindsdb_path}/etc/',
            f'{mindsdb_path}/var/'
        )
    ]

    # if windows
    if os.name == 'nt':
        tuples.extend([
            (
                os.path.join(os.environ['APPDATA'], 'mindsdb'),
                os.path.join(os.environ['APPDATA'], 'mindsdb'),
            )
        ])
    else:
        tuples.extend([
            (
                '/etc/mindsdb',
                '/var/lib/mindsdb'
            ),
            (
                '{}/.local/etc/mindsdb'.format(Path.home()),
                '{}/.local/var/lib/mindsdb'.format(Path.home())
            )
        ])

    return tuples


def get_or_create_dir_struct():
    for tup in get_paths():
        try:
            for _dir in tup:
                assert os.path.exists(_dir)
                assert os.access(_dir, os.W_OK) is True

            config_dir = tup[0]

            return config_dir, tup[1]
        except Exception:
            pass

    for tup in get_paths():
        try:
            for _dir in tup:
                create_directory(_dir)
                assert os.access(_dir, os.W_OK) is True

            config_dir = tup[0]

            return config_dir, tup[1]

        except Exception:
            pass

    raise Exception('MindsDB storage directory does not exist and could not be created')


def do_init_migration(paths):
    ''' That initial migration for storage structure. Should be called once after user updates to 2.8.0.
        When we decide all active users has update (after a month?), this function can be removed.
    '''
    # move predictors files by their directories
    endings = [
        '_heavy_model_metadata.pickle',
        '_light_model_metadata.pickle',
        '_lightwood_data'
    ]
    for ending in endings:
        for p in Path(paths['predictors']).iterdir():
            if p.is_file() and p.name.endswith(ending):
                predictor_name = p.name[:-len(ending)]
                predictor_path = Path(paths['predictors']).joinpath(predictor_name)
                create_directory(predictor_path)
                new_file_name = ending[1:]
                shutil.move(
                    str(p),
                    str(predictor_path.joinpath(new_file_name))
                )
                if new_file_name == 'light_model_metadata.pickle':
                    with open(str(predictor_path.joinpath(new_file_name)), 'rb') as fp:
                        lmd = pickle.load(fp)

                    if 'ludwig_data' in lmd and 'ludwig_save_path' in lmd['ludwig_data']:
                        lmd['ludwig_data']['ludwig_save_path'] = os.path.join(paths['predictors'], lmd['name'], 'ludwig_data')

                    if 'lightwood_data' in lmd and 'save_path' in lmd['lightwood_data']:
                        lmd['lightwood_data']['save_path'] = os.path.join(paths['predictors'], lmd['name'], 'lightwood_data')

                    with open(os.path.join(paths['predictors'], lmd['name'], 'light_model_metadata.pickle'), 'wb') as fp:
                        pickle.dump(lmd, fp, protocol=pickle.HIGHEST_PROTOCOL)

    for p in Path(paths['predictors']).iterdir():
        if p.is_file() and p.name != 'start.mdb_base':
            p.unlink()

    # mopve each datasource files from ds_name/datasource/{file} to ds_name/{file}
    for p in Path(paths['datasources']).iterdir():
        if p.is_dir():
            datasource_folder = p.joinpath('datasource')
            if datasource_folder.is_dir():
                for f in datasource_folder.iterdir():
                    shutil.move(
                        str(f),
                        str(p.joinpath(f.name))
                    )
                shutil.rmtree(datasource_folder)


def create_dirs_recursive(path):
    if isinstance(path, dict):
        for p in path.values():
            create_dirs_recursive(p)
    elif isinstance(path, str):
        create_directory(path)
    else:
        raise ValueError(f'Wrong path: {path}')
