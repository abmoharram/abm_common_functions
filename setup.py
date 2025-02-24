from setuptools import find_packages, setup

setup(
    name="abm_dommon_functions",
    packages=find_packages(include=["src"]),
    version="0.1.1",
    description="ABM common_functions",
    author="Me",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
