# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuxsuite",
    author="Linaro Limited",
    description="The fun Linux kernel development service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Linaro/tuxsuite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Operating System Kernels :: Linux",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["attrs", "Click", "requests", "pyyaml"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    entry_points="""
        [console_scripts]
        tuxsuite=tuxsuite.cli:main
    """,
)
