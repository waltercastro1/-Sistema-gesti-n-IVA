import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import os

# Archivo donde se guardarán los datos
ARCHIVO_DATOS = "datos_iva.pkl"
ARCHIVO_USUARIOS = "usuarios.pkl"

# Variables globales
transacciones = []
libro_iva_ventas = []
libro_iva_compras = []

# Cargar datos al iniciar el programa
def cargar_datos():
    global transacciones, libro_iva_ventas, libro_iva_compras
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "rb") as archivo:
            datos = pickle.load(archivo)
            transacciones = datos["transacciones"]
            libro_iva_ventas = datos["libro_iva_ventas"]
            libro_iva_compras = datos["libro_iva_compras"]

        # Asegurarse de que todas las transacciones tengan un ID
        for i, t in enumerate(transacciones):
            if "id" not in t:
                t["id"] = i + 1  # Asignar un ID único basado en su posición en la lista
    else:
        transacciones = []
        libro_iva_ventas = []
        libro_iva_compras = []

# Guardar datos al cerrar el programa
def guardar_datos():
    datos = {
        "transacciones": transacciones,
        "libro_iva_ventas": libro_iva_ventas,
        "libro_iva_compras": libro_iva_compras
    }
    with open(ARCHIVO_DATOS, "wb") as archivo:
        pickle.dump(datos, archivo)

# Función para cargar usuarios
def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "rb") as archivo:
            return pickle.load(archivo)
    else:
        # Usuarios predeterminados
        usuarios = {
            "admin": {"contraseña": "admin123", "rol": "administrador"},
            "empleado": {"contraseña": "empleado123", "rol": "empleado"}
        }
        with open(ARCHIVO_USUARIOS, "wb") as archivo:
            pickle.dump(usuarios, archivo)
        return usuarios

# Función para verificar credenciales
def verificar_credenciales(usuario, contraseña):
    usuarios = cargar_usuarios()
    if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
        return usuarios[usuario]["rol"]
    return None

