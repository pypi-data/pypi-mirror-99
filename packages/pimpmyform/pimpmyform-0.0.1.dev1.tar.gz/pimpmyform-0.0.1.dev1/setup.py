from setuptools import find_packages, setup

setup(
    name="pimpmyform",
    version='0.0.1.dev1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'python-dotenv'
    ]
)