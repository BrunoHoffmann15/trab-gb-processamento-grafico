import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from components.filter import filter_options
<<<<<<< HEAD
=======
from components.sticker import stickers_options, add_stickers_to_image, add_activated_stickers_sticker
>>>>>>> 9e0aeee (feat: adiciona stickers)

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

<<<<<<< HEAD
    if original_image is None:
        return

    # Pega a imagem original
    img_frame = original_image.copy()
=======
    img_frame = cv.resize(img_frame, (400, 400))
    img_frame = add_stickers_to_image(img_frame)
>>>>>>> 9e0aeee (feat: adiciona stickers)
    img_frame = apply_filter(img_frame)

    # Ajusta a imagem
    img_frame = cv.resize(img_frame, (400, 400))
    img = Image.fromarray(cv.cvtColor(img_frame, cv.COLOR_BGR2RGB))
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

def update_video_frame():
    global cap, video_running

    if video_running:
        ret, frame = cap.read()

        if ret:
            # Aplica o filtro no vídeo
            frame = apply_filter(frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = cv.resize(frame, (384, 216))  # Resize 

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
        original_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Salva a imagem original
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
<<<<<<< HEAD
    global img_frame

    # Coordenadas do click
=======
    global img_frame, sticker_selected

    if sticker_selected is None:
        return
    
    # Coordenadas do clique
>>>>>>> 9e0aeee (feat: adiciona stickers)
    x, y = event.x, event.y
    add_activated_stickers_sticker(sticker_selected, x, y)

<<<<<<< HEAD
    if img_frame is not None:
        # Adiciona um texto na imagem no local clicado
        cv.putText(img_frame, f"({x},{y})", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
=======
    if not video_running:
>>>>>>> 9e0aeee (feat: adiciona stickers)
        render_image()

# Função para adicionar stickers
def add_sticker(sticker_name):
<<<<<<< HEAD
    print(f"Sticker '{sticker_name}' added!")
=======
    global sticker_selected
    sticker_selected = sticker_name

    print(f"Sticker '{sticker_name}' adicionado!")
>>>>>>> 9e0aeee (feat: adiciona stickers)

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
