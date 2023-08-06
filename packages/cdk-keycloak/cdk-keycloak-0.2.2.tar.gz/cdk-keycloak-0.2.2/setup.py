import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-keycloak",
    "version": "0.2.2",
    "description": "CDK construct library that allows you to create KeyCloak service on AWS in TypeScript or Python",
    "license": "Apache-2.0",
    "url": "https://github.com/aws-samples/cdk-keycloak.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws-samples/cdk-keycloak.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_keycloak",
        "cdk_keycloak._jsii"
    ],
    "package_data": {
        "cdk_keycloak._jsii": [
            "cdk-keycloak@0.2.2.jsii.tgz"
        ],
        "cdk_keycloak": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-autoscaling>=1.73.0, <2.0.0",
        "aws-cdk.aws-certificatemanager>=1.73.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.73.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.73.0, <2.0.0",
        "aws-cdk.aws-elasticloadbalancingv2>=1.73.0, <2.0.0",
        "aws-cdk.aws-iam>=1.73.0, <2.0.0",
        "aws-cdk.aws-logs>=1.73.0, <2.0.0",
        "aws-cdk.aws-rds>=1.73.0, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.73.0, <2.0.0",
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
