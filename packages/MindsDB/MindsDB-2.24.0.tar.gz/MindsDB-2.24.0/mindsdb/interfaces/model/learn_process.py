import os
import torch.multiprocessing as mp

from mindsdb.__about__ import __version__ as mindsdb_version
from mindsdb.interfaces.database.database import DatabaseWrapper
from mindsdb.utilities.os_specific import get_mp_context
from mindsdb.interfaces.storage.db import session, Predictor
from mindsdb.interfaces.storage.fs import FsSotre
from mindsdb.utilities.config import Config


ctx = mp.get_context('spawn')


def run_learn(name, from_data, to_predict, kwargs, datasource_id):
    import mindsdb_native
    import mindsdb_datasources
    import mindsdb

    config = Config()
    fs_store = FsSotre()

    company_id = os.environ.get('MINDSDB_COMPANY_ID', None)

    mdb = mindsdb_native.Predictor(name=name, run_env={'trigger': 'mindsdb'})

    predictor_record = Predictor.query.filter_by(company_id=company_id, name=name).first()
    predictor_record.datasource_id = datasource_id
    predictor_record.to_predict = to_predict
    predictor_record.native_version = mindsdb_native.__version__
    predictor_record.mindsdb_version = mindsdb_version
    predictor_record.learn_args = {
        'to_predict': to_predict,
        'kwargs': kwargs
    }
    predictor_record.data = {
        'name': name,
        'status': 'training'
    }
    session.commit()

    to_predict = to_predict if isinstance(to_predict, list) else [to_predict]
    data_source = getattr(mindsdb_datasources, from_data['class'])(*from_data['args'], **from_data['kwargs'])

    try:
        mdb.learn(
            from_data=data_source,
            to_predict=to_predict,
            **kwargs
        )
    except Exception:
        pass

    fs_store.put(name, f'predictor_{company_id}_{predictor_record.id}', config['paths']['predictors'])

    model_data = mindsdb_native.F.get_model_data(name)

    predictor_record = Predictor.query.filter_by(company_id=company_id, name=name).first()
    predictor_record.data = model_data
    session.commit()

    DatabaseWrapper().register_predictors([model_data])

class LearnProcess(ctx.Process):
    daemon = True

    def __init__(self, *args):
        super(LearnProcess, self).__init__(args=args)

    def run(self):
        '''
        running at subprocess due to
        ValueError: signal only works in main thread

        this is work for celery worker here?
        '''
        import setproctitle

        try:
            setproctitle.setproctitle('mindsdb_native_process')
        except Exception:
            pass

        name, from_data, to_predict, kwargs, datasource_id = self._args
        run_learn(name, from_data, to_predict, kwargs, datasource_id)
