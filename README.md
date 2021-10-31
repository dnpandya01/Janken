# Janken
---
It's a game of Rock-Paper-Scissor played through the network with the help of Deep Learning for action recognition.</br>
This project was created solely for the purpose of Hackathon hackCBS4.0.
# Table of Contents
---
+ **Technologies**
+ **Setup**
+ **Status**
+ **Demo**

# Technologies
---
Weights files required:-</br>
[Weight file](https://drive.google.com/file/d/1gNxZ09NeJhaZmsE8fvLRtNQTNfvsEYbK/view)</br>
Make sure to keep this file in the same hierarchy as the other files in this repository. 

Project is created with:-
+ python 3.9.0
+ tensorFlow 2.5.0
+ Flask 2.0.1
+ keyboard 0.13.5
+ pubnub 5.4.0
+ opencv-python 4.5.3.56


# Setup
---
This game works on a peer - peer connection and hence it requires to be run on two distinct machines simultaneously.</br>
Both the parties need to download all the files except app.py and opp.py</br>
Player 1 needs to download app.py whereas, Player 2 needs to download opp.py 


To run this project on your machine perform the following steps:-

Step 1: Install all the technologies which are mentioned under Technologies Section.</br>
        Example</br>
        `pip install tensorflow==2.5.0`

Step 2: Download all the files from this repository and keep them in the same hierarchical order.

Step 3: Player 1 has to execute app.py</br> 
        Example</br>
        `python app.py`</br>
        Player 2 has to execute opp.py</br>
        Example</br>
        `python opp.py`
        
Step 4: Run the localhost on your machine by pasting the address provided by the command prompt in your browser.

Step 5: Perform the actions within blue box.</br>
        When the camera stops, press spacebar to get the result.</br>
        Keep in mind that the spacebar needs to be pressed simultaneously on both the machines within an interval of five seconds.</br>
        Enjoy the game!

# Status
---
**Completed**


# Demo
---
Demo is available [here](https://www.youtube.com/watch?v=E4M2RIxXBBU&ab_channel=PandyaDharv)
