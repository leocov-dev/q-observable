from setuptools import find_packages, setup

setup(
    name="QObservable",
    packages=find_packages(include=["q_observable"]),
    version="0.1.0",
    description="Asynchronous Observables for Qt in Python",
    author="Leonardo Covarrubias",
    license="MIT",
    install_requires=["typing_extensions=~4.4.0; python_version<3.8"],
    setup_requires=[],
    tests_require=[],
    test_suite="tests",
)
