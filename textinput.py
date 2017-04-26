# Adapted from: https://github.com/wbphelps/VKeyboard

# TODO: add autoscroll to textbox

import pygame
from pygame.locals import *

class TextInput(): # Handles the text input box and manages the cursor
    def __init__(self, screen, text, x, y, w, h):
        self.screen = screen
        self.text = text
        self.cursorpos = len(text)
        self.x = x
        self.y = y

        self.w = w
        self.h = h
        self.rect = Rect(x, y, w, h)
        self.layer = pygame.Surface((self.w, self.h))
        self.background = pygame.Surface((self.w, self.h))
        self.background.fill((0, 0, 0))  # fill with black

        rect = screen.get_rect()
        fsize = int(rect.height / 12 + 0.5)  # font size proportional to screen height
        self.txtFont = pygame.font.SysFont('Courier New', fsize, bold=True)
        # attempt to figure out how many chars will fit on a line
        # this does not work with proportional fonts
        tX = self.txtFont.render("XXXXXXXXXX", 1, (255, 255, 0))  # 10 chars
        rtX = tX.get_rect()  # how big is it?
        self.lineChars = int(self.w / (rtX.width / 10)) - 1  # chars per line (horizontal)
        self.lineH = rtX.height  # pixels per line (vertical)
        #        print 'txtinp: width={} rtX={} font={} lineChars={} lineH={}'.format(self.w,rtX,fsize, self.lineChars,self.lineH)

        self.cursorlayer = pygame.Surface((2, 22))  # thin vertical line
        self.cursorlayer.fill((255, 255, 255))  # white vertical line
        self.cursorvis = True

        self.cursorX = len(text) % self.lineChars
        self.cursorY = int(len(text) / self.lineChars)  # line 1

        self.draw()

    def draw(self):
        ''' Draw the text input box '''
        self.layer.fill((0, 0, 0))  # clear the layer
        pygame.draw.rect(self.layer, (255, 255, 255), (0, 0, self.w, self.h), 1)  # draw the box

        length = len(self.text)
        if length > 2*self.lineChars: # only show the last 2 lines, wrapping text
            txt1 = self.text[length - 2*self.lineChars : length - self.lineChars]  # line 1
            txt2 = self.text[length - self.lineChars:]  # line 2
        else:
            txt1 = self.text[:self.lineChars]  # line 1
            txt2 = self.text[self.lineChars:]  # line 2

        t1 = self.txtFont.render(txt1, 1, (255, 255, 0))  # line 1
        self.layer.blit(t1, (4, 4))
        t2 = self.txtFont.render(txt2, 1, (255, 255, 0))  # line 2
        self.layer.blit(t2, (4, 4 + self.lineH))

        self.screen.blit(self.background, self.rect)
        self.screen.blit(self.layer, self.rect)
        self.drawcursor()

        pygame.display.update()


    def flashcursor(self):
        ''' Toggle visibility of the cursor '''
        if self.cursorvis:
            self.cursorvis = False
        else:
            self.cursorvis = True

        self.screen.blit(self.background, self.rect)
        self.screen.blit(self.layer, self.rect)

        if self.cursorvis:
            self.drawcursor()
        pygame.display.update()

    def addcharatcursor(self, letter):
        ''' Add a character whereever the cursor is currently located '''
        if self.cursorpos < len(self.text):
            # Inserting in the middle
            self.text = self.text[:self.cursorpos] + letter + self.text[self.cursorpos:]
            self.cursorpos += 1
            self.draw()
            return
        self.text += letter
        self.cursorpos += 1
        self.draw()

    def backspace(self):
        ''' Delete a character before the cursor position '''
        if self.cursorpos == 0: return
        self.text = self.text[:self.cursorpos - 1] + self.text[self.cursorpos:]
        self.cursorpos -= 1
        self.draw()
        return

    def deccursor(self):
        ''' Move the cursor one space left '''
        if self.cursorpos == 0: return
        self.cursorpos -= 1
        self.draw()

    def inccursor(self):
        ''' Move the cursor one space right (but not beyond the end of the text) '''
        if self.cursorpos == len(self.text): return
        self.cursorpos += 1
        self.draw()

    def drawcursor(self):
        ''' Draw the cursor '''
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

    def setcursor(self, pos):  # move cursor to char nearest position (x,y)
        line = int((pos[1] - self.y) / self.lineH)  # vertical
        if line > 1: line = 1  # only 2 lines
        x = pos[0] - self.x + line * self.w  # virtual x position
        p = 0
        l = len(self.text)
        while p < l:
            text = self.txtFont.render(self.text[:p + 1], 1, (255, 255, 255))  # how many pixels to next char?
            rtext = text.get_rect()
            textX = rtext.x + rtext.width
            if textX >= x: break  # we found it
            p += 1
        self.cursorpos = p
        self.draw()
