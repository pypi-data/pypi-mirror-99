import pathlib
import re
from codecs import open
from setuptools import setup, find_packages

root = pathlib.Path(__file__).parent.absolute()

with open('serde/__init__.py', 'r', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup_requires = [
    'pytest-runner',
]

requires = [
    'dataclasses;python_version==\'3.6\'',
    'stringcase',
    'typing_inspect>=0.4.0',
    'jinja2',
]
msgpack_requires = ['msgpack']
toml_requires = ['toml']
yaml_requires = ['pyyaml']

tests_require = [
    'coverage',
    'pytest',
    'pytest-cov',
    'pytest-flake8',
    'mypy',
    'flake8',
]

setup(
    name='pyserde',
    version=version,
    description='Serialization library on top of dataclasses.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='yukinarit',
    author_email='yukinarit84@gmail.com',
    url='https://github.com/yukinarit/pyserde',
    packages=find_packages(exclude=['test_serde', 'bench']),
    package_data={'serde': ['py.typed']},
    python_requires=">=3.6",
    setup_requires=setup_requires,
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        'msgpack': msgpack_requires,
        'toml': toml_requires,
        'yaml': yaml_requires,
        'all': msgpack_requires + toml_requires + yaml_requires,
        'test': tests_require,
    },
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
