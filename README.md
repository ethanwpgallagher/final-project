# ECM3401 Final Project by Ethan Gallagher

## Description
This is the web application developed for ECM3401 Final Project, with the accompanying paper titled "A Comparative Analysis of Convolutional Neural Network Architectures for Diagnosing Diabetic Retinopathy".

This file details the basic instructions for installing and running the software, with further documentation contained in each section of the codebase.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Dataset](#dataset)
- [Usage](#usage)
- [Contact](#contact)

## Prerequisites
There are a couple of prerequisites to consider and some software that needs to be installed.

- Docker
    - Docker needs to be installed on the machine, which can be installed from https://docs.docker.com/get-docker/
    - Once installed, run the desktop hub and the Docker application will start in the background, then the application is ready to build
- Python
    - Python also needs to be installed and updated to the correct version - minimum 3.11.5
- ReactJS
    - To use ReactJS, Node.js needs to be installed on the computer. This can be done from https://nodejs.org/en/download. This includes npm, which is needed to run React files
- MacOS vs Windows
    - In MacOS, some folders may not appear visible until opened in an IDE such as VS Code. One way to check is to open Finder at the location of the cloned repo (see [Installation](#installation)), and compare the number of internal files and folders in List and Icon view, as there may be a slight disparity. The files are all there, but there may be an OS issue preventing them from being initially visible. They can all be opened from list view, and can be opened in an IDE
    - In Windows, all files should be visible and accessible

## Installation
Once the necessary software has been installed, the software can be started using Docker

```bash
# Clone the repo
git clone git@github.com:ethanwpgallagher/final-project.git
# Navigate to the project directory
cd final-project
# Start docker
docker compose build && docker compose up
```
This will start the docker containers and install all the necessary software within them. 
## Dataset
The dataset used for this project was obtained from the Kaggle website at the following link https://www.kaggle.com/c/aptos2019-blindness-detection/data

To download the dataset, follow the instructions on the website, before loading it into a desired location, ensuring to change filepaths in the files doing any processing on the images downloaded.
## Usage
This repository is only permitted for use by the markers of ECM3401.
## Contact
If there are any issues, please contact me via the following:
- Email - eg546@exeter.ac.uk
