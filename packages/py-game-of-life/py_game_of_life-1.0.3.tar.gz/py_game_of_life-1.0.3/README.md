# Conway's Game of Life 


![Photo from the game](game_screenshot.png)


This is Game of Live game simulation, created with pygame

### The game have few simple rules 

* Every cell have 8 neighbours cells 
* Any live cell with fewer than two, or more than three  live  neighbours cells, dies 
* Any live cell with two or three live neighbours, live to next generation 
* Any dead cell with exactly three live neighbours becomes live next generation 

In this version I considered the end of each edge to be the start of the opposite edge, this way we won't have  shapes stuck at the edges 

## Inispiration 
This project is inspired from [DevDungeon's Video](https://www.youtube.com/watch?v=VNAU7HH4QRw)

Installation
-------------------

Install with Pip:

    pip install py_game_of_life


Install from the source:

    pythom setup.py install

Running
--------

Run via launch script installed with pip:

    py_game_of_life

Run as a python module:

    pythom -m  py_game_of_life

Controls
---------

#### press `s` to pause and resume the game
#### press `r` to randomize and start over
#### press `q` to quit

Source Code
--------------

https://github.com/BodaSadalla98/Cookbook/tree/main/python/game_of_live

