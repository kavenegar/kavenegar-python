from setuptools import setup
import sys

requires = ['requests>=0.10.8']
if sys.version_info < (2, 6):
    requires.append('simplejson')

setup(
    name = "kavenegar",
    py_modules = ['kavenegar'],
    version = "1.1.3",
    description = "Kavenegar Python library",
    author = "Kavenegar Team",
    author_email = "support@kavenegar.com",
    url = "https://github.com/kavenegar/kavenegar-python",
    keywords = ["kavenegar", "sms"],
    install_requires = requires,
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        ]
     )