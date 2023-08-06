from setuptools import find_packages, setup

setup(
    name="pimpmydb",
    version='0.0.12.dev1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'mysql-connector-python',
        'python-dotenv'
    ]
)