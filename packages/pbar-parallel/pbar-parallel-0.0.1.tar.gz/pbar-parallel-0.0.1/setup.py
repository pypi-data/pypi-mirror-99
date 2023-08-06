from setuptools import setup

setup(
    name="pbar-parallel",
    author="Mats L. Richter",
    author_email="matrichter@uos.de",
    version="0.0.1",
    description="Provides a Wrapper arround joblibs Parallel object for displaying a progress bar",
    py_modules=["pbar_parallel"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        "attrs",
        "joblib",
        "tqdm"
    ],
    extras_requires=[
        "pytest >= 3.7"
    ]
)