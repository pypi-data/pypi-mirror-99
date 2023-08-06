import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-triggers",
    "version": "0.0.5",
    "description": "cdk-triggers",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/cdk-triggers.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-team@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/cdk-triggers.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_triggers",
        "cdk_triggers._jsii"
    ],
    "package_data": {
        "cdk_triggers._jsii": [
            "cdk-triggers@0.0.5.jsii.tgz"
        ],
        "cdk_triggers": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda>=1.92.0, <2.0.0",
        "aws-cdk.core>=1.92.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.24.0, <2.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
