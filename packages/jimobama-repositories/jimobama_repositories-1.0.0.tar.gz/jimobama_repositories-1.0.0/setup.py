import setuptools
import os;

long_description = "";
readMEFile =  "README.md"
if (os.path.exists(readMEFile)):
  with open(readMEFile , "r") as fh:
      long_description = fh.read()
    
setuptools.setup(name = "jimobama_repositories",
      version="1.0.0",
      description="Manager Json files easy for your configuration tools",
      long_description =long_description,
      url="https://github.com/miljimo/jimo_repositories.git",
      long_description_content_type="text/markdown",
      author="Obaro I. Johnson",
      author_email="johnson.obaro@hotmail.com",
      packages=["jimobama_repositories"],
      install_requires=[],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",         
    ],python_requires='>=3.0');

