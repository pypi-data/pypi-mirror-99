import setuptools

setuptools.setup(
    name="funchouse",
    packages=setuptools.find_packages(exclude=["funchouse_tests"]),
    install_requires=[
        "dagster==0.10.2",
        "dagit==0.10.2",
        "pytest",
    ],
)
