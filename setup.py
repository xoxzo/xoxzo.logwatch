from setuptools import setup, find_packages

setup(
    name="xoxzo.logwatch",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        'Baker==1.3',
        'pytz>=2016.3',
    ],
    entry_points={
        'console_scripts': [
            'logwatch = xoxzo.logwatch.main:main',
        ],
    },
)
