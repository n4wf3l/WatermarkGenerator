import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

FINAL_SIZE = 1080   # Taille finale souhaitée (1080x1080)
PREVIEW_SIZE = 500  # Taille du Canvas d'aperçu (500x500)

class SnapshotEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur d'Image - Snapshot")
        self.root.geometry("850x750")
        self.root.configure(bg="#2C2F33")
        
        # Canvas d'aperçu
        self.canvas = tk.Canvas(root, width=PREVIEW_SIZE, height=PREVIEW_SIZE, bg="white")
        self.canvas.pack(pady=10)
        
        # Contrôles de déplacement et zoom
        control_frame = tk.Frame(root, bg="#2C2F33")
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="↑", command=lambda: self.move(0, -20), width=5).grid(row=0, column=1)
        tk.Button(control_frame, text="←", command=lambda: self.move(-20, 0), width=5).grid(row=1, column=0)
        tk.Button(control_frame, text="→", command=lambda: self.move(20, 0), width=5).grid(row=1, column=2)
        tk.Button(control_frame, text="↓", command=lambda: self.move(0, 20), width=5).grid(row=2, column=1)
        tk.Button(control_frame, text="+", command=self.zoom_in, width=5).grid(row=1, column=1, padx=10)
        tk.Button(control_frame, text="-", command=self.zoom_out, width=5).grid(row=3, column=1)
        
        # Boutons d'action
        self.btn_load = tk.Button(root, text="Choisir une Image",
                                  command=self.load_image,
                                  bg="#7289DA", fg="white", font=("Arial", 12, "bold"))
        self.btn_load.pack(pady=5)
        
        self.btn_generate = tk.Button(root, text="Générer avec Watermark",
                                      command=self.generate_final,
                                      bg="#99AAB5", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_generate.pack(pady=5)
        
        self.btn_save_no = tk.Button(root, text="Enregistrer sans Watermark",
                                     command=self.save_no_watermark,
                                     bg="#43B581", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_save_no.pack(pady=5)
        
        self.btn_save_yes = tk.Button(root, text="Enregistrer avec Watermark",
                                      command=self.save_with_watermark,
                                      bg="#F04747", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_save_yes.pack(pady=5)
        
        # Variables pour l'image et son affichage
        self.source_image = None  # Image PIL d'origine
        self.current_preview = None  # Aperçu PIL généré (500x500)
        self.tk_preview = None  # Image Tkinter pour le canvas
        
        # Position et zoom dans l'aperçu
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Logo pour watermark (si disponible)
        try:
            self.logo = Image.open("logoDMS.png").convert("RGBA")
        except Exception:
            self.logo = None
            print("⚠️  Logo 'logoDMS.png' introuvable.")
        
        # Stockage des rendus finaux
        self.final_no_wm = None
        self.final_with_wm = None

    # --- Chargement de l'image ---
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.bmp *.gif")])
        if not path:
            return
        self.source_image = Image.open(path).convert("RGBA")
        # Réinitialiser la position et le zoom
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.update_preview()
        self.btn_generate.config(state=tk.NORMAL)
        self.btn_save_no.config(state=tk.NORMAL)

    # --- Mise à jour de l'aperçu ---
    def update_preview(self):
        """Génère l'aperçu (PIL) basé sur la source, le zoom et le déplacement, et l'affiche."""
        if self.source_image is None:
            return
        # Appliquer le zoom
        w = int(self.source_image.width * self.zoom)
        h = int(self.source_image.height * self.zoom)
        img_zoomed = self.source_image.resize((w, h), Image.LANCZOS)
        # Créer une image de fond pour l'aperçu (500x500)
        preview_img = Image.new("RGBA", (PREVIEW_SIZE, PREVIEW_SIZE), (240, 240, 240, 255))
        # Calculer la position pour centrer l'image zoomée selon les offsets
        # self.offset_x, self.offset_y correspondent aux décalages par rapport au centre du canvas
        center_x = PREVIEW_SIZE // 2 + self.offset_x
        center_y = PREVIEW_SIZE // 2 + self.offset_y
        pos_x = center_x - (w // 2)
        pos_y = center_y - (h // 2)
        preview_img.paste(img_zoomed, (pos_x, pos_y), img_zoomed)
        self.current_preview = preview_img  # On stocke cet aperçu PIL
        self.tk_preview = ImageTk.PhotoImage(preview_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_preview)

    # --- Contrôles de déplacement et zoom ---
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.update_preview()

    def move_img(self, dx, dy):
        self.move(dx, dy)

    def move_pic(self, dx, dy):
        self.move(dx, dy)

    def move_image(self, dx, dy):
        self.move(dx, dy)
    
    def move_img2(self, dx, dy):
        self.move(dx, dy)
    
    def move_img3(self, dx, dy):
        self.move(dx, dy)
    
    def move_img4(self, dx, dy):
        self.move(dx, dy)
    
    def move_pic_final(self, dx, dy):
        self.move(dx, dy)

    def move_img5(self, dx, dy):
        self.move(dx, dy)

    def move_pic6(self, dx, dy):
        self.move(dx, dy)

    # Pour simplifier, on utilise "move" pour tous les boutons de déplacement.
    def move_pic(self, dx, dy):
        self.move(dx, dy)

    def zoom_in(self):
        self.zoom *= 1.1
        self.update_preview()

    def zoom_out(self):
        self.zoom /= 1.1
        if self.zoom < 0.1:
            self.zoom = 0.1
        self.update_preview()

    # --- Génération du rendu final ---
    def generate_final(self):
        """Prend l'aperçu actuel (500x500) et l'upscale à 1080x1080, puis ajoute le watermark si disponible."""
        if self.current_preview is None:
            return
        # Utiliser directement l'aperçu PIL stocké
        final_img = self.current_preview.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
        self.final_no_wm = final_img.copy()
        # Si logo disponible, ajouter le watermark
        if self.logo:
            wm_w = int(FINAL_SIZE * 0.1)
            wm_h = int(wm_w * (self.logo.height / self.logo.width))
            logo_resized = self.logo.resize((wm_w, wm_h), Image.LANCZOS)
            final_img.paste(logo_resized, (10, 10), logo_resized)
        self.final_with_wm = final_img
        self.btn_save_yes.config(state=tk.NORMAL)

    # --- Boutons pour générer final ---
    def generate_final(self):
        if self.current_preview is None:
            return
        final_img = self.current_preview.resize((FINAL_SIZE, FINAL_SIZE), Image.LANCZOS)
        self.final_no_wm = final_img.copy()
        if self.logo:
            wm_w = int(FINAL_SIZE * 0.1)
            wm_h = int(wm_w * (self.logo.height / self.logo.width))
            logo_resized = self.logo.resize((wm_w, wm_h), Image.LANCZOS)
            final_img.paste(logo_resized, (10, 10), logo_resized)
        self.final_with_wm = final_img
        self.btn_save_yes.config(state=tk.NORMAL)
    
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

    # --- Liaison des boutons d'action à nos fonctions de sauvegarde ---
    def save_no_mark(self):
        self.save_no_watermark()

    def save_with_mark(self):
        self.save_with_watermark()

    # Liaison pour le bouton "Générer"
    def generate_output(self):
        self.generate_final()


if __name__ == "__main__":
    root = tk.Tk()
    app = SnapshotEditor(root)
    root.mainloop()
