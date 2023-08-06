import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-sns-lambda",
    "version": "1.93.0",
    "description": "CDK Constructs for AWS SNS to AWS Lambda integration",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/aws-solutions-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-solutions-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_solutions_constructs.aws_sns_lambda",
        "aws_solutions_constructs.aws_sns_lambda._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_sns_lambda._jsii": [
            "aws-sns-lambda@1.93.0.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_sns_lambda": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam==1.93.0",
        "aws-cdk.aws-kms==1.93.0",
        "aws-cdk.aws-lambda-event-sources==1.93.0",
        "aws-cdk.aws-lambda==1.93.0",
        "aws-cdk.aws-sns==1.93.0",
        "aws-cdk.core==1.93.0",
        "aws-solutions-constructs.core==1.93.0",
        "constructs>=3.2.0, <4.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
