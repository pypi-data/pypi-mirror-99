import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="en_audio2text-soumyade", # Replace with your own username
    version="0.0.1.2",
    author="Soumya De",
    author_email="cs.soumyade@gmail.com",
    description="small wrapper around speech recognition package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cssoumyade/en_audio2text",
    project_urls={
        "Bug Tracker": "https://github.com/cssoumyade/en_audio2text/issues",
    },
    classifiers=[
	"Development Status :: 2 - Pre-Alpha",
	"Intended Audience :: Other Audience",
	"Topic :: Education :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
