from setuptools import setup, find_packages

version = __import__(
    "touchtechnology.public", fromlist=["touchtechnology"]
).get_version()

setup(
    name="touchtechnology-public",
    version=version,
    url="http://www.touchtechnology.com.au/",
    author="Touch Technology Pty Ltd",
    author_email="support@touchtechnology.com.au",
    description="Publicly released components used in all Touch Technology library code.",
    install_requires=["Django",],
    extras_require={},
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=["touchtechnology"],
    zip_safe=False,
)
