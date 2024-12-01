from PIL import Image, ImageTk
import cv2 as cv

activated_stickers = []


def remove_activated_stickers():
  activated_stickers.clear()

def add_activated_stickers_sticker(sticker_name, position_x, position_y):
  activated_stickers.append({ "name": sticker_name, 
                             "position_x": position_x, 
                             "position_y": position_y, 
                             "path": stickers_options[sticker_name]["path"],
                             "scale": stickers_options[sticker_name]["scale"]})

def add_stickers_to_image(image_frame):
  if image_frame is None:
    return
  
  for sticker in activated_stickers:
    background = image_frame
    foreground = cv.imread(sticker["path"], cv.IMREAD_UNCHANGED)
    foreground = cv.cvtColor(foreground, cv.COLOR_BGRA2RGBA)

    width = int(foreground.shape[1] * sticker["scale"])
    height = int(foreground.shape[0] * sticker["scale"])
    dimension = (width, height)

    foreground = cv.resize(foreground, dimension, interpolation=cv.INTER_AREA)

    image_frame = apply_sticker(background, foreground, sticker["position_x"], sticker["position_y"])
  
  return image_frame

def apply_sticker(background, foreground, pos_x=None, pos_y=None):
    """
    Cola um sticker (foreground) com canal alpha em um fundo (background),
    ajustando posição pelo centro e cortando se ultrapassar as bordas.

    Parameters:
        background: numpy.ndarray
            Imagem de fundo (BGR).
        foreground: numpy.ndarray
            Imagem do sticker (RGBA, com canal alpha).
        pos_x: int
            Posição X do centro do sticker no fundo.
        pos_y: int
            Posição Y do centro do sticker no fundo.

    Returns:
        numpy.ndarray
            Imagem final com o sticker aplicado.
    """
    # Converter o sticker para BGR
    sticker = cv.cvtColor(foreground, cv.COLOR_RGBA2BGR)

    # Separar canais do foreground (com alpha)
    b, g, r, a = cv.split(foreground)

    # Dimensões das imagens
    f_rows, f_cols, _ = foreground.shape
    b_rows, b_cols, _ = background.shape

    # Ajustar pos_x e pos_y para serem o centro background
    if pos_x is None:
        pos_x = b_cols // 2
    if pos_y is None:
        pos_y = b_rows // 2

    # Coordenadas do sticker ajustadas para o centro
    x_start = pos_x - f_cols // 2
    y_start = pos_y - f_rows // 2

    # Calcula os cortes para evitar extrapolação das bordas
    bg_x_start = max(0, x_start)
    bg_y_start = max(0, y_start)
    bg_x_end = min(b_cols, x_start + f_cols)
    bg_y_end = min(b_rows, y_start + f_rows)

    fg_x_start = max(0, -x_start)
    fg_y_start = max(0, -y_start)
    fg_x_end = fg_x_start + (bg_x_end - bg_x_start)
    fg_y_end = fg_y_start + (bg_y_end - bg_y_start)

    # Recorta as regiões de sobreposição
    sticker = sticker[fg_y_start:fg_y_end, fg_x_start:fg_x_end]
    mask = a[fg_y_start:fg_y_end, fg_x_start:fg_x_end]
    mask_inv = cv.bitwise_not(mask)
    roi = background[bg_y_start:bg_y_end, bg_x_start:bg_x_end]

    # Combinar as imagens usando máscaras
    img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
    img_fg = cv.bitwise_and(sticker, sticker, mask=mask)
    res = cv.add(img_bg, img_fg)

    # Atualizar o fundo com o resultado
    background[bg_y_start:bg_y_end, bg_x_start:bg_x_end] = res

    return background



stickers_options = {
  'Óculos': { 'path': "./content/stickers/black-glasses-isolated-png.webp", 'scale': 0.2 },
  'Coração': { 'path': "./content/stickers/heart.webp", 'scale': 0.07 },
  'Dinossauro': { 'path': "./content/stickers/dinossauro.webp", 'scale': 0.10 },
  'Cachorro': { 'path': "./content/stickers/cachorro.webp", 'scale': 0.20 },
  'Robo': { 'path': "./content/stickers/robo.webp", 'scale': 0.24 },
  'Limpar Todos' : None
}