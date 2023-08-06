import os
from setuptools import find_packages, setup
setuptools_kwargs = {
    'install_requires': [
        "flake8==3.8.4",
        "jieba==0.42.1",
        "mccabe == 0.6.1",
        "numpy==1.20.1",
        "pandas==1.2.3",
        "pycodestyle==2.6.0",
        "pyflakes==2.2.0",
        "python-dateutil==2.8.1",
        "pytz==2021.1",
        "six==1.15.0"
    ],
    'zip_safe': False,
}
# Get long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='my-nlp-wrangler',
    version='0.0.3',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,

    author='Claire.Wu',
    author_email='jjudy708618@gmail.com',
    url='https://github.com/jjudy60334/my-nlp-wrangler',
    keywords=[],
    classifiers=["Programming Language :: Python :: 3",
                 "Development Status :: 1 - Planning"],
    python_requires='>=3.7',
    **setuptools_kwargs
)
