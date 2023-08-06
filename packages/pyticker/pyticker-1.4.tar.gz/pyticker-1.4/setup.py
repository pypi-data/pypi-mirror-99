from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pyticker",
    version="1.4",
    description="Terminal based stocks and portfolio tracks.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/priyanshus/pyticker",
    python_requires=">=3.8",
    license="MIT",
    install_requires=["prompt-toolkit>=3.0.3", "dataclasses-json>=0.5.2", "requests>=2.25.1"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="terminal-app finance stocks ticker",
    packages=find_packages(),
    entry_points={"console_scripts": ["pyticker = pyticker.pyticker_main:main"]}
)
