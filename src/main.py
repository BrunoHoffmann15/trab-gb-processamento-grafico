import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from components.filter import filter_options
from components.sticker import add_stickers_to_image, add_activated_stickers_sticker, stickers_options

img_frame = None  
original_image = None  
cap = None
activated_filter = None
video_running = False
positions_to_apply_sticker = []
sticker_selected = None

# Função para renderizar imagem
def render_image():
    global img_frame, original_image

    stop_camera()

    if original_image is None:
        return

    # Pega a imagem original
    img_frame = original_image.copy()
    img_frame = add_stickers_to_image(img_frame)
    img_frame = apply_filter(img_frame)

    # Ajusta a imagem
    img_frame = cv.resize(img_frame, (400, 400))
    img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)
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

        canvas.itemconfig(image_container, image="")
        canvas.image = None

def resize_video(frame):
    altura_original, largura_original = frame.shape[:2]

    canvas_size = 400

    # Calcular o ponto de corte para centralizar
    x_centro = largura_original // 2
    y_centro = altura_original // 2

    # Calcular as coordenadas para cortar a imagem
    x_inicio = max(0, x_centro - canvas_size // 2)
    y_inicio = max(0, y_centro - canvas_size // 2)
    x_fim = x_inicio + canvas_size
    y_fim = y_inicio + canvas_size

    # Garantir que os limites não extrapolem a imagem original
    x_fim = min(x_fim, largura_original)
    y_fim = min(y_fim, altura_original)

    imagem_recortada = frame[y_inicio:y_fim, x_inicio:x_fim]

    imagem_ajustada = cv.resize(imagem_recortada, (canvas_size, canvas_size), interpolation=cv.INTER_AREA)

    return imagem_ajustada


def update_video_frame():
    global cap, video_running

    if video_running:
        ret, frame = cap.read()

        if ret:
            # Aplica o filtro no vídeo
            frame = resize_video(frame)  # Resize

            frame = add_stickers_to_image(frame)
            frame = apply_filter(frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # Converte para uma imagem Tkinter
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.itemconfig(image_container, image=imgtk)
            canvas.image = imgtk  # Referência para evitar garbage collection

            # Continue updating
            canvas.after(10, update_video_frame)
        else:
            cap.release()

# Função para capturar vídeo e exibir no canvas
def open_camera():
    global cap, video_running

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        tk.messagebox.showerror("Error", "Could not access the camera")
        return

    video_running = True
    update_video_frame()

# Função para fazer upload de uma imagem
def upload_photo():
    global img_frame, original_image

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if file_path:
        img = cv.imread(file_path)
        original_image = cv.resize(img, (400, 400))

        img_frame = original_image.copy() 
        render_image()

def apply_filter(frame):
    if activated_filter:
        frame = activated_filter(frame)
    return frame

# Função para selecionar o filtro
def select_filter(filter_name):
    global activated_filter
    activated_filter = filter_options.get(filter_name)

    if not video_running:
        render_image()

def on_canvas_click(event):
    global img_frame, sticker_selected

    if sticker_selected is None:
        return
    
    # Coordenadas do clique
    x, y = event.x, event.y
    add_activated_stickers_sticker(sticker_selected, x, y)

    if not video_running:
        render_image()

# Função para adicionar stickers
def add_sticker(sticker_name):
    global sticker_selected
    sticker_selected = sticker_name

    print(f"Sticker '{sticker_name}' adicionado!")

# Criação da interface principal
root = tk.Tk()
root.title("Photo Editor")

# Botões Principais
image_frame = tk.LabelFrame(root, text="Image", padx=5, pady=5)
image_frame.grid(row=0, column=0, columnspan=4, pady=10)

camera_btn = tk.Button(image_frame, text="Open Camera", command=open_camera)
camera_btn.grid(row=1, column=0, padx=5, pady=5)

upload_btn = tk.Button(image_frame, text="Upload Photo", command=upload_photo)
upload_btn.grid(row=1, column=1, padx=5, pady=5)

# Canvas para exibir a imagem
canvas = tk.Canvas(root, width=400, height=400, bg="gray")
canvas.grid(row=1, column=0, columnspan=4, pady=10)
image_container = canvas.create_image(200, 200, anchor=tk.CENTER)

canvas.bind("<Button-1>", on_canvas_click)

# Botões por filtros
filters_frame = tk.LabelFrame(root, text="Filters", padx=5, pady=5)
filters_frame.grid(row=2, column=0, columnspan=4, pady=10)

filter_names = filter_options.keys()

for i, filter_name in enumerate(filter_names):
    btn = tk.Button(filters_frame, text=filter_name, command=lambda f=filter_name: select_filter(f))
    btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)

# Botões para stickers
stickers_frame = tk.LabelFrame(root, text="Stickers", padx=5, pady=5)
stickers_frame.grid(row=3, column=0, columnspan=4, pady=10)

sticker_names = stickers_options.keys()
for i, sticker_name in enumerate(sticker_names):
    btn = tk.Button(stickers_frame, text=sticker_name, command=lambda s=sticker_name: add_sticker(s))
    btn.grid(row=0, column=i, padx=5, pady=5)

# Loop da aplicação
root.mainloop()
