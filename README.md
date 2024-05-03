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
    - In Windows, all files should be visible and accessible. In order to run Docker you must have WSL2 set up and installed, otherwise this application will not build and load due to the docker containers being linux based. If there are any issues building the containers, follow https://docs.docker.com/desktop/wsl/ , otherwise try using a Linux based platform or MacOS for the system of choice.
- Saved models
    - Due to the limited size of the submission, the saved_models are in the SharePoint and also in the github repository but not in the code uploaded in the zip file. If running the code from the zip file, copy the saved models from the SharePoint or the GitHub repo and place them in /final-project/backend/ml/saved_models in order for the code to run as intended

## Installation
Once the necessary software has been installed, the software can be started using Docker

```bash
# Clone the repo if necessary
git clone git@github.com:ethanwpgallagher/final-project.git
# Navigate to the project directory
cd final-project
# Start docker
docker compose build && docker compose up
```
This will start the docker containers and install all the necessary software within them, as long as you have Docker installed and running correctly.
## Dataset
The dataset used for this project was obtained from the Kaggle website at the following link https://www.kaggle.com/c/aptos2019-blindness-detection/data

To download the dataset, follow the instructions on the website, before loading it into a desired location, ensuring to change filepaths in the files doing any processing on the images downloaded.
## Usage
This repository is only permitted for use by the markers of ECM3401.
## Contact
If there are any issues, please contact me via the following:
- Email - eg546@exeter.ac.uk
