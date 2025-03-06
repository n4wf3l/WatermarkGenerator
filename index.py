import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

font_path = "Elemental End italic.ttf"  # Pour Texte 1 et 2
font_path_text3 = "Poppins-Bold.ttf"      # Pour Texte 3

FINAL_SIZE = 1080   # Taille finale (1080x1080)
PREVIEW_SIZE = 500  # Taille de l'aperçu (500x500)

class SnapshotEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur d'Image - Snapshot")
        self.root.geometry("900x950")
        self.root.configure(bg="#2C2F33")
        
        # Création d'un conteneur scrollable
        container = tk.Frame(root, bg="#2C2F33")
        container.pack(fill="both", expand=True)
        
        self.canvas_scroll = tk.Canvas(container, bg="#2C2F33")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollable_frame = tk.Frame(self.canvas_scroll, bg="#2C2F33")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(
                scrollregion=self.canvas_scroll.bbox("all")
            )
        )
        
        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Widgets dans le conteneur scrollable ---
        # Canvas d'aperçu
        self.canvas = tk.Canvas(self.scrollable_frame, width=PREVIEW_SIZE, height=PREVIEW_SIZE, bg="white")
        self.canvas.pack(pady=10)
        
        # Contrôles de déplacement et zoom
        control_frame = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="↑", command=lambda: self.move(0, -20), width=5).grid(row=0, column=1)
        tk.Button(control_frame, text="←", command=lambda: self.move(-20, 0), width=5).grid(row=1, column=0)
        tk.Button(control_frame, text="→", command=lambda: self.move(20, 0), width=5).grid(row=1, column=2)
        tk.Button(control_frame, text="↓", command=lambda: self.move(0, 20), width=5).grid(row=2, column=1)
        tk.Button(control_frame, text="+", command=self.zoom_in, width=5).grid(row=1, column=1, padx=10)
        tk.Button(control_frame, text="-", command=self.zoom_out, width=5).grid(row=3, column=1)
        
        # Zone de saisie pour 3 textes avec boutons de contrôle et couleur
        
        # Texte 1 (Elemental End italic, marge haute, couleur par défaut blanc)
        self.text1_size_factor = 0.12
        self.text1_margin = 0.50
        self.text1_color = "white"
        frame1 = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        frame1.pack(pady=5)
        tk.Label(frame1, text="Texte 1 (Elemental End italic, marge haute)", bg="#2C2F33", fg="white").grid(row=0, column=0, columnspan=5)
        self.text_input1 = tk.Entry(frame1, font=("Arial", 14))
        self.text_input1.grid(row=1, column=0, columnspan=4, pady=2)
        self.text_input1.insert(0, "Votre texte 1 ici")
        tk.Button(frame1, text="+T", command=lambda: self.adjust_text_size(1, 1), width=4).grid(row=2, column=0)
        tk.Button(frame1, text="-T", command=lambda: self.adjust_text_size(1, -1), width=4).grid(row=2, column=1)
        tk.Button(frame1, text="↑", command=lambda: self.adjust_margin(1, 1), width=4).grid(row=2, column=2)
        tk.Button(frame1, text="↓", command=lambda: self.adjust_margin(1, -1), width=4).grid(row=2, column=3)
        tk.Button(frame1, text="Couleur", command=lambda: self.choose_color(1), width=6).grid(row=2, column=4, padx=5)
        
        # Texte 2 (Elemental End italic, couleur par défaut blanc)
        self.text2_size_factor = 0.12
        self.text2_margin = 0.20
        self.text2_color = "white"
        frame2 = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        frame2.pack(pady=5)
        tk.Label(frame2, text="Texte 2 (Elemental End italic)", bg="#2C2F33", fg="white").grid(row=0, column=0, columnspan=5)
        self.text_input2 = tk.Entry(frame2, font=("Arial", 14))
        self.text_input2.grid(row=1, column=0, columnspan=4, pady=2)
        self.text_input2.insert(0, "Votre texte 2 ici")
        tk.Button(frame2, text="+T", command=lambda: self.adjust_text_size(2, 1), width=4).grid(row=2, column=0)
        tk.Button(frame2, text="-T", command=lambda: self.adjust_text_size(2, -1), width=4).grid(row=2, column=1)
        tk.Button(frame2, text="↑", command=lambda: self.adjust_margin(2, 1), width=4).grid(row=2, column=2)
        tk.Button(frame2, text="↓", command=lambda: self.adjust_margin(2, -1), width=4).grid(row=2, column=3)
        tk.Button(frame2, text="Couleur", command=lambda: self.choose_color(2), width=6).grid(row=2, column=4, padx=5)
        
        # Texte 3 (Poppins Bold, couleur par défaut noir)
        self.text3_size_factor = 0.12
        self.text3_margin = 0.10
        self.text3_color = "black"
        frame3 = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        frame3.pack(pady=5)
        tk.Label(frame3, text="Texte 3 (Poppins Bold)", bg="#2C2F33", fg="white").grid(row=0, column=0, columnspan=5)
        self.text_input3 = tk.Entry(frame3, font=("Arial", 14))
        self.text_input3.grid(row=1, column=0, columnspan=4, pady=2)
        self.text_input3.insert(0, "Votre texte 3 ici")
        tk.Button(frame3, text="+T", command=lambda: self.adjust_text_size(3, 1), width=4).grid(row=2, column=0)
        tk.Button(frame3, text="-T", command=lambda: self.adjust_text_size(3, -1), width=4).grid(row=2, column=1)
        tk.Button(frame3, text="↑", command=lambda: self.adjust_margin(3, 1), width=4).grid(row=2, column=2)
        tk.Button(frame3, text="↓", command=lambda: self.adjust_margin(3, -1), width=4).grid(row=2, column=3)
        tk.Button(frame3, text="Couleur", command=lambda: self.choose_color(3), width=6).grid(row=2, column=4, padx=5)
        
        # Mise à jour automatique dès modification des champs de texte
        self.text_input1.bind("<KeyRelease>", lambda e: self.generate_final())
        self.text_input2.bind("<KeyRelease>", lambda e: self.generate_final())
        self.text_input3.bind("<KeyRelease>", lambda e: self.generate_final())
        
        # Boutons d'action (dans le conteneur scrollable)
        self.btn_load = tk.Button(self.scrollable_frame, text="Choisir une Image",
                                  command=self.load_image,
                                  bg="#7289DA", fg="white", font=("Arial", 12, "bold"))
        self.btn_load.pack(pady=5)
        self.btn_generate = tk.Button(self.scrollable_frame, text="Générer avec Watermark",
                                      command=self.generate_final,
                                      bg="#99AAB5", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_generate.pack(pady=5)
        self.btn_save_no = tk.Button(self.scrollable_frame, text="Enregistrer sans Watermark",
                                     command=self.save_no_watermark,
                                     bg="#43B581", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_save_no.pack(pady=5)
        self.btn_save_yes = tk.Button(self.scrollable_frame, text="Enregistrer avec Watermark",
                                      command=self.save_with_watermark,
                                      bg="#F04747", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_save_yes.pack(pady=5)
        
        # Variables pour l'image et son affichage
        self.source_image = None
        self.current_preview = None
        self.tk_preview = None
        
        # Position et zoom dans l'aperçu
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Chargement du watermark (watermark.png)
        try:
            self.watermark = Image.open("watermark.png").convert("RGBA")
        except Exception:
            self.watermark = None
            print("⚠️  Fichier 'watermark.png' introuvable.")
        
        # Stockage des rendus finaux
        self.final_no_wm = None
        self.final_with_wm = None

    # --- Chargement de l'image ---
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.bmp *.gif")])
        if not path:
            return
        self.source_image = Image.open(path).convert("RGBA")
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.update_preview()
        self.btn_generate.config(state=tk.NORMAL)
        self.btn_save_no.config(state=tk.NORMAL)

    # --- Mise à jour de l'aperçu ---
    def update_preview(self):
        if self.source_image is None:
            return
        w = int(self.source_image.width * self.zoom)
        h = int(self.source_image.height * self.zoom)
        img_zoomed = self.source_image.resize((w, h), Image.LANCZOS)
        preview_img = Image.new("RGBA", (PREVIEW_SIZE, PREVIEW_SIZE), (240, 240, 240, 255))
        center_x = PREVIEW_SIZE // 2 + self.offset_x
        center_y = PREVIEW_SIZE // 2 + self.offset_y
        pos_x = center_x - (w // 2)
        pos_y = center_y - (h // 2)
        preview_img.paste(img_zoomed, (pos_x, pos_y), img_zoomed)
        self.current_preview = preview_img
        self.tk_preview = ImageTk.PhotoImage(preview_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_preview)

    # --- Contrôles de déplacement et zoom ---
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.update_preview()

    def zoom_in(self):
        self.zoom *= 1.1
        self.update_preview()

    def zoom_out(self):
        self.zoom /= 1.1
        if self.zoom < 0.1:
            self.zoom = 0.1
        self.update_preview()

    # --- Choix de la couleur du texte ---
    def choose_color(self, input_num):
        color = colorchooser.askcolor()[1]
        if not color:
            return
        if input_num == 1:
            self.text1_color = color
        elif input_num == 2:
            self.text2_color = color
        elif input_num == 3:
            self.text3_color = color
        self.generate_final()
        
    # --- Ajustement de la taille du texte ---
    def adjust_text_size(self, input_num, delta):
        if input_num == 1:
            self.text1_size_factor += 0.01 * delta
            if self.text1_size_factor < 0.01:
                self.text1_size_factor = 0.01
        elif input_num == 2:
            self.text2_size_factor += 0.01 * delta
            if self.text2_size_factor < 0.01:
                self.text2_size_factor = 0.01
        elif input_num == 3:
            self.text3_size_factor += 0.01 * delta
            if self.text3_size_factor < 0.01:
                self.text3_size_factor = 0.01
        self.generate_final()

    # --- Ajustement de la marge du texte (vertical) ---
    def adjust_margin(self, input_num, delta):
        if input_num == 1:
            self.text1_margin += 0.01 * delta
            if self.text1_margin < 0:
                self.text1_margin = 0
        elif input_num == 2:
            self.text2_margin += 0.01 * delta
            if self.text2_margin < 0:
                self.text2_margin = 0
        elif input_num == 3:
            self.text3_margin += 0.01 * delta
            if self.text3_margin < 0:
                self.text3_margin = 0
        self.generate_final()

    # --- Génération du rendu final ---
    def generate_final(self):
        if self.current_preview is None:
            return
        final_img = self.current_preview.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
        self.final_no_wm = final_img.copy()
        if self.watermark:
            wm_full = self.watermark.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
            final_img.paste(wm_full, (0, 0), wm_full)
        draw = ImageDraw.Draw(final_img)
        # Texte 1
        text1 = self.text_input1.get().strip()
        if text1:
            try:
                font_size1 = int(FINAL_SIZE * self.text1_size_factor)
                font1 = ImageFont.truetype(font_path, font_size1)
            except Exception as e:
                print("Erreur de police texte 1:", e)
                font1 = ImageFont.load_default()
            margin1 = FINAL_SIZE * self.text1_margin
            x1 = FINAL_SIZE / 2
            y1 = FINAL_SIZE - (margin1 / 2)
            draw.text((x1, y1), text1, font=font1, fill=self.text1_color, anchor="mm")
        # Texte 2
        text2 = self.text_input2.get().strip()
        if text2:
            try:
                font_size2 = int(FINAL_SIZE * self.text2_size_factor)
                font2 = ImageFont.truetype(font_path, font_size2)
            except Exception as e:
                print("Erreur de police texte 2:", e)
                font2 = ImageFont.load_default()
            margin2 = FINAL_SIZE * self.text2_margin
            x2 = FINAL_SIZE / 2
            y2 = FINAL_SIZE - (margin2 / 2)
            draw.text((x2, y2), text2, font=font2, fill=self.text2_color, anchor="mm")
        # Texte 3 (Poppins Bold)
        text3 = self.text_input3.get().strip()
        if text3:
            try:
                font_size3 = int(FINAL_SIZE * self.text3_size_factor)
                font3 = ImageFont.truetype(font_path_text3, font_size3)
            except Exception as e:
                print("Erreur de police texte 3:", e)
                font3 = ImageFont.load_default()
            margin3 = FINAL_SIZE * self.text3_margin
            x3 = FINAL_SIZE / 2
            y3 = FINAL_SIZE - (margin3 / 2)
            draw.text((x3, y3), text3, font=font3, fill=self.text3_color, anchor="mm")
        self.final_with_wm = final_img
        self.btn_save_yes.config(state=tk.NORMAL)
        final_preview = final_img.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.LANCZOS)
        self.tk_preview = ImageTk.PhotoImage(final_preview)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_preview)

    # --- Sauvegarde ---
    def save_no_watermark(self):
        if self.final_no_wm is None:
            self.generate_final()
        if self.final_no_wm:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                self.final_no_wm.save(path)

    def save_with_watermark(self):
        if self.final_with_wm is None:
            self.generate_final()
        if self.final_with_wm:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                self.final_with_wm.save(path)

    def save_no_mark(self):
        self.save_no_watermark()

    def save_with_mark(self):
        self.save_with_watermark()

    def generate_output(self):
        self.generate_final()

if __name__ == "__main__":
    root = tk.Tk()
    app = SnapshotEditor(root)
    root.mainloop()
