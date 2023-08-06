import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-fargate-run-task",
    "version": "0.0.71",
    "description": "Define and run container tasks on AWS Fargate immediately or with schedule",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-fargate-run-task.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-fargate-run-task.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_fargate_run_task",
        "cdk_fargate_run_task._jsii"
    ],
    "package_data": {
        "cdk_fargate_run_task._jsii": [
            "cdk-fargate-run-task@0.0.71.jsii.tgz"
        ],
        "cdk_fargate_run_task": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.73.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.73.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.73.0, <2.0.0",
        "aws-cdk.aws-events>=1.73.0, <2.0.0",
        "aws-cdk.aws-logs>=1.73.0, <2.0.0",
        "aws-cdk.core>=1.73.0, <2.0.0",
        "aws-cdk.custom-resources>=1.73.0, <2.0.0",
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
