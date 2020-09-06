"""setup.py
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="branflake",
    version="0.0.0.dev3",
    author="Curt Gilman",
    author_email="curt@goneaway.blog",
    description="A modified, simplified 128-bit pseudo-flake ID generator for Python",
    keywords="flake flakeid",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://goneaway.blog/misc/branflake-python",
    project_urls={
        'Source': 'https://github.com/curt/branflake'
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
