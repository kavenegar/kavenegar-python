from setuptools import setup
import sys

requires = ['requests>=0.10.8']
if sys.version_info < (2, 6):
    requires.append('simplejson')

setup(
    name = "kavenegar",
    py_modules = ['kavenegar'],
    version = "1.2.0",
    description = "Kavenegar Python library",
    author = "Kavenegar Team",
    author_email = "support@kavenegar.com",
    url = "https://github.com/kavenegar/kavenegar-python",
    keywords = ["kavenegar", "sms"],
    python_requires=">=3.7",
    install_requires = requires,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        ]
     )
