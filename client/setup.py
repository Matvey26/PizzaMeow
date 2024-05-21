from setuptools import setup, find_packages

setup(
    name='pizza-cli',
    version='0.2',
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        pizza=pizza_cli_app.cli:main
    """
)
