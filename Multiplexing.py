import sys
import parallel
import time
from graphics import *
from button import Button

class ParallelD(object):
    def __init__(self):
        '''Inicia y pone blanco el display.'''
        win = GraphWin("Marquesina")
        win.setCoords(0,0,6,7)
        win.setBackground("gray")
        self.win = win
        self.__createButtons()
        self.__createDisplay()
        self.display1 = [' '] * 4
        self._update()

    def __createButtons(self):
        bSpecs = [(1,2,'7'), (2.7,2,'8'), (4.4,2,'9'),
                  (1,3,'4'), (2.7,3,'5'), (4.4,3,'6'),
                  (1,4,'1'), (2.7,4,'2'), (4.4,4,'3')]
        self.buttons = []
        for (cx,cy,label) in bSpecs:
            self.buttons.append(Button(self.win,Point(cx,cy),1.5,.7,label))
        # create the larger = button
        self.buttons.append(Button(self.win, Point(4.8,1), 2, .7, "0"))
        self.buttons.append(Button(self.win, Point(1.1,1), 1.8, .8, "ENTER"))
        self.buttons.append(Button(self.win, Point(2.9,1), 1.5, .8, "Clear"))
        # activate all buttons
        for b in self.buttons:
            b.activate()

    def __createDisplay(self):
        bg = Rectangle(Point(0.5,5.5), Point(5.5,6.5))
        bg.setFill('white')
        bg.draw(self.win)
        text = Text(Point(3,6), "0")
        text.draw(self.win)
        text.setFace("helvetica")
        text.setStyle("bold")
        text.setSize(16)
        self.display = text

    def getButton(self):
        while True:
            p = self.win.getMouse()
            for b in self.buttons:
                if b.clicked(p):
                    return b.getLabel()

    def setData(self,data):
        '''Bits 0-3 son el numero.
           Bits 4-7 son las posiciones.
        '''
        self.display = [' '] * 4
        value = data & 0xF
        if data & 0x10:
            self.display[0] = str(value)
        if data & 0x20:
            self.display[1] = str(value)
        if data & 0x40:
            self.display[2] = str(value)
        if data & 0x80:
            self.display[3] = str(value)
        self._update()

    def processButton(self, key):
        p = parallel.Parallel()
        if key == '1':
            texto=self.display.getText()
            self.display.setText(texto+"1")

        elif key == '2':
            texto=self.display.getText()
            self.display.setText(texto+"2")
                  
        elif key == '3':
            texto=self.display.getText()
            self.display.setText(texto+"3")

        elif key == '4':
            texto=self.display.getText()
            self.display.setText(texto+"4")

        elif key == '5':
            texto=self.display.getText()
            self.display.setText(texto+"5")

        elif key == '6':
            texto=self.display.getText()
            self.display.setText(texto+"6")

        elif key == '7':
            texto=self.display.getText()
            self.display.setText(texto+"7")

        elif key == '8':
            texto=self.display.getText()
            self.display.setText(texto+"8")

        elif key == '9':
            texto=self.display.getText()
            self.display.setText(texto+"9")

        elif key == '0':
            texto=self.display.getText()
            self.display.setText(texto+"0")

        elif key == 'Clear':
            self.display.setText("")

        if key == 'ENTER':
            text=self.display.getText()
            nums=text
            stream = 'XXXX' + nums + 'XXXX'
            data = [0] * 4
            for i in range(len(stream)-3):
                # Precompute data
                for pos in range(4):
                    value = stream[i+pos]
                    data[pos] = 0 if value == 'X' else (1<<(pos+4)) + int(value)
                # "Flicker" the display...
                for delay in xrange(1000):
                    # Display each position briefly.
                    for d in data:
                        p.setData(d)
                        time.sleep(0.0001)
                # Clear the display when done
                p.setData(0)

    def _update(self):
        '''Manda a los displays.'''
        sys.stdout.write(''.join(self.display1) + '\r')
        time.sleep(0.0001)

    def run(self):
        # Infinite 'event loop' to process button clicks.
        while True:
            key = self.getButton()
            self.processButton(key)

if __name__ == '__main__':
    disp=ParallelD()
    disp.run()
