import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import database as db
from PIL import Image, ImageTk
from subprocess import Popen
from shutil import copy
import os, uuid

'''  Objetivos
- Bordas para os jogos e fundo melhorado
- personalização e mais funções (renomear, redefinir caminho .exe)
- e depois, quero a minha primeira versão a ser lançada pra pc como um .exe

sugestões
- scroll
- 

'''

def browse_file():
    try:
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(
                ("All files", "*.*"),
                ("Executables", "*.exe"),
                ("Images", "*.png;")
            )
        )
        
        # If user cancels, file_path will be empty
        if not file_path:
            return
        
        return file_path
        # Optional: Show a message
        # messagebox.showinfo("File Selected", f"You selected:\n{file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def addProgram():
    file_path = browse_file()
    name = simpledialog.askstring('', "Dê um nome a ele")

    if not name or not file_path:
        return
    
    if file_path and name:
        db.insertProgram(name, file_path)
        refreshList()

def createCard(name, exePath, imgPath):
    cardFrame = tk.Frame(mainFrame, width=240, height=260, relief='groove', padx=10)
    cardFrame.pack_propagate(False)
    cardFrame.config(cursor='hand2')

    img = Image.open(imgPath)
    img = img.resize((240, 240), Image.Resampling.LANCZOS)

    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(cardFrame, image=tk_img)
    label.image = tk_img  # REFERENCIA PRA IMG NÃO SUMIR
    label.pack()

    textLabel = tk.Label(cardFrame, text=name, wraplength=240, justify='center')
    textLabel.pack(anchor='center')

    cardFrame.bind('<Button-1>', lambda e, p=exePath: lauchProgram(p))
    label.bind('<Button-1>', lambda e, p=exePath: lauchProgram(p))

    cardFrame.bind('<Button-3>', lambda event, p=exePath: programMenu(event, p))
    label.bind('<Button-3>', lambda event, p=exePath: programMenu(event, p))

    return cardFrame

def pickImage(exePath):
    try:
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=(
                ("All files", "*.*"),
                ("Images", "*.png;")
            )
        )
        
        # If user cancels, file_path will be empty
        if not file_path:
            return

        try:
            Image.open(file_path)
        except:
            messagebox.showerror('Erro', 'Formato inválido de imagem')
            return

        # Copying the file
        ext = os.path.splitext(file_path)[1]
        unique_name = str(uuid.uuid4()) + ext # img format
        new_path = os.path.join("Covers/saved", unique_name)

        copy(file_path, new_path)

        db.defImg(exePath, new_path)
        refreshList()
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def lauchProgram(path):
    try:
        Popen(path)
    except Exception as e:
        messagebox.showerror('Erro ao lançar o programa, talvez terá que escolher o caminho novamente')

def programMenu(event, path):
    MiniMenu = tk.Menu(root, tearoff=0) # Mini menu, o secundario pequeninin

    MiniMenu.add_command(label='Executar programa', command=lambda: lauchProgram(path))
    MiniMenu.add_command(label='Definir imagem', command=lambda: pickImage(path))
    MiniMenu.add_separator()
    MiniMenu.add_command(label='Remover programa', command=lambda: deleteProgram(path))
    
    try:
        MiniMenu.tk_popup(event.x_root, event.y_root)
    finally:
        MiniMenu.grab_release()

def refreshList():
    cards = mainFrame.winfo_children()
    for widget in cards:
        widget.destroy()

    programs = db.getAllPrograms()
    columns = 3
    for col in range(columns):
        mainFrame.grid_columnconfigure(col, weight=1)
    
    for index, program in enumerate(programs):
        row = index // columns
        col = index % columns
        id, name, path, imgPath = program
        card = createCard(name, path, imgPath)
        card.grid(row=row, column=col, padx=20, pady=20)
        
def deleteProgram(path):
    db.deleteProgram(path)
    refreshList()

def on_enter(e):
    """Change button style when mouse enters."""
    e.widget['background'] = 'lightgrey' 
    # e.widget['foreground'] = 'white'    # White text

def on_leave(e):
    """Revert button style when mouse leaves."""
    # e.widget['background'] = 'SystemButtonFace'  # Default button color
    e.widget['background'] = 'grey'
    e.widget['foreground'] = 'black'             # Default text color

db.createTable() # garantir que a tabela seja atualizada depois da exclusão

root = tk.Tk()
root.title('Catalogo de Games')
root.state('zoomed')
root.geometry('800x600')
root.minsize(800, 600)

sideFrame = tk.Frame(root, bg="lightgrey", width=180)
sideFrame.pack_propagate(False)
sideFrame.pack(side="left", fill='y')

text1 = 'Bem vindo ou meu catalogo!, um local para organizar seus programas ou jogos para ter um mais facil e personalizado acesso!'
text2 = 'Para adicionar seus programas, clique no botão de + mostrado na tela ali embaixo'
tutorial = tk.Label(sideFrame, text=text1, pady=15, wraplength=180, font=('Arial', 10, 'bold'), bg='lightgrey')
tutorial.pack(pady=15)

tutorial2 = tk.Label(sideFrame, text=text2, pady=15, wraplength=180, font=('Arial', 10, 'bold'), bg='lightgrey')
tutorial2.pack(pady=15)

mainFrame = tk.Frame(root)
mainFrame.pack(fill="both", expand=True)

btnAdd = tk.Button(root, text="+",font=('Arial', 30, 'bold'), relief='flat',bg='grey',activebackground='grey', padx=20, pady=10, command=addProgram)
btnAdd.place(relx=0.97, rely=0.95, anchor='se')
btnAdd.config(cursor='hand2')

btnAdd.bind('<Enter>', on_enter)
btnAdd.bind('<Leave>', on_leave)

refreshList()
root.mainloop()