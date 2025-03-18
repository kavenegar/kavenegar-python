from setuptools import setup

requires = ["https>=0.28"]

setup(
    name="kavenegar",
    python_requires=">=3.8",
    py_modules=["kavenegar"],
    version="1.2.0",
    description="Kavenegar Python library",
    author="Kavenegar Team",
    author_email="support@kavenegar.com",
    url="https://github.com/kavenegar/kavenegar-python",
    keywords=["kavenegar", "sms"],
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
    ],
)
