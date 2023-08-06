import unittest
import os
import shutil
from datetime import datetime
from pprint import pprint

import pandas as pd

from aistac.components.abstract_component import AbstractComponent
from aistac.handlers.abstract_handlers import ConnectorContract
from aistac.intent.python_cleaners_intent import PythonCleanersIntentModel as ControlIntentModel
from aistac.properties.abstract_properties import AbstractPropertyManager
from aistac.properties.property_manager import PropertyManager


class ControlPropertyManager(AbstractPropertyManager):

    def __init__(self, task_name, username: str=None):
        # set additional keys
        root_keys = []
        knowledge_keys = []
        username = username if isinstance(username, str) else 'Control'
        super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys, username=username)


class ControlComponent(AbstractComponent):

    DEFAULT_MODULE = 'aistac.handlers.python_handlers'
    DEFAULT_SOURCE_HANDLER = 'PythonSourceHandler'
    DEFAULT_PERSIST_HANDLER = 'PythonPersistHandler'

    def __init__(self, property_manager: ControlPropertyManager, intent_model: ControlIntentModel,
                 default_save=None, reset_templates: bool = None, template_path: str=None, template_module: str=None,
                 template_source_handler: str=None, template_persist_handler: str=None, align_connectors: bool = None):
        super().__init__(property_manager=property_manager, intent_model=intent_model, default_save=default_save,
                         reset_templates=reset_templates, template_path=template_path, template_module=template_module,
                         template_source_handler=template_source_handler,
                         template_persist_handler=template_persist_handler, align_connectors=align_connectors)

    @classmethod
    def from_uri(cls, task_name: str, uri_pm_path: str, username: str, uri_pm_repo: str=None, pm_file_type: str=None,
                 pm_module: str=None, pm_handler: str=None, pm_kwargs: dict=None, default_save=None,
                 reset_templates: bool=None, template_path: str=None, template_module: str=None,
                 template_source_handler: str=None, template_persist_handler: str=None, align_connectors: bool=None,
                 default_save_intent: bool=None, default_intent_level: bool=None, order_next_available: bool=None,
                 default_replace_intent: bool=None, has_contract: bool=None):
        pm_file_type = pm_file_type if isinstance(pm_file_type, str) else 'pickle'
        pm_module = pm_module if isinstance(pm_module, str) else 'aistac.handlers.python_handlers'
        pm_handler = pm_handler if isinstance(pm_handler, str) else 'PythonPersistHandler'
        _pm = ControlPropertyManager(task_name=task_name, username=username)
        _intent_model = ControlIntentModel(property_manager=_pm, default_save_intent=default_save_intent,
                                           default_intent_level=default_intent_level,
                                           order_next_available=order_next_available,
                                           default_replace_intent=default_replace_intent)
        super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, default_save=default_save,
                                 uri_pm_repo=uri_pm_repo, pm_file_type=pm_file_type, pm_module=pm_module,
                                 pm_handler=pm_handler, pm_kwargs=pm_kwargs, has_contract=has_contract)
        return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save,
                   reset_templates=reset_templates, template_path=template_path, template_module=template_module,
                   template_source_handler=template_source_handler, template_persist_handler=template_persist_handler,
                   align_connectors=align_connectors)

