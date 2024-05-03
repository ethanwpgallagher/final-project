# ECM3401 Final Project by Ethan Gallagher - Frontend

## Description
This is the web application developed for ECM3401 Final Project, with the accompanying paper titled "A Comparative Analysis of Convolutional Neural Network Architectures for Diagnosing Diabetic Retinopathy".

This file details the information regarding the frontend section of the codebase, with information on folder structure and functionality.
The developed code is inside the folder src, so this README is primarily about that section.
## Table of Contents
- [src](#src)
    - [Pages](#pages)
    - [Components](#components)
    - [Tests](#tests)
- [Package.json and node_modules](#packagejson-and-node_modules)
- [Dockerfile](#dockerfile)

## src
### Pages
Contains the code for the separate pages displayed in the web application, which each contain different components which change based on certain conditions on that page
- About.js -> displays the about page and its respective component for the application
- Analysis.js -> displays the model analysis page outline, with the AnalysisComponent inside it
- Diagnosis.js -> display the diagnosis page outline with DiagnosisContent and Result components inside
- Home.js -> displays the home page outline
### Components
The components sit inside the pages and change based on specified conditions in the application
- AboutContent.js -> display information about the application
- AnalysisContent.js -> displays the graphs containing the data on each models training and testing performances
- DiagnosisContent.js -> contains the dropdown menu and upload retinal image button to receive a DR diagnosis
- DiagnosisResult.js -> displays the diagnosis given from the backend for the uploaded image
- Footer.js -> displays the footer
- HomeContent.js -> displays the content on the home page
- TopMenu.js -> contains and displays the different page options, where clicking them takes you to said page. Accessible from any page in the application
### Tests
Contains unit tests for every page and component in the application. To run, make sure you're inside the 'client' folder and run the command
```
npm test
```
## Package.json and node_modules
The package.json file lists all of the different packages required for the application. When npm starts the application, these are all installed and can be found in the node_modules folder
## Dockerfile
The Dockerfile here is used to start the frontend docker container and start running the react web app.
## Usage
This repository is only permitted for use by the markers of ECM3401.
## Contact
If there are any issues, please contact me via the following:
- Email - eg546@exeter.ac.uk
