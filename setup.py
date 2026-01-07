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
    description="A vim-mode readline implementation with Rich styling, validation, centralized theming, and Rich Prompt API integration",
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
        "rich>=12.0.0",  # Rich is now required for the enhanced theming and Rich components
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
        ],
        "demos": [
            # All dependencies for running demos are in base install now
        ],
    },
    entry_points={
        "console_scripts": [
            "vim-readline-demo=demos.validated_rich_demo:main",
            "vim-readline-themes=demos.theme_showcase_rich:main",
            "vim-readline-hello=hello_app_rich:main",
            "vim-readline-rich-prompt=demos.vim_rich_prompt:main",
            "vim-readline-prompt-api=demos.rich_prompt_api_demo:main",
        ],
    },
    keywords="vim, readline, prompt-toolkit, text-editor, terminal, cli, rich, validation, theming",
    project_urls={
        "Bug Reports": "https://github.com/anthropics/vim_input_v02/issues",
        "Source": "https://github.com/anthropics/vim_input_v02",
    },
)