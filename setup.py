from setuptools import setup, find_packages

setup(
    name="cli",
    version="1.0.0",
    description="Psp command line",
    author="Ezequiel-Cheque",
    package_dir={"": "psp-cli"},
    py_modules=["main"],
    packages=find_packages(where='psp-cli'),
    include_package_data=True,
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            'cli = main:cli',
        ],
    },
)