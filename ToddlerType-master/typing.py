# Toddler Type
# By Jon Anderson squiggs@theskedge.com

import random
import sqlite3
import pygame
import sys
import os
import locale
from pygame.locals import *

basepath = os.path.dirname(os.path.abspath(__file__))
connection = sqlite3.connect(basepath + "/words.db")

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

def main():
    global DISPLAYSURF, BIGFONT, TITLEFONT, LEVEL, CUR
    pygame.init()

    pygame.event.set_allowed(None)
    pygame.event.set_allowed([KEYUP, QUIT])
    DISPLAYSURF = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT], pygame.FULLSCREEN)
    TITLEFONT = pygame.font.Font('freesansbold.ttf', 60)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 160)
    LEVEL = 0
    TITLE = "Beginner Mode"

    pygame.display.set_caption(TITLE)

    show_title_screen(TITLE)
    pygame.event.clear()
    event = pygame.event.wait()

    while True:
        CUR = connection.cursor()
        CUR.execute("SELECT * FROM words WHERE language = 'eng' AND level = " + str(LEVEL))
        current_level = LEVEL
        wordArray = list(CUR.fetchall())
        random.shuffle(wordArray)
        for word in wordArray:
            if current_level != LEVEL:
                break

            show_word(word)

            pygame.display.update()
            #pygame.time.wait(1000)
    connection.close()


def make_text_objs(text, font, fontcolor):
    surf = font.render(text, True, fontcolor)
    return surf, surf.get_rect()


def show_word(word):
    global LEVEL
    text = word[0]
    DISPLAYSURF.fill(BGCOLOR)
    typed = ''
    to_type = text

    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), TITLEFONT, TEXTCOLOR)
    level_rect.topleft = (10, 10)
    DISPLAYSURF.blit(level_surf, level_rect)

    #word_level_surf, word_level_rect = make_text_objs('Word: ' + str(int(word[1])), TITLEFONT, TEXTCOLOR)
    #word_level_rect.topright = (WINDOWWIDTH - 10, 10)
    #DISPLAYSURF.blit(word_level_surf, word_level_rect)

    title_surf, title_rect = make_text_objs(text.upper(), BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    title_surf, title_rect = make_text_objs(text.upper(), BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 2, int(WINDOWHEIGHT / 2) - 2)
    DISPLAYSURF.blit(title_surf, title_rect)

    while typed != text:
        next_letter = to_type[0]

        pygame.event.clear()
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif pygame.key.name(event.key) == next_letter:
                    break
                elif event.key == K_UP:
                    LEVEL = min(5, LEVEL + 1)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), TITLEFONT, TEXTCOLOR)
                    level_surf.fill(BGCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), TITLEFONT, TEXTCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                elif event.key == K_DOWN:
                    LEVEL = max(0, LEVEL - 1)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), TITLEFONT, TEXTCOLOR)
                    level_surf.fill(BGCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                    level_surf, level_rect = make_text_objs('Level: ' + str(LEVEL), TITLEFONT, TEXTCOLOR)
                    level_rect.topleft = (10, 10)
                    DISPLAYSURF.blit(level_surf, level_rect)
                elif K_0 <= event.key <= K_7:
                    newlevel = int(pygame.key.name(event.key))
                    CUR.execute("UPDATE words SET level = " + str(newlevel) + " WHERE word = '" + word[0] + "'")
                    word_level_surf, word_level_rect = make_text_objs('Word: ' + str(newlevel), TITLEFONT, TEXTCOLOR)
                    word_level_rect.topright = (WINDOWWIDTH - 10, 10)
                    word_level_surf.fill(BGCOLOR)
                    DISPLAYSURF.blit(word_level_surf, word_level_rect)
                    word_level_surf, word_level_rect = make_text_objs('Word: ' + str(newlevel), TITLEFONT, TEXTCOLOR)
                    word_level_rect.topright = (WINDOWWIDTH - 10, 10)
                    DISPLAYSURF.blit(word_level_surf, word_level_rect)

        to_type = to_type[1:]
        typed = typed + next_letter
        typed_surf, typed_rect = make_text_objs(typed.upper(), BIGFONT, TEXTHIGHLIGHT)
        DISPLAYSURF.blit(typed_surf, title_rect)


def show_title_screen(text):
    title_surf, title_rect = make_text_objs(text, TITLEFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    title_surf, title_rect = make_text_objs(text, TITLEFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 2, int(WINDOWHEIGHT / 2) - 2)
    DISPLAYSURF.blit(title_surf, title_rect)

    pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
