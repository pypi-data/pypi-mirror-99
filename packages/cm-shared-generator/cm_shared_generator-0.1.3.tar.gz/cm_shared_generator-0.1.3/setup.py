import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cm_shared_generator",
    version="0.1.3",
    author="Célien Menneteau",
    author_email="celien.menneteau@gmail.com",
    description="Shared generator between process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Juquod/cm_shared_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)