# Función para agregar una transacción
def agregar_transaccion():
    def guardar():
        tipo = combo_tipo.get()
        fecha = entry_fecha.get().strip()
        concepto = entry_concepto.get().strip()
        try:
            importe = float(entry_importe.get())
        except ValueError:
            messagebox.showerror("Error", "El importe debe ser un número válido.")
            return

        iva = importe * 0.21
        id_transaccion = len(transacciones) + 1
        transacciones.append({
            'id': id_transaccion,
            'tipo': tipo,
            'fecha': fecha,
            'concepto': concepto,
            'importe': importe,
            'iva': iva
        })
        if tipo == 'venta':
            libro_iva_ventas.append({
                'id': id_transaccion,
                'fecha': fecha,
                'importe': importe,
                'iva': iva
            })
        elif tipo == 'compra':
            libro_iva_compras.append({
                'id': id_transaccion,
                'fecha': fecha,
                'importe': importe,
                'iva': iva
            })
        messagebox.showinfo("Éxito", "Transacción agregada correctamente.")
        ventana_agregar.destroy()

    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Transacción")
    ventana_agregar.geometry("400x300")
    ventana_agregar.config(bg="#f0f8ff")

    tk.Label(ventana_agregar, text="Tipo:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    combo_tipo = ttk.Combobox(ventana_agregar, values=["venta", "compra"], state="readonly")
    combo_tipo.pack(pady=5)

    tk.Label(ventana_agregar, text="Fecha (YYYY-MM-DD):", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.pack(pady=5)

    tk.Label(ventana_agregar, text="Concepto:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_concepto = tk.Entry(ventana_agregar)
    entry_concepto.pack(pady=5)

    tk.Label(ventana_agregar, text="Importe ($):", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_importe = tk.Entry(ventana_agregar)
    entry_importe.pack(pady=5)

    tk.Button(ventana_agregar, text="Guardar", command=guardar, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=10)
    tk.Button(ventana_agregar, text="Cancelar", command=ventana_agregar.destroy, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=5)

# Función para ver las transacciones
def ver_transacciones():
    ventana_ver = tk.Toplevel(root)
    ventana_ver.title("Ver Transacciones")
    ventana_ver.geometry("800x400")
    ventana_ver.config(bg="#f0f8ff")

    tk.Label(ventana_ver, text="ID\tTipo\tFecha\t\tConcepto\t\tImporte\t\tIVA", font=("Arial", 10, "bold"), bg="#f0f8ff").pack(anchor="w", padx=10)

    texto = tk.Text(ventana_ver, wrap=tk.NONE, bg="#ffffff", font=("Arial", 10))
    texto.pack(fill=tk.BOTH, expand=True)

    for t in transacciones:
        texto.insert(tk.END, f'{t["id"]}\t{t["tipo"]}\t{t["fecha"]}\t{t["concepto"]}\t${t["importe"]:.2f}\t${t["iva"]:.2f}\n')

    scrollbar = tk.Scrollbar(ventana_ver, orient=tk.VERTICAL, command=texto.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    texto.config(yscrollcommand=scrollbar.set)

# Función para calcular el balance
def calcular_balance():
    ventas = sum([t['importe'] for t in transacciones if t['tipo'] == 'venta'])
    compras = sum([t['importe'] for t in transacciones if t['tipo'] == 'compra'])
    iva_ventas = sum([t['iva'] for t in transacciones if t['tipo'] == 'venta'])
    iva_compras = sum([t['iva'] for t in transacciones if t['tipo'] == 'compra'])
    iva_total = iva_ventas - iva_compras
    balance = ventas - compras

    mensaje = (
        f'Ventas: ${ventas:.2f}\n'
        f'Compras: ${compras:.2f}\n'
        f'IVA ventas: ${iva_ventas:.2f}\n'
        f'IVA compras: ${iva_compras:.2f}\n'
        f'IVA total: ${iva_total:.2f}\n'
        f'Balance: ${balance:.2f}'
    )
    messagebox.showinfo("Balance", mensaje)

# Función para generar el libro de IVA de ventas
def generar_iva_ventas():
    ventana_iva_ventas = tk.Toplevel(root)
    ventana_iva_ventas.title("Libro IVA Ventas")
    ventana_iva_ventas.geometry("800x400")
    ventana_iva_ventas.config(bg="#f0f8ff")

    tk.Label(ventana_iva_ventas, text="Fecha\t\tImporte\t\tIVA", font=("Arial", 10, "bold"), bg="#f0f8ff").pack(anchor="w", padx=10)

    texto = tk.Text(ventana_iva_ventas, wrap=tk.NONE, bg="#ffffff", font=("Arial", 10))
    texto.pack(fill=tk.BOTH, expand=True)

    for t in libro_iva_ventas:
        texto.insert(tk.END, f'{t["fecha"]}\t${t["importe"]:.2f}\t${t["iva"]:.2f}\n')

    scrollbar = tk.Scrollbar(ventana_iva_ventas, orient=tk.VERTICAL, command=texto.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    texto.config(yscrollcommand=scrollbar.set)

# Función para generar el libro de IVA de compras
def generar_iva_compras():
    ventana_iva_compras = tk.Toplevel(root)
    ventana_iva_compras.title("Libro IVA Compras")
    ventana_iva_compras.geometry("800x400")
    ventana_iva_compras.config(bg="#f0f8ff")

    tk.Label(ventana_iva_compras, text="Fecha\t\tImporte\t\tIVA", font=("Arial", 10, "bold"), bg="#f0f8ff").pack(anchor="w", padx=10)

    texto = tk.Text(ventana_iva_compras, wrap=tk.NONE, bg="#ffffff", font=("Arial", 10))
    texto.pack(fill=tk.BOTH, expand=True)

    for t in libro_iva_compras:
        texto.insert(tk.END, f'{t["fecha"]}\t${t["importe"]:.2f}\t${t["iva"]:.2f}\n')

    scrollbar = tk.Scrollbar(ventana_iva_compras, orient=tk.VERTICAL, command=texto.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    texto.config(yscrollcommand=scrollbar.set)

# Función para eliminar una transacción
def eliminar_transaccion():
    def eliminar():
        try:
            id_eliminar = int(entry_id.get())
            transaccion_encontrada = None
            for t in transacciones:
                if t['id'] == id_eliminar:
                    transaccion_encontrada = t
                    break

            if transaccion_encontrada:
                transacciones[:] = [t for t in transacciones if t['id'] != id_eliminar]
                if transaccion_encontrada['tipo'] == 'venta':
                    libro_iva_ventas[:] = [v for v in libro_iva_ventas if v['id'] != id_eliminar]
                elif transaccion_encontrada['tipo'] == 'compra':
                    libro_iva_compras[:] = [c for c in libro_iva_compras if c['id'] != id_eliminar]
                messagebox.showinfo("Éxito", "Transacción eliminada correctamente.")
                ventana_eliminar.destroy()
            else:
                messagebox.showerror("Error", "ID de transacción no encontrado.")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número válido.")

    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Transacción")
    ventana_eliminar.geometry("300x200")
    ventana_eliminar.config(bg="#f0f8ff")

    tk.Label(ventana_eliminar, text="ID de la transacción a eliminar:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_id = tk.Entry(ventana_eliminar)
    entry_id.pack(pady=5)

    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=10)
    tk.Button(ventana_eliminar, text="Cancelar", command=ventana_eliminar.destroy, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)

# Función para modificar una transacción
def modificar_transaccion():
    def modificar():
        try:
            id_modificar = int(entry_id.get())
            transaccion_encontrada = None
            for t in transacciones:
                if t['id'] == id_modificar:
                    transaccion_encontrada = t
                    break

            if transaccion_encontrada:
                tipo = combo_tipo.get()
                fecha = entry_fecha.get().strip()
                concepto = entry_concepto.get().strip()
                importe = float(entry_importe.get())
                iva = importe * 0.21

                # Actualizar la transacción
                transaccion_encontrada.update({
                    'tipo': tipo,
                    'fecha': fecha,
                    'concepto': concepto,
                    'importe': importe,
                    'iva': iva
                })

                # Actualizar el libro correspondiente
                if tipo == 'venta':
                    for v in libro_iva_ventas:
                        if v['id'] == id_modificar:
                            v.update({
                                'fecha': fecha,
                                'importe': importe,
                                'iva': iva
                            })
                elif tipo == 'compra':
                    for c in libro_iva_compras:
                        if c['id'] == id_modificar:
                            c.update({
                                'fecha': fecha,
                                'importe': importe,
                                'iva': iva
                            })

                messagebox.showinfo("Éxito", "Transacción modificada correctamente.")
                ventana_modificar.destroy()
            else:
                messagebox.showerror("Error", "ID de transacción no encontrado.")
        except ValueError:
            messagebox.showerror("Error", "El ID o el importe deben ser números válidos.")

    ventana_modificar = tk.Toplevel(root)
    ventana_modificar.title("Modificar Transacción")
    ventana_modificar.geometry("400x300")
    ventana_modificar.config(bg="#f0f8ff")

    tk.Label(ventana_modificar, text="ID de la transacción a modificar:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_id = tk.Entry(ventana_modificar)
    entry_id.pack(pady=5)

    tk.Label(ventana_modificar, text="Nuevo tipo:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    combo_tipo = ttk.Combobox(ventana_modificar, values=["venta", "compra"], state="readonly")
    combo_tipo.pack(pady=5)

    tk.Label(ventana_modificar, text="Nueva fecha (YYYY-MM-DD):", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_fecha = tk.Entry(ventana_modificar)
    entry_fecha.pack(pady=5)

    tk.Label(ventana_modificar, text="Nuevo concepto:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_concepto = tk.Entry(ventana_modificar)
    entry_concepto.pack(pady=5)

    tk.Label(ventana_modificar, text="Nuevo importe ($):", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_importe = tk.Entry(ventana_modificar)
    entry_importe.pack(pady=5)

    tk.Button(ventana_modificar, text="Modificar", command=modificar, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=10)
    tk.Button(ventana_modificar, text="Cancelar", command=ventana_modificar.destroy, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=5)

# Pantalla de inicio de sesión
def pantalla_inicio_sesion():
    def iniciar_sesion():
        usuario = entry_usuario.get().strip()
        contraseña = entry_contraseña.get().strip()
        rol = verificar_credenciales(usuario, contraseña)
        if rol:
            messagebox.showinfo("Inicio de Sesión", f"Bienvenido, {usuario} ({rol})")
            ventana_login.destroy()
            main(rol)  # Pasamos el rol al menú principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("300x200")
    ventana_login.config(bg="#f0f8ff")

    tk.Label(ventana_login, text="Usuario:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:", bg="#f0f8ff", font=("Arial", 10)).pack(pady=5)
    entry_contraseña = tk.Entry(ventana_login, show="*")
    entry_contraseña.pack(pady=5)

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=10)
    tk.Button(ventana_login, text="Salir", command=ventana_login.quit, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=5)

    ventana_login.mainloop()

# Menú principal (restringido por rol)
def main(rol):
    global root
    root = tk.Tk()
    root.title("Sistema de Gestión de IVA")
    root.geometry("500x500")
    root.config(bg="#e0f7fa")

    # Cargar datos al iniciar
    cargar_datos()

    tk.Label(root, text="--- Sistema de Gestión de IVA ---", font=("Arial", 14, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=10)
    tk.Label(root, text="Seleccione una opción:", font=("Arial", 12), bg="#e0f7fa", fg="#00796b").pack(pady=10)

    # Funciones disponibles para todos los roles
    tk.Button(root, text="1. Agregar Transacción", command=agregar_transaccion, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)
    tk.Button(root, text="2. Ver Transacciones", command=ver_transacciones, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)
    tk.Button(root, text="3. Calcular Balance", command=calcular_balance, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)
    tk.Button(root, text="4. Generar Libro IVA Ventas", command=generar_iva_ventas, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)
    tk.Button(root, text="5. Generar Libro IVA Compras", command=generar_iva_compras, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)

    # Funciones disponibles solo para administradores
    if rol == "administrador":
        tk.Button(root, text="6. Eliminar Transacción", command=eliminar_transaccion, width=30, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=5)
        tk.Button(root, text="7. Modificar Transacción", command=modificar_transaccion, width=30, bg="#76c893", fg="white", font=("Arial", 10)).pack(pady=5)

    tk.Button(root, text="0. Salir", command=lambda: [guardar_datos(), root.quit()], width=30, bg="#ff6b6b", fg="white", font=("Arial", 10)).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    pantalla_inicio_sesion()