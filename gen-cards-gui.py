#!/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import gen_cards

# root window
root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('Gerar cards')

# store csv address and pictures_folder
csv = tk.StringVar()
pictures_folder = tk.StringVar()


def generate_clicked():
    #start progress bar
    popup = tk.Toplevel()
    tk.Label(popup, text="Executando").grid(row=0,column=0)

    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=3)
    progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    popup.pack_slaves()

    progress_var.set(1)
    popup.update()

    run_cmd()

    progress_var.set(3)
    popup.update()

    popup.destroy()

    return 0

def run_cmd():
    try:
        gen_cards.main(csv.get(), pictures_folder.get())
        showinfo(
            title='Information',
            message="Finalizado"
        )
    except Exception as e:
        showinfo(
            title='Information',
            message="Erro: " + str(e)
        )


# Sign in frame
generate = ttk.Frame(root)
generate.pack(padx=10, pady=10, fill='x', expand=True)

# csv
csv_label = ttk.Label(generate, text="Arquivo csv")
csv_label.pack(fill='x', expand=True)

csv_entry = ttk.Entry(generate, textvariable=csv)
csv_entry.pack(fill='x', expand=True)
csv_entry.focus()

# pictures_folder
pictures_folder_label = ttk.Label(generate, text="Pasta de fotos")
pictures_folder_label.pack(fill='x', expand=True)

pictures_folder_entry = ttk.Entry(generate, textvariable=pictures_folder)
pictures_folder_entry.pack(fill='x', expand=True)

# login button
generate_button = ttk.Button(generate, text="Gerar arquivos", command=generate_clicked)
generate_button.pack(fill='x', expand=True, pady=10)

root.mainloop()
