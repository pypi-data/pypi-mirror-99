import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.aws-elasticloadbalancingv2-actions",
    "version": "1.95.1",
    "description": "Integration actions for AWS ElasticLoadBalancingV2",
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
        "aws_cdk.aws_elasticloadbalancingv2_actions",
        "aws_cdk.aws_elasticloadbalancingv2_actions._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_elasticloadbalancingv2_actions._jsii": [
            "aws-elasticloadbalancingv2-actions@1.95.1.jsii.tgz"
        ],
        "aws_cdk.aws_elasticloadbalancingv2_actions": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cognito==1.95.1",
        "aws-cdk.aws-ec2==1.95.1",
        "aws-cdk.aws-elasticloadbalancingv2==1.95.1",
        "aws-cdk.aws-iam==1.95.1",
        "aws-cdk.core==1.95.1",
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
