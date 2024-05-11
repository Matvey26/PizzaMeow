from setuptools import setup

setup(
    name='pizza-cli',
    version='0.1',
    packages=['pizza_cli_app', 'pizza_cli_app/commands', 'pizza_cli_app/api', 'pizza_cli_app/utils'],
    entry_points="""
        [console_scripts]
        pizza=pizza_cli_app.cli:main
    """
)
