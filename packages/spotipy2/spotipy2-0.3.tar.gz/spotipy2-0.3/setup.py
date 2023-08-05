from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="spotipy2",
    version="0.3",
    description="The next generation Spotify Web API wrapper for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/CyanBook/spotipy2",
    download_url="https://github.com/CyanBook/spotipy2/releases/latest",
    author="CyanBook",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="spotify spotipy api wrapper client library oauth",
    project_urls={
        "Tracker": "https://github.com/CyanBook/spotipy2/issues",
        "Community": "https://github.com/CyanBook/spotipy2",
        "Source": "https://t.me/spotipy2"
    },
    python_requires="~=3.7",
    packages=find_packages()
)
