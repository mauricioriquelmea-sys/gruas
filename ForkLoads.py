import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Requiere: pip install Pillow
import sys
import os

class AppCargasPortuarias:
    def __init__(self, root):
        self.root = root
        self.root.title("Structural Lab | Cargas Maquinaria Portuaria")
        self.root.geometry("950x700") 
        self.root.configure(bg="#ffffff")

        self.font_title = ("Arial", 14, "bold")
        self.font_label = ("Arial", 10)
        
        # --- LÓGICA DE RUTA PARA IMÁGENES ---
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
            
        self.create_widgets()

    def create_widgets(self):
        # Título Superior
        tk.Label(self.root, text="ESTIMACIÓN DE CARGAS DE MAQUINARIA PORTUARIA", 
                 font=self.font_title, bg="#003366", fg="white", pady=15).pack(fill=tk.X)

        # Contenedor Principal (Dos columnas)
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # --- COLUMNA IZQUIERDA: INPUTS Y RESULTADOS ---
        left_col = tk.Frame(main_frame, bg="#ffffff")
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        frame_inputs = tk.LabelFrame(left_col, text=" Parámetros de Entrada ", font=("Arial", 10, "bold"), bg="#f8f9fa", padx=15, pady=15)
        frame_inputs.pack(fill=tk.X)

        self.vars = {
            "Wc": ["Carga Contenedor (Wc) [kg]:", "30000"],
            "Wt": ["Peso Cargador (Wt) [kg]:", "50000"],
            "Fd": ["Factor Dinámico (Fd):", "1.20"],
            "M":  ["Ruedas Eje Frontal (M):", "4"],
            "X1": ["Distancia X1 [m]:", "1.50"],
            "X2": ["Distancia X2 [m]:", "-3.50"],
            "Xt": ["Distancia XT [m]:", "-1.00"]
        }

        self.entries = {}
        for i, (key, info) in enumerate(self.vars.items()):
            tk.Label(frame_inputs, text=info[0], font=self.font_label, bg="#f8f9fa").grid(row=i, column=0, sticky="w", pady=3)
            entry = tk.Entry(frame_inputs, width=15)
            entry.insert(0, info[1])
            entry.grid(row=i, column=1, pady=3, padx=10)
            self.entries[key] = entry

        self.btn_calc = tk.Button(left_col, text="CALCULAR CARGAS", command=self.calcular,
                                  bg="#c0392b", fg="white", font=("Arial", 11, "bold"), pady=8, cursor="hand2")
        self.btn_calc.pack(pady=15, fill=tk.X)

        self.frame_res = tk.LabelFrame(left_col, text=" Resultados Finales ", font=("Arial", 10, "bold"), bg="#f8f9fa", padx=15, pady=15)
        self.frame_res.pack(fill=tk.X)

        self.lbl_w1 = tk.Label(self.frame_res, text="W1 (Carga Frontal): ---", font=("Arial", 11, "bold"), fg="#003366", bg="#f8f9fa")
        self.lbl_w1.pack(pady=5)
        self.lbl_w2 = tk.Label(self.frame_res, text="W2 (Carga Trasera): ---", font=("Arial", 11, "bold"), fg="#27ae60", bg="#f8f9fa")
        self.lbl_w2.pack(pady=5)

        # --- COLUMNA DERECHA: IMÁGEN DE REFERENCIA ---
        right_col = tk.Frame(main_frame, bg="#ffffff")
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_col, text="Esquema de Distribución de Cargas (Figura 4.2)", font=("Arial", 10, "italic"), bg="#ffffff").pack()
        
        # Cargar y mostrar la imagen F1.jpg con ruta absoluta
        img_path = os.path.join(self.base_path, "F1.jpg")
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"No se encuentra F1.jpg en: {self.base_path}")
                
            pil_img = Image.open(img_path)
            # Redimensionar dinámicamente
            pil_img = pil_img.resize((500, 420), Image.LANCZOS)
            self.img_ref = ImageTk.PhotoImage(pil_img)
            img_label = tk.Label(right_col, image=self.img_ref, bg="#ffffff")
            img_label.pack(pady=10)
        except Exception as e:
            tk.Label(right_col, text=f"\n\n⚠️ Error de Archivo:\n{e}", fg="red", bg="#ffffff", font=("Arial", 9)).pack()

    def calcular(self):
        try:
            wc = float(self.entries["Wc"].get())
            wt = float(self.entries["Wt"].get())
            fd = float(self.entries["Fd"].get())
            m = float(self.entries["M"].get())
            x1 = float(self.entries["X1"].get())
            x2 = float(self.entries["X2"].get())
            xt = float(self.entries["Xt"].get())

            if x1 == x2:
                messagebox.showerror("Error", "X1 y X2 no pueden ser iguales (división por cero).")
                return

            # Ecuación 4.7
            a1 = -x2 / (x1 - x2)
            a2 = -x1 / (x2 - x1)
            b1 = (wt * (xt - x2)) / (x1 - x2)
            b2 = (wt * (xt - x1)) / (x2 - x1)

            # Ecuación 4.6
            w1 = fd * ((a1 * wc + b1) / m)
            w2 = fd * ((a2 * wc + b2) / 2)

            self.lbl_w1.config(text=f"W1 (Carga Frontal): {w1:,.1f} kg")
            self.lbl_w2.config(text=f"W2 (Carga Trasera): {w2:,.1f} kg")

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCargasPortuarias(root)
    root.mainloop()