class AbstractComponentTest(unittest.TestCase):

    def setUp(self):
        for var in environ():
            if var in os.environ:
                del os.environ[var]
        os.environ['HADRON_PM_PATH'] = os.path.join(os.environ['PWD'], 'work')
        os.environ['HADRON_PM_TYPE'] = 'json'
        os.environ['HADRON_USERNAME'] = 'TestUser'
        PropertyManager._remove_all()

    def tearDown(self):
        for var in environ():
            if var in os.environ:
                del os.environ[var]
        try:
            shutil.rmtree(os.path.join(os.environ['PWD'], 'work'))
        except:
            pass

    def test_runs(self):
        """Basic smoke test"""
        inst = ControlComponent.from_env('test', has_contract=False)
        self.assertTrue(isinstance(inst, ControlComponent))

    def test_init_exceptions(self):
        with self.assertRaises(ValueError) as context:
            ControlComponent(None, None)
        self.assertTrue("The contract_pm must be a concrete implementation of the AbstractPropertyManager" in str(context.exception))
        with self.assertRaises(ValueError) as context:
            ControlComponent(ControlPropertyManager('demo'), None)
        self.assertTrue("The intent_model must be a concrete implementation of the AbstractIntent" in str(context.exception))

    def test_has_contract(self):
        ControlComponent.from_env('test', default_save=False, has_contract=False)
        with self.assertRaises(FileNotFoundError) as context:
            ControlComponent.from_env('test', default_save=False, has_contract=True)
        self.assertTrue("The property manager domain contact" in str(context.exception))

    def test_scratch_pad(self):
        model = ControlComponent.scratch_pad()
        self.assertGreaterEqual(str(type(model)).find('PythonCleanersIntentModel'), 0)

    def test_from_memory(self):
        model: ControlComponent = ControlComponent.from_memory()
        self.assertGreaterEqual(str(type(model)).find('ControlComponent'), 0)

    def test_intent_model(self):
        model = ControlComponent.from_env('tester', has_contract=False).intent_model
        self.assertGreaterEqual(str(type(model)).find('PythonCleanersIntentModel'), 0)

    def test_pm(self):
        model = ControlComponent.from_env('tester', has_contract=False).pm
        self.assertGreaterEqual(str(type(model)).find('ControlPropertyManager'), 0)

    def test_pm_reset(self):
        inst = ControlComponent.from_env('test', has_contract=False, default_save=False)
        inst.set_version('v2.01')
        inst.set_description('test_desc')
        inst.set_source('test.csv')
        self.assertEqual(inst.pm.version, 'v2.01')
        self.assertEqual(inst.pm.description, 'test_desc')
        self.assertTrue(inst.pm.has_connector(inst.CONNECTOR_SOURCE))
        inst.pm_reset()
        self.assertEqual(inst.pm.version, 'v0.00')
        self.assertEqual(inst.pm.description, '')
        self.assertFalse(inst.pm.has_connector(inst.CONNECTOR_SOURCE))

    def test_remove_connector_contract(self):
        inst = ControlComponent.from_env('test', has_contract=False, default_save=False)
        inst.set_source('test.csv')
        self.assertTrue(inst.pm.has_connector(inst.CONNECTOR_SOURCE))
        inst.remove_connector_contract(inst.CONNECTOR_SOURCE)
        self.assertFalse(inst.pm.has_connector(inst.CONNECTOR_SOURCE))

    def test_version_status_description(self):
        cc: ControlComponent = ControlComponent.from_env('test', has_contract=False, default_save=False)
        self.assertEqual('v0.00', cc.pm.version)
        self.assertEqual('discovery', cc.pm.status)
        self.assertEqual('', cc.pm.description)
        cc.set_version('v1.01')
        cc.set_status('stable')
        cc.set_description('this is a test')
        self.assertEqual('v1.01', cc.pm.version)
        self.assertEqual('stable', cc.pm.status)
        self.assertEqual('this is a test', cc.pm.description)

    def test_intent_report(self):
        instance = ControlComponent.from_env('test', has_contract=False)
        data = {'A': [1,2,3,4,5], 'B': [4,2,6,1,3]}
        data = instance.intent_model.auto_clean_header(data, case='upper')
        data = instance.intent_model.auto_remove_columns(data, predominant_max=0.98)
        result = instance.pm.report_intent()
        control = {'creator': ['TestUser', 'TestUser'],
                   'level': ['A', 'A'],
                   'order': ['0', '0'],
                   'intent': ['auto_clean_header', 'auto_remove_columns'],
                   'parameters': [["case='upper'"], ['predominant_max=0.98']]}
        self.assertDictEqual(control, result)

    def test_report_connectors(self):
        instance = ControlComponent.from_env('task', has_contract=False)
        report = instance.pm.report_connectors(inc_pm=True, inc_template=True)
        control = [instance.pm.CONNECTOR_PM_CONTRACT, instance.TEMPLATE_SOURCE, instance.TEMPLATE_PERSIST]
        self.assertCountEqual(control, report.get('connector_name'))
        control = ['PythonPersistHandler', 'PythonSourceHandler', 'PythonPersistHandler']
        self.assertCountEqual(control, report.get('handler'))
        control = ['aistac.handlers.python_handlers']*3
        self.assertCountEqual(control, report.get('module_name'))
        self.assertIn(os.environ.get('HADRON_PM_PATH') + '/hadron_pm_control_task.json', report.get('uri'))

    def test_PM_from_env(self):
        os.environ['HADRON_PM_PATH'] = "work/test/contracts?A=24&B=fred"
        os.environ['HADRON_PM_TYPE'] = 'pickle'
        os.environ['HADRON_PM_MODULE'] = 'aistac.handlers.python_handlers'
        os.environ['HADRON_PM_HANDLER'] = 'PythonPersistHandler'
        instance = ControlComponent.from_env('task', has_contract=False, encoding='Latin1')
        result = instance.pm.get_connector_contract(instance.pm.CONNECTOR_PM_CONTRACT)
        self.assertEqual('work/test/contracts/hadron_pm_control_task.pickle', result.uri)
        self.assertEqual('PythonPersistHandler', result.handler)
        self.assertEqual('aistac.handlers.python_handlers', result.module_name)
        self.assertDictEqual({'A': '24', 'B': 'fred', 'encoding': 'Latin1'}, result.kwargs)

    def test_DEFAULT_from_env(self):
        os.environ['HADRON_DEFAULT_PATH'] = "HADRON_DEFAULT_PATH?A=24&B=fred"
        os.environ['HADRON_DEFAULT_MODULE'] = "tests.handlers.test_handlers"
        os.environ['HADRON_DEFAULT_SOURCE_HANDLER'] = "TestSourceHandler"
        os.environ['HADRON_DEFAULT_PERSIST_HANDLER'] = "TestPersistHandler"
        instance = ControlComponent.from_env('task', has_contract=False, encoding='Latin1')
        source = instance.pm.get_connector_contract(instance.TEMPLATE_SOURCE)
        self.assertEqual('HADRON_DEFAULT_PATH?A=24&B=fred', source.uri)
        self.assertEqual('TestSourceHandler', source.handler)
        self.assertEqual('tests.handlers.test_handlers', source.module_name)
        self.assertDictEqual({}, source.kwargs)
        persist = instance.pm.get_connector_contract(instance.TEMPLATE_PERSIST)
        self.assertEqual('HADRON_DEFAULT_PATH?A=24&B=fred', persist.uri)
        self.assertEqual('TestPersistHandler', persist.handler)
        self.assertEqual('tests.handlers.test_handlers', persist.module_name)
        self.assertDictEqual({}, persist.kwargs)
        os.environ['HADRON_CONTROL_PATH'] = "HADRON_CONTROL_PATH?C=24&B=fred"
        os.environ['HADRON_CONTROL_MODULE'] = "aistac.handlers.python_handlers"
        os.environ['HADRON_CONTROL_SOURCE_HANDLER'] = "PythonSourceHandler"
        os.environ['HADRON_CONTROL_PERSIST_HANDLER'] = "PythonPersistHandler"
        instance = ControlComponent.from_env('task', has_contract=False)
        source = instance.pm.get_connector_contract(instance.TEMPLATE_SOURCE)
        self.assertEqual('HADRON_CONTROL_PATH?C=24&B=fred', source.uri)
        self.assertEqual('PythonSourceHandler', source.handler)
        self.assertEqual('aistac.handlers.python_handlers', source.module_name)
        self.assertDictEqual({}, source.kwargs)
        persist = instance.pm.get_connector_contract(instance.TEMPLATE_PERSIST)
        self.assertEqual('HADRON_CONTROL_PATH?C=24&B=fred', persist.uri)
        self.assertEqual('PythonPersistHandler', persist.handler)
        self.assertEqual('aistac.handlers.python_handlers', persist.module_name)
        self.assertDictEqual({}, persist.kwargs)

    def test_from_environ(self):
        os.environ['HADRON_PM_PATH'] = "work/${BUCKET}/${TASK}"
        os.environ['HADRON_PM_TYPE'] = 'pickle'
        os.environ['HADRON_PM_MODULE'] = '${MODULE}'
        os.environ['HADRON_PM_HANDLER'] = '${HANDLER}'
        os.environ['BUCKET'] = 'contracts'
        os.environ['TASK'] = 'task'
        os.environ['MODULE'] = 'aistac.handlers.python_handlers'
        os.environ['HANDLER'] = 'PythonPersistHandler'
        instance = ControlComponent.from_env('task', has_contract=False)
        cc = instance.pm.get_connector_contract(connector_name=instance.pm.CONNECTOR_PM_CONTRACT)
        self.assertTrue(cc.uri.startswith('work/contracts/task/'))
        self.assertEqual("aistac.handlers.python_handlers", cc.module_name)
        self.assertEqual("PythonPersistHandler", cc.handler)
        self.assertTrue(cc.raw_uri.startswith('work/${BUCKET}/${TASK}/'))
        self.assertEqual("${MODULE}", cc.raw_module_name)
        self.assertEqual("${HANDLER}", cc.raw_handler)

    def test_connector_file_pattern(self):
        manager = ControlComponent.from_env('task', has_contract=False)
        state_connector = ConnectorContract(
            uri=manager.pm.file_pattern(path=f"{os.environ['HADRON_PM_PATH']}/data/", name='version', versioned=True),
            module_name=manager.DEFAULT_MODULE,
            handler=manager.DEFAULT_PERSIST_HANDLER,
            version="v1.01")
        temporal_connector = ConnectorContract(
            uri=manager.pm.file_pattern(path=f"{os.environ['HADRON_PM_PATH']}/data/", name='temporal', stamped='DAYS'),
            module_name=manager.DEFAULT_MODULE,
            handler=manager.DEFAULT_PERSIST_HANDLER)
        manager.add_connector_contract(connector_name='persist_book_state', connector_contract=state_connector)
        manager.add_connector_contract(connector_name='temporal_state', connector_contract=temporal_connector)
        manager.persist_canonical(connector_name='persist_book_state', canonical=pd.DataFrame({'A': [1,2,3,4]}))
        self.assertTrue(os.path.exists(f"{os.environ['HADRON_PM_PATH']}/data/hadron_CONTROL_task_version_v1.01.pickle"))
        manager.persist_canonical(connector_name='temporal_state', canonical=pd.DataFrame({'A': [1,2,3,4]}))
        dt = datetime.now().strftime("%Y%m%d")
        self.assertTrue(os.path.exists(f"{os.environ['HADRON_PM_PATH']}/data/hadron_CONTROL_task_temporal_{dt}.pickle"))

    def test_add_connector_uri(self):
        manager = ControlComponent.from_env('task', has_contract=False)
        cc = ConnectorContract(uri="/usr/jdoe/code/local_file.pickle", module_name=manager.DEFAULT_MODULE,handler=manager.DEFAULT_PERSIST_HANDLER)
        manager.add_connector_contract(connector_name='connector', connector_contract=cc)
        self.assertEqual("/usr/jdoe/code/local_file.pickle", manager.pm.get_connector_contract(connector_name='connector').uri)

    def test_set_connector_version(self):
        manager = ControlComponent.from_env('task', has_contract=False)
        cc = ConnectorContract(uri="local_file.pickle", module_name=manager.DEFAULT_MODULE,handler=manager.DEFAULT_PERSIST_HANDLER, version="v1.01")
        manager.add_connector_contract(connector_name='connector', connector_contract=cc)
        self.assertEqual("v1.01", manager.pm.get_connector_contract(connector_name='connector').version)
        manager.set_connector_version(connector_names='connector', version="v2.11")
        self.assertEqual("v2.11", manager.pm.get_connector_contract(connector_name='connector').version)

    def test_set_source_uri(self):
        inst = ControlComponent.from_env('test', has_contract=False, default_save=False)
        inst.set_source_uri("http://raw.github.com/test/filename.csv")
        contract = inst.pm.get_connector_contract(inst.CONNECTOR_SOURCE)
        self.assertEqual("http://raw.github.com/test/filename.csv", contract.raw_uri)

    def test_set_persist_uri(self):
        inst = ControlComponent.from_memory()
        inst.set_persist_uri("http://raw.github.com/test/filename.csv")
        contract = inst.pm.get_connector_contract(inst.CONNECTOR_PERSIST)
        self.assertEqual("http://raw.github.com/test/filename.csv", contract.raw_uri)

    def test_report_eviron(self):
        manager = ControlComponent.from_env('test', has_contract=False, default_save=False)
        result = manager.report_environ(hide_not_set=False)
        control = {'HADRON_CONTROL_HANDLER': 'not used',
                   'HADRON_CONTROL_MODULE': 'not used',
                   'HADRON_CONTROL_PATH': 'not used',
                   'HADRON_CONTROL_PERSIST_HANDLER': 'not used',
                   'HADRON_CONTROL_PERSIST_MODULE': 'not used',
                   'HADRON_CONTROL_PERSIST_PATH': 'not used',
                   'HADRON_CONTROL_SOURCE_HANDLER': 'not used',
                   'HADRON_CONTROL_SOURCE_MODULE': 'not used',
                   'HADRON_CONTROL_SOURCE_PATH': 'not used',
                   'HADRON_CONTROL_TEST_HANDLER': 'not used',
                   'HADRON_CONTROL_TEST_MODULE': 'not used',
                   'HADRON_CONTROL_TEST_PATH': 'not used',
                   'HADRON_CONTROL_TEST_PERSIST_HANDLER': 'not used',
                   'HADRON_CONTROL_TEST_PERSIST_MODULE': 'not used',
                   'HADRON_CONTROL_TEST_PERSIST_PATH': 'not used',
                   'HADRON_CONTROL_TEST_SOURCE_HANDLER': 'not used',
                   'HADRON_CONTROL_TEST_SOURCE_MODULE': 'not used',
                   'HADRON_CONTROL_TEST_SOURCE_PATH': 'not used',
                   'HADRON_DEFAULT_HANDLER': 'not used',
                   'HADRON_DEFAULT_MODULE': 'not used',
                   'HADRON_DEFAULT_PATH': 'not used',
                   'HADRON_DEFAULT_PERSIST_HANDLER': 'not used',
                   'HADRON_DEFAULT_PERSIST_MODULE': 'not used',
                   'HADRON_DEFAULT_PERSIST_PATH': 'not used',
                   'HADRON_DEFAULT_SOURCE_HANDLER': 'not used',
                   'HADRON_DEFAULT_SOURCE_MODULE': 'not used',
                   'HADRON_DEFAULT_SOURCE_PATH': 'not used',
                   'HADRON_PM_HANDLER': 'default',
                   'HADRON_PM_MODULE': 'default',
                   'HADRON_PM_PATH': f"{os.environ.get('PWD')}/work",
                   'HADRON_PM_REPO': 'not used',
                   'HADRON_PM_TYPE': 'json',
                   'HADRON_USERNAME': 'TestUser'}
        self.maxDiff = None
        self.assertDictEqual(control, result)

    def test_default_connector(self):
        manager = ControlComponent.from_env('task', has_contract=False)
        # source
        connector = manager.pm.get_connector_contract(manager.TEMPLATE_SOURCE)
        self.assertEqual('./hadron/data', connector.uri)
        self.assertEqual('aistac.handlers.python_handlers', connector.module_name)
        self.assertEqual('PythonSourceHandler', connector.handler)
        # persist
        manager = ControlComponent.from_env('task', has_contract=False)
        connector = manager.pm.get_connector_contract(manager.TEMPLATE_PERSIST)
        self.assertEqual('./hadron/data', connector.uri)
        self.assertEqual('aistac.handlers.python_handlers', connector.module_name)
        self.assertEqual('PythonPersistHandler', connector.handler)
        # set source
        manager.add_connector_from_template(connector_name='source', uri_file='mysource.pickle', template_name=manager.TEMPLATE_SOURCE)
        connector = manager.pm.get_connector_contract('source')
        self.assertEqual('./hadron/data/mysource.pickle', connector.uri)
        self.assertEqual('aistac.handlers.python_handlers', connector.module_name)
        self.assertEqual('PythonSourceHandler', connector.handler)
        # set persist
        manager.add_connector_from_template(connector_name='persist', uri_file='mypersist.pickle', template_name=manager.TEMPLATE_PERSIST)
        connector = manager.pm.get_connector_contract('persist')
        self.assertEqual('./hadron/data/mypersist.pickle', connector.uri)
        self.assertEqual('aistac.handlers.python_handlers', connector.module_name)
        self.assertEqual('PythonPersistHandler', connector.handler)

    def test_modify_connector_from_template(self):
        os.environ['HADRON_DEFAULT_MODULE'] = 'aistac.handlers.python_handlers'
        os.environ['HADRON_DEFAULT_SOURCE_HANDLER'] = 'PythonSourceHandler'
        os.environ['HADRON_DEFAULT_PERSIST_HANDLER'] = 'PythonPersistHandler'
        manager = ControlComponent.from_env('task', has_contract=False)
        self.assertTrue(manager.pm.has_connector(manager.TEMPLATE_SOURCE))
        self.assertTrue(manager.pm.has_connector(manager.TEMPLATE_PERSIST))
        source = ConnectorContract(uri="/tmp/local/data/source_file.pickle", module_name=manager.DEFAULT_MODULE, handler=manager.DEFAULT_SOURCE_HANDLER)
        manager.add_connector_contract(connector_name='my_source', connector_contract=source, template_aligned=True)
        persist = ConnectorContract(uri="s3://bucket/path/persist_file.pickle", module_name=manager.DEFAULT_MODULE, handler=manager.DEFAULT_PERSIST_HANDLER)
        manager.add_connector_contract(connector_name='my_persist', connector_contract=persist, template_aligned=True)
        manager.reset_template_connectors(align=True)
        result = manager.pm.get_connector_contract('my_source')
        self.assertEqual('./hadron/data/source_file.pickle', result.uri)
        self.assertEqual('aistac.handlers.python_handlers', result.module_name)
        self.assertEqual('PythonSourceHandler', result.handler)
        result = manager.pm.get_connector_contract('my_persist')
        self.assertEqual('./hadron/data/persist_file.pickle', result.uri)
        self.assertEqual('aistac.handlers.python_handlers', result.module_name)
        self.assertEqual('PythonPersistHandler', result.handler)
        os.environ.pop('HADRON_DEFAULT_MODULE')
        os.environ.pop('HADRON_DEFAULT_SOURCE_HANDLER')
        os.environ.pop('HADRON_DEFAULT_PERSIST_HANDLER')

    def test_set_report_persist(self):
        manager = ControlComponent.from_env('task', has_contract=False, default_save=False)
        result = manager.set_report_persist([manager.REPORT_SCHEMA, manager.REPORT_INTENT, manager.REPORT_NOTES])
        self.assertEqual(['primary_schema', 'intent', 'notes'], result)
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/hadron_control_task_primary_schema_v0.00.json', result)
        self.assertEqual(6, len(manager.pm.connector_contract_list))
        manager.pm.reset_connector_contracts()
        manager.reset_template_connectors()
        manager.set_report_persist(manager.REPORT_SCHEMA)
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/hadron_control_task_primary_schema_v0.00.json', result)
        self.assertEqual(4, len(manager.pm.connector_contract_list))
        manager.set_report_persist([{'report': manager.REPORT_SCHEMA}])
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/hadron_control_task_primary_schema_v0.00.json', result)
        manager.set_report_persist(reports=[{'report': manager.REPORT_SCHEMA, 'file_type': 'csv'}])
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/hadron_control_task_primary_schema_v0.00.csv', result)
        manager.set_report_persist(reports=[{'report': manager.REPORT_SCHEMA, 'file_type': 'csv', 'versioned': False}])
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/hadron_control_task_primary_schema.csv', result)
        manager.set_report_persist(reports=[{'report': manager.REPORT_SCHEMA, 'uri_file': 'my_file.csv'}])
        result = manager.pm.get_connector_contract(manager.REPORT_SCHEMA).uri
        self.assertEqual('./hadron/data/my_file.csv', result)

    def test_add_runbook_level(self):
        manager = ControlComponent.from_env('task', has_contract=False, default_save=False)
        manager.add_run_book_level(book_name='Default', run_level='One')
        self.assertEqual(['One'], manager.pm.get_run_book('Default'))
        manager.add_run_book_level(book_name='Default', run_level='One')
        self.assertEqual(['One'], manager.pm.get_run_book('Default'))
        manager.add_run_book_level(book_name='Default', run_level='Two')
        self.assertEqual(['One', 'Two'], manager.pm.get_run_book('Default'))
        manager.add_run_book_level(book_name='Default', run_level='One')
        self.assertEqual(['Two', 'One'], manager.pm.get_run_book('Default'))
        manager.add_run_book('Default', run_levels=['One', 'Two', 'One', 'Three'])
        manager.add_run_book_level(book_name='Default', run_level='One')
        self.assertEqual(['Two', 'Three', 'One'], manager.pm.get_run_book('Default'))


