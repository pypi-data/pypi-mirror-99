import re

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('slashpy/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md', encoding='utf-8') as f:
    readme = f.read()
    # I'll use this later, idk


setup(
    name='slashpy',
    author='AlexFlipnote',
    url='https://github.com/AlexFlipnote/discord_slash.py',
    license='MIT',
    version=version,
    install_requires=requirements,
    python_requires='>=3.6',
    packages=['slashpy'],
    description='Discord Slash command builder made in Python',
    long_description=readme,
    include_package_data=True
)
