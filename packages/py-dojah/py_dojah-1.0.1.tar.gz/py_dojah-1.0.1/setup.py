import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_dojah", # Replace with your own username
    version="1.0.1",
    author="Kolapo Olamidun",
    author_email="kolapoolamidun@gmail.com",
    description="An API wrapper for dojah.io API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Olamidun/py-dojah",
    project_urls={
        "Documentation": "https://github.com/Olamidun/py-dojah/blob/master/README.md",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests']
)