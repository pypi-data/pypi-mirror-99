import os
import stat
from os.path import join

from catcher.core.runner import Runner
from catcher.utils.module_utils import load_external_actions
from test.abs_test_class import TestClass


class ExternalTest(TestClass):
    def __init__(self, method_name):
        super().__init__('external', method_name)

    def test_run_external(self):
        self.write_module('math', '''#!/bin/bash
        one=$(echo ${1} | jq -r '.add.the')
        two=$(echo ${1} | jq -r '.add.to')
        echo $((${one} + ${two}))
        ''')
        self.populate_file('main.yaml', '''---
        steps:
            - math:
                add: {the: 1, to: 2}
                register: {sum: '{{ OUTPUT }}'}
            - check: {equals: {the: '{{ sum }}', is: 3}}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_dir])
        self.assertTrue(runner.run_tests())

    def test_run_external_with_vars(self):
        self.write_module('math', '''#!/bin/bash
        one=$(echo ${1} | jq -r '.add.the')
        two=$(echo ${1} | jq -r '.add.to')
        echo $((${one} + ${two}))
        ''')
        self.populate_file('main.yaml', '''---
        variables:
            one: 1
            two: 2
        steps:
            - math:
                add: {the: '{{ one }}', to: '{{ two }}'}
                register: {sum: '{{ OUTPUT }}'}
            - check: {equals: {the: '{{ sum }}', is: 3}}
        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_dir])
        self.assertTrue(runner.run_tests())

    def test_python_module(self):
        self.write_module('hello.py', '''from catcher.steps.external_step import ExternalStep
from catcher.steps.step import update_variables


class Hello(ExternalStep):
    """
    Very important and useful step. Says hello to input. Return as a string.
    Example usage.
    ::
        hello:
            say: 'John Doe'
            register: {greeting='{{ OUTPUT }}'}

    """
    @update_variables
    def action(self, includes: dict, variables: dict) -> (dict, str):
        body = self.simple_input(variables)
        person = body['say']
        return variables, 'hello {}'.format(person)
                ''')
        self.populate_file('main.yaml', '''---
                variables:
                    person: 'John Doe'
                steps:
                    - hello:
                        say: '{{ person }}'
                        register: {greeting: '{{ OUTPUT }}'}
                    - check: {equals: {the: '{{ greeting }}', is: 'hello John Doe'}}
                ''')
        load_external_actions(join(self.test_dir, 'hello.py'))
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_dir])
        self.assertTrue(runner.run_tests())

    def test_run_jar(self):
        self.copy_resource('MyClass.jar')
        self.populate_file('main.yaml', '''---
                                        variables:
                                            person: 'John Doe'
                                        steps:
                                            - MyClass.jar:
                                                say: '{{ person }}'
                                                register: {greeting: '{{ OUTPUT }}'}
                                            - check: {equals: {the: '{{ greeting.strip() }}', is: 'hello John Doe'}}
                                        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_resources])
        self.assertTrue(runner.run_tests())

    # make sure javac is available in the PATH to pass this test
    def test_compile_and_run_java(self):
        self.copy_resource('MyClass.java')
        self.copy_resource('OtherClass.java')
        self.populate_file('main.yaml', '''---
                                variables:
                                    person: 'John Doe'
                                steps:
                                    - MyClass.java:
                                        say: '{{ person }}'
                                        register: {greeting: '{{ OUTPUT }}'}
                                    - check: {equals: {the: '{{ greeting.strip() }}', is: 'hello John Doe'}}
                                ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_resources])
        self.assertTrue(runner.run_tests())

    # make sure kotlinc is available in the PATH to pass this test
    def test_compile_and_run_kotlin(self):
        self.copy_resource('hello.kt')
        self.populate_file('main.yaml', '''---
                                        variables:
                                            person: 'John Doe'
                                        steps:
                                            - hello.kt:
                                                say: '{{ person }}'
                                                register: {greeting: '{{ OUTPUT }}'}
                                            - check: {equals: {the: '{{ greeting.strip() }}', is: 'hello John Doe'}}
                                        ''')
        runner = Runner(self.test_dir, join(self.test_dir, 'main.yaml'), None, modules=[self.test_resources])
        self.assertTrue(runner.run_tests())

    def test_python_module_with_json(self):
        self.write_module('print.py', '''from catcher.steps.external_step import ExternalStep
from catcher.steps.step import update_variables

class Print(ExternalStep):

    @update_variables
    def action(self, includes: dict, variables: dict) -> (dict, str):
        body = self.simple_input(variables)
        data = body['the']
        return variables, 'data is: {}'.format(data)
                    ''')
        self.populate_file('inventory.yml', '''---
                complex_conf:
                  field: 'value'
                  json_field: '{"host": "http://minio:9000","aws_access_key_id":"minio","aws_secret_access_key":"minio123"}'
                ''')
        self.populate_file('main.yaml', '''---
                    steps:
                        - print:
                            the: '{{ complex_conf }}'
                    ''')
        load_external_actions(join(self.test_dir, 'print.py'))
        runner = Runner(self.test_dir,
                        join(self.test_dir, 'main.yaml'),
                        join(self.test_dir, 'inventory.yml'),
                        modules=[self.test_dir])
        self.assertTrue(runner.run_tests())

    def write_module(self, name: str, body: str):
        self.populate_file(name, body)
        path = join(self.test_dir, name)
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
