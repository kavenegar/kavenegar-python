from setuptools import setup, find_packages

setup(
    name="kavenegar-client",
    version="1.1.4",
    description="A professional Python client for the Kavenegar REST API (SMS, Verify, Call, Account)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Reza Torabi , Kavenegar Team",
    author_email="rezatutor475@gmail.com , support@kavenegar.com",
    url="https://github.com/kavenegar/kavenegar-python",
    license="MIT",
    packages=find_packages(exclude=("tests", "examples")),
    include_package_data=True,
    install_requires=[
        "requests>=2.20.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://kavenegar.com/rest.html",
        "Source": "https://github.com/yourusername/kavenegar-client",
        "Tracker": "https://github.com/yourusername/kavenegar-client/issues",
    },
)
