import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycss",
    version="0.0.1",
    author="Ayaan Imran",
    author_email="miskiacuberayaan2509@gmail.com",
    description="A package that will help you to color your output!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayaan-Imran/pycss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
