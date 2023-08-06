import setuptools
setuptools.setup(
    name = "python-termenu",
    version = "0.0.9",
    author = "iiPython",
    author_email = "ben@iipython.cf",
    description = "Simple terminal-based menus in Python",
    long_description = open("README.md", "r").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/ii-Python/termenu",
    project_urls = {
        "Bug Tracker": "https://github.com/ii-Python/termenu/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6",
)
