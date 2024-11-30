import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from components.filter import filter_options;

img_frame = None
cap = None
activated_filter = None
video_running = False

# Função para renderizar imagem
def render_image():
    global img_frame, cap

    stop_camera()

    img_frame = apply_filter(img_frame)
    img = Image.fromarray(img_frame)
    imgtk = ImageTk.PhotoImage(image=img)

    canvas.itemconfig(image_container, image=imgtk)
    canvas.image = imgtk


def stop_camera():
    global cap, video_running

    if video_running:
        video_running = False

        if cap is not None:
            cap.release()
            cap = None

        # Limpa o Canvas
        canvas.itemconfig(image_container, image="")
        canvas.image = None


def update_video_frame():
    global cap, video_running

    if video_running:
        ret, frame = cap.read()

        if ret:
            # Converte o frame para RGB
            frame = apply_filter(frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = cv.resize(frame, (384, 216))  # Ajusta ao tamanho do canvas

            # Converte o frame para uma imagem do Tkinter
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.itemconfig(image_container, image=imgtk)
            canvas.image = imgtk  # Referência para evitar garbage collection

            # Continua atualizando
            canvas.after(10, update_video_frame)
        else:
            cap.release()

# Função para capturar vídeo e exibir no canvas
def open_camera():
    global cap, video_running

    # Inicializa a captura de vídeo

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        tk.messagebox.showerror("Erro", "Não foi possível acessar a câmera")
        return

    # Atualiza os frames no canvas
    video_running = True
    update_video_frame()

# Função para fazer upload de uma imagem
def upload_photo():
    global img_frame
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if file_path:
        img = cv.imread(file_path)
        img_frame = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        render_image()


def apply_filter(frame):
    if activated_filter:
        frame = activated_filter(frame)
    
    return frame

# Função para aplicar filtros
def select_filter(filter_name):
    global activated_filter
    activated_filter = filter_options.get(filter_name)

    if not video_running:
        render_image()

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

filter_names = filter_options.keys()

for i, filter_name in enumerate(filter_names):
    btn = tk.Button(filters_frame, text=filter_name, command=lambda f=filter_name: select_filter(f))
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
