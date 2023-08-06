import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-apigateway-sagemakerendpoint",
    "version": "1.92.0",
    "description": "CDK Constructs for AWS API Gateway and Amazon SageMaker Endpoint integration.",
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
        "aws_solutions_constructs.aws_apigateway_sagemakerendpoint",
        "aws_solutions_constructs.aws_apigateway_sagemakerendpoint._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_apigateway_sagemakerendpoint._jsii": [
            "aws-apigateway-sagemakerendpoint@1.92.0.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_apigateway_sagemakerendpoint": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway==1.92.0",
        "aws-cdk.aws-iam==1.92.0",
        "aws-cdk.aws-logs==1.92.0",
        "aws-cdk.core==1.92.0",
        "aws-solutions-constructs.core==1.92.0",
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
