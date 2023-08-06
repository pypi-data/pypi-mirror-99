import setuptools


with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_emulator", # Replace with your own username
    version="0.0.2",
    author="MMGC 2021",
    author_email="240326315@qq.com",
    description="The competition system for MMGC 2021",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AItransCompetition/simple_emulator/tree/mmgc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    package_data={
        '':["*txt", "*csv"]
    }
)
