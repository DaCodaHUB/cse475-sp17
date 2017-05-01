 # Adapted from: https://github.com/wbphelps/VKeyboard

# TODO: add autoscroll to textbox, up and down arrow key movement

#Demo:
 #String that lights up the corresponding keys at 1 sec intervals
 #Home row keys are red when no finger is resting on it and turn off when there is a finger resting

import pygame, textwrap
from pygame.locals import *

class TextInput(): # Handles the text input box and manages the cursor
    def __init__(self, screen, text, x, y, w, h):
        self.screen = screen
        self.x = x
        self.y = y

        self.w = w
        self.h = h
        self.rect = Rect(x, y, w, h)
        self.layer = pygame.Surface((self.w, self.h))
        self.background = pygame.Surface((self.w, self.h))
        self.background.fill((0, 0, 0))  # fill with black

        rect = screen.get_rect()
        fsize = int(rect.height / 20 + 0.5)  # font size proportional to screen height
        self.txtFont = pygame.font.SysFont('Courier New', fsize, bold=True)
        # attempt to figure out how many chars will fit on a line - does not work with proportional fonts
        tX = self.txtFont.render("XXXXXXXXXX", 1, (255, 255, 0))  # 10 chars
        rtX = tX.get_rect()  # how big is it?
        self.lineChars = int(self.w / (rtX.width / 10))  # chars per line (horizontal)
        self.lineH = rtX.height  # pixels per line (vertical)
        self.numLines = h / self.lineH # number of visible lines
        #self.lineW = rtX.width / 5 - 4
        print "Num visible lines: {}".format(self.numLines)

        print "number of chars per line: {}".format(self.lineChars)
        self.text = textwrap.wrap(text, self.lineChars)

        self.cursorlayer = pygame.Surface((1, self.lineH * .8))  # thin vertical line
        self.cursorlayer.fill((255, 255, 255))  # white vertical line
        self.cursorlayer.set_alpha(255 * .8) # transparency
        self.cursorvis = True

        lastLineIndex = len(self.text)-1
        self.cursorX = len(self.text[lastLineIndex])
        self.cursorY = lastLineIndex

        self.draw()

    def draw(self): # Draw this text input box
        self.layer.fill((0, 0, 0))  # clear the layer
        pygame.draw.rect(self.layer, (255, 255, 255), (0, 0, self.w, self.h), 1)  # draw the box

        print "TEXT: {}".format(self.text)
        lines = len(self.text)
        if lines > self.numLines: # only show the last lines visible, wrapping text
            visibleLines = self.text[lines - self.numLines : lines]
        else:
            visibleLines = self.text[:lines]

        for i in range(len(visibleLines)):
            t1 = self.txtFont.render(visibleLines[i], 1, (255, 255, 0))
            self.layer.blit(t1, (4, 4 + i*self.lineH))

        self.screen.blit(self.background, self.rect)
        self.screen.blit(self.layer, self.rect)

        #self.drawcursor()

        pygame.display.update()

    def flashcursor(self): # Toggle visibility of the cursor
        if self.cursorvis:
            self.cursorvis = False
        else:
            self.cursorvis = True

        self.screen.blit(self.background, self.rect)
        self.screen.blit(self.layer, self.rect)

        if self.cursorvis:
            self.drawcursor()
        pygame.display.update()

    def addcharatcursor(self, letter): # Add a character where the cursor is currently located

        # Add case for inserting in the middle

        if(len(self.text) <= self.cursorY):
            self.text.append(letter)
        else:
            self.text[self.cursorY] += letter

        if(len(self.text[self.cursorY]) > self.lineChars):
            splitLines = textwrap.wrap(self.text[self.cursorY], self.lineChars)
            print splitLines
            self.text[self.cursorY] = splitLines[0]
            self.text.append(splitLines[1])
            self.cursorX = len(self.text[len(self.text)-1])# may be bug here
            self.cursorY += 1
        else:
            self.cursorX += 1

        self.draw()

    def backspace(self): # Delete a character before the cursor position
        if len(self.text) == 0: return
        self.text[self.cursorY] = self.text[self.cursorY][:self.cursorX - 1] + self.text[self.cursorY][self.cursorX:]
        if(self.text[self.cursorY] == ''):
            self.text.pop()
        self.deccursor()
        print "Y, X: {} {}".format(self.cursorY, self.cursorX)
        self.draw()
        return

    def deccursor(self): # Move the cursor one space left
        if self.cursorX == 1 and self.cursorY == 0: return
        if self.cursorX == 1:
            self.cursorY -= 1
            self.cursorX = len(self.text[self.cursorY])
        else:
            self.cursorX -= 1
        self.draw()

    def inccursor(self): # Move the cursor one space right (but not beyond the end of the text)
        if self.cursorX == 0 and self.cursorY == 0: return
        if self.cursorX == len(self.text[self.cursorY]):
            self.cursorY += 1
            self.cursorX = 0
        else:
            self.cursorX += 1
        self.draw()

    def drawcursor(self): # Draw the cursor
        # need a way to find the lines that are currently visible

        line = int(self.cursorpos / self.lineChars)  # line number
        if line > 1: line = 1
        x = 4
        y = 4 + self.y + line * self.lineH
        # Calc width of text to this point
        if self.cursorpos > 0:
            linetext = self.text[line * self.lineChars:self.cursorpos]
            rtext = self.txtFont.render(linetext, 1, (255, 255, 255))
            textpos = rtext.get_rect()
            x = x + textpos.width + 1
        self.screen.blit(self.cursorlayer, (x, y))