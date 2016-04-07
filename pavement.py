from paver.tasks import task, BuildFailure, needs
from paver.easy import sh
from paver.setuputils import setup, find_package_data


@needs('unit_tests', 'behave_tests', 'run_pylint', "sdist")
@task
def default():
    pass


# Unit tests
@task
def unit_tests():
    sh('py.test --cov-report term --cov-report html --cov-report xml --cov=wallthick tests/unit')


# Acceptance tests
@task
def behave_tests():
    sh('behave tests/features')


# Lint check
@task
def run_pylint():
    try:
        sh('pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" wallthick/ > pylint.txt')
    except BuildFailure:
        pass

# Package set up
package_data = find_package_data()
entry_points = {
    'console_scripts': [
        'run_server = wallthick:main',
        ]
}

setup(name='wallthick',
      version='0.0.1',
      author='Ben Randerson',
      author_email='ben.m.randerson@gmail.com',
      maintainer='Ben Randerson',
      description='Subsea pipeline wall thickness design calculations',
      license='License :: Public Domain',
      include_package_data=True,
      packages=['wallthick'],
      package_data=package_data,
      entry_points=entry_points)


@task
@needs('paver.misctasks.generate_setup',
       'distutils.command.sdist')
def sdist():
    """Generates the setup file and packages up the
  commercial_inventory application."""
