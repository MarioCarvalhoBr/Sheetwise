"""
User login/registration screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import re
import sys
import os

# Add src to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from utils.i18n_manager import _, get_i18n

class LoginView:
    """User login/registration interface"""
    
    def __init__(self, on_login_success=None):
        self.on_login_success = on_login_success
        self.root = None
        self.setup_window()
    
    def setup_window(self):
        """Configure main window"""
        self.root = ThemedTk(theme="arc")
        self.root.title(_('app.login_title'))
        
        # Calcular tamanho da janela com base na resolução da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Sistema inteligente de dimensionamento para tela de login
        # Objetivos: janela grande o suficiente para interação, mas não excessiva
        min_width, min_height = 500, 400  # Tamanhos mínimos para usabilidade
        
        # Adaptação para telas pequenas (netbooks, tablets, etc.)
        if screen_width < 800:
            min_width = int(screen_width * 0.9)  # 90% da largura em telas pequenas
        if screen_height < 600:
            min_height = int(screen_height * 0.8)  # 80% da altura em telas pequenas
        
        # Calcular tamanho ideal baseado na tela
        max_width = int(screen_width * 0.4)   # Máximo 40% da largura
        max_height = int(screen_height * 0.5)  # Máximo 50% da altura
        
        # Determinar tamanho final (entre mínimo e máximo, com limite superior)
        window_width = max(min_width, min(max_width, 600))   # Limite máximo: 600px
        window_height = max(min_height, min(max_height, 500)) # Limite máximo: 500px
        
        # Calcular posição para centralizar
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)
        
        # Garantir que a janela seja atualizada
        self.root.update_idletasks()
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela na tela (método de fallback)"""
        self.root.update_idletasks()
        
        # Obter tamanho atual da janela
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Se o tamanho for muito pequeno, usar valores padrão
        if width < 100:
            width = 500
        if height < 100:
            height = 400
        
        # Calcular posição central
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def setup_styles(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para título
        style.configure("Title.TLabel", 
                       font=("Arial", 18, "bold"),
                       foreground="#2c3e50")
        
        # Estilo para subtítulo
        style.configure("Subtitle.TLabel",
                       font=("Arial", 10),
                       foreground="#7f8c8d")
        
        # Estilo para botão principal
        style.configure("Primary.TButton",
                       font=("Arial", 11, "bold"),
                       padding=(20, 10))
        
        # Estilo para entrada
        style.configure("Custom.TEntry",
                       font=("Arial", 11),
                       padding=10)
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        title_label = ttk.Label(main_frame, 
                               text=_('app.title'),
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame,
                                  text=_('app.subtitle'),
                                  style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 30))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=20)
        
        # Username field
        ttk.Label(form_frame, text=_('login.username'), font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=40)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        # Pre-preencher com valor padrão para facilitar testes
        self.username_entry.insert(0, "ababa")
        
        # Email field
        ttk.Label(form_frame, text=_('login.email'), font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.email_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 20))
        # Pre-fill with default value for testing
        self.email_entry.insert(0, "ababa@ababa.com")

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.login_button = ttk.Button(button_frame,
                                      text=_('login.login_button'),
                                      style="Primary.TButton",
                                      command=self.handle_login)
        self.login_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.register_button = ttk.Button(button_frame,
                                         text=_('login.register_button'),
                                         command=self.handle_register)
        self.register_button.pack(side=tk.RIGHT)
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # Focar no campo username
        self.username_entry.focus()
    
    def validate_email(self, email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_form(self):
        """Validate form data"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not username:
            messagebox.showerror(_('common.error'), _('login.validation.empty_username'))
            self.username_entry.focus()
            return False
        
        if len(username) < 3:
            messagebox.showerror(_('common.error'), "Username must have at least 3 characters.")
            self.username_entry.focus()
            return False
        
        if not email:
            messagebox.showerror(_('common.error'), _('login.validation.empty_email'))
            self.email_entry.focus()
            return False
        
        if not self.validate_email(email):
            messagebox.showerror(_('common.error'), _('login.validation.invalid_email'))
            self.email_entry.focus()
            return False
        
        return True
    
    def handle_login(self):
        """Try to login user"""
        if not self.validate_form():
            return
        
        email = self.email_entry.get().strip()
        
        if self.on_login_success:
            self.on_login_success(email, is_new_user=False)
    
    def handle_register(self):
        """Register new user"""
        if not self.validate_form():
            return
        
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if self.on_login_success:
            self.on_login_success(email, username=username, is_new_user=True)
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror(_('common.error'), message)
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        messagebox.showinfo("Sucesso", message)
    
    def destroy(self):
        """Destrói a janela"""
        if self.root:
            self.root.destroy()
    
    def run(self):
        """Executa o loop da interface"""
        if self.root:
            self.root.mainloop()