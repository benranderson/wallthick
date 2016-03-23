from paver.tasks import task, BuildFailure, needs
from paver.easy import sh

@needs('unit_tests', 'behave_tests', 'run_pylint')
@task
def default():
    pass

@task
def unit_tests():
    sh('py.test --cov-report term --cov=wallthick tests/unit')

@task
def behave_tests():
    sh('behave tests/features')

@task
def run_pylint():
    try:
        sh('pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" wallthick/ > pylint.txt')
    except BuildFailure:
        pass