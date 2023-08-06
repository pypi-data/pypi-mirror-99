from setuptools import setup

setup(
    name='python-damas',
    version='1.0.2',
    author='Erick Ghuron',
    author_email='ghuron@usp.br',
    packages=['damas'],
    description='Uma biblioteca do jogo de damas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ghurone/python-damas',
    license='MIT',
    keywords='damas jogo ghuron',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment :: Board Games'
    ]
)