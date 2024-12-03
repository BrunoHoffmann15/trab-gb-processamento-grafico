import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from components.filter import filter_options
from components.sticker import add_stickers_to_image, add_activated_stickers_sticker, remove_activated_stickers, stickers_options

# Declaração de variáveis globais.
img_frame = None  
original_image = None  
cap = None
activated_filter = None
video_running = False
positions_to_apply_sticker = []
sticker_selected = None

# Salva a imagem atual.
def save_last_image(image_frame):
    cv.imwrite("output/last_modified_image.png", image_frame)

# Função para renderizar imagem.
def render_image():
    global img_frame, original_image

    # Termina a chamada para câmera.
    stop_camera()

    # Verifica se a imagem original é nula, se sim não renderiza.
    if original_image is None:
        return

    # Pega a imagem original.
    img_frame = original_image.copy()

    # Aplica filtros e adiciona stickers.
    img_frame = add_stickers_to_image(img_frame)
    img_frame = apply_filter(img_frame)

    # Salva imagem.
    save_last_image(img_frame)

    # Adiciona cor a imagem.
    img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

    # Adiciona imagem no canvas da tela.
    img = Image.fromarray(img_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.itemconfig(image_container, image=imgtk)
    canvas.image = imgtk

# Termina a chamada da câmera
def stop_camera():
    global cap, video_running

    # Verifica se o vídeo está executando
    if video_running:
        video_running = False

        # Faz release da câmera
        if cap is not None:
            cap.release()
            cap = None

        # Remove a imagem do canvas.
        canvas.itemconfig(image_container, image="")
        canvas.image = None

# Função para fazer resize do frame e centralizar.
def resize_frame(frame):
    # Obtém o tamanho e largura original do frame.
    original_height, original_width = frame.shape[:2]

    # Considera o tamanho do canvas.
    canvas_size = 400

    # Calcula o ponto de corte para centralizar
    x_center = original_width // 2
    y_center = original_height // 2

    # Calcula as coordenadas para cortar a imagem
    x_inicio = max(0, x_center - canvas_size // 2)
    y_inicio = max(0, y_center - canvas_size // 2)
    x_fim = x_inicio + canvas_size
    y_fim = y_inicio + canvas_size

    # Garantir que os limites não extrapolem a imagem original
    x_fim = min(x_fim, original_width)
    y_fim = min(y_fim, original_height)

    # Realiza o corte da imagem.
    imagem_recortada = frame[y_inicio:y_fim, x_inicio:x_fim]

    # Chama o resize passando o tamanho do canvas.
    imagem_ajustada = cv.resize(imagem_recortada, (canvas_size, canvas_size), interpolation=cv.INTER_AREA)

    return imagem_ajustada

# Função para fazer update do frame do vídeo.
def update_video_frame():
    global cap, video_running

    # Verifica se o vídeo está executando.
    if video_running:
        ret, frame = cap.read()

        if ret:
            # Aplica o resize no frame atual.
            frame = resize_frame(frame)

            # Aplica filtros e stickers.
            frame = add_stickers_to_image(frame)
            frame = apply_filter(frame)

            # Salva imagem.
            save_last_image(frame)

            # Adiciona cor para foto.
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            # Adiona imagem no canvas.
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.itemconfig(image_container, image=imgtk)
            canvas.image = imgtk

            # Adiciona after para continuar fazendo update dos frames.
            canvas.after(10, update_video_frame)
        else:
            cap.release()

# Função para capturar vídeo e exibir no canvas
def open_camera():
    global cap, video_running

    cap = cv.VideoCapture(0)

    # Verifica se é possível abrir a câmera.
    if not cap.isOpened():
        tk.messagebox.showerror("Error", "Could not access the camera")
        return

    video_running = True

    # Realiza o update do frame do vídeo.
    update_video_frame()

# Função para fazer upload de uma imagem
def upload_photo():
    global img_frame, original_image

    # Obtém a pasta para importar.
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    # Verifica se a pasta existe.
    if file_path:
        # Lê o conteúdo do arquivo.
        img = cv.imread(file_path)

        # Faz o resize da imagem e armazena como original.
        original_image = cv.resize(img, (400, 400))

        # Faz a cópia da foto original para o image_frame.
        img_frame = original_image.copy() 

        # Renderiza a imagem.
        render_image()

# Função para adicionar filtro.
def apply_filter(frame):
    if activated_filter:
        frame = activated_filter(frame)
    return frame

# Função para selecionar o filtro
def select_filter(filter_name):
    global activated_filter

    # Obtém o filtro ativo.
    activated_filter = filter_options.get(filter_name)

    # Se vídeo não está executando renderiza a imagem.
    if not video_running:
        render_image()

# Função de controle do processo de onclick do canvas.
def on_canvas_click(event):
    global img_frame, sticker_selected

    # Verifica se não há stickers selecionados.
    if sticker_selected is None:
        return
    
    # Obtém coordenadas do clique.
    x, y = event.x, event.y

    # Adiciona o sticker como ativo.
    add_activated_stickers_sticker(sticker_selected, x, y)

    # Verifica se precisa renderizar imagem.
    if not video_running:
        render_image()

# Função para adicionar stickers.
def handle_sticker(option_selected):
    global sticker_selected

    # Verifica se precisa limpar os sticker.
    if option_selected == "Limpar Todos":
        sticker_selected = None

        # Remove todos os stickers
        remove_activated_stickers()

        # Verifica se precisa renderizar imagem.
        if not video_running:
            render_image()

    else:
        sticker_selected = option_selected

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
    btn = tk.Button(stickers_frame, text=sticker_name, command=lambda s=sticker_name: handle_sticker(s))
    btn.grid(row=0, column=i, padx=5, pady=5)

# Loop da aplicação
root.mainloop()
