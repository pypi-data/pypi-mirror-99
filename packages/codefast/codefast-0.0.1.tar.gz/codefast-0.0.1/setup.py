import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codefast",
    version="0.0.1", # Latest version .
    author="R2FsCg",
    author_email="r2fscg@gmail.com",
    description="A package for faster coding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/codefast",
    packages=setuptools.find_packages(),
    install_requires=[
        'colorlog>=4.6.1', 'lxml',
        'smart-open', 'pillow', 'bs4', 'arrow', 'numpy', 'termcolor'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
