# Pandemie

A solution for the Pandemie problem given within the [InformatiCup2020](https://github.com/informatiCup/informatiCup2020)
competition.


## Table of Contents
* [Requirements](#requirements)
* [How to Run](#how-to-run)
* [Usage](#usage)
* [Software Architecture](#software-architecture)
* [Theoretical Overview](#theoretical-overview)
* [Technical Documentation](#technical-documentation)
    * [Backend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Backend)
    * [Frontend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Frontend)
* [Contributors](#contributors)

## Requirements
Since the project is containerized in two docker images, you only need to have the following installed on your local machine:

* `docker`
* `docker-compose`

You can surely run the software without having `docker-compose` or even `docker` installed by running each image individually.
A detailed how-to-run description can be found in [how-to-run-manual](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Usage/00.-How-to-Run). 

## How to Run
* Clone the repository 
    
    ``` 
    git clone https://gitlab.com/omar.araboghli/pandemie.git
    ```
* `TODO:` [Download](here the download link) the trained model provided by us and add it to `pandemie/backend`

     ```
     mv path/to/downloaded/file `path/to/pandemie`/backend
     ```
* Change into pandemie directory
    
     ```
    cd pandemie
    ```
* Build the containers
    
    ```
    docker-compose build
    ```
* Run the images

    ```
    docker-compose up
    ```
    
If everything is ok, the terminal will prompt you that the backend and the frontend images are running on
`localhost:50123` and `localhost:80`, respectively.

## Usage
If you only want to test our backend web service implementation you can 
let the client send a POST request to the endpoint `http://localhost:50123/play`.
* Windows 
    ```
    ic20_windows.exe -t 0 -u http://localhost:50123/play
    ```
* Linux 
    ```
    ./ic20_linux -t 0 -u http://localhost:50123/play
    ```

Otherwise, you can test our pandemic simulation by calling the `localhost:80` on the browser and pressing the **start game** button!

For more details, please check the [usage-manual](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Usage).

## Software Architecture
Interested in how all components are connected to each other ? Then visit this [page](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Software-Architecture)!

## Theoretical Overview
We are representing a solution using a Reinforcement Deep Q-Learning method.
If you are interested in how we solved this problem in details, we recommend to get started
in this [page](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Theoretical-Overview/Introdcution)!

## Technical Documentation
A detailed description of the technichal documentation could be found
for the [Backend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Backend)
as well as for the [Frontend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Frontend).

## Contributors
All rights are reserved for the Computer Science Master students **Omar Arab Oghli** and **Muaid Mughrabi**
of Gottfried Wilhelm Leibniz University of Hannover
