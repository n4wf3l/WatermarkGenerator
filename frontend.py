import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps

# Chemins de police
font_path = "Elemental End italic.ttf"   # Pour Texte 1 et Texte 2
font_path_text3 = "Poppins Bold.ttf"     # Pour Texte 3

FINAL_SIZE = 1080   # Taille finale (1080x1080)
PREVIEW_SIZE = 500  # Taille du Canvas d'aperçu (500x500)

class SnapshotEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur d'Image - Frontend Pro")
        self.geometry("1000x950")
        self.configure(bg="#2C2F33")
        
        # Couleur du watermark (None = pas de teinte)
        self.wm_color = None
        
        # 1) Bouton pour choisir la couleur du watermark dans la colonne de gauche
        left_frame = tk.Frame(self, bg="#2C2F33")
        left_frame.pack(side="left", padx=10, pady=10)
        
        self.btn_wm_color = tk.Button(
            left_frame,
            text="Couleur Watermark",
            command=self.choose_wm_color,
            bg="#CCCCCC",
            fg="black",
            font=("Arial", 12, "bold")
        )
        self.btn_wm_color.pack(pady=5)
        
        # 2) Conteneur scrollable pour l'interface complète
        container = tk.Frame(self, bg="#2C2F33")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas_scroll = tk.Canvas(container, bg="#2C2F33")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas_scroll.yview)
        
        self.scrollable_frame = tk.Frame(canvas_scroll, bg="#2C2F33")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ----------------------------
        # Colonne de gauche (dans scrollable_frame) : Image et contrôles d'image
        # ----------------------------
        left_frame2 = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        left_frame2.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Canvas d'aperçu
        self.canvas = tk.Canvas(left_frame2, width=PREVIEW_SIZE, height=PREVIEW_SIZE, bg="white")
        self.canvas.pack(pady=10)
        
        # Bouton pour choisir l'image
        self.btn_load = tk.Button(
            left_frame2,
            text="Choisir une Image",
            command=self.load_image,
            bg="#7289DA",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.btn_load.pack(pady=5)
        
        # Contrôles de déplacement et zoom
        ctrl_frame = tk.Frame(left_frame2, bg="#2C2F33")
        ctrl_frame.pack(pady=10)
        
        tk.Button(ctrl_frame, text="↑", command=lambda: self.move(0, -20), width=5).grid(row=0, column=1)
        tk.Button(ctrl_frame, text="←", command=lambda: self.move(-20, 0), width=5).grid(row=1, column=0)
        tk.Button(ctrl_frame, text="→", command=lambda: self.move(20, 0), width=5).grid(row=1, column=2)
        tk.Button(ctrl_frame, text="↓", command=lambda: self.move(0, 20), width=5).grid(row=2, column=1)
        tk.Button(ctrl_frame, text="+", command=self.zoom_in, width=5).grid(row=1, column=1, padx=10)
        tk.Button(ctrl_frame, text="-", command=self.zoom_out, width=5).grid(row=3, column=1)
        
        # Panneau d'action
        action_frame = tk.Frame(left_frame2, bg="#2C2F33")
        action_frame.pack(pady=10)
        
        self.btn_generate = tk.Button(
            action_frame,
            text="Générer avec Watermark",
            command=self.generate_final,
            bg="#99AAB5",
            fg="white",
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.btn_generate.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_save_no = tk.Button(
            action_frame,
            text="Enregistrer sans Watermark",
            command=self.save_no_watermark,
            bg="#43B581",
            fg="white",
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.btn_save_no.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_save_yes = tk.Button(
            action_frame,
            text="Enregistrer avec Watermark",
            command=self.save_with_watermark,
            bg="#F04747",
            fg="white",
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.btn_save_yes.grid(row=2, column=0, padx=5, pady=5)
        
        # ----------------------------
        # Colonne de droite (dans scrollable_frame) : Paramétrage des textes
        # ----------------------------
        right_frame = tk.Frame(self.scrollable_frame, bg="#2C2F33")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        
        # Texte 1 (Elemental End italic)
        self.text1_size_factor = 0.08
        self.text1_margin = 0.65
        self.text1_color = "white"
        
        frame1 = tk.LabelFrame(
            right_frame,
            text="Texte 1 (Elemental End italic, marge haute)",
            bg="#2C2F33",
            fg="white",
            font=("Arial", 12, "bold")
        )
        frame1.pack(fill="x", pady=5, padx=5)
        
        self.text_input1 = tk.Entry(frame1, font=("Arial", 14))
        self.text_input1.pack(fill="x", padx=5, pady=2)
        self.text_input1.insert(0, "Text1")
        
        btns1 = tk.Frame(frame1, bg="#2C2F33")
        btns1.pack(pady=2)
        
        tk.Button(btns1, text="+T", command=lambda: self.adjust_text_size(1, 1), width=4).grid(row=0, column=0, padx=2)
        tk.Button(btns1, text="-T", command=lambda: self.adjust_text_size(1, -1), width=4).grid(row=0, column=1, padx=2)
        tk.Button(btns1, text="↑", command=lambda: self.adjust_margin(1, 1), width=4).grid(row=0, column=2, padx=2)
        tk.Button(btns1, text="↓", command=lambda: self.adjust_margin(1, -1), width=4).grid(row=0, column=3, padx=2)
        
        tk.Button(btns1, text="Couleur", command=lambda: self.choose_color(1), width=6)\
            .grid(row=1, column=0, columnspan=4, padx=2, pady=2)
        
        # Texte 2 (Elemental End italic)
        self.text2_size_factor = 0.10
        self.text2_margin = 0.45
        self.text2_color = "white"
        
        frame2 = tk.LabelFrame(
            right_frame,
            text="Texte 2 (Elemental End italic)",
            bg="#2C2F33",
            fg="white",
            font=("Arial", 12, "bold")
        )
        frame2.pack(fill="x", pady=5, padx=5)
        
        self.text_input2 = tk.Entry(frame2, font=("Arial", 14))
        self.text_input2.pack(fill="x", padx=5, pady=2)
        self.text_input2.insert(0, "Text2")
        
        btns2 = tk.Frame(frame2, bg="#2C2F33")
        btns2.pack(pady=2)
        
        tk.Button(btns2, text="+T", command=lambda: self.adjust_text_size(2, 1), width=4).grid(row=0, column=0, padx=2)
        tk.Button(btns2, text="-T", command=lambda: self.adjust_text_size(2, -1), width=4).grid(row=0, column=1, padx=2)
        tk.Button(btns2, text="↑", command=lambda: self.adjust_margin(2, 1), width=4).grid(row=0, column=2, padx=2)
        tk.Button(btns2, text="↓", command=lambda: self.adjust_margin(2, -1), width=4).grid(row=0, column=3, padx=2)
        
        tk.Button(btns2, text="Couleur", command=lambda: self.choose_color(2), width=6)\
            .grid(row=0, column=4, padx=2)
        
        # Texte 3 (Poppins Bold)
        self.text3_size_factor = 0.06
        self.text3_margin = 0.21
        self.text3_color = "black"
        
        frame3 = tk.LabelFrame(
            right_frame,
            text="Texte 3 (Poppins Bold)",
            bg="#2C2F33",
            fg="white",
            font=("Arial", 12, "bold")
        )
        frame3.pack(fill="x", pady=5, padx=5)
        
        self.text_input3 = tk.Entry(frame3, font=("Arial", 14))
        self.text_input3.pack(fill="x", padx=5, pady=2)
        self.text_input3.insert(0, "Text3")
        
        btns3 = tk.Frame(frame3, bg="#2C2F33")
        btns3.pack(pady=2)
        
        tk.Button(btns3, text="+T", command=lambda: self.adjust_text_size(3, 1), width=4).grid(row=0, column=0, padx=2)
        tk.Button(btns3, text="-T", command=lambda: self.adjust_text_size(3, -1), width=4).grid(row=0, column=1, padx=2)
        tk.Button(btns3, text="↑", command=lambda: self.adjust_margin(3, 1), width=4).grid(row=0, column=2, padx=2)
        tk.Button(btns3, text="↓", command=lambda: self.adjust_margin(3, -1), width=4).grid(row=0, column=3, padx=2)
        
        tk.Button(btns3, text="Couleur", command=lambda: self.choose_color(3), width=6)\
            .grid(row=0, column=4, padx=2)
        
        # Mise à jour automatique dès modification des champs de texte
        self.text_input1.bind("<KeyRelease>", lambda e: self.generate_final())
        self.text_input2.bind("<KeyRelease>", lambda e: self.generate_final())
        self.text_input3.bind("<KeyRelease>", lambda e: self.generate_final())
        
        # Boutons d'action en bas de la colonne de droite
        action_frame = tk.Frame(right_frame, bg="#2C2F33")
        action_frame.pack(pady=10)
        
        self.btn_generate = tk.Button(
            action_frame,
            text="Générer avec Watermark",
            command=self.generate_final,
            bg="#99AAB5",
            fg="white",
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.btn_generate.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_save_yes = tk.Button(
            action_frame,
            text="Enregistrer avec Watermark",
            command=self.save_with_watermark,
            bg="#F04747",
            fg="white",
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.btn_save_yes.grid(row=2, column=0, padx=5, pady=5)
        
        # Variables d'image
        self.source_image = None
        self.current_preview = None
        self.tk_preview = None
        
        # Position & zoom
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Chargement du watermark (watermark.png)
        try:
            self.watermark = Image.open("watermark.png").convert("RGBA")
        except Exception:
            self.watermark = None
            print("⚠️  Fichier 'watermark.png' introuvable.")
        
        self.final_no_wm = None
        self.final_with_wm = None

    # --- Bouton "Choisir une Image" ---
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.bmp *.gif")])
        if not path:
            return
        self.source_image = Image.open(path).convert("RGBA")
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.update_preview()
        self.generate_final()  # Actualise le rendu
        self.btn_generate.config(state=tk.NORMAL)
        self.btn_save_no.config(state=tk.NORMAL)

    # --- Mise à jour de l'aperçu (canvas) ---
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

    # --- Contrôles de déplacement & zoom ---
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

    # --- Couleur du texte ---
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

    # --- Couleur du watermark ---
    def choose_wm_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.wm_color = color
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

    # --- Ajustement de la marge du texte ---
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
        
        # 1) On part de l'aperçu agrandi à 1080x1080
        final_img = self.current_preview.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
        self.final_no_wm = final_img.copy()
        
        # 2) Watermark
        if self.watermark:
            wm_full = self.watermark.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
            
            # Si on a choisi une couleur, on colorise
            if self.wm_color:
                # Extraire le canal alpha
                wm_alpha = wm_full.split()[-1]
                # Convertir en RGB sans alpha
                wm_rgb = wm_full.convert("RGB")
                # Convertir en gris
                wm_gray = wm_rgb.convert("L")
                # Coloriser
                wm_colored = ImageOps.colorize(wm_gray, black=(0,0,0,0), white=self.wm_color)
                wm_colored = wm_colored.convert("RGBA")
                # Réappliquer le canal alpha d'origine
                wm_colored.putalpha(wm_alpha)
                wm_full = wm_colored
            
            # Coller le watermark (avec son alpha)
            final_img.paste(wm_full, (0, 0), wm_full)
        
        # 3) Dessin du texte
        draw = ImageDraw.Draw(final_img)
        
        # --- Texte 1 ---
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
        
        # --- Texte 2 ---
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
        
        # --- Texte 3 (Poppins Bold) ---
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
        
        # 4) On stocke la version finale
        self.final_with_wm = final_img
        self.btn_save_yes.config(state=tk.NORMAL)
        
        # 5) Mise à jour de l'aperçu final
        final_preview = final_img.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.LANCZOS)
        self.tk_preview = ImageTk.PhotoImage(final_preview)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_preview)

    # --- Sauvegarde sans watermark ---
    def save_no_watermark(self):
        if self.final_no_wm is None:
            self.generate_final()
        if self.final_no_wm:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                self.final_no_wm.save(path)

    # --- Sauvegarde avec watermark ---
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
    app = SnapshotEditor()
    app.mainloop()
