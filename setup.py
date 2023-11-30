import os
from setuptools import setup
from wisemen import __version__

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8"
) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wisemen-wagtail-core",
    version=__version__,
    packages=["wisemen"],
    include_package_data=True,
    license="BSD License",
    description="A Wagtail/Django setup, enriched with Wisemen's most-used (third-party) helpers, tools and packages.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/appwise/wisemen-wagtail-core/src",
    author="Wisemen",
    author_email="tim.vanderlinden@appwise.be",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
        "Framework :: Django :: 4.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    python_requires=">=3.11",
    # install_requires=[] is not needed, because we use poetry
    entry_points={
        "console_scripts": ["wisemen=wisemen.bin.wisemen:main"]
    },
    zip_safe=False,
)
