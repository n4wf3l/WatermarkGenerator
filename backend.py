# backend.py
from PIL import Image, ImageDraw, ImageFont

def generate_final_image(
    preview_img,           # L'aperçu PIL (500x500)
    final_size,            # La taille finale (par ex. 1080)
    watermark,             # Le watermark PIL (ou None)
    font_path,             # Chemin pour Texte 1 et 2
    font_path_text3,       # Chemin pour Texte 3 (Poppins Bold)
    text1, text1_size_factor, text1_margin, text1_color,
    text2, text2_size_factor, text2_margin, text2_color,
    text3, text3_size_factor, text3_margin, text3_color
):
    # Upscale l'aperçu pour obtenir l'image finale
    final_img = preview_img.resize((final_size, final_size), Image.LANCZOS)
    final_no_wm = final_img.copy()
    
    # Si un watermark est fourni, on le redimensionne pour couvrir toute la surface et on le colle
    if watermark:
        wm_full = watermark.resize((final_size, final_size), Image.LANCZOS)
        final_img.paste(wm_full, (0, 0), wm_full)
    
    draw = ImageDraw.Draw(final_img)
    
    # Texte 1
    if text1:
        try:
            font_size1 = int(final_size * text1_size_factor)
            font1 = ImageFont.truetype(font_path, font_size1)
        except Exception as e:
            print("Erreur de police texte 1:", e)
            font1 = ImageFont.load_default()
        margin1 = final_size * text1_margin
        x1 = final_size / 2
        y1 = final_size - (margin1 / 2)
        draw.text((x1, y1), text1, font=font1, fill=text1_color, anchor="mm")
    
    # Texte 2
    if text2:
        try:
            font_size2 = int(final_size * text2_size_factor)
            font2 = ImageFont.truetype(font_path, font_size2)
        except Exception as e:
            print("Erreur de police texte 2:", e)
            font2 = ImageFont.load_default()
        margin2 = final_size * text2_margin
        x2 = final_size / 2
        y2 = final_size - (margin2 / 2)
        draw.text((x2, y2), text2, font=font2, fill=text2_color, anchor="mm")
    
    # Texte 3 (utilise une police différente)
    if text3:
        try:
            font_size3 = int(final_size * text3_size_factor)
            font3 = ImageFont.truetype(font_path_text3, font_size3)
        except Exception as e:
            print("Erreur de police texte 3:", e)
            font3 = ImageFont.load_default()
        margin3 = final_size * text3_margin
        x3 = final_size / 2
        y3 = final_size - (margin3 / 2)
        draw.text((x3, y3), text3, font=font3, fill=text3_color, anchor="mm")
    
    final_with_wm = final_img
    return final_no_wm, final_with_wm
