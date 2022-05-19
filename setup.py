import codecs
import os
import setuptools


def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
  )

install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

version = '0.0.3'

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "vtuberwiki-py",
  version = version,
  author = "S. Daffa",
  author_email = "satriadaffa420@gmail.com",
  description = "vtuberwiki-py is a Python wrapper for VirtualYoutuber Fandom API.",
  long_description = long_description,
  long_description_content_type='text/markdown',
  license = "MIT",
  keywords = "python wikia virtualyoutuber fandom API",
  url = "https://github.com/daffpy/vtuberwiki-py",
  install_requires = install_reqs,
  packages = ['vtuberwiki'],
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ]
)