from setuptools import setup, find_packages

setup(
    name="clipnotes",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
        "psutil",
    ],
    extras_require={
        "dev": ["pytest", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "clipnotes=clipnotes:main",
        ],
    },
    package_data={
        "clipnotes": ["example-weak-to-strong-generalization.md"],
    },
    author="Thomas",
    description="A tool to monitor clipboard and save contents with context",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
)
