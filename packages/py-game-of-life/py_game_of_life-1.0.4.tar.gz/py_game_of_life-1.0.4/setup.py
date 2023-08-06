from setuptools import setup
import os


def readme_file_content():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    readme_path = os.path.join(dir_path, 'README.md')
    file_contents = ''
    with open(readme_path, 'r') as readme:
        file_contents = readme.read()

    return file_contents


setup(
    name='py_game_of_life',
    version='1.0.4',
    description='Conway\'s Game of Life Simulation, implemented with pygame',
    long_description=readme_file_content(),
    long_description_content_type='text/markdown',
    url='https://github.com/BodaSadalla98/Cookbook/tree/main/python/game_of_live',
    author='BodaSadalla',
    author_email='boda998@yahoo.com',
    license='GPL-3.0',
    packages=['pygameoflife'],
    entry_points={
        'console_scripts': [
            'py_game_of_life = pygameoflife.__main__:main',
        ],
    },

    zip_safe=False,
    install_requires=[
        'pygame'
    ],
    python_requires='>=3.0',
)
