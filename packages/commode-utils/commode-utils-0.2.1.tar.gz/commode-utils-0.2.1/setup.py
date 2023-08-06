from setuptools import setup

VERSION = "0.2.1"

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    install_requires = [line.strip() for line in requirements_file]

setup_args = dict(
    name="commode-utils",
    version=VERSION,
    description="Set of useful functions and modules for Code Modeling",
    long_description_content_type="text/markdown",
    long_description=readme,
    install_requires=install_requires,
    license="Apache 2.0",
    package_data={"commode_utils": ["py.typed"]},
    packages=["commode_utils", "commode_utils.metrics", "commode_utils.modules"],
    zip_safe=False,
    author="Egor Spirin",
    author_email="spirin.egor@gmail.com",
    keywords=[],
    url="https://github.com/SpirinEgor/commode-utils",
    download_url="https://pypi.org/project/commode-utils/",
)

if __name__ == "__main__":
    setup(**setup_args)
