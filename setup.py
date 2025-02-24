from setuptools import find_packages, setup

setup(
    name='abm_common_functions',
    packages=find_packages(include=['src']),
    version='0.1.0',
    description='ABM common_functions',
    author='Me',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
