from setuptools import setup

setup(
    name='asynctornado',
    version='1.0',
    py_modules=['asynctornado'],
    install_requires=[
        "Click",
        "tornado",
        "flask",
        "colorama",
        "termcolor",
    ],
    entry_points='''
        [console_scripts]
        bootup=asynctornado.cli:cli_bootup
    ''',
)