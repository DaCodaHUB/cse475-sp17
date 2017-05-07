'''
	Adapted from https://github.com/NoOutlet/ToddlerType

	To get started, just run "python typing.py". You can then press any key on the title screen to get to the words.
	Use the up/down arrow keys to change the level and difficulty of the words.
	The program uses a SQLite database which is included. Also included are a json and a csv of the words.
	
	Dependencies
	============
	* Python 2.7
	* Pygame
	* SQLite3
'''

import random
import sqlite3
import pygame
import sys
import os
import threading
import time
from pygame.locals import *
from string import maketrans

basepath = os.path.dirname(os.path.abspath(__file__))
connection = sqlite3.connect(basepath + "/sentences.db")

# could remove the hard-coded dimensions
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
LIGHTBLUE = (20, 20, 175)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
TEXTHIGHLIGHT = LIGHTBLUE
SHIFTED = False

Uppercase = maketrans("abcdefghijklmnopqrstuvwxyz`1234567890-=[]\;\',./",
                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?')

def main():
    global DISPLAYSURF, BIGFONT, BIGFONT, SMALLFONT, LEVEL, CUR, ERROR_SOUND, ERRORS, WORDS, WORDS_PER_MIN
    pygame.init()
    ERROR_SOUND = pygame.mixer.Sound("error.wav")

    pygame.event.set_allowed(None)
    pygame.event.set_allowed([KEYUP, KEYDOWN, QUIT])
    DISPLAYSURF = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT], pygame.FULLSCREEN)
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 25)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 40)
    LEVEL = 0
    ERRORS = 0
    WORDS = 0
    WORDS_PER_MIN = 0.0
    TITLE = "Intermediate Mode"

    pygame.display.set_caption(TITLE)

    show_title_screen(TITLE)
    pygame.event.clear()
    event = pygame.event.wait()
    update_timer(time.time())

    while True:
        CUR = connection.cursor()
        CUR.execute("SELECT * FROM sentences WHERE level = " + str(LEVEL))
        current_level = LEVEL
        wordArray = list(CUR.fetchall())
        random.shuffle(wordArray)

        for word in wordArray:
            if current_level != LEVEL:
                break

            show_word(word)
            WORDS += 1

            pygame.display.update()
            #pygame.time.wait(1000)
    connection.close()


def make_text_objs(text, font, fontcolor):
    surf = font.render(text, True, fontcolor)
    return surf, surf.get_rect()


