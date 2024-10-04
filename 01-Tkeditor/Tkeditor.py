from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

root = Tk()
root.geometry('800x500')
root.title('Untitled - Tkeditor')
root.iconbitmap('Tkinter-Projects//01-Tkeditor//icons//pypad.ico')

def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

# Theme choice
def theme():
    global bgc, fgc
    val = themechoice.get()
    clrs = clrschms.get(val)
    fgc, bgc = clrs.split('.')
    fgc, bgc = '#' + fgc, '#' + bgc
    textPad.config(bg=bgc, fg=fgc)

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        infobar.pack_forget()

def update_line_number(event=None):
    txt = ''
    if showln.get(): 
        endline, endcolumn = textPad.index('end-1c').split('.')
        txt = '//n'.join(map(str, range(1, int(endline))))
    lnlabel.config(text=txt, anchor='nw')
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s' % (currline, curcolumn))

def highlight_line(interval=100):
    textPad.tag_remove("active_line", 1.0, "end")
    textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
    textPad.after(interval, toggle_highlight)

def undo_highlight():
    textPad.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()

#########################################################################
def about():
    messagebox.showinfo("About", "A Editor using Tkinter by Leohc92")

def help_box(event=None):
    messagebox.showinfo("Help", "For help email to chenyu.wu@outlook.com", icon='question')

def exit_editor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

root.protocol('WM_DELETE_WINDOW', exit_editor)

#########################################################################

# Demo of indexing and tagging features of text widget
def select_all(event=None):   
    textPad.tag_add('sel', '1.0', 'end')

def on_find(event=None):
    t2 = Toplevel(root)
    t2.title('Find')
    t2.geometry('300x65+200+250')
    t2.transient(root)
    Label(t2, text="Find All:").grid(row=0, column=0, pady=4, sticky='e')
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
    c = IntVar()
    Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(t2, text='Find All', underline=0, command=lambda: search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=4)
    
    def close_search():
        textPad.tag_remove('match', '1.0', END)
        t2.destroy()
    
    t2.protocol('WM_DELETE_WINDOW', close_search)

def search_for(needle, cssnstv, textPad, t2, e):
    textPad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
            if not pos: break
            lastpos = '%s+%dc' % (pos, len(needle))
            textPad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
        textPad.tag_config('match', foreground='red', background='yellow')
    e.focus_set()
    t2.title('%d matches found' % count)

########################################################################
# Leveraging built-in text widget functionalities

def undo():
    textPad.event_generate("<<Undo>>")
    update_line_number()

def redo():
    textPad.event_generate("<<Redo>>")
    update_line_number()

def cut():
    textPad.event_generate("<<Cut>>")
    update_line_number()

def copy():
    textPad.event_generate("<<Copy>>")
    update_line_number()

def paste():
    textPad.event_generate("<<Paste>>")
    update_line_number()

######################################################################
def new_file(event=None):
    global filename
    filename = None
    root.title("Untitled - Tkeditor")
    textPad.delete(1.0, END)
    update_line_number()

def open_file(event=None):
    global filename
    filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if filename == "":
        filename = None
    else:
        root.title(os.path.basename(filename) + " - Tkeditor")
        textPad.delete(1.0, END)
        with open(filename, "r") as fh:
            textPad.insert(1.0, fh.read())
    update_line_number()

def save(event=None):
    global filename
    try:
        with open(filename, 'w') as f:
            letter = textPad.get(1.0, 'end')
            f.write(letter)
    except:
        save_as()

def save_as():
    global filename
    f = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if f:
        filename = f
        with open(f, 'w') as fh:
            textoutput = textPad.get(1.0, END)
            fh.write(textoutput)
        root.title(os.path.basename(f) + " - Tkeditor")

######################################################################
# Defining icons for compound menu demonstration
newicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//new_file.gif')
openicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//open_file.gif')
saveicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//save.gif')
cuticon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//cut.gif')
copyicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//copy.gif')
pasteicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//paste.gif')
undoicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//undo.gif')
redoicon = PhotoImage(file='Tkinter-Projects//01-Tkeditor//icons//redo.gif')

# Define a menu bar
menubar = Menu(root)

# File menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=new_file)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=openicon, underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_editor)
menubar.add_cascade(label="File", menu=filemenu)

# Edit menu
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", compound=LEFT, image=undoicon, accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label="Redo", compound=LEFT, image=redoicon, accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", compound=LEFT, image=cuticon, accelerator='Ctrl+X', command=cut)
editmenu.add_command(label="Copy", compound=LEFT, image=copyicon, accelerator='Ctrl+C', command=copy)
editmenu.add_command(label="Paste", compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command=paste)  # Fixed typo here
editmenu.add_separator()
editmenu.add_command(label="Find", underline=0, accelerator='Ctrl+F', command=on_find)
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator='Ctrl+A', underline=7, command=select_all)

# View menu
viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
hltln.set(1)
viewmenu.add_checkbutton(label="Highlight Active Line", variable=hltln, command=toggle_highlight)

# Help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Help", command=help_box)
menubar.add_cascade(label="Help", menu=helpmenu)

# Attach the menu bar to the root window
root.config(menu=menubar)

# Text widget and scrollbar widget
textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)

# Correctly linking the scrollbar to the text widget
scroll = Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

# Info Bar
infobar = Label(textPad, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

# Line number display
lnlabel = Label(textPad, width=4, bg='grey', fg='white', anchor='nw')
lnlabel.pack(side=LEFT, fill=Y)

# Right-click context menu
cmenu = Menu(root, tearoff=0)
cmenu.add_command(label="Cut", command=cut)
cmenu.add_command(label="Copy", command=copy)
cmenu.add_command(label="Paste", command=paste)

textPad.bind("<Button-3>", popup)
textPad.bind("<KeyRelease>", update_line_number)

# Run the main event loop
root.mainloop()
