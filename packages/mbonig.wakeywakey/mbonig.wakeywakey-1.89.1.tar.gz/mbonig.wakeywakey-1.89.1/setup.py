import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.wakeywakey",
    "version": "1.89.1",
    "description": "A CDK construct that will automatically start a stopped EC2 instance at a given time.",
    "license": "Apache-2.0",
    "url": "https://github.com/mbonig/wakeywakey",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/wakeywakey"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.wakeywakey",
        "mbonig.wakeywakey._jsii"
    ],
    "package_data": {
        "mbonig.wakeywakey._jsii": [
            "wakeywakey@1.89.1.jsii.tgz"
        ],
        "mbonig.wakeywakey": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.89.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.89.0, <2.0.0",
        "aws-cdk.aws-events>=1.89.0, <2.0.0",
        "aws-cdk.aws-iam>=1.89.0, <2.0.0",
        "aws-cdk.aws-lambda-nodejs>=1.89.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.89.0, <2.0.0",
        "aws-cdk.core>=1.89.0, <2.0.0",
        "cdk-iam-floyd==0.120.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.16.0, <2.0.0",
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
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
