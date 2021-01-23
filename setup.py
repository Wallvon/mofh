import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mofh",
    version="0.0.2",
    author="Robert S.",
    author_email="admin@robert-s.dev",
    description="Async API wrapper for https://myownfreehost.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wallvon/mofh",
    packages=setuptools.find_packages(),
    keywords = ['mofh', 'myownfreehost', 'vistapanel', 'vpanel', 'byet', 'ifastnet', 'byethost', 'freehosting', 'free-hosting', 'api-wrapper', 'api', 'wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp"],
    python_requires='>=3.7',
)
