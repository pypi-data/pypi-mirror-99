import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "projen",
    "version": "0.17.17",
    "description": "CDK for software projects",
    "license": "Apache-2.0",
    "url": "https://github.com/projen/projen.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<benisrae@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/projen/projen.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "projen",
        "projen._jsii",
        "projen.deps",
        "projen.github",
        "projen.java",
        "projen.python",
        "projen.tasks",
        "projen.vscode",
        "projen.web"
    ],
    "package_data": {
        "projen._jsii": [
            "projen@0.17.17.jsii.tgz"
        ],
        "projen": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.25.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": [
        "src/projen/_jsii/bin/projen"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
