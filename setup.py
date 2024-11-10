import pathlib

import setuptools

setuptools.setup(
    name="soradb",
    version="1.0.0",
    description="Soradb is a Python class designed to simplify interactions with MongoDB databases, the operation of soradb is similar to the pymongo",
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://amalnath.vercel.app",
    author="Amal Nath H",
    author_email="amalnath0600@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    project_urls={
        "Documentation": "https://github.com/MrTG-CodeBot/soradb/blob/main/README.md",
        "source": "https://github.com/MrTG-CodeBot/soradb",
    },
    python_requires= ">=3.8.0",
    install_requires=["pymongo"],
    packages=setuptools.find_packages(),
    include_package_data=True
)
