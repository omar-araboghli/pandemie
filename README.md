# Pandemie

A solution for the Pandemie problem given within the [InformatiCup2020](https://github.com/informatiCup/informatiCup2020)
competition.


## Table of Contents
* [How to Run](#how-to-run)
* [Software Architecture](#software-architecture)
* [Theoretical Overview](#theoretical-overview)
* [Future Works](#future-works)
* [Technical Documentation](#technical-documentation)
* [Wiki](#wiki)

## How to Run

### Backend
* Windows 
    ```
    ic20_windows.exe -t 0 -u http://ec2-18-208-197-210.compute-1.amazonaws.com:443/play
    ```
* Linux 
    ```
    ./ic20_linux -t 0 -u http://ec2-18-208-197-210.compute-1.amazonaws.com:443/play
    ```
### Frontend
If you want to enjoy our pandemic simulation go [here](http://ec2-18-208-197-210.compute-1.amazonaws.com)

For more run options, please check the [how-to-run-manual](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Usage/00.-How-to-Run).

## Software Architecture
This [section](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Software-Architecture) describes the different used components and
how they communicate with each other.

## Theoretical Overview
We are representing a solution using a Reinforcement Deep Q-Learning method.
If you are interested in how we solved this problem in details, we recommend to get started
in this [page](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Theoretical-Overview/01.-Introduction).

## Future Works
Due to time constraints many other plans that unfortunately couldn't be applied are discussed
in this [section](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Theoretical-Overview/06.-Future-Work).

## Technical Documentation
A detailed description of the technichal documentation could be found
for the [Backend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Backend)
as well as for the [Frontend](https://gitlab.com/omar.araboghli/pandemie/-/wikis/Technical-Documentation/Frontend).

## Wiki
For more information please visit our [Wiki](https://gitlab.com/omar.araboghli/pandemie/-/wikis/pages).
