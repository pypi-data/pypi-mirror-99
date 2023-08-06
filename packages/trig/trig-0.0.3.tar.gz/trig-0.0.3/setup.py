import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="trig",
    version="0.0.3",
    author="Tom Fryers",
    description="Many trigonometric functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Tom_Fryers/trig",
    py_modules=["trig"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
