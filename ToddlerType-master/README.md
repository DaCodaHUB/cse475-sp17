ToddlerType 0.2.1
=================

ToddlerType is a game for teaching young children new words, how letters form words(eg. in English, left to right), how to type, and how to spell.

To get started, just run "python typing.py". You can then press any key on the title screen to get to the words. You can then type numbers to set the level of the current word or use the up/down arrow keys to change what level you are playing at.

The program uses a SQLite database which is included. Also included are a json and a csv of the words.

I have a level attribute on each Word document. The idea is that some words are too long or they represent concepts which are too complicated for young children. As it is, all words are set to 0 because I couldn't decide how to objectively decide what level a word should be. So if you are playing this game with your child and see a word that you think is too long or conceptually challenging, you can press a number key to change the level of that word. Then as your child gets
older, you can increase the level at which they are playing by pressing the up arrow key.

Dependencies
============

* Python 2.7
* Pygame
* SQLite3


About Development
=================

I made this game for my son to use. I was inspired by KLettres but found that the lack of reward or fanfare upon success caused him to become bored by it. I also felt that he could learn letters while learning words, so I added a vocabulary.

The current fanfare noises were made by my son, Peregrin Fire. Feel free to replace them with sounds of your own choosing.
