from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import colorchooser as cs
from TranslateUaToPy import SortKeywords, UaToPy, StrToLines
from UaFunctions import *
from UaColorWords import IndexKeywords, IndexBuiltins, IndexConstants
from traceback import format_exc
from sys import exc_info


class WindowForm(object):
    def __init__(self, Master: Tk):
        self.Master = Master
        Master.title("Консоль")
        Master.resizable(0, 0)
        Master["bg"] = WindowTextBGColor
        try:
            Master.call('wm', 'iconphoto', Master._w, PhotoImage(file="python.png"))
        except TclError:
            pass
        self.DirVar = StringVar()
        self.DirVar.set("")
        self.PositionVar = StringVar()
        self.PositionVar.set("1:0")
        self.Menu = Menu(Master)
        self.File = Menu(self.Menu, tearoff=0, bg=MenuTextBGColor, fg=MenuTextColor,
                         font=(WindowTextFont, WindowTextSize))
        # self.File.add_command(label="Нове вікно", command=self.NewWindow)
        self.File.add_command(label="Новий файл", command=self.NewFile, accelerator="F1")
        self.File.add_command(label="Відкрити", command=self.OpenFile, accelerator="F2")
        self.File.add_command(label="Зберегти", command=self.SaveFile, accelerator="F3")
        self.File.add_command(label="Зберегти як...", command=self.SaveAsFile, accelerator="F4")
        self.File.add_command(label="Закрити", command=self.CloseFile, accelerator="F9")
        self.Menu.add_cascade(label="Файл", menu=self.File)
        self.Frame = Frame(Master)
        self.Frame.pack()
        self.DirectoryLabel = Label(self.Frame, textvariable=self.DirVar, bg=WindowTextBGColor, fg=WindowTextColor,
                                    font=(WindowTextFont, WindowTextSize))
        self.DirectoryLabel.pack()
        self.Frame2 = Frame(Master)
        self.Frame2.pack()
        self.Memo = Text(self.Frame2, width=80, relief=RAISED, border=4, height=20, undo=True, fg=WidgetTextColor,
                         bg=WidgetTextBGColor, insertbackground="white", selectbackground="#00008C",
                         font=(WidgetTextFont, WidgetTextSize))
        self.Memo.insert("1.0", """функція привіт(іменування):
	повернути "Ну шо ж здоров " + іменування + "!"
	

вивести в консоль("Привіт бро, скажи своє ім'я:")
ім_я = ввести з консолі()
якщо ім_я == "не скажу":
	вивести в консоль("Ваш безкоштовний період життя закінчився")
інакше:
	вивести в консоль(привіт(ім_я))""")
        self.Memo.focus_set()
        self.Memo.pack(side=LEFT, fill=Y)
        self.line: str = ""
        self.indices: set = set()
        self.Scroll = Scrollbar(self.Frame2, command=self.Memo.yview, bg=WidgetTextBGColor)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Frame3 = Frame(Master)
        self.Frame3.pack(anchor=E)
        self.TextPosition = Label(self.Frame3, textvariable=self.PositionVar, bg=WindowTextBGColor, fg=WindowTextColor,
                                  font=(WindowTextFont, WindowTextSize))
        self.TextPosition.pack()
        self.DirectoryMenu = Menu(tearoff=0, bg=MenuTextBGColor, fg=MenuTextColor,
                                  font=(WindowTextFont, WindowTextSize))
        self.DirectoryMenu.add_command(label="Копіювати директорію")
        self.RightMenu = Menu(tearoff=0, bg=MenuTextBGColor, fg=MenuTextColor,
                              font=(WindowTextFont, WindowTextSize))
        self.RightMenu.add_command(label="Копіювати", command=self.Copy, accelerator="Ctrl+C")
        self.RightMenu.add_command(label="Копіювати все", command=self.CopyAll, accelerator="Ctrl+A+C")
        self.RightMenu.add_command(label="Вставити", command=self.Paste, accelerator="Ctrl+V")
        self.RightMenu.add_command(label="Видалити все", command=lambda: self.Memo.delete(1.0, END),
                                   accelerator="Ctrl+A+Del")
        self.RightMenu.add_command(label="Скасувати", command=lambda: self.Undo(None), accelerator="Ctrl+Z")
        self.RightMenu.add_command(label="Повторити", command=lambda: self.Redo(None), accelerator="Ctrl+Y")
        self.DirectoryLabel.bind("<Button-3>", lambda event: self.DirectoryMenu.post(event.x_root, event.y_root))
        self.Memo.config(yscrollcommand=self.Scroll.set)
        self.Memo.bindtags(('Text', 'post-class-bindings', '.', 'all'))
        self.Memo.bind_class("post-class-bindings", "<KeyPress>", self.Callback)
        self.Memo.bind_class("post-class-bindings", "<Button-1>", self.GetPosition)
        self.Memo.bind_class("post-class-bindings", "<B1-Motion>", self.GetPosition)
        self.Memo.bind_class("post-class-bindings", "<Button-3>", self.AppearRightMenu)
        if Directory != "":
            try:
                op = open(Directory)
                read = op.read()
                op.close()
                self.DirVar.set(Directory)
                self.Memo.insert(END, read)
            except:
                pass
        Master.attributes("-topmost", False)
        Master.bind("<Escape>", lambda e: Uthon.wm_iconify())
        Master.bind("<Control-z>", self.Undo)
        Master.bind("<Control-y>", self.Redo)
        Master.config(menu=self.Menu)

        self.OutLevel = Toplevel(Master)
        self.OutLevel.protocol("WM_DELETE_WINDOW", lambda: self.OutLevel.state("withdrawn"))
        self.OutLevel.title("Вивід")
        self.OutLevel.state("withdrawn")
        XScrollbarO = Scrollbar(self.OutLevel, orient=HORIZONTAL)
        XScrollbarO.pack(side=BOTTOM, fill=X)
        YScrollbarO = Scrollbar(self.OutLevel)
        YScrollbarO.pack(side=RIGHT, fill=Y)
        self.OutMemo = Text(self.OutLevel, wrap=NONE, state=DISABLED,
                            xscrollcommand=XScrollbarO.set, insertbackground="white",
                            yscrollcommand=YScrollbarO.set, width=80, relief=RAISED, border=4, height=20,
                            fg=WidgetTextColor, bg=WidgetTextBGColor, font=(WidgetTextFont, WidgetTextSize))
        self.OutMemo.pack()
        XScrollbarO.config(command=self.OutMemo.xview)
        YScrollbarO.config(command=self.OutMemo.yview)

        self.InLevel = Toplevel(Master)
        self.InLevel.protocol("WM_DELETE_WINDOW", self.InLevelExit)
        self.InLevel.title("Введення з клавіатури")
        self.InLevel.state("withdrawn")
        XScrollbarI = Scrollbar(self.InLevel, orient=HORIZONTAL)
        XScrollbarI.pack(side=BOTTOM, fill=X)
        YScrollbarI = Scrollbar(self.InLevel)
        YScrollbarI.pack(side=RIGHT, fill=Y)
        self.InMemo = Text(self.InLevel, wrap=NONE,
                           xscrollcommand=XScrollbarI.set, insertbackground="white",
                           yscrollcommand=YScrollbarI.set, width=80, relief=RAISED, border=4, height=20,
                           fg=WidgetTextColor, bg=WidgetTextBGColor, font=(WidgetTextFont, WidgetTextSize))
        self.InMemo.pack()
        self.InMemo.bind("<Return>", self.InMemoReturn)
        self.inputing: bool = False
        self.input_get: str = ""
        XScrollbarI.config(command=self.InMemo.xview)
        YScrollbarI.config(command=self.InMemo.yview)

    def InLevelExit(self):
        self.inputing: bool = False
        self.input_get: str = ""
        self.InLevel.state("withdrawn")

    def InMemoReturn(self, event):
        self.input_get = self.InMemo.get("1.0", END)
        self.inputing = False
        self.InLevel.state("withdrawn")

    def Undo(self, event):
        try:
            self.Memo.edit_undo()
        except:
            pass

    def Redo(self, event):
        try:
            self.Memo.edit_redo()
        except:
            pass

    def AppearRightMenu(self, event):
        self.RightMenu.post(event.x_root, event.y_root)

    def Copy(self):
        self.Memo.clipboard_clear()
        try:
            self.Memo.clipboard_append(self.Memo.get(SEL_FIRST, SEL_LAST))
        except TclError:
            self.Memo.clipboard_append("")

    def CopyAll(self):
        self.Memo.clipboard_clear()
        self.Memo.clipboard_append(self.Memo.get(1.0, END))

    def Paste(self):  # !!!!!!!!
        pos: int = int(self.Memo.index(INSERT).split(".")[0])
        self.Memo.insert(self.Memo.index(INSERT), self.Master.clipboard_get())
        for line in StrToLines(self.Master.clipboard_get()):
            print(line)
            # self.ColorLine(line, pos)
            pos += 1

    def GetPosition(self, event=None):
        a = self.Memo.index(INSERT).split('.')
        self.PositionVar.set(f'{a[0]}:{a[1]}')

    def CloseFile(self):
        self.DirVar.set("")
        self.Memo.delete(1.0, END)
        self.PositionVar.set("1:0")

    def NewFile(self):
        self.SaveFile()
        a = fd.asksaveasfilename(initialdir="/", title="Створення нового файлу", defaultextension=".py",
                                 filetypes=(("Python file", ".py"), ("Text file", ".txt"), ("HTML file", ".html")))
        if a != "":
            self.DirVar.set(a)
            self.Memo.delete(1.0, END)
            self.PositionVar.set("1:0")

    def SaveFile(self):
        if self.DirVar.get() != "":
            op = open(self.DirVar.get(), "w").close()
            op = open(self.DirVar.get(), "w")
            op.write(self.Memo.get(1.0, END))
            op.close()

    def SaveAsFile(self):
        a = fd.asksaveasfilename(initialdir="/", title="Збереження", defaultextension=".py",
                                 filetypes=(("Python file", ".py"), ("Text file", ".txt"), ("HTML file", ".html")))
        self.SaveFile()
        if a != "":
            self.DirVar.set(a)

    def OpenFile(self):
        a = fd.askopenfilename()
        if a != "":
            try:
                op = open(a, encoding='UTF-8')
                self.Memo.delete(1.0, END)
                for i in op:
                    self.Memo.insert(END, i)
                op.close()
                if a.endswith(".rb"):
                    pass
                self.DirVar.set(a)
                self.GetPosition()
            except UnicodeDecodeError:
                try:
                    op = open(a, encoding='ISO-8859-1')
                    self.Memo.delete(1.0, END)
                    for i in op:
                        self.Memo.insert(END, i)
                    op.close()
                    self.DirVar.set(a)
                    self.GetPosition()
                except:
                    mb.showwarning("Неможливість дії", "Файл не може бути відкритий.")

    def Interprete(self):
        script: str = self.Memo.get("1.0", END)
        try:
            print("Початок програми.")
            exec(UaToPy(script))
            print("Кінець програми.")
        except Exception:
            print("Виникла помилка.")
            st: str = format_exc()[
                      format_exc().rfind('File "<string>", line ') + 22:
                      ]  # !!!!!!!
            for i in range(len(st)):
                if st[i] not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    exc_line = st[:i]
                    break
            self.Memo.mark_set("insert", f"{exc_line}.0")
            self.Memo.see(f"{exc_line}.0")
            self.Memo.tag_add("exception", "insert", "insert lineend")
            self.Memo.tag_config("exception", background="red", foreground="white")
            mb.showwarning(exc_info()[0].__name__, f"Рядок {exc_line}\n" + str(exc_info()[1]).capitalize())
            self.Memo.tag_delete("exception")

    def TranslateToPython(self):
        cout(UaToPy(self.Memo.get("1.0", END)))

    def ColorLine(self, line: str, line_pos: int):
        key_ind = IndexKeywords(line)
        built_ind = IndexBuiltins(line)
        const_ind = IndexConstants(line)
        for i in range(1, len(key_ind), 2):
            self.Memo.tag_add("keywords", f"{line_pos}.{key_ind[i - 1]}", f"{line_pos}.{key_ind[i]}")
            self.Memo.tag_config("keywords", foreground="#CC6EDD", font=("", 14, "bold"))
        for i in range(1, len(built_ind), 2):
            self.Memo.tag_add("builtins", f"{line_pos}.{built_ind[i - 1]}", f"{line_pos}.{built_ind[i]}")
            self.Memo.tag_config("builtins", foreground="#F06372", font=("", 14, "bold"))
        for i in range(1, len(const_ind), 2):
            self.Memo.tag_add("constants", f"{line_pos}.{const_ind[i - 1]}", f"{line_pos}.{const_ind[i]}")
            self.Memo.tag_config("constants", foreground="#FFC90E", font=("", 14, "bold"))

    def Callback(self, event):
        if event.keysym in ("1", "2", "3", "4", "5", "6", "7", "8", "9",
                            "0", "equal", "plus", "minus", "exclam", "at",
                            "percent", "ampersand", "asterisk", "less", "greater", "slash"):
            self.Memo.tag_add("numbers_operators", "insert-1chars")
            self.Memo.tag_config("numbers_operators", foreground="cyan")
        elif event.keysym in ("parenleft", "parenright", "bracketleft",
                              "bracketright", "braceleft", "braceright", "comma", "colon", "semicolon"):
            self.Memo.tag_add("brackets_dots", "insert-1chars")
            self.Memo.tag_config("brackets_dots", foreground="white")
        elif event.keysym == "F5":
            self.Interprete()
        elif event.keysym == "F1":
            self.NewFile()
        elif event.keysym == "F2":
            self.OpenFile()
        elif event.keysym == "F3":
            self.SaveFile()
        elif event.keysym == "F4":
            self.SaveAsFile()
        elif event.keysym == "F6":
            self.TranslateToPython()
        elif event.keysym == "F9":
            self.CloseFile()
        self.line = self.Memo.get("insert linestart", "insert lineend")
        self.ColorLine(self.line, self.Memo.index(INSERT).split('.')[0])
        # print(set([*key_ind, *built_ind, *const_ind]).difference(self.indices))
        # if set([*key_ind, *built_ind, *const_ind]) != self.indices and len(self.indices) > 1:
        #     print(tuple(self.indices)[1])
        #     tup_indices = tuple(self.indices)
        #     self.Memo.tag_remove("keywords", f"{line_pos}.{tup_indices[0]}", f"{line_pos}.{tup_indices[1]}")
        # self.indices = set([*key_ind, *built_ind, *const_ind])
        # if len(self.Memo.tag_ranges("constants")) > 0:
        #     print(self.Memo.tag_ranges("constants"))
        self.GetPosition()


