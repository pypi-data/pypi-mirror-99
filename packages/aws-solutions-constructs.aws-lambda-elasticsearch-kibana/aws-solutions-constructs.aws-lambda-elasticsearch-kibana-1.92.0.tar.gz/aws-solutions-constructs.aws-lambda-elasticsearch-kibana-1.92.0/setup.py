import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-lambda-elasticsearch-kibana",
    "version": "1.92.0",
    "description": "CDK Constructs for AWS Lambda to AWS Elasticsearch with Kibana integration",
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
        "aws_solutions_constructs.aws_lambda_elasticsearch_kibana",
        "aws_solutions_constructs.aws_lambda_elasticsearch_kibana._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_lambda_elasticsearch_kibana._jsii": [
            "aws-lambda-elasticsearch-kibana@1.92.0.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_lambda_elasticsearch_kibana": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudwatch==1.92.0",
        "aws-cdk.aws-cognito==1.92.0",
        "aws-cdk.aws-elasticsearch==1.92.0",
        "aws-cdk.aws-iam==1.92.0",
        "aws-cdk.aws-lambda==1.92.0",
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
