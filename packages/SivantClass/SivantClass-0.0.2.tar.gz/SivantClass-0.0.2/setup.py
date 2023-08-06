from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="SivantClass",
    version="0.0.2",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sivant1361/sivant_hello",
    author="Sivant M",
    author_email="sivant1313@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["SivantClass"],
    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "weather-reporter=weather_reporter.cli:main",sivant9994532266

    #     ]
    # },
)