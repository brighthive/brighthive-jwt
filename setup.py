try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

REQUIRED_PACKAGES = ["pyjwt[crypto]"]

setup(
    name="bhjwt",
    version="0.0.3",
    author="Brighthive",
    # author_email="engineering@brighthive.io",
    # description="Brighthive Library for JWT",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/brighthive/brighthive-jwt-authorization-lib",
    # classifiers=[
    #     "Programming Language :: Python :: 3.8",
    #     "Operating System :: OS Independent",
    # ],
    packages=setuptools.find_packages(),
    # python_requires=">=3.8",
    install_requires=REQUIRED_PACKAGES,
)
