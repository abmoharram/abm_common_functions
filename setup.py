from setuptools import find_packages, setup

setup(
    name="abm_common_functions",
    packages=find_packages(include=["abm_common_functions"]),
    version="0.1.1",
    description="ABM common functions",
    authors=["Ahmed Moharram"],
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