def environ():
    return ['HADRON_CONTROL_HANDLER',
            'HADRON_CONTROL_MODULE',
            'HADRON_CONTROL_PATH',
            'HADRON_CONTROL_PERSIST_HANDLER',
            'HADRON_CONTROL_PERSIST_MODULE',
            'HADRON_CONTROL_PERSIST_PATH',
            'HADRON_CONTROL_SOURCE_HANDLER',
            'HADRON_CONTROL_SOURCE_MODULE',
            'HADRON_CONTROL_SOURCE_PATH',
            'HADRON_CONTROL_TEST_HANDLER',
            'HADRON_CONTROL_TEST_MODULE',
            'HADRON_CONTROL_TEST_PATH',
            'HADRON_CONTROL_TEST_PERSIST_HANDLER',
            'HADRON_CONTROL_TEST_PERSIST_MODULE',
            'HADRON_CONTROL_TEST_PERSIST_PATH',
            'HADRON_CONTROL_TEST_SOURCE_HANDLER',
            'HADRON_CONTROL_TEST_SOURCE_MODULE',
            'HADRON_CONTROL_TEST_SOURCE_PATH',
            'HADRON_DEFAULT_HANDLER',
            'HADRON_DEFAULT_MODULE',
            'HADRON_DEFAULT_PATH',
            'HADRON_DEFAULT_PERSIST_HANDLER',
            'HADRON_DEFAULT_PERSIST_MODULE',
            'HADRON_DEFAULT_PERSIST_PATH',
            'HADRON_DEFAULT_SOURCE_HANDLER',
            'HADRON_DEFAULT_SOURCE_MODULE',
            'HADRON_DEFAULT_SOURCE_PATH',
            'HADRON_PM_HANDLER',
            'HADRON_PM_MODULE',
            'HADRON_PM_PATH',
            'HADRON_PM_REPO',
            'HADRON_PM_TYPE']

if __name__ == '__main__':
    unittest.main()
