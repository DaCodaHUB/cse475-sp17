# Adapted from: https://github.com/wbphelps/VKeyboard

import pygame, time, globals, os, sched
from key import VKey
from textinput import TextInput
from pygame.locals import *
from screeninfo import get_monitors

class VirtualKeyboard():
    def __init__(self, screen):

        self.screen = screen
        self.rect = self.screen.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height

        # make a copy of the screen
        self.screenCopy = screen.copy()

        # create a background surface
        self.background = pygame.Surface(self.rect.size)
        self.background.fill((0, 0, 0))  # fill with black
        self.background.set_alpha(127)  # 50% transparent
        # blit background to screen
        self.screen.blit(self.background, (0, 0))

        self.keyW = int(self.w / 12 + 0.5)  # key width with border
        self.keyH = int(self.h / 8 + 0.5)  # key height

        self.x = (self.w - self.keyW * 12) / 2  # centered
        self.y = 5  # stay away from the edges (better touch)
        #        print 'keys x {} w {} keyW {} keyH {}'.format(self.x, self.w, self.keyW, self.keyH)

        pygame.font.init()  # Just in case
        self.keyFont = pygame.font.Font(None, self.keyW)  # keyboard font

        # set dimensions for text input box
        #self.textW = self.w-(self.keyW+2) # leave room for escape key (?)
        self.textW = self.keyW * 12
        self.textH = self.keyH * 2 - 6

        # self.caps = bool(GetKeyState(VK_CAPITAL)) # 0 = no caps lock, 1 = caps lock on
        self.caps = False
        self.shifted = False
        self.keys = []
        #        self.textbox = pygame.Surface((self.rect.width,self.keyH*2))
        self.addkeys()  # add all the keys
        self.paintkeys()  # paint all the keys

        pygame.display.update()

    def run(self, text=''):
        self.text = text
        # create an input text box
        # create a text input box with room for 2 lines of text. leave room for the escape key
        self.input = TextInput(self.screen, self.text, self.x, self.y, self.textW, self.textH)

        # main event loop (hog all processes since we're on top, but someone might want
        # to rewrite this to be more event based...
        while True:
            time.sleep(0.02)  # 10/second is often enough
            events = pygame.event.get()
            if events is not None:
                for e in events:
                    if (e.type == KEYDOWN and e.key > 0):
                        if e.key == K_ESCAPE:
                            return self.text  # Return what we started with
                        elif e.key == K_RETURN:
                            return self.input.text  # Return what the user entered
                        elif e.key == K_LEFT:
                            self.input.deccursor()
                            pygame.display.flip()
                        elif e.key == K_RIGHT:
                            self.input.inccursor()
                            pygame.display.flip()
                        elif e.key == K_BACKSPACE:
                            self.selectkey('<-')
                            self.input.backspace()
                            self.paintkeys()
                        elif e.key == K_SPACE:
                            self.selectkey('space')
                            self.input.addcharatcursor(' ')
                            self.paintkeys()
                        elif e.key == K_RSHIFT or e.key == K_LSHIFT:
                            self.shifted = True
                            self.togglecaps()
                            self.selectkey("shift")
                            self.paintkeys()
                        elif e.key == K_CAPSLOCK:
                            self.caps = True
                            self.togglecaps()
                            self.paintkeys()
                        else:
                            charac = chr(e.key)
                            self.selectkey(charac)
                            self.input.addcharatcursor(charac)
                            self.paintkeys()
                            #print "pressed key {}".format(e.key)

                    elif (e.type == KEYUP and e.key > 0):
                        if (e.key == K_RSHIFT or e.key == K_LSHIFT):
                            self.shifted = False
                            self.togglecaps()
                        elif e.key == K_CAPSLOCK:
                            self.caps = False
                            self.togglecaps()
                        #print "unpressed key {}".format(e.key)
                        self.unselectall()
                        self.paintkeys()
                    elif (e.type == MOUSEBUTTONDOWN):
                        self.selectatmouse()
                    elif (e.type == MOUSEBUTTONUP):
                        if self.clickatmouse():
                            # user clicked enter or escape if returns True
                            self.clear()
                            return self.input.text  # Return what the user entered
                    elif (e.type == MOUSEMOTION):
                        if e.buttons[0] == 1:
                            # user click-dragged to a different key?
                            self.selectatmouse()
                    elif (e.type == pygame.QUIT):
                        return self.text  # Return what we started with

    def selectkey(self, caption):
        for key in self.keys:
            if key.caption.lower() == caption:
                key.selected = True
                key.dirty = True
                return True
        return False

    def unselectall(self, force=False):
        ''' Force all the keys to be unselected
            Marks any that change as dirty to redraw '''
        for key in self.keys:
            if key.selected:
                key.selected = False
                key.dirty = True

    def clickatmouse(self):
        ''' Check to see if the user is pressing down on a key and draw it selected '''
        self.unselectall()
        for key in self.keys:
            keyrect = Rect(key.x, key.y, key.w, key.h)
            if keyrect.collidepoint(pygame.mouse.get_pos()):
                key.dirty = True
                if key.bskey:
                    # Backspace
                    self.input.backspace()
                    self.paintkeys()
                    return False
                if key.spacekey:
                    self.input.addcharatcursor(' ')
                    self.paintkeys()
                    return False
                if key.shiftkey:
                    key.selected = True;
                    key.dirty = True;
                    self.caps = ~self.caps
                    self.togglecaps()
                    self.paintkeys()
                    return False
                if key.enter:
                    return True
                if self.caps:
                    keycap = key.caption.translate(Uppercase)
                else:
                    keycap = key.caption
                self.input.addcharatcursor(keycap)
                self.paintkeys()
                return False

        self.paintkeys()
        return False

    def togglecaps(self):
        for key in self.keys:
            key.dirty = True

    def selectatmouse(self):
        # User has touched the screen - is it inside the textbox, or inside a key rect?
        self.unselectall()
        pos = pygame.mouse.get_pos()
        #        print 'touch {}'.format(pos)
        if self.input.rect.collidepoint(pos):
            #            print 'input {}'.format(pos)
            self.input.setcursor(pos)
        else:
            for key in self.keys:
                keyrect = Rect(key.x, key.y, key.w, key.h)
                if keyrect.collidepoint(pos):
                    key.selected = True
                    key.dirty = True
                    self.paintkeys()
                    return

        self.paintkeys()

    def addkeys(self):  # Add all the keys for the virtual keyboard 
        x = self.x
        y = self.y + self.textH + self.keyH / 4

        row = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
        for item in row:
            onekey = VKey(item, x, y, self.keyW, self.keyH, self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        y += self.keyH  # overlap border
        x = self.x

        row = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']']
        for item in row:
            onekey = VKey(item, x, y, self.keyW, self.keyH, self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        y += self.keyH
        x = self.x

        row = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'']
        for item in row:
            onekey = VKey(item, x, y, self.keyW, self.keyH, self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        x = self.x + self.keyW / 2
        y += self.keyH

        row = ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
        for item in row:
            onekey = VKey(item, x, y, self.keyW, self.keyH, self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        x = self.x + 1
        y += self.keyH + self.keyH / 4

        #        print 'addkeys keyW {} keyH {}'.format(self.keyW, self.keyH)

        onekey = VKey('Shift', x, y, int(self.keyW * 2.5), self.keyH, self.keyFont)
        onekey.special = True
        onekey.shiftkey = True
        self.keys.append(onekey)
        x += onekey.w + self.keyW / 6

        onekey = VKey('Space', x, y, self.keyW * 5, self.keyH, self.keyFont)
        onekey.special = True
        onekey.spacekey = True
        self.keys.append(onekey)
        x += onekey.w + self.keyW / 6

        onekey = VKey('Enter', x, y, int(self.keyW * 2.5), self.keyH, self.keyFont)
        onekey.special = True
        onekey.enter = True
        self.keys.append(onekey)
        x += onekey.w + self.keyW / 3

        onekey = VKey('<-', x, y, int(self.keyW * 1.2 + 0.5), self.keyH, self.keyFont)
        onekey.special = True
        onekey.bskey = True
        self.keys.append(onekey)
        x += onekey.w + self.keyW / 3

    def paintkeys(self):
        ''' Draw the keyboard (but only if they're dirty.) '''
        for key in self.keys:
            key.draw(self.screen, self.background, self.caps ^ self.shifted)
        pygame.display.update()

    def clear(self):
        ''' Put the screen back to before we started '''
        self.screen.blit(self.screenCopy, (0, 0))
        pygame.display.update()


WINDOWSIZE = .75
		
def main():
    pygame.init()

    # create window and center it
    screen = get_monitors().pop()
    screen_width = screen.width
    screen_height = screen.height
    window_width = int(round(screen_width * WINDOWSIZE))
    window_height = int(round(screen_height * WINDOWSIZE))
    # pos_x = screen_width / 2 - window_width / 2
    # pos_y = screen_height - window_height
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)
    # os.environ['SDL_VIDEO_CENTERED'] = '0'

    surf = pygame.display.set_mode([window_width, window_height])
    vkeybd = VirtualKeyboard(surf)
    userinput = vkeybd.run()
    print "User Entered: " + userinput

if __name__ == "__main__":
    main()
