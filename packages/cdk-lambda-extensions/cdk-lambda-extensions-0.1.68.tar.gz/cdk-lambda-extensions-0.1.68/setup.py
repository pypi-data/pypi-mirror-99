import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-lambda-extensions",
    "version": "0.1.68",
    "description": "AWS CDK construct library that allows you to add any AWS Lambda extensions to the Lambda functions",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-lambda-extensions.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-lambda-extensions.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_lambda_extensions",
        "cdk_lambda_extensions._jsii"
    ],
    "package_data": {
        "cdk_lambda_extensions._jsii": [
            "cdk-lambda-extensions@0.1.68.jsii.tgz"
        ],
        "cdk_lambda_extensions": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda>=1.73.0, <2.0.0",
        "aws-cdk.aws-s3>=1.73.0, <2.0.0",
        "aws-cdk.core>=1.73.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
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
