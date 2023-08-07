import setuptools

with open("README.md") as f:
  README = f.read()
  
setuptools.setup(
  name="QuranAPI",
  version="0.0.9",
  description="Get Quran verses into discord through your discord bot!",
  long_description=README,
  long_description_content_type="text/markdown",
  author="nooby xviii",
  author_email="xviii2008@gmail.com",
  packages=setuptools.find_packages(),
  include_package_data=True,
  install_requires=["discord.py", "aiohttp"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.7"
  )
  