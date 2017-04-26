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

        self.cursorlayer = pygame.Surface((1, self.lineH * .8))  # thin vertical line
        self.cursorlayer.fill((255, 255, 255))  # white vertical line
        self.cursorvis = True

        self.cursorX = len(text) % self.lineChars
        self.cursorY = int(len(text) / self.lineChars)  # line 1

        self.draw()

        #lines = self.__spacelines("Mar. Good now, sit down, and tell me he that knows, Why this same strict and most observant watch So nightly toils the subject of the land, And why such daily cast of brazen cannon And foreign mart for implements of war;", 50);
        #print lines

    def draw(self): # Draw this text input box
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

    def addcharatcursor(self, letter): # Add a character whereever the cursor is currently located
        if self.cursorpos < len(self.text):
            # Inserting in the middle
            self.text = self.text[:self.cursorpos] + letter + self.text[self.cursorpos:]
            self.cursorpos += 1
            self.draw()
            return
        self.text += letter
        self.cursorpos += 1
        self.draw()

    def backspace(self): # Delete a character before the cursor position
        if self.cursorpos == 0: return
        self.text = self.text[:self.cursorpos - 1] + self.text[self.cursorpos:]
        self.cursorpos -= 1
        self.draw()
        return

    def deccursor(self): # Move the cursor one space left
        if self.cursorpos == 0: return
        self.cursorpos -= 1
        self.draw()

    def inccursor(self): # Move the cursor one space right (but not beyond the end of the text)
        if self.cursorpos == len(self.text): return
        self.cursorpos += 1
        self.draw()

    def drawcursor(self): # Draw the cursor
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

    def __spacelines(self, text, width): # fits text into lines of the given width, breaking on spaces
        words = text.split()
        count = len(words)
        offsets = [0]
        for w in words:
            offsets.append(offsets[-1] + len(w))

        minima = [0] + [10 ** 20] * count
        breaks = [0] * (count + 1)

        def cost(i, j):
            w = offsets[j] - offsets[i] + j - i - 1
            if w > width:
                return 10 ** 10 * (w - width)
            return minima[i] + (width - w) ** 2

        def smawk(rows, columns):
            stack = []
            i = 0
            while i < len(rows):
                if stack:
                    c = columns[len(stack) - 1]
                    if cost(stack[-1], c) < cost(rows[i], c):
                        if len(stack) < len(columns):
                            stack.append(rows[i])
                        i += 1
                    else:
                        stack.pop()
                else:
                    stack.append(rows[i])
                    i += 1
            rows = stack

            if len(columns) > 1:
                smawk(rows, columns[1::2])

            i = j = 0
            while j < len(columns):
                if j + 1 < len(columns):
                    end = breaks[columns[j + 1]]
                else:
                    end = rows[-1]
                c = cost(rows[i], columns[j])
                if c < minima[columns[j]]:
                    minima[columns[j]] = c
                    breaks[columns[j]] = rows[i]
                if rows[i] < end:
                    i += 1
                else:
                    j += 2

        n = count + 1
        i = 0
        offset = 0
        while True:
            r = min(n, 2 ** (i + 1))
            edge = 2 ** i + offset
            smawk(range(0 + offset, edge), range(edge, r + offset))
            x = minima[r - 1 + offset]
            for j in range(2 ** i, r - 1):
                y = cost(j + offset, r - 1 + offset)
                if y <= x:
                    n -= j
                    i = 0
                    offset += j
                    break
            else:
                if r == n:
                    break
                i = i + 1

        lines = []
        j = count
        while j > 0:
            i = breaks[j]
            lines.append(' '.join(words[i:j]))
            j = i
        lines.reverse()
        return lines
