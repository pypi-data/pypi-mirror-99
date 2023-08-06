from setuptools import setup, find_packages

with open("requirements.txt") as r:
    requirements = r.read().split("\n")
    r.close()

# with open("Readme.md") as r:
#     readme = r.read()
#     r.close()

setup(
   name='SMRCBuilder',
   version='0.2',
   description='A Library To Help Build Your SmartRC Interface',
   license="MIT",
   author='NoKodaAddictions',
   author_email='nokodaaddictions@gmail.com',
   url="https://nokodaaddictions.github.io/Projects/SmartRC/SMRCBuilder.html",
   packages=find_packages(),
   install_requires=requirements
)
#2021 NoKodaAddictions