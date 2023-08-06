#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="urwid_picker_widgets",
      version="0.1",
      description="Specialized picker widgets for urwid "
                  "that extend its features.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Ezio-Sarthak/urwid_picker_widgets",
      author="Sarthak Garg",
      author_email="grgsrthk.dev20@gmail.com",
      license="MIT",
      packages=["urwid_picker_widgets",
                "urwid_picker_widgets.assisting_modules",
                "urwid_picker_widgets.widgets"],
      install_requires=["urwid"],
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Unix",
                   "Intended Audience :: Developers",
                   "Environment :: Console",
                   "Topic :: Software Development :: Widget Sets"],
      python_requires=">=3.6",
)
