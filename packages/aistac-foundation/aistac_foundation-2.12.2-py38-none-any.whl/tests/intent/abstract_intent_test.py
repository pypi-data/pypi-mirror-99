import unittest
import os
import shutil

from aistac.handlers.abstract_handlers import ConnectorContract
from aistac.intent.python_cleaners_intent import PythonCleanersIntentModel
from aistac.properties.abstract_properties import AbstractPropertyManager
from aistac.properties.property_manager import PropertyManager


class ControlPropertyManager(AbstractPropertyManager):

    def __init__(self, task_name: str, username: str=None):
        # set additional keys
        root_keys = []
        knowledge_keys = []
        username = username if isinstance(username, str) else 'default'
        super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys, username=username)

    @classmethod
    def manager_name(cls) -> str:
        return str(cls.__name__).lower().replace('propertymanager', '')


class IntentModelTest(unittest.TestCase):

    def setUp(self):
        self.connector = ConnectorContract(uri='contracts/config_contract.pkl?sep=.&encoding=Latin1',
                                           module_name='aistac.handlers.python_handlers',
                                           handler='PythonPersistHandler')
        try:
            os.makedirs('contracts')
        except:
            pass
        PropertyManager._remove_all()
        self.pm = ControlPropertyManager('test_abstract_properties')
        self.pm.set_property_connector(self.connector)

    def tearDown(self):
        try:
            shutil.rmtree('contracts')
        except:
            pass

    def test_runs(self):
        """Basic smoke test"""
        PythonCleanersIntentModel(property_manager=self.pm)

    def test_run_intent_pipeline(self):
        model = PythonCleanersIntentModel(property_manager=self.pm)
        canonical = {'A': [1,4,7], 'B': [4,5,9]}
        result = model.run_intent_pipeline(canonical=canonical, inplace=False)
        self.assertDictEqual(canonical, result)
        model.to_remove(data=canonical, headers=['B'], inplace=True)
        model.auto_clean_header(data=canonical, case='lower', inplace=True)
        result = model.run_intent_pipeline(canonical=canonical, inplace=False)
        self.assertDictEqual({'a': [1, 4, 7]}, result)

    def test_run_intent_pipeline_levels(self):
        model = PythonCleanersIntentModel(property_manager=self.pm)
        data = {'A': [1,4,7], 'B': [4,5,9]}
        model.to_remove(data=data, headers=['B'], inplace=False, intent_level=0)
        model.auto_clean_header(data=data, case='lower', inplace=False, intent_level=1)
        result = model.run_intent_pipeline(canonical=data, inplace=False, intent_levels=0)
        self.assertDictEqual({'A': [1, 4, 7]}, result)
        result = model.run_intent_pipeline(canonical=data, inplace=False, intent_levels=1)
        self.assertDictEqual({'a': [1,4,7], 'b': [4,5,9]}, result)
        result = model.run_intent_pipeline(canonical=data, inplace=False, intent_levels=[0, 1, 2])
        self.assertDictEqual({'a': [1,4,7]}, result)




if __name__ == '__main__':
    unittest.main()
