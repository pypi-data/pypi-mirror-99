import time
import json
import requests

from litebo.utils.config_space import json as config_json
from litebo.utils.config_space import Configuration
from litebo.utils.constants import SUCCESS


class RemoteAdvisor(object):
    def __init__(self, config_space,
                 server_ip, port,
                 task_id='remote_bo',
                 num_constraints=0,
                 num_objs=1,
                 sample_strategy: str = 'bo',
                 advisor_type='default',
                 surrogate_type=None,
                 acq_type=None,
                 acq_optimizer_type='local_random',
                 max_runs=200,
                 init_strategy='random_explore_first',
                 initial_configurations=None,
                 initial_runs=3,
                 random_state=1):

        # Assign task id
        self.task_id = time.time() if task_id is None else task_id

        # Store and serialize config space
        self.config_space = config_space
        config_space_json = config_json.write(config_space)

        # Check setup
        self.num_objs = num_objs
        self.num_constraints = num_constraints
        self.acq_type = acq_type
        self.constraint_surrogate_type = None
        self.surrogate_type = surrogate_type
        self.check_setup()

        # Set options
        if initial_configurations is not None and isinstance(initial_configurations[0], Configuration):
            initial_configurations = [config.get_dictionary() for config in initial_configurations]
        self.max_iterations = max_runs
        options = {
            'optimization_strategy': sample_strategy,
            'surrogate_type': surrogate_type,
            'acq_type': acq_type,
            'acq_optimizer_type': acq_optimizer_type,
            'init_strategy': init_strategy,
            'initial_configurations': initial_configurations,
            'initial_trials': initial_runs,
            'random_state': random_state
        }

        # Construct base url.
        self.base_url = 'http://%s:%d/bo_advice/' % (server_ip, port)

        # Register task
        requests.post(self.base_url + 'task_register/',
                      data={'task_id': self.task_id, 'config_space_json': config_space_json,
                            'num_constraints': num_constraints, 'num_objs': num_objs,
                            'options': json.dumps(options)})

    def check_setup(self):
        """
        Check num_objs, num_constraints, acq_type, surrogate_type.
        """
        assert isinstance(self.num_objs, int) and self.num_objs >= 1
        assert isinstance(self.num_constraints, int) and self.num_constraints >= 0

        # single objective no constraint
        if self.num_objs == 1 and self.num_constraints == 0:
            if self.acq_type is None:
                self.acq_type = 'ei'
            assert self.acq_type in ['ei', 'eips', 'logei', 'pi', 'lcb', 'lpei', ]
            if self.surrogate_type is None:
                self.surrogate_type = 'prf'

        # multi-objective with constraints
        elif self.num_objs > 1 and self.num_constraints > 0:
            if self.acq_type is None:
                self.acq_type = 'mesmoc2'
            assert self.acq_type in ['mesmoc', 'mesmoc2']
            if self.surrogate_type is None:
                self.surrogate_type = 'gp_rbf'
            if self.constraint_surrogate_type is None:
                if self.acq_type == 'mesmoc2':
                    self.constraint_surrogate_type = 'gp'
                else:
                    self.constraint_surrogate_type = 'gp_rbf'
            if self.acq_type == 'mesmoc' and self.surrogate_type != 'gp_rbf':
                self.surrogate_type = 'gp_rbf'
                self.logger.warning('Surrogate model has changed to Gaussian Process with RBF kernel '
                                    'since MESMOC is used. Surrogate_type should be set to \'gp_rbf\'.')
            if self.acq_type == 'mesmoc' and self.constraint_surrogate_type != 'gp_rbf':
                self.surrogate_type = 'gp_rbf'
                self.logger.warning('Constraint surrogate model has changed to Gaussian Process with RBF kernel '
                                    'since MESMOC is used. Surrogate_type should be set to \'gp_rbf\'.')

        # multi-objective no constraint
        elif self.num_objs > 1:
            if self.acq_type is None:
                self.acq_type = 'mesmo'
            assert self.acq_type in ['mesmo', 'usemo']
            if self.surrogate_type is None:
                if self.acq_type == 'mesmo':
                    self.surrogate_type = 'gp_rbf'
                else:
                    self.surrogate_type = 'gp'
            if self.acq_type == 'mesmo' and self.surrogate_type != 'gp_rbf':
                self.surrogate_type = 'gp_rbf'
                self.logger.warning('Surrogate model has changed to Gaussian Process with RBF kernel '
                                    'since MESMO is used. Surrogate_type should be set to \'gp_rbf\'.')

        # single objective with constraints
        elif self.num_constraints > 0:
            if self.acq_type is None:
                self.acq_type = 'eic'
            assert self.acq_type in ['eic', 'ts']
            if self.surrogate_type is None:
                if self.acq_type == 'ts':
                    self.surrogate_type = 'gp'
                else:
                    self.surrogate_type = 'prf'
            if self.constraint_surrogate_type is None:
                self.constraint_surrogate_type = 'gp'
            if self.acq_type == 'ts' and self.surrogate_type != 'gp':
                self.surrogate_type = 'gp'
                self.logger.warning('Surrogate model has changed to Gaussian Process '
                                    'since TS is used. Surrogate_type should be set to \'gp\'.')

    def get_suggestion(self):
        res = requests.post(self.base_url + 'get_suggestion/',
                            data={'task_id': self.task_id})
        if res.status_code != 200:
            print('Get suggestion failed.')
            raise Exception('Server error %d' % res.status_code)
        else:
            config_dict = res.json()
            return config_dict

    def update_observation(self, config_dict, objs, constraints=[], trial_state=SUCCESS):
        res = requests.post(self.base_url + 'update_observation/',
                            data={'task_id': self.task_id, 'config': json.dumps(config_dict),
                                  'objs': json.dumps(objs), 'constraints': json.dumps(constraints),
                                  'trial_state': trial_state})
        if res.status_code != 200:
            print('Update observation failed.')
            raise Exception('Server error %s' % res.status_code)

    def get_result(self):
        res = requests.post(self.base_url + 'get_result/', data={'task_id': self.task_id})
        res_dict = res.json()
        result = json.loads(res_dict.get('result'))
        history = json.loads(res_dict.get('history'))
        return result, history
