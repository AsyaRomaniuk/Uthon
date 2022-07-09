from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import colorchooser as cs
from CodeTranslatorToPython import Translator
import os


def INPUT():
    global WIDGETTEXTBGCOLOR, t

    def QUIT(event):
        w = tt.get('Ряд:1  Ст:0', END)
        t.destroy()

    try:
        t.destroy()
    except:
        pass
    w = ''
    t = Toplevel(UTHON)
    t.title('Ввід')
    tt = Text(t, font=('Monaco', 14), bg=WIDGETTEXTBGCOLOR)
    tt.pack()
    tt.bind('<Return>', QUIT)
    t.mainloop()
    return w


def PRINT(text):
    global WIDGETTEXTBGCOLOR, t

    try:
        t.destroy()
    except:
        pass

    t = Toplevel(UTHON)
    t.title('Вивід')
    tt = Text(t, font=('Monaco', 14), bg=WIDGETTEXTBGCOLOR)
    tt.insert('1.0', str(text))
    tt.pack()
    tt.config(state=DISABLED)
    t.mainloop()


def COMMANDS():
    return Translator.trn


class WINDOW(Tk):
    def __init__(self, MASTER):
        self.RB = False
        self.MASTER = MASTER
        self.LANGSTATE = True
        MASTER.title("Консоль")
        MASTER.resizable(0, 0)
        MASTER["bg"] = WINDOWTEXTBGCOLOR
        try:
            MASTER.call('wm', 'iconphoto', MASTER._w, PhotoImage(file="python.png"))
        except:
            pass
        self.MASTER_WINDOW_STATE = False
        self.DIRVAR = StringVar()
        self.DIRVAR.set("")
        self.POSITION = StringVar()
        self.POSITION.set("Ряд:1  Ст:0")
        self.MENU = Menu(MASTER)
        self.FILE = Menu(self.MENU, tearoff=0, bg=MENUTEXTBGCOLOR, fg=MENUTEXTCOLOR,
                         font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.FILE.add_command(label="Нове вікно", command=self.NEWWINDOW)
        self.FILE.add_command(label="Новий файл", command=self.NEWFILE, accelerator="F1")
        self.FILE.add_command(label="Відкрити", command=self.OPENFILE, accelerator="F2")
        self.FILE.add_command(label="Зберегти", command=self.SAVEFILE, accelerator="F3")
        self.FILE.add_command(label="Зберегти як...", command=self.SAVEASFILE, accelerator="F4")
        self.FILE.add_command(label="Закрити", command=self.CLOSEFILE, accelerator="F9")
        self.OPTIONS = Menu(self.MENU, tearoff=0, bg=MENUTEXTBGCOLOR, fg=MENUTEXTCOLOR,
                            font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.OPTIONS.add_command(label="Змінити налаштування", command=self.CHANGESETTINGS)
        self.MENU.add_cascade(label="Файл", menu=self.FILE)
        self.MENU.add_cascade(label="Вигляд", command=self.EDITWINDOW)
        self.MENU.add_cascade(label="Налаштування", menu=self.OPTIONS)
        self.FRAME = Frame(MASTER)
        self.FRAME.pack()
        self.DIRECTORYLABEL = Label(self.FRAME, textvariable=self.DIRVAR, bg=WINDOWTEXTBGCOLOR, fg=WINDOWTEXTCOLOR,
                                    font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.DIRECTORYLABEL.pack()
        self.FRAME2 = Frame(MASTER)
        self.FRAME2.pack()
        self.COMMANDS = Text(self.FRAME2, width=80, relief=RAISED, border=5, height=20, undo=True, fg=WIDGETTEXTCOLOR,
                             bg=WIDGETTEXTBGCOLOR,
                             font=(WIDGETTEXTFONT, WIDGETTEXTSIZE))
        self.COMMANDS.focus_set()
        self.COMMANDS.pack(side=LEFT, fill=Y)
        self.SCROLL = Scrollbar(self.FRAME2, command=self.COMMANDS.yview, bg=WIDGETTEXTBGCOLOR)
        self.SCROLL.pack(side=RIGHT, fill=Y)
        self.FRAME3 = Frame(MASTER)
        self.FRAME3.pack()
        self.TEXTPOSITION = Label(self.FRAME3, textvariable=self.POSITION, bg=WINDOWTEXTBGCOLOR, fg=WINDOWTEXTCOLOR,
                                  font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.TEXTPOSITION.pack()
        self.DIRECTORYMENU = Menu(tearoff=0, bg=MENUTEXTBGCOLOR, fg=MENUTEXTCOLOR,
                                  font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.DIRECTORYMENU.add_command(label="Скопіювати директорію", command=self.COPYDIRECTORY)
        self.RIGHTMENU = Menu(tearoff=0, bg=MENUTEXTBGCOLOR, fg=MENUTEXTCOLOR,
                              font=(WINDOWTEXTFONT, WINDOWTEXTSIZE))
        self.RIGHTMENU.add_command(label="Скопіювати все", command=self.COPY, accelerator="Ctrl+C")
        self.RIGHTMENU.add_command(label="Вставити", command=self.PASTE, accelerator="Ctrl+V")
        self.RIGHTMENU.add_command(label="Видалити все", command=lambda: self.COMMANDS.delete(1.0, END),
                                   accelerator="Ctrl+A+Del")
        self.RIGHTMENU.add_command(label="Скасувати", command=lambda: self.UNDO(None), accelerator="Ctrl+Z")
        self.RIGHTMENU.add_command(label="Повторити", command=lambda: self.REDO(None), accelerator="Ctrl+Y")
        self.DIRECTORYLABEL.bind("<Button-3>", lambda event: self.DIRECTORYMENU.post(event.x_root, event.y_root))
        self.COMMANDS.config(yscrollcommand=self.SCROLL.set)
        self.COMMANDS.bind("<Key>", self.GETPOSITION)
        self.COMMANDS.bind("<Button-1>", self.GETPOSITION)
        self.COMMANDS.bind("<B1-Motion>", self.GETPOSITION)
        self.COMMANDS.bind("<Button-3>", self.APPEARRIGHTMENU)
        if DIRECTORY != "":
            try:
                op = open(DIRECTORY)
                read = op.read()
                op.close()
                self.DIRVAR.set(DIRECTORY)
                self.COMMANDS.insert(END, read)
            except:
                pass
        path = '@%s' % os.path.join(os.environ['WINDIR'], 'Cursors/arrow_r.cur').replace('\\', '/')
        self.DIRECTORYLABEL.config(cursor=path)
        self.TEXTPOSITION.config(cursor=path)
        MASTER.attributes("-topmost", False)
        MASTER.bind("<Escape>", lambda e: UTHON.wm_iconify())
        MASTER.bind("<Key>", self.CALLBACK)
        MASTER.bind("<Control-z>", self.UNDO)
        MASTER.bind("<Control-y>", self.REDO)
        MASTER.config(menu=self.MENU, cursor=path)

    def UNDO(self, event):
        try:
            self.COMMANDS.edit_undo()
        except:
            pass

    def REDO(self, event):
        try:
            self.COMMANDS.edit_redo()
        except:
            pass

    def APPEARRIGHTMENU(self, event):
        self.RIGHTMENU.post(event.x_root, event.y_root)

    def COPY(self):
        self.COMMANDS.clipboard_clear()
        text = self.COMMANDS.get(1.0, END)
        self.COMMANDS.clipboard_append(text)

    def PASTE(self):
        self.COMMANDS.insert(self.COMMANDS.index(INSERT), self.MASTER.clipboard_get())

    def COPYDIRECTORY(self):
        self.MASTER.clipboard_clear()
        self.MASTER.clipboard_append(self.DIRVAR.get())

    def CHANGESETTINGS(self):
        pass

    def EDITWINDOW(self):
        LEVEL = Toplevel(bg=WINDOWTEXTBGCOLOR)
        LEVEL.title("Налаштовування")
        LEVEL.geometry("300x550")
        LEVEL.minsize(250, 300)
        LEVEL.maxsize(600, 600)
        LEVEL.grab_set()
        LEVEL.focus_set()
        VAR1 = StringVar()
        VAR2 = StringVar()
        VAR3 = StringVar()
        VAR4 = StringVar()
        VAR5 = StringVar()
        VAR6 = StringVar()
        VAR7 = StringVar()
        VAR8 = StringVar()
        VAR9 = StringVar()
        VAR10 = StringVar()
        VAR11 = StringVar()
        VAR12 = StringVar()
        VAR13 = StringVar()
        VAR1.set(WIDGETTEXTFONT)
        VAR2.set(WIDGETTEXTSIZE)
        VAR3.set(WIDGETTEXTCOLOR)
        VAR4.set(WIDGETTEXTBGCOLOR)
        VAR5.set(WINDOWTEXTFONT)
        VAR6.set(WINDOWTEXTSIZE)
        VAR7.set(WINDOWTEXTCOLOR)
        VAR8.set(WINDOWTEXTBGCOLOR)
        VAR9.set(MENUTEXTFONT)
        VAR10.set(MENUTEXTSIZE)
        VAR11.set(MENUTEXTCOLOR)
        VAR12.set(MENUTEXTBGCOLOR)
        VAR13.set(MENUTEXTACTIVEBG)
        FRAME = Frame(LEVEL)
        FRAME2 = LabelFrame(FRAME, text="Текстовий віджет", font=16, bd=6, bg=WINDOWTEXTBGCOLOR)
        FRAME3 = LabelFrame(FRAME, text="Вікно", font=16, bd=6, bg=WINDOWTEXTBGCOLOR)
        FRAME4 = LabelFrame(LEVEL, text="Меню", font=16, bd=6, bg=WINDOWTEXTBGCOLOR)
        TLAB1 = LabelFrame(FRAME2, text="Шрифт тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB2 = LabelFrame(FRAME2, text="Розмір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB3 = LabelFrame(FRAME2, text="Колір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB4 = LabelFrame(FRAME2, text="Фоновий колір", bd=3, bg=WINDOWTEXTBGCOLOR)
        LAB1 = Label(TLAB1, textvariable=VAR1, bg=WINDOWTEXTBGCOLOR)
        LAB2 = Label(TLAB2, textvariable=VAR2, bg=WINDOWTEXTBGCOLOR)
        LAB3 = Label(TLAB3, textvariable=VAR3, bg=WINDOWTEXTBGCOLOR)
        LAB4 = Label(TLAB4, textvariable=VAR4, bg=WINDOWTEXTBGCOLOR)
        ENTRY1 = Entry(TLAB1)
        ENTRY1.insert(END, VAR1.get())
        SCALE = Scale(TLAB2, background=WINDOWTEXTBGCOLOR, from_=1, to=72, orient=HORIZONTAL,
                      command=lambda e: VAR2.set(SCALE.get()))
        SCALE.set(WIDGETTEXTSIZE)
        BUTTON3 = ttk.Button(TLAB3, text="Вибрати", command=self.GETCOLOR)
        BUTTON4 = ttk.Button(TLAB4, text="Вибрати", command=self.GETCOLOR)
        TLAB5 = LabelFrame(FRAME3, text="Шрифт тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB6 = LabelFrame(FRAME3, text="Розмір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB7 = LabelFrame(FRAME3, text="Колір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB8 = LabelFrame(FRAME3, text="Фоновий колір", bd=3, bg=WINDOWTEXTBGCOLOR)
        LAB5 = Label(TLAB5, textvariable=VAR5, bg=WINDOWTEXTBGCOLOR)
        LAB6 = Label(TLAB6, textvariable=VAR6, bg=WINDOWTEXTBGCOLOR)
        LAB7 = Label(TLAB7, textvariable=VAR7, bg=WINDOWTEXTBGCOLOR)
        LAB8 = Label(TLAB8, textvariable=VAR8, bg=WINDOWTEXTBGCOLOR)
        ENTRY2 = Entry(TLAB5)
        ENTRY2.insert(END, VAR5.get())
        SCALE2 = Scale(TLAB6, background=WINDOWTEXTBGCOLOR, from_=1, to=30, orient=HORIZONTAL,
                       command=lambda e: VAR6.set(SCALE2.get()))
        SCALE2.set(WINDOWTEXTSIZE)
        BUTTON7 = ttk.Button(TLAB7, text="Вибрати", command=self.GETCOLOR)
        BUTTON8 = ttk.Button(TLAB8, text="Вибрати", command=self.GETCOLOR)
        TLAB9 = LabelFrame(FRAME4, text="Шрифт тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB10 = LabelFrame(FRAME4, text="Розмір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB11 = LabelFrame(FRAME4, text="Колір тексту", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB12 = LabelFrame(FRAME4, text="Фоновий колір", bd=3, bg=WINDOWTEXTBGCOLOR)
        TLAB13 = LabelFrame(FRAME4, text="Активний фоновий колір", bd=3, bg=WINDOWTEXTBGCOLOR)
        LAB9 = Label(TLAB9, textvariable=VAR9, bg=WINDOWTEXTBGCOLOR)
        LAB10 = Label(TLAB10, textvariable=VAR10, bg=WINDOWTEXTBGCOLOR)
        LAB11 = Label(TLAB11, textvariable=VAR11, bg=WINDOWTEXTBGCOLOR)
        LAB12 = Label(TLAB12, textvariable=VAR12, bg=WINDOWTEXTBGCOLOR)
        LAB13 = Label(TLAB13, textvariable=VAR13, bg=WINDOWTEXTBGCOLOR)
        ENTRY3 = Entry(TLAB9)
        ENTRY3.insert(END, VAR9.get())
        SCALE3 = Scale(TLAB10, background=WINDOWTEXTBGCOLOR, from_=1, to=30, orient=HORIZONTAL,
                       command=lambda e: VAR10.set(SCALE3.get()))
        SCALE3.set(MENUTEXTSIZE)
        BUTTON11 = ttk.Button(TLAB11, text="Вибрати", command=self.GETCOLOR)
        BUTTON12 = ttk.Button(TLAB12, text="Вибрати", command=self.GETCOLOR)
        BUTTON13 = ttk.Button(TLAB13, text="Вибрати", command=self.GETCOLOR)
        BUTTONSAVE = ttk.Button(LEVEL, text="Зберегти і вийти")
        TLAB1.grid(columnspan=2, row=0, column=0)
        LAB1.grid(row=1, column=0)
        ENTRY1.grid(row=1, column=1)
        TLAB2.grid(columnspan=2, row=2, column=0)
        LAB2.grid(row=3, column=0)
        SCALE.grid(row=3, column=1)
        TLAB3.grid(columnspan=2, row=4, column=0)
        LAB3.grid(row=5, column=0)
        BUTTON3.grid(row=5, column=1)
        TLAB4.grid(columnspan=2, row=6, column=0)
        LAB4.grid(row=7, column=0)
        BUTTON4.grid(row=7, column=1)
        TLAB5.grid(columnspan=2, row=0, column=0)
        LAB5.grid(row=1, column=0)
        ENTRY2.grid(row=1, column=1)
        TLAB6.grid(columnspan=2, row=2, column=0)
        LAB6.grid(row=3, column=0)
        SCALE2.grid(row=3, column=1)
        TLAB7.grid(columnspan=2, row=4, column=0)
        LAB7.grid(row=5, column=0)
        BUTTON7.grid(row=5, column=1)
        TLAB8.grid(columnspan=2, row=6, column=0)
        LAB8.grid(row=7, column=0)
        BUTTON8.grid(row=7, column=1)
        TLAB9.grid(columnspan=2, row=0, column=0)
        LAB9.grid(row=1, column=0)
        ENTRY3.grid(row=1, column=1)
        TLAB10.grid(columnspan=2, row=2, column=0)
        LAB10.grid(row=3, column=0)
        SCALE3.grid(row=3, column=1)
        TLAB11.grid(columnspan=2, row=4, column=0)
        LAB11.grid(row=5, column=0)
        BUTTON11.grid(row=5, column=1)
        TLAB12.grid(columnspan=2, row=6, column=0)
        LAB12.grid(row=7, column=0)
        BUTTON12.grid(row=7, column=1)
        TLAB13.grid(columnspan=2, row=8, column=0)
        LAB13.grid(row=9, column=0)
        BUTTON13.grid(row=9, column=1)
        FRAME2.pack(side=LEFT)
        FRAME3.pack(side=RIGHT)
        FRAME4.pack()
        FRAME.pack(expand=1)
        BUTTONSAVE.pack()

    def GETCOLOR(self):
        a = cs.askcolor(title="Колір")

    def GETPOSITION(self, event):
        a = self.COMMANDS.index(INSERT).split('.')
        self.POSITION.set(f'Ряд:{a[0]}  Ст:{a[1]}')
        self.COLORCOMMANDSWORDS(mode=self.LANGSTATE)

    def NEWWINDOW(self):
        self.UTHON = Toplevel()
        W = WINDOW(self.UTHON)
        self.UTHON.mainloop()

    def CLOSEFILE(self):
        self.DIRVAR.set("")
        self.COMMANDS.delete(1.0, END)
        self.POSITION.set("Ряд:1  Ст:0")

    def NEWFILE(self):
        self.SAVEFILE()
        a = fd.asksaveasfilename(initialdir="/", title="Створення нового файлу", defaultextension=".py",
                                 filetypes=(("Python file", ".py"), ("Text file", ".txt"), ("HTML file", ".html")))
        if a != "":
            self.DIRVAR.set(a)
            self.COMMANDS.delete(1.0, END)
            self.POSITION.set("Ряд:1  Ст:0")

    def SAVEFILE(self):
        if self.DIRVAR.get() != "":
            op = open(self.DIRVAR.get(), "w").close()
            op = open(self.DIRVAR.get(), "w")
            op.write(self.COMMANDS.get(1.0, END))
            op.close()

    def SAVEASFILE(self):
        a = fd.asksaveasfilename(initialdir="/", title="Збереження", defaultextension=".py",
                                 filetypes=(("Python file", ".py"), ("Text file", ".txt"), ("HTML file", ".html")))
        self.SAVEFILE()
        if a != "":
            self.DIRVAR.set(a)

    def OPENFILE(self):
        a = fd.askopenfilename()
        if a != "":
            try:
                op = open(a, encoding='UTF-8')
                self.COMMANDS.delete(1.0, END)
                for i in op:
                    self.COMMANDS.insert(END, i)
                op.close()
                #
                if a.endswith(".rb"):
                    self.RB = True
                #
                self.DIRVAR.set(a)
                self.GETPOSITION(None)
            except UnicodeDecodeError:
                # cp1252
                # ascii
                # utf-16
                # ISO-8859-1
                try:
                    op = open(a, encoding='ISO-8859-1')
                    self.COMMANDS.delete(1.0, END)
                    for i in op:
                        self.COMMANDS.insert(END, i)
                    op.close()
                    self.DIRVAR.set(a)
                    self.GETPOSITION(None)
                except:
                    mb.showwarning("Неможливість дії", "Файл не може бути відкритий.")

    def INTERPRETE(self):
        code = self.COMMANDS.get("1.0", END).split('\n')
        code = list(map(lambda x: x + '\n', code))
        code = Translator.Translate(code)
        try:
            exec(code)
        except Exception as e:
            mb.showwarning("Помилка", e)
        except:
            pass

    def TRANSLATETOPYTHON(self):
        code = self.COMMANDS.get("1.0", END).split('\n')
        code = list(map(lambda x: x + '\n', code))
        code = Translator.Translate(code, True)
        PRINT(code)

    def COLORCOMMANDSWORDS(self, mode=True):
        self.LANGSTATE = True if mode else False
        code = self.COMMANDS.get("1.0", END).split('\n')
        code = list(map(lambda x: x + '\n', code))
        tpl = Translator.ColorWords(code, mode)
        a = 'red' if mode else 'green'

        for i in range(len(tpl)):
            self.COMMANDS.tag_add(a.upper(), '{0}.{1}'.format(tpl[i][0], tpl[i][1]),
                                  '{0}.{1}'.format(tpl[i][0], tpl[i][1] + tpl[i][2]))
        self.COMMANDS.tag_configure(a.upper(), foreground=a)

    def CALLBACK(self, event):
        if event.keysym == "F5":
            self.INTERPRETE()
        elif event.keysym == "F1":
            self.NEWFILE()
        elif event.keysym == "F2":
            self.OPENFILE()
        elif event.keysym == "F3":
            self.SAVEFILE()
        elif event.keysym == "F4":
            self.SAVEASFILE()
        elif event.keysym == "F6":
            self.TRANSLATETOPYTHON()
        elif event.keysym == "F7":
            self.COLORCOMMANDSWORDS()
        elif event.keysym == "F8":
            self.COLORCOMMANDSWORDS(mode=False)
        elif event.keysym == "F9":
            self.CLOSEFILE()
        elif event.keysym == "Insert":
            self.COMMANDS.insert(self.COMMANDS.index(INSERT), '()')
            num = self.COMMANDS.index(INSERT)
            self.COMMANDS.mark_set(INSERT, num[:2] + str(int(num[2:]) - 1))
        # elif event.keysym == "'" and ALT:
        #    self.COMMANDS.insert(self.COMMANDS.index(INSERT), '""')
        #    self.COMMANDS.delete('end - 1 chars')
        #    num = self.COMMANDS.index(INSERT)
        #    self.COMMANDS.mark_set(INSERT, num[:2] + str(int(num[2]) - 1))


def CHECKDIRECTORY():
    DEFAULT = """WINDOWTEXTSIZE:10
WINDOWTEXTCOLOR:black
WINDOWTEXTBGCOLOR:white
WINDOWTEXTFONT:Arial
WIDGETTEXTSIZE:10
WIDGETTEXTCOLOR:black
WIDGETTEXTBGCOLOR:white
WIDGETTEXTFONT:Arial
MENUTEXTSIZE:10
MENUTEXTACTIVEBG:blue
MENUTEXTBGCOLOR:white
MENUTEXTCOLOR:black
MENUTEXTFONT:Arial
DIRECTORY:"""
    if not os.path.exists(r"\UTHON\settings.utt"):
        createname = open(r"\UTHON\settings.utt", "w")
        createname.write(DEFAULT)
        createname.close()


def REVALUEREADING(textvariable, value):
    op = open(r"\UTHON\settings.utt")
    read = op.readlines()
    op.close()
    # for line in range(read):
    #     if textvariable in read[line]:


def READINGVALUES():
    global WINDOWTEXTSIZE, WINDOWTEXTCOLOR, WINDOWTEXTBGCOLOR, WINDOWTEXTFONT
    global WIDGETTEXTBGCOLOR, WIDGETTEXTFONT, WIDGETTEXTSIZE, WIDGETTEXTCOLOR
    global MENUTEXTSIZE, MENUTEXTACTIVEBG, MENUTEXTBGCOLOR, MENUTEXTCOLOR, MENUTEXTFONT
    global DIRECTORY
    vars = ["WINDOWTEXTSIZE:", "WINDOWTEXTCOLOR:", "WINDOWTEXTBGCOLOR:", "WINDOWTEXTFONT:",
            "WIDGETTEXTSIZE:",
            "WIDGETTEXTCOLOR:", "WIDGETTEXTBGCOLOR:", "WIDGETTEXTFONT:", "MENUTEXTSIZE:", "MENUTEXTCOLOR:",
            "MENUTEXTBGCOLOR:", "MENUTEXTFONT:", "MENUTEXTACTIVEBG:", "DIRECTORY:"]
    reading = open(r"\UTHON\settings.utt", encoding='UTF-8')
    for line in reading.readlines():
        for i in range(len(vars)):
            if vars[i] in line:
                if vars[i] != vars[-1]:
                    res = line[line.find(":") + 1:line.find(r"\n")]
                    globals()[vars[i][:-1]] = "".join(res.split())
                else:
                    res = line[line.find(":") + 1:]
                    globals()[vars[i][:-1]] = "".join(res.split())
    reading.close()


if not os.path.exists(r"\UTHON"):
    os.mkdir(r"\UTHON")

WINDOWTEXTSIZE = 10
WINDOWTEXTCOLOR = "black"
WINDOWTEXTBGCOLOR = "#cdcdcd"
WINDOWTEXTFONT = "Arial"
WIDGETTEXTSIZE = 14
WIDGETTEXTCOLOR = "#98ae44"
WIDGETTEXTBGCOLOR = "#e8ffe8"
WIDGETTEXTFONT = "Monaco"
MENUTEXTSIZE = 10
MENUTEXTCOLOR = "black"
MENUTEXTBGCOLOR = "#cdcdcd"
MENUTEXTFONT = "Arial"
MENUTEXTACTIVEBG = "blue"
DIRECTORY = ""
CHECKDIRECTORY()
READINGVALUES()

t = ''

UTHON = Tk()
UTHON.protocol("WM_DELETE_WINDOW", lambda: UTHON.destroy() if mb.askyesno("Вихід",
                                                                          "Програма закінчить роботу.\nВи бажаєте вийти?") else False)
W = WINDOW(UTHON)
UTHON.mainloop()
