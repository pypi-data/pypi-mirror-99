from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

print(find_packages())
setup(
    name="keyword-extraction-has",
    packages=find_packages(),
    version="0.3.0",
    description="the implementation  ths keyword extraction technique "
                "described in the following paper : https://tinyurl.com/59b9ewb2",
    author="Simon Meoni",
    license="MIT",
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    extract_keywords=has_keyword_extractor.cli:keyword_extractor
    """
)
