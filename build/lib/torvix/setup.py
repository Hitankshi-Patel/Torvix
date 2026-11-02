#!/usr/bin/env python3
"""
Setup script for Torvix - AI-powered terminal assistant
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Torvix - AI-powered terminal assistant"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="torvix",
    version="1.0.0",
    description="AI-powered terminal assistant for natural language command execution",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Torvix Team",
    author_email="contact@torvix.ai",
    url="https://github.com/torvix/torvix",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'torvix=torvix.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="ai, terminal, cli, assistant, automation, natural-language",
    project_urls={
        "Bug Reports": "https://github.com/torvix/torvix/issues",
        "Source": "https://github.com/torvix/torvix",
        "Documentation": "https://torvix.readthedocs.io/",
    },
)
