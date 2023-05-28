from setuptools import setup

setup(
    name='run-app',
    version='1.0',
    packages=['app'],
    entry_points={
        'console_scripts': [
            'run-app=app.app:main',
        ],
    },
)