[FlapPyBird](https://github.com/Jassu7082/FlapPyBird)
===============

A Flappy Bird Clone made using [python-pygame][pygame]



[pygame]: http://www.pygame.org
[one-file-game]: https://github.com/sourabhv/FlapPyBird/blob/038359dc6122f8d851e816ddb3e7d28229d585e5/flappy.py

Game Description
---------------------------
We are employing computer vision to recognize specific hand movements, which correspond to the birds' jumps in the flappy-bird game.
Below is the identified image of the hand. The movement captured in this image's frames helps identify the specific gestures needed to play the game.

<img src="https://github.com/Jassu7082/FlapPyBird/assets/93179274/e7e5d06a-a1ff-4217-af6f-4e178813ea1a" alt="FlapPyBird Image" width="500" height="400">


How to play
---------------------------
1. The primary rule of Flappy Bird is to navigate the bird through obstacles without touching them or the ground.

2. We maneuver the bird by making a specific hand gesture —> Touching the tips of the index and thumb fingers to form an "O" shape.

3. Ensure adequate lighting conditions before playing to ensure a seamless gameplay experience.

Setup (as tested on Windows)
---------------------------

1. Install Python 3 from [here](https://www.python.org/download/releases/) 

2. Run `make init` (this will install pip packages, use virtualenv or something similar if you don't want to install globally)

3. Use this code to install the required libraries to play `pip install pygame opencv-python-headless mediapipe numpy` .

4. Allow the camera permissions to play.

5. Run `main.py` to play the game. 

6. Use <kbd>&uarr;</kbd> or <kbd>Space</kbd> key to play and <kbd>Esc</kbd> to close the game.

7. To play the game in the browser, you can optionally use `make web` command (pygbag).

   

Notable forks
-------------
- [FlapPy touch to control the bird](https://github.com/Jassu7082/FlapPyBird)
- [FlapPyBlink Blink to control the bird](https://github.com/sero583/FlappyBlink)
- [FlappyBird Fury Mode](https://github.com/Cc618/FlapPyBird)
- [FlappyBird Model Predictive Control](https://github.com/philzook58/FlapPyBird-MPC)
- [FlappyBird OpenFrameworks Port](https://github.com/TheLogicMaster/ofFlappyBird)
- [FlappyBird On Quantum Computing](https://github.com/WingCode/QuFlapPyBird)

Made something awesome from FlapPyBird? Add it to the list :)


Demo
----------


https://github.com/Jassu7082/FlapPyBird/assets/93179274/1986222a-ca05-4fac-b1d4-20e2fff2e7db




