import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-null",
    "version": "0.1.33",
    "description": "Prebuilt null Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/terraform-cdk-providers/cdktf-provider-null.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/terraform-cdk-providers/cdktf-provider-null.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_null",
        "cdktf_cdktf_provider_null._jsii"
    ],
    "package_data": {
        "cdktf_cdktf_provider_null._jsii": [
            "provider-null@0.1.33.jsii.tgz"
        ],
        "cdktf_cdktf_provider_null": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "cdktf>=0.1.0, <0.2.0",
        "constructs>=3.0.4, <4.0.0",
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
