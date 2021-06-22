import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRED_PACKAGES = ["boto3", "pyjwt[crypto]"]

setuptools.setup(
    name="brighthive_jwt_authorization_lib",
    # version="0.0.1",
    author="Brighthive",
    author_email="engineering@brighthive.io",
    description="Brighthive Library for JWT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brighthive/brighthive-jwt-authorization-lib",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=REQUIRED_PACKAGES,
)
