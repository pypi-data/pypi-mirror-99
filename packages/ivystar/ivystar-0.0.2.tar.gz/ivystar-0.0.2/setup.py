from setuptools import setup, find_packages

setup(
    name="ivystar",
    packages=find_packages(),
    version='0.0.2',
    description="python tools package of ivystar",
    author="qinhaining",
    author_email='qhn614@126.com',
    url="",
    download_url="",
    keywords=['command', 'line', 'tool'],
    classifiers=[],
    entry_points={
        'console_scripts': [
    ]
    },
    install_requires=[
        'numpy',
        'requests',
    ]
)
