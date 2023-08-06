import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cleantxt",
    version="0.0.6",
    author="Aymen Jemi",
    author_email="jemiaymen@gmail.com",
    description="cleaning text from noise for nlp tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jemiaymen/cleantxt",
    project_urls={
        "Bug Tracker": "https://github.com/jemiaymen/cleantxt/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=("tests",)),
    install_requires=[
        "tqdm"
    ],


    entry_points={
        "console_scripts": [
            "cleantxt=cleantxt.__main__:main",
        ]
    },
    python_requires=">=3.6",
)