def cout(*args, end="\n"):
    if W.OutLevel.state() == "withdrawn":
        W.OutLevel.state("normal")
        W.OutLevel.focus()
    W.OutMemo["state"] = NORMAL
    pos = int(W.OutMemo.index(END).split(".")[0])
    for expr in args:
        W.OutMemo.tag_delete("last_out")
        W.OutMemo.insert(END, expr + end)
        W.OutMemo.tag_add("last_out", f"{pos - 1}.0", END)
        W.OutMemo.tag_config("last_out", foreground="white")
    W.OutMemo["state"] = DISABLED


def cin():  # !!!!!!!!!
    W.InLevel.state("normal")
    W.InMemo.focus()
    W.InMemo.delete("1.0", END)
    W.inputing = True
    while W.inputing:
        Uthon.update()
    return W.input_get


def outclear():
    W.OutMemo["state"] = NORMAL
    W.OutMemo.delete("1.0", END)
    W.OutMemo["state"] = DISABLED


WindowTextSize = 10
WindowTextColor = "#E1E3EA"
WindowTextBGColor = "#404856"
WindowTextFont = "Arial"
WidgetTextSize = 14
WidgetTextColor = "#9198A5"
WidgetTextBGColor = "#272C35"
WidgetTextFont = "Monaco"
# MenuTextSize = 10
MenuTextColor = "#E1E3EA"
MenuTextBGColor = "#272C35"
# MenuTextFont = "Arial"
# MENUTEXTACTIVEBG = "blue"
Directory = ""
SortKeywords()

Uthon = Tk()
# Uthon.protocol("WM_DELETE_WINDOW",
#                lambda: Uthon.destroy() if mb.askyesno("Вихід",
#                                                       "Програма закінчить роботу.\nВи бажаєте вийти?") else False)
W = WindowForm(Uthon)
Uthon.mainloop()
