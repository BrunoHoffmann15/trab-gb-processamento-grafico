import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# Função para abrir a câmera
def open_camera():
    print("")

# Função para fazer upload de uma imagem
def upload_photo():
    print("")

# Função para aplicar filtros
def apply_filter(filter_name):
    print(f"Filtro '{filter_name}' aplicado!")

# Função para adicionar stickers
def add_sticker(sticker_name):
    print(f"Sticker '{sticker_name}' adicionado!")

# Criação da interface principal
root = tk.Tk()
root.title("Editor de Fotos")

# Botões principais
image_frame = tk.LabelFrame(root, text="Imagem", padx=5, pady=5)
image_frame.grid(row=0, column=0, columnspan=4, pady=10)

camera_btn = tk.Button(image_frame, text="Abrir Câmera", command=open_camera)
camera_btn.grid(row=1, column=0, padx=5, pady=5)

upload_btn = tk.Button(image_frame, text="Fazer Upload", command=upload_photo)
upload_btn.grid(row=1, column=1, padx=5, pady=5)

# Canvas para exibir a imagem
canvas = tk.Canvas(root, width=400, height=400, bg="gray")
canvas.grid(row=1, column=0, columnspan=4, pady=10)
image_container = canvas.create_image(200, 200, anchor=tk.CENTER)

# Botões para filtros
filters_frame = tk.LabelFrame(root, text="Filtros", padx=5, pady=5)
filters_frame.grid(row=2, column=0, columnspan=4, pady=10)

filter_names = [f"Filtro {i+1}" for i in range(10)]

for i, filter_name in enumerate(filter_names):
    btn = tk.Button(filters_frame, text=filter_name, command=lambda f=filter_name: apply_filter(f))
    btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)

# Botões para stickers
stickers_frame = tk.LabelFrame(root, text="Stickers", padx=5, pady=5)
stickers_frame.grid(row=3, column=0, columnspan=4, pady=10)

sticker_names = [f"Sticker {i+1}" for i in range(5)]
for i, sticker_name in enumerate(sticker_names):
    btn = tk.Button(stickers_frame, text=sticker_name, command=lambda s=sticker_name: add_sticker(s))
    btn.grid(row=0, column=i, padx=5, pady=5)

# Inicia o loop da interface
root.mainloop()
