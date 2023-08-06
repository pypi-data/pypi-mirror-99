import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dewil",
    version="0.1.1a",
    author="nobody",
    author_email="nobody@example.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://example.com",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
    ]
)
