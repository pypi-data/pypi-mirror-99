import setuptools

__version__ = "1.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pelican-webassets-babeljsx",
    version=__version__,
    author="R Hooper",
    author_email="rhooper@toybox.ca",
    description="A simple plugin that registers the babeljsx Jinja2 filter.",
    keywords="pelican webassets babeljsx plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/rhooper/pelican-webassets-babeljsx",
    project_urls={
        "Bug Tracker": "https://github.com/rhooper/pelican-webassets-babeljsx/issues",
        "Source": "https://github.com/rhooper/pelican-webassets-babeljsx/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pelican.plugins.webassets_babeljsx"],
    python_requires=">=3.6",
    install_requires=["pelican>4.5.0,<5", "dukpy"],
)
