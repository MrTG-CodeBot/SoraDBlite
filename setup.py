import pathlib

import setuptools

setuptools.setup(
    name="SoraDBlite",
    version="1.1.4",
    description="SoraDBlite is a Python class designed to simplify interactions with MongoDB databases, the operation of SoraDBlite is similar to the pymongo. It is also a lite version of pymongo.Added Sora AI integration for error detection and solution.",
    long_description=pathlib.Path("README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    url="https://amalnath.vercel.app",
    author="Amal Nath H",
    author_email="amalnath0600@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    project_urls={
        "Documentation": "https://github.com/MrTG-CodeBot/SoraDBlite/blob/main/README.md",
        "source": "https://github.com/MrTG-CodeBot/SoraDBlite",
    },
    python_requires= ">=3.8.0",
    install_requires=["pymongo", "google-generativeai"],
    packages=setuptools.find_packages(),
    include_package_data=True
)
