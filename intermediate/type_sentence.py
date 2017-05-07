# adapted from https://github.com/NoOutlet/ToddlerType

import random, sqlite3, pygame, sys, textwrap, os, threading, time
from pygame.locals import *
from os import listdir
from os.path import isfile, join

basepath = os.path.dirname(os.path.abspath(__file__))
path = basepath + "/Sentences/Tests/"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

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

def main():
    global DISPLAYSURF, BIGFONT, BIGFONT, SMALLFONT, LEVEL, CUR, ERROR_SOUND, ERRORS, WORDS, WORDS_PER_MIN, LINES
    pygame.init()
    ERROR_SOUND = pygame.mixer.Sound("error.wav")

    pygame.event.set_allowed(None)
    pygame.event.set_allowed([KEYUP, QUIT])
    DISPLAYSURF = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT], pygame.FULLSCREEN)
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 25)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 40)
    LEVEL = 0
    ERRORS = 0
    WORDS = 0
    WORDS_PER_MIN = 0.0
    TITLE = "Sentences"

    file = random.choice(onlyfiles)
    f = open(path + file, "r")
    contents = f.read()
    LINES = textwrap.wrap(contents, 40)

    pygame.display.set_caption(TITLE)

    show_title_screen(TITLE)
    pygame.event.clear()
    event = pygame.event.wait()
    update_timer(time.time())

    while True:
        for i in range(0, len(LINES), 3):
            showLines(LINES[i : i+3])

            pygame.display.update()
            #pygame.time.wait(1000)


def make_text_objs(text, font, fontcolor):
    surf = font.render(text, True, fontcolor)
    return surf, surf.get_rect()


def showLines(threeLines):
    global LEVEL, ERRORS, WORDS
    print threeLines

    text = threeLines[0] + "\n" + threeLines[1] + "\n" + threeLines[2]
    DISPLAYSURF.fill(BGCOLOR)
    typed = ''
    to_type = text
    print "TEXT: {}".format(text)

    '''
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



    title_surf, title_rect = make_text_objs(text.upper(), BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 2, int(WINDOWHEIGHT / 2) - 2)
    DISPLAYSURF.blit(title_surf, title_rect)
    '''

    title_surf, title_rect = make_text_objs(text.upper(), BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
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
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif pygame.key.name(event.key) == next_letter:
                    break
                elif pygame.key.name(event.key) != "unknown key":
                    ERROR_SOUND.play()
                    ERRORS += 1
                    print "Expected key: {}\tGot key: {}".format(next_letter, pygame.key.name(event.key))
                    '''
                    error_surf, error_rect = make_text_objs('ErrorsXX: ' + str(ERRORS), SMALLFONT, TEXTCOLOR)
                    error_surf.fill(BGCOLOR)
                    error_rect.center = (int(WINDOWWIDTH / 2), level_rect.center[1])
                    DISPLAYSURF.blit(error_surf, error_rect)
                    error_surf, error_rect = make_text_objs('Errors: ' + str(ERRORS), SMALLFONT, TEXTCOLOR)
                    error_rect.center = (int(WINDOWWIDTH / 2), level_rect.center[1])
                    DISPLAYSURF.blit(error_surf, error_rect)
                    '''
                    

        to_type = to_type[1:]
        typed = typed + next_letter
        typed_surf, typed_rect = make_text_objs(typed.upper(), BIGFONT, TEXTHIGHLIGHT)
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
