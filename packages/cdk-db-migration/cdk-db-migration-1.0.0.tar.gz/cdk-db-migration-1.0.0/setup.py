import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-db-migration",
    "version": "1.0.0",
    "description": "CDK Construct for managing DB migrations",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/cdk-db-migration",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-db-migration.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_db_migration",
        "cdk_db_migration._jsii"
    ],
    "package_data": {
        "cdk_db_migration._jsii": [
            "cdk-db-migration@1.0.0.jsii.tgz"
        ],
        "cdk_db_migration": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudformation>=1.50.0, <2.0.0",
        "aws-cdk.aws-glue>=1.50.0, <2.0.0",
        "aws-cdk.aws-iam>=1.50.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.50.0, <2.0.0",
        "aws-cdk.core>=1.50.0, <2.0.0",
        "constructs>=3.2.80, <4.0.0",
        "jsii>=1.26.0, <2.0.0",
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
