![build](https://github.com/elhusseiniali/loki/workflows/build/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/elhusseiniali/loki/badge.svg?branch=master)](https://coveralls.io/github/elhusseiniali/loki?branch=master)

#  loki
##  Table of contents
*  [Introduction](#introduction)
*  [Setup](#setup)
*  [Phase One](#phase-one)

##  Introduction
Loki is a flask app built to provide a friendly UI to use [Foolbox](https://foolbox.readthedocs.io/en/stable/) with some facial recognition systems.
The project aims to provide some user-friendly visualizations for different attacks and some useful metrics on the robustness of facial recognition systems.
It is being developed for the Software Engineering course (M1) given at ENS Paris-Saclay in 2020-2021.

##  Setup
We recommend using Python 3.6 or newer.
You will have to create your own virtual environment [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a great option for that. You will need to install the
requirements using `pip install -r requirements.txt` (use pip3 if you aren't using pyenv). If this is your first time running the project, you will need to instantiate an empty database using
`python reset.py`.

You can run the app using `python run.py`. The terminal will show you what address to use to visit the app in a modern browser (usually it is something like localhost:5000/ or localhost:5001/).


Our admin panel so far has no privilege checking whatsoever (we know, we'll fix it later), which means that you can access it by going to the `/admin` path (e.g. localhost:5000/admin).


## Phase One
(This is specifically for the course instructors)
We provided some data to test out the classifier (two images, found under  `loki/static/data`). Remember to use  `python reset.py` the first time, to get things working (as described in [Setup](#setup)).