def show_word(word):
    global LEVEL, ERRORS, WORDS, SHIFTED
    text = word[0]
    DISPLAYSURF.fill(BGCOLOR)
    typed = ''
    to_type = text

    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), SMALLFONT, TEXTCOLOR)
    level_rect.topleft = (10, 10)
    DISPLAYSURF.blit(level_surf, level_rect)

    error_surf, error_rect = make_text_objs('Errors: ' + str(ERRORS), SMALLFONT, TEXTCOLOR)
    error_rect.center = (int(WINDOWWIDTH / 2), level_rect.center[1])
    DISPLAYSURF.blit(error_surf, error_rect)

    word_level_surf, word_level_rect = make_text_objs('Words/Min: %.1f' % WORDS_PER_MIN, SMALLFONT, TEXTCOLOR)
    word_level_rect.topright = (WINDOWWIDTH - 10, 10)
    DISPLAYSURF.blit(word_level_surf, word_level_rect)

    word_surf, word_rect = make_text_objs('Words: ' + str(WORDS), SMALLFONT, TEXTCOLOR)
    word_rect.bottomleft = (10, WINDOWHEIGHT - 10)
    DISPLAYSURF.blit(word_surf, word_rect)

    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 2, int(WINDOWHEIGHT / 2) - 2)
    DISPLAYSURF.blit(title_surf, title_rect)

    while typed != text:
        next_letter = to_type[0]
        print "light up letter: {}".format(next_letter)

        pygame.event.clear()
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and (event.key == K_RSHIFT or event.key == K_LSHIFT):
                SHIFTED = True
                print SHIFTED
            elif event.type == KEYUP and event.key > 0:

                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RSHIFT or event.key == K_LSHIFT:
                    SHIFTED = False
                    print SHIFTED
                elif event.key == K_UP: # up a level
                    LEVEL = min(7, LEVEL + 1)
                    level_surf, level_rect = make_text_objs('LevelXX: ' + str(LEVEL), SMALLFONT, TEXTCOLOR)
                    level_surf.fill(BGCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), SMALLFONT, TEXTCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                elif event.key == K_DOWN: # down a level
                    LEVEL = max(0, LEVEL - 1)
                    level_surf, level_rect = make_text_objs('LevelXX: ' + str(LEVEL), SMALLFONT, TEXTCOLOR)
                    level_surf.fill(BGCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), SMALLFONT, TEXTCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                elif event.key < 256:
                    charac = chr(event.key)
                    if SHIFTED:
                        charac = chr(event.key).translate(Uppercase)
                    #print "Pygame Name: {}".format(pygame.key.name(event.key))
                    print "Charac: {}".format(charac)
                    if(charac == next_letter):
                        break

                    ERROR_SOUND.play()
                    ERRORS += 1
                    #print "Expected key: {}\tGot key: {}".format(next_lffdddetter, pygame.key.name(event.key))
                    error_surf, error_rect = make_text_objs('ErrorsXX: ' + str(ERRORS), SMALLFONT, TEXTCOLOR)
                    error_surf.fill(BGCOLOR)
                    error_rect.center = (int(WINDOWWIDTH / 2), level_rect.center[1])
                    DISPLAYSURF.blit(error_surf, error_rect)
                    error_surf, error_rect = make_text_objs('Errors: ' + str(ERRORS), SMALLFONT, TEXTCOLOR)
                    error_rect.center = (int(WINDOWWIDTH / 2), level_rect.center[1])
                    DISPLAYSURF.blit(error_surf, error_rect)

        to_type = to_type[1:]
        typed = typed + next_letter
        typed_surf, typed_rect = make_text_objs(typed, BIGFONT, TEXTHIGHLIGHT)
        DISPLAYSURF.blit(typed_surf, title_rect)


def show_title_screen(text):
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 2, int(WINDOWHEIGHT / 2) - 2)
    DISPLAYSURF.blit(title_surf, title_rect)

    pygame.display.update()

# runs in separate thread and shows the time on the screen
def update_timer(start):
    global DISPLAYSURF, WORDS, WORDS_PER_MIN
    t = threading.Timer(.1, update_timer, (start,))
    t.daemon = True
    t.start()
    #print "TIME: {}".format(time.time() - start)
    difference = int(time.time() - start)
    time_surf, time_rect = make_text_objs('TimeXX: ' + str(difference), SMALLFONT, TEXTCOLOR)
    time_surf.fill(BGCOLOR)
    time_rect.bottomright = (WINDOWWIDTH - 10, WINDOWHEIGHT - 10)
    DISPLAYSURF.blit(time_surf, time_rect)
    time_surf, time_rect = make_text_objs('Time: ' + str(difference), SMALLFONT, TEXTCOLOR)
    time_rect.bottomright = (WINDOWWIDTH - 10, WINDOWHEIGHT - 10)
    DISPLAYSURF.blit(time_surf, time_rect)

    if(difference > 0 and difference % 5 == 0): # update words per min every 5s
        WORDS_PER_MIN = float(WORDS) / difference * 60
        word_level_surf, word_level_rect = make_text_objs('Words/MinXX: %.1f' % WORDS_PER_MIN, SMALLFONT, TEXTCOLOR)
        word_level_surf.fill(BGCOLOR)
        word_level_rect.topright = (WINDOWWIDTH - 10, 10)
        DISPLAYSURF.blit(word_level_surf, word_level_rect)
        word_level_surf, word_level_rect = make_text_objs('Words/Min: %.1f' % WORDS_PER_MIN, SMALLFONT, TEXTCOLOR)
        word_level_rect.topright = (WINDOWWIDTH - 10, 10)
        DISPLAYSURF.blit(word_level_surf, word_level_rect)

    pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
