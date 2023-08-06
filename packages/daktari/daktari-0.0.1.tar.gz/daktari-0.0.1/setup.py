import setuptools
import pathlib

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name="daktari",
    version="0.0.1",
    description="Assist in setting up developer environments",
    long_description=README,
    long_description_content_type="text/markdown",    
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "daktari = daktari.__main__:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
