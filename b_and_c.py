# -*- coding: utf-8 -*-

import sys
import random
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class game(QObject):
    new_str = Signal(str)
    game_winn = Signal(int)
    ans_str = Signal(str)
    
    
    def __init__(self):
        QObject.__init__(self)
        
        
    def new(self):
        self.corr = False
        self.last = ''        
        self.cou = 0
        self.ans = '0000'
        while self.ans[0] == '0' or len(set(self.ans)) != 4:
            self.ans = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 4))
        print(self.ans)
        self.new_str.emit("")
            
        
    def setValue(self, value):
        try:
            int(value)
            if value[0] not in ('1', '2', '3', '4', '5', '6', '7', '8', '9') or len(value) != 4 or len(set(value)) != 4:
                self.corr = False
                return
            else:
                self.user_num = value
                self.corr = True
        except:
            self.corr = False
            return
        
        
    def check(self):
        if not self.corr:
            self.new_str.emit("Некорректный ввод")
        else:
            if self.last == self.user_num:
                return
            self.last = self.user_num
            self.cou += 1
            cow = 0
            bull = 0
            for i in range(4):
                if self.ans[i] == self.user_num[i]:
                    bull += 1
                elif self.user_num[i] in self.ans:
                    cow += 1
            if bull == 4:
                self.new_str.emit("Правильно!\nВаше число ходов: " + str(self.cou))
                self.game_winn.emit(self.cou)
            else:
                self.new_str.emit("быков: " + str(bull) + ', ' + ' коров: ' + str(cow) + '.')
            
            
    def show_ans(self):
        self.new_str.emit("Правильный ответ: " + self.ans)
    
    
    
      
 
    
    



app = QApplication(sys.argv)
Window_1 = QMainWindow()
Window_1.resize(300, 300)
Window_2 = QMainWindow()
Window_2.resize(300, 300)
Window_2.hide()
Text_N = QLabel("БЫКИ И КОРОВЫ:   УГАДЫВАЙ", Window_1)
Text_N.setGeometry(60, 0, 100000, 40)

LineEdit = QLineEdit(Window_1)
LineEdit.setGeometry(10, 80, 100, 30)
LineEdit.hide()
Text = QLabel(Window_1)
Text.setGeometry(120, 120, 100000, 30)



t_game = game()



new_game_but = QPushButton("Новая игра", Window_1)
new_game_but.setGeometry(10, 40, 100, 30)


give_up_but = QPushButton("Сдаться", Window_1)
give_up_but.setGeometry(10, 40, 100, 30)
give_up_but.hide()


check_but = QPushButton("Проверить", Window_1)
check_but.setGeometry(10, 120, 100, 30)
check_but.clicked.connect(t_game.check)
check_but.hide()

new_game_but.clicked.connect(t_game.new)
new_game_but.clicked.connect(new_game_but.hide)
new_game_but.clicked.connect(give_up_but.show)
new_game_but.clicked.connect(LineEdit.show)
new_game_but.clicked.connect(check_but.show)


give_up_but.clicked.connect(new_game_but.show)
give_up_but.clicked.connect(t_game.show_ans)
give_up_but.clicked.connect(give_up_but.hide)
give_up_but.clicked.connect(LineEdit.hide)
give_up_but.clicked.connect(check_but.hide)

t_game.new_str.connect(Text.setText)

t_game.game_winn.connect(new_game_but.show)
t_game.game_winn.connect(give_up_but.hide)
t_game.game_winn.connect(check_but.hide)
t_game.game_winn.connect(LineEdit.hide)
LineEdit.textChanged.connect(t_game.setValue)

LineEdit.textChanged.connect(t_game.setValue)



ch_game_but = QPushButton("Другой\n режим", Window_1)
ch_game_but.setGeometry(10, 160, 100, 50)
ch_game_but.clicked.connect(Window_2.show)
ch_game_but.clicked.connect(Window_1.hide)



class game_mash(QObject):
    new_str = Signal(str)
    game_winn = Signal(bool)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.corr = False
        
        
    def new(self):
        line = [str(i) for i in range(1, 10)]
        for q in range(3):
            new = []
            for i in range(10):
                for pref in line:
                    if str(i) not in pref:
                        new.append(pref + str(i))
            line = new[::]        
        self.cou = 0
        self.line = line[::]
        self.new_str.emit("Я думаю... " + self.line[0])
            
        
    def setValue(self, value):
        try:
            self.b, self.c = map(int, value.split())
            self.corr = True
        except:
            self.corr = False
            return
        
        
    def check(self):
        if not self.corr:
            self.new_str.emit("Некорректный ввод")
        else:
            if self.b != 4:
                neww = []
                for i in range(1, len(self.line)):
                    bull = 0
                    cow = 0
                    for j in range(4):
                        if self.line[0][j] == self.line[i][j]:
                            bull += 1
                        elif self.line[i][j] in self.line[0]:
                            cow += 1        
                    if cow == self.c and bull == self.b:
                        neww.append(self.line[i])
                self.line = neww[::]
                if len(self.line) == 0:
                    self.new_str.emit("ТЫ ЧТО-ТО НАПУТАЛ.")
                    self.game_winn.emit(True)
                else:
                    self.new_str.emit("Я думаю... " + self.line[0])
            else:
                self.new_str.emit("Я УГАДАЛ! УРА!")
                self.game_winn.emit(True)
            


            
th_game = game_mash()

ch_game_but2 = QPushButton("Другой\n режим", Window_2)
ch_game_but2.setGeometry(10, 160, 100, 50)
ch_game_but2.clicked.connect(Window_1.show)
ch_game_but2.clicked.connect(Window_2.hide)


Text_N2 = QLabel("БЫКИ И КОРОВЫ: ЗАГАДЫВАЙ", Window_2)
Text_N2.setGeometry(60, 0, 100000, 40)



Text2 = QLabel(Window_2)
Text2.setGeometry(120, 120, 100000, 30)

Text3 = QLabel("Введите через пробел\n число быков и число кров.", Window_2)
Text3.setGeometry(10, 30, 100000, 50)
Text3.hide()


LineEdit2 = QLineEdit(Window_2)
LineEdit2.setGeometry(10, 80, 100, 30)
LineEdit2.hide()

new_game_but2 = QPushButton("Новая игра", Window_2)
new_game_but2.setGeometry(10, 40, 100, 30)

check_but2 = QPushButton("Ответить", Window_2)
check_but2.setGeometry(10, 120, 100, 30)
check_but2.hide()


new_game_but2.clicked.connect(LineEdit2.show)
new_game_but2.clicked.connect(Text3.show)
new_game_but2.clicked.connect(check_but2.show)
new_game_but2.clicked.connect(new_game_but2.hide)
new_game_but2.clicked.connect(th_game.new)

check_but2.clicked.connect(th_game.check)
th_game.new_str.connect(Text2.setText)
th_game.game_winn.connect(new_game_but2.show)
th_game.game_winn.connect(check_but2.hide)
th_game.game_winn.connect(LineEdit2.hide)
th_game.game_winn.connect(Text3.hide)
LineEdit2.textChanged.connect(th_game.setValue)



Window_1.show()
app.exec_()
