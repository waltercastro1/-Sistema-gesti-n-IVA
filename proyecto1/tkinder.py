import os
import pickle
from tkinter import *
from tkinter import messagebox

# Definición de la clase Auto
class Auto:
    def __init__(self, patente, modelo, estado=1):
        self.patente = patente
        self.modelo = modelo
        self.estado = estado  # 1: Disponible, 0: Vendido

    def __str__(self):
        return f"Patente: {self.patente}, Modelo: {self.modelo}, Estado: {'Disponible' if self.estado == 1 else 'Vendido'}"

# Función para buscar un auto por patente
def buscar(fd, m, p):
    t = os.path.getsize(fd)
    fp_inicial = m.tell()
    m.seek(0, 0)
    posicion = -1
    while m.tell() < t:
        fp = m.tell()
        aut = pickle.load(m)
        if aut.patente == p:
            posicion = fp
            break
    m.seek(fp_inicial, 0)
    return posicion

# Punto 1: Alta de automóviles
def alta(fd):
    def guardar():
        patente = entry_patente.get().strip()
        if not patente or patente == "0":
            messagebox.showinfo("Alta", "Proceso cancelado.")
            ventana_alta.destroy()
            return

        try:
            modelo = int(entry_modelo.get())
        except ValueError:
            messagebox.showerror("Error", "El modelo debe ser un número entero.")
            return

        with open(fd, 'a+b') as m:
            pos = buscar(fd, m, patente)
            if pos == -1:
                aut = Auto(patente, modelo)
                pickle.dump(aut, m)
                m.flush()
                messagebox.showinfo("Alta", "Registro grabado en el archivo.")
            else:
                messagebox.showwarning("Alta", "Patente repetida... alta rechazada.")

    # Ventana para dar de alta
    ventana_alta = Toplevel(root)
    ventana_alta.title("Alta de Automóviles")
    ventana_alta.geometry("300x200")

    Label(ventana_alta, text="Patente:").pack(pady=5)
    entry_patente = Entry(ventana_alta)
    entry_patente.pack(pady=5)

    Label(ventana_alta, text="Modelo:").pack(pady=5)
    entry_modelo = Entry(ventana_alta)
    entry_modelo.pack(pady=5)

    Button(ventana_alta, text="Guardar", command=guardar).pack(pady=10)
    Button(ventana_alta, text="Cancelar", command=ventana_alta.destroy).pack(pady=5)

# Punto 2: Modificación de estado de un automóvil
def modificacion(fd):
    def modificar():
        patente = entry_patente_mod.get().strip()
        if not patente or patente == "0":
            messagebox.showinfo("Modificación", "Proceso cancelado.")
            ventana_modificacion.destroy()
            return

        if not os.path.exists(fd):
            messagebox.showerror("Error", "El archivo no existe. Use la opción 1 para crearlo.")
            return

        with open(fd, 'r+b') as m:
            pos = buscar(fd, m, patente)
            if pos != -1:
                m.seek(pos, 0)
                aut = pickle.load(m)
                if aut.estado == 0:
                    messagebox.showinfo("Modificación", "El automóvil ya fue vendido.")
                else:
                    aut.estado = 0
                    m.seek(pos, 0)
                    pickle.dump(aut, m)
                    messagebox.showinfo("Modificación", "El automóvil cambió su estado a VENDIDO.")
            else:
                messagebox.showwarning("Modificación", "Ese registro no existe en el archivo.")

    # Ventana para modificar
    ventana_modificacion = Toplevel(root)
    ventana_modificacion.title("Modificar Estado")
    ventana_modificacion.geometry("300x150")

    Label(ventana_modificacion, text="Patente del automóvil:").pack(pady=5)
    entry_patente_mod = Entry(ventana_modificacion)
    entry_patente_mod.pack(pady=5)

    Button(ventana_modificacion, text="Modificar", command=modificar).pack(pady=10)
    Button(ventana_modificacion, text="Cancelar", command=ventana_modificacion.destroy).pack(pady=5)

# Punto 3: Listado completo de automóviles
def listado_completo(fd):
    if not os.path.exists(fd):
        messagebox.showerror("Error", "El archivo no existe. Use la opción 1 para crearlo.")
        return

    lista = []
    with open(fd, 'rb') as m:
        while True:
            try:
                aut = pickle.load(m)
                lista.append(str(aut))
            except EOFError:
                break

    # Mostrar listado en una nueva ventana
    ventana_listado = Toplevel(root)
    ventana_listado.title("Listado Completo")
    ventana_listado.geometry("400x300")

    scrollbar = Scrollbar(ventana_listado)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(ventana_listado, yscrollcommand=scrollbar.set)
    for item in lista:
        listbox.insert(END, item)
    listbox.pack(fill=BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

# Punto 4: Listado filtrado de automóviles disponibles
def listado_filtrado(fd):
    def filtrar():
        try:
            modelo = int(entry_modelo_filtro.get())
        except ValueError:
            messagebox.showerror("Error", "El modelo debe ser un número entero.")
            return

        if not os.path.exists(fd):
            messagebox.showerror("Error", "El archivo no existe. Use la opción 1 para crearlo.")
            return

        lista = []
        with open(fd, 'rb') as m:
            while True:
                try:
                    aut = pickle.load(m)
                    if aut.estado == 1 and aut.modelo > modelo:
                        lista.append(str(aut))
                except EOFError:
                    break

        # Mostrar listado en una nueva ventana
        ventana_filtrado = Toplevel(root)
        ventana_filtrado.title("Listado Filtrado")
        ventana_filtrado.geometry("400x300")

        scrollbar = Scrollbar(ventana_filtrado)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(ventana_filtrado, yscrollcommand=scrollbar.set)
        for item in lista:
            listbox.insert(END, item)
        listbox.pack(fill=BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

    # Ventana para filtrar
    ventana_filtro = Toplevel(root)
    ventana_filtro.title("Filtrar Automóviles")
    ventana_filtro.geometry("300x150")

    Label(ventana_filtro, text="Modelo mínimo:").pack(pady=5)
    entry_modelo_filtro = Entry(ventana_filtro)
    entry_modelo_filtro.pack(pady=5)

    Button(ventana_filtro, text="Filtrar", command=filtrar).pack(pady=10)
    Button(ventana_filtro, text="Cancelar", command=ventana_filtro.destroy).pack(pady=5)

# Menú principal
def main():
    global root
    root = Tk()
    root.title("Sistema de Gestión de Automóviles")
    root.geometry("500x400")

    Label(root, text="/////////////// Bienvenido a nuestro Menu Automóviles ///////////////", font=("Arial", 14)).pack(pady=10)
    Label(root, text="Seleccione una opción:", font=("Arial", 12)).pack(pady=10)

    Button(root, text="1. Alta de Automóviles", command=lambda: alta("automoviles.aut"), width=30).pack(pady=5)
    Button(root, text="2. Modificación de Estado", command=lambda: modificacion("automoviles.aut"), width=30).pack(pady=5)
    Button(root, text="3. Listado Completo", command=lambda: listado_completo("automoviles.aut"), width=30).pack(pady=5)
    Button(root, text="4. Listado Filtrado", command=lambda: listado_filtrado("automoviles.aut"), width=30).pack(pady=5)
    Button(root, text="0. Salir", command=root.quit, width=30).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()