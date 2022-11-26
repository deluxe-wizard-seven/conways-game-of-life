# Flappy Plane Game

### Project Description

This is a basic simulation of Conway's Game of Life. `Pygame` module is used in making this project. 

#### Conway's Game of Life

Devised by the British mathematician John Horton Conway, this is an ___evolutionalary game___ which is essentially a ___zero-player game___ in essence, the present states of the "cell" depends on the previous its previous state and its neighbours' states. The "cell" has two states namely ```ALIVE``` and ```DEAD```. The rules are as follows :

- Any live cell with fewer than two live neighbours dies(by underpopulation)
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies(by overpopulation)
- Any dead cell with exactly three live neighbours becomes a live cell(by reproduction)

You can find more about Conway's Game of Life [here](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

### Author

Dipto Bhattacharjee

### Version

1.0.0

### Prerequisites and how to run the game

- ***Python 3.10.8*** or above. You can download Python from [here](https://www.python.org/)
- The dependencies are listed in the _requirements.txt_ file.
- The dependencies can be downloaded using the following command `pip install -r requirements.txt` if `pip` is not installed in your system then you can try out `python -m pip install -r requirements.txt`
- After all these required applications you just have to run the `game.py` file using the following command `python game.py`

### Controls

- ```SPACE``` : To play/pause the simulation
- ```n``` : To generate the next generation
- ```p``` : To generate the previous generation
- ```+``` : To increase the speed of the simulation (MAX SPEED = 1000 fps)
- ```-``` : To decrease the speed of the simulation (MIN SPEED = 1 fps)
- ```r``` : To generate a random group of "living" cells
- ```t``` : To toggle the states of the cells
- ```k``` : Kill all the cells
- ```e``` : Resurrect all the cells back to life
- ```LEFT MOUSE CLICK``` : To make the current cell alive
- ```RIGHT MOUSE CLICK``` : To toggle the state of the current cell