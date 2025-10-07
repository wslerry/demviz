from setuptools import setup, find_packages

setup(
    name="demviz",
    version="0.1.0",
    description="A Python package for visualizing DEM files with VTK and map grid overlays.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lerry William Seling",
    author_email="your.email@example.com",
    url="https://github.com/wslerry/demviz",
    packages=find_packages(),
    install_requires=[
        "vtk>=9.0.0",
        "opencv-python>=4.5.0",
        "numpy>=1.20.0",
        "GDAL>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "demviz = demviz.visualizer:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)