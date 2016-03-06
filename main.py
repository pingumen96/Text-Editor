import tkinter
from tkinter import ttk
from tkinter import filedialog
import os

root = tkinter.Tk()
root.title('Editor di testo by Pingumen96')

file = None

#variabili utili
global placed_terminal
placed_terminal=False


def load(text_widget):
    global file, file_path
    file_path = filedialog.askopenfilename()
    file = open(file_path, 'r')
    text_widget.delete(0.1, 'end')
    text_widget.insert(0.1, file.read())


def save(text_widget, save_as=False):
    global file, file_path
    print(text_widget.get(0.1, 'end'))
    if file and not save_as:
        try:
            file = open(file_path, 'w')
            file.write(text_widget.get(0.1, 'end'))
            file.close()
        except:
            print('Non è stato possibile salvare il file.')
    elif (not file) or (file and save_as):
        try:
            file_path = filedialog.asksaveasfilename(filetypes=[(
                '.txt', 'File di testo'), ('.py', 'Sorgente Python'), ('.cpp', 'Sorgente C++')])
            file = open(file_path, 'w')
            file.write(text_widget.get(0.1, 'end'))
            file.close()
        except:
            pass


# funzione che si occupa di far comparire il menù premendo il tasto destro
# del mouse
def right_click_menu(event):
	# mostra il menù partendo dalla posizione definita con .post()
	right_click_text_menu.post(event.x_root, event.y_root)


def right_click_menu_destroy(widget):
	# semplicemente toglie il menù apparentemente senza perdite di memoria
	right_click_text_menu.unpost()
	pass

# funzione per far comparire e scomparire il terminale


def embedded_terminal():
    global placed_terminal
    if not placed_terminal:
        global term_frame
        term_frame = tkinter.Frame(height=200, width=700)
        term_frame.grid(sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        wid = term_frame.winfo_id()
        os.system('xterm -into %d -geometry 1360x150 &' % wid) #os.system('xterm -into %d -geometry 1360x150 -sb &' % wid)
        placed_terminal=True
    elif placed_terminal:
        term_frame.grid_remove()
        placed_terminal=False


# considerare refactoring perché la funzione sta diventando grande
def main_gui():  # creazione interfaccia grafica
    # dichiarazione casella di testo
    text = tkinter.Text(root)

    menu_bar = tkinter.Menu(root)

    # menu file
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Apri...', command=lambda: load(text))
    file_menu.add_command(label='Salva', command=lambda: save(text))
    file_menu.add_command(label='Salva con nome',
                          command=lambda: save(text, True))
    menu_bar.add_cascade(label='File', menu=file_menu)

    # menu modifica
    edit_menu = tkinter.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(
        label='Taglia', command=lambda: text.event_generate('<<Cut>>'))
    edit_menu.add_command(
        label='Copia', command=lambda: text.event_generate('<<Copy>>'))
    edit_menu.add_command(
        label='Incolla', command=lambda: text.event_generate('<<Paste>>'))
    menu_bar.add_cascade(label='Modifica', menu=edit_menu)

    # menu visualizza
    view_menu=tkinter.Menu(menu_bar,tearoff=0)
    view_menu.add_checkbutton(label='Terminale',command=lambda:embedded_terminal())
    menu_bar.add_cascade(label='Visualizza',menu=view_menu)

    # menu viene preparato
    root.config(menu=menu_bar)



    # casella di testo
    text.grid(sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

    # menu click destro del mouse su casella di testo
    global right_click_text_menu
    right_click_text_menu=tkinter.Menu(text,tearoff=0)
    right_click_text_menu.add_command(label='Taglia',command=lambda: text.event_generate('<<Cut>>'))
    right_click_text_menu.add_command(label='Copia',command=lambda: text.event_generate('<<Copy>>'))
    right_click_text_menu.add_command(label='Incolla',command=lambda: text.event_generate('<<Paste>>'))
    # fa corrispondere evento del premere tasto destro a funzione
    text.bind('<Button-3>',right_click_menu)
    text.bind('<Button-1>',lambda event:right_click_menu_destroy(right_click_text_menu))

    # terminale embeddato, prove
    # embedded_terminal()

    # permette ai vari widget di espandersi come devono
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) 



root.minsize(200, 30)
main_gui()
root.mainloop()
