import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.custom-resources",
    "version": "1.95.0",
    "description": "Constructs for implementing CDK custom resources",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.custom_resources",
        "aws_cdk.custom_resources._jsii"
    ],
    "package_data": {
        "aws_cdk.custom_resources._jsii": [
            "custom-resources@1.95.0.jsii.tgz"
        ],
        "aws_cdk.custom_resources": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudformation==1.95.0",
        "aws-cdk.aws-ec2==1.95.0",
        "aws-cdk.aws-iam==1.95.0",
        "aws-cdk.aws-lambda==1.95.0",
        "aws-cdk.aws-logs==1.95.0",
        "aws-cdk.aws-sns==1.95.0",
        "aws-cdk.core==1.95.0",
        "constructs>=3.3.69, <4.0.0",
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
        "License :: OSI Approved",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 1"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
