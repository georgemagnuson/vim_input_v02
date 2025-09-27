#!/usr/bin/env python3
"""
Setup script for vim_readline package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A vim-mode readline implementation based on prompt-toolkit"

# Read version from package
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'vim_readline', '__init__.py')
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "0.1.0"

setup(
    name="vim-readline",
    version=get_version(),
    author="Generated with Claude Code",
    author_email="noreply@anthropic.com",
    description="A vim-mode readline implementation for single-buffer text editing",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/anthropics/vim_input_v02",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Text Editors",
    ],
    python_requires=">=3.7",
    install_requires=[
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "rich": [
            "rich>=12.0.0",
        ],
        "dev": [
            "pytest",
            "pytest-cov",
            "rich>=12.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vim-readline-demo=vim_readline.examples:main",
        ],
    },
    keywords="vim, readline, prompt-toolkit, text-editor, terminal, cli",
    project_urls={
        "Bug Reports": "https://github.com/anthropics/vim_input_v02/issues",
        "Source": "https://github.com/anthropics/vim_input_v02",
    },
)