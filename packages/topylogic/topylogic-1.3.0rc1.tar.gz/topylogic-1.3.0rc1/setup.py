import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="topylogic",
        version="1.3.0.rc1",
        author="Matthew Stern",
        author_email="msstern98@gmail.com",
        description="Context Free/Switching DFA/NFA library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mstern98/topylogic-git",
        project_urls={
            "Bug Tracker": "https://github.com/mstern98/topylogic-git/issues",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        package_dir={"": "src"},
        package_data={"": ['_topylogic.so', '_topylogic.pyd']},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.6",
)
