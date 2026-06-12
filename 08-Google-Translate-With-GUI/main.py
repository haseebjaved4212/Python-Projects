import customtkinter as ctk
import googletrans
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox

# Configuration
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TranslateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Translate")
        self.geometry("900x550")
        self.minsize(800, 500)
        
        self.translator = Translator()
        self.languages = googletrans.LANGUAGES
        
        # Prepare language list (capitalized)
        self.lang_list = [lang.capitalize() for lang in self.languages.values()]
        self.lang_codes = {v.capitalize(): k for k, v in self.languages.items()}
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="Google Translate", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(20, 10))
        
        # Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0) # Middle button column
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Source Language Dropdown
        self.src_lang_var = ctk.StringVar(value="English")
        self.src_lang_combo = ctk.CTkComboBox(self.main_frame, values=["Auto Detect"] + self.lang_list, variable=self.src_lang_var, font=ctk.CTkFont(size=14))
        self.src_lang_combo.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        # Target Language Dropdown
        self.dest_lang_var = ctk.StringVar(value="Spanish")
        self.dest_lang_combo = ctk.CTkComboBox(self.main_frame, values=self.lang_list, variable=self.dest_lang_var, font=ctk.CTkFont(size=14))
        self.dest_lang_combo.grid(row=0, column=2, padx=10, pady=(0, 10), sticky="ew")
        
        # Source Textbox
        self.src_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=16), border_width=2, corner_radius=10)
        self.src_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Target Textbox
        self.dest_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=16), border_width=2, corner_radius=10, state="disabled", fg_color=("gray90", "gray16"))
        self.dest_textbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Center Frame for Translate Button
        self.center_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.center_frame.grid(row=1, column=1, padx=10, pady=10)
        
        self.translate_btn = ctk.CTkButton(self.center_frame, text="Translate ➔", font=ctk.CTkFont(size=16, weight="bold"), command=self.perform_translation, height=40)
        self.translate_btn.pack(pady=20)
        
        # Bottom controls (Clear and Copy)
        self.src_controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.src_controls_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.src_clear_btn = ctk.CTkButton(self.src_controls_frame, text="Clear", command=self.clear_src, width=80)
        self.src_clear_btn.pack(side="left")
        
        self.src_copy_btn = ctk.CTkButton(self.src_controls_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.src_textbox), width=80)
        self.src_copy_btn.pack(side="right")
        
        self.dest_controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.dest_controls_frame.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="ew")
        
        self.dest_clear_btn = ctk.CTkButton(self.dest_controls_frame, text="Clear", command=self.clear_dest, width=80)
        self.dest_clear_btn.pack(side="left")
        
        self.dest_copy_btn = ctk.CTkButton(self.dest_controls_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.dest_textbox, is_disabled=True), width=80)
        self.dest_copy_btn.pack(side="right")
        
    def perform_translation(self):
        text_to_translate = self.src_textbox.get("1.0", "end-1c").strip()
        if not text_to_translate:
            return
            
        src_lang = self.src_lang_var.get()
        dest_lang = self.dest_lang_var.get()
        
        src_code = 'auto' if src_lang == "Auto Detect" else self.lang_codes.get(src_lang, 'auto')
        dest_code = self.lang_codes.get(dest_lang, 'en')
        
        try:
            # Show translating state
            self.translate_btn.configure(text="Translating...", state="disabled")
            self.update_idletasks()
            
            result = self.translator.translate(text_to_translate, src=src_code, dest=dest_code)
            
            # Enable target textbox to insert text
            self.dest_textbox.configure(state="normal")
            self.dest_textbox.delete("1.0", "end")
            self.dest_textbox.insert("1.0", result.text)
            self.dest_textbox.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Translation Error", f"An error occurred while translating.\n\nMake sure you have an active internet connection.\n\nDetails: {str(e)}")
        finally:
            self.translate_btn.configure(text="Translate ➔", state="normal")

    def clear_src(self):
        self.src_textbox.delete("1.0", "end")
        
    def clear_dest(self):
        self.dest_textbox.configure(state="normal")
        self.dest_textbox.delete("1.0", "end")
        self.dest_textbox.configure(state="disabled")
        
    def copy_to_clipboard(self, textbox, is_disabled=False):
        if is_disabled:
            textbox.configure(state="normal")
            text = textbox.get("1.0", "end-1c")
            textbox.configure(state="disabled")
        else:
            text = textbox.get("1.0", "end-1c")
            
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update() # Required for clipboard to update

if __name__ == "__main__":
    app = TranslateApp()
    app.mainloop()
