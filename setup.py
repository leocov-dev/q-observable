from setuptools import find_packages, setup

setup(
    name="qobservable",
    packages=find_packages(include=["lib"]),
    version="0.1.0",
    description="Observables for Python Qt",
    author="Leonardo Covarrubias",
    license="MIT",
    install_requires=["typing_extensions=~4.4.0; python_version<3.8"],
    setup_requires=[],
    tests_require=[],
    test_suite="test",
)
