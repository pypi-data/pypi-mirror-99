from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='WikipediaCategoryResolver',
    version='1.0.3',
    packages=['WikipediaCategoryResolver'],
    description='Named Entity Recognition using Wikipedia API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False
)