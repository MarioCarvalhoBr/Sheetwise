"""
Main application screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
try:
    from tkinter import filedialog
except ImportError:
    import tkinter.filedialog as filedialog
from ttkthemes import ThemedTk
import os
from datetime import datetime
import sys

# Add src to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from utils.i18n_manager import _, get_i18n

class ToolTip:
    """Classe para criar tooltips"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.tooltip = None

    def on_enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, 
                        background="lightyellow", relief="solid", 
                        borderwidth=1, font=("Arial", 9))
        label.pack()

    def on_leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class MainView:
    """Interface principal do aplicativo"""
    
    def __init__(self, usuario_data, initial_theme="arc", initial_dark_mode=False, on_logout=None, on_analyze=None, on_delete_execution=None, on_refresh_executions=None):
        self.usuario_data = usuario_data
        self.initial_theme = initial_theme
        self.initial_dark_mode = initial_dark_mode
        self.on_logout = on_logout
        self.on_analyze = on_analyze
        self.on_delete_execution = on_delete_execution
        self.on_refresh_executions = on_refresh_executions
        self.root = None
        self.files_status = {
            'clientes': False,
            'vendas': False,
            'enderecos': False  # opcional
        }
        self.selected_folder = ""
        self.setup_window()
    
    def setup_window(self):
        """Configure main window"""
        self.root = ThemedTk(theme=self.initial_theme)
        self.root.title(_('app.main_title') + f" - {self.usuario_data['username']}")
        
        # Calcular tamanho da janela com base na tela (com padding de 10%)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Usar 80% da tela (10% padding de cada lado)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)
        
        # Variável para controlar estado de maximização
        self.is_maximized = False
        
        # Centralizar na tela
        ## self.center_window()
        
        # Configurar estilo
        self.setup_styles()
        
        # Apply initial dark mode if enabled
        if self.initial_dark_mode:
            self.apply_dark_mode(True)
        
        # Criar interface
        self.create_widgets()
        
        # Configurar evento de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar atalhos de teclado
        self.setup_keyboard_shortcuts()
    
    def update_interface_text(self):
        """Update interface text with current language"""
        # Update window title
        self.root.title(_('app.main_title') + f" - {self.usuario_data['username']}")
        
        # Update button texts if they exist
        if hasattr(self, 'logout_button'):
            self.logout_button.configure(text=_('main.logout'))
        if hasattr(self, 'refresh_button'):
            self.refresh_button.configure(text=_('main.refresh'))
        if hasattr(self, 'browse_button'):
            self.browse_button.configure(text=_('main.folder_selection.browse'))
        if hasattr(self, 'analyze_button'):
            self.analyze_button.configure(text=_('main.analysis.analyze_button'))
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        
        # Obter dimensões atuais da janela
        self.root.geometry("")  # Reset geometry to get natural size
        self.root.update_idletasks()
        
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # Se não foi definido ainda, usar as dimensões calculadas
        if width < 100:  # Valor muito pequeno indica que ainda não foi definido
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            width = int(screen_width * 0.8)
            height = int(screen_height * 0.8)
        
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def setup_styles(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        
        # Estilos para diferentes elementos
        style.configure("Header.TLabel", 
                       font=("Arial", 16, "bold"),
                       foreground="#2c3e50")
        
        style.configure("Section.TLabel",
                       font=("Arial", 12, "bold"),
                       foreground="#34495e")
        
        style.configure("Status.TLabel",
                       font=("Arial", 10),
                       padding=5)
        
        style.configure("Success.TLabel",
                       font=("Arial", 10),
                       foreground="#27ae60")
        
        style.configure("Error.TLabel",
                       font=("Arial", 10),
                       foreground="#e74c3c")
        
        # Configuração mais robusta para o botão Analisar
        style.configure("Analyze.TButton",
                       font=("Arial", 14, "bold"),
                       foreground="white",
                       background="#3498db",
                       borderwidth=3,
                       relief="solid",
                       bordercolor="white",
                       focuscolor="none",
                       padding=(30, 15))
        
        # Mapeamento de estados para cores
        style.map("Analyze.TButton",
                 background=[
                     ('active', '#2980b9'),      # Quando hover
                     ('disabled', '#95a5a6'),    # Quando desabilitado
                     ('!disabled', '#3498db')    # Quando habilitado normal
                 ],
                 foreground=[
                     ('disabled', '#7f8c8d'),    # Texto cinza quando desabilitado
                     ('!disabled', 'white')      # Texto branco quando habilitado
                 ],
                 bordercolor=[
                     ('disabled', '#bdc3c7'),    # Contorno cinza quando desabilitado
                     ('!disabled', 'white')      # Contorno branco quando habilitado
                 ],
                 relief=[
                     ('disabled', 'solid'),
                     ('!disabled', 'solid')
                 ])
    
    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        # F11 para maximizar/restaurar
        self.root.bind('<F11>', lambda e: self.toggle_maximize())
        
        # Ctrl+M para maximizar/restaurar  
        self.root.bind('<Control-m>', lambda e: self.toggle_maximize())
        
        # Escape para restaurar se maximizado
        self.root.bind('<Escape>', lambda e: self.restore_window() if self.is_maximized else None)
    
    def create_tooltip(self, widget, text):
        """Cria tooltip para um widget"""
        return ToolTip(widget, text)
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal com scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Seção de seleção de pasta
        self.create_folder_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Seção de verificação de arquivos
        self.create_files_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Seção de configuração da análise
        self.create_analysis_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Seção de execuções
        self.create_executions_section(main_frame)
    
    def create_header(self, parent):
        """Create header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title and user information
        title_label = ttk.Label(header_frame, 
                               text=_('app.title'),
                               style="Header.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Frame for user buttons
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        user_info = ttk.Label(user_frame, 
                             text=_('main.welcome', username=self.usuario_data['username']),
                             font=("Arial", 10))
        user_info.pack(side=tk.LEFT, padx=(0, 10))
        
        # Maximize/restore button
        self.maximize_btn = ttk.Button(user_frame, 
                                      text="🗖", 
                                      width=3,
                                      command=self.toggle_maximize)
        self.maximize_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Add tooltip to button
        self.create_tooltip(self.maximize_btn, "Maximize/Restore (F11 or Ctrl+M)")
        
        # Refresh button
        self.refresh_button = ttk.Button(user_frame,
                                       text=_('main.refresh'),
                                       command=self.refresh_executions)
        self.refresh_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Settings button
        settings_btn = ttk.Button(user_frame,
                                text="⚙",
                                width=3,
                                command=self.show_settings)
        settings_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        self.logout_button = ttk.Button(user_frame, 
                               text=_('main.logout'),
                               command=self.handle_logout)
        self.logout_button.pack(side=tk.RIGHT)
    
    def create_folder_section(self, parent):
        """Cria seção de seleção de pasta"""
        folder_frame = ttk.LabelFrame(parent, text="1. Seleção da Pasta de Dados", padding=15)
        folder_frame.pack(fill=tk.X, pady=10)
        
        # Botão para selecionar pasta
        select_frame = ttk.Frame(folder_frame)
        select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(select_frame,
                  text="Selecionar Pasta",
                  command=self.select_folder).pack(side=tk.LEFT)
        
        # Label para mostrar pasta selecionada
        self.folder_label = ttk.Label(select_frame,
                                     text="Nenhuma pasta selecionada",
                                     foreground="#7f8c8d")
        self.folder_label.pack(side=tk.LEFT, padx=(15, 0))
    
    def create_files_section(self, parent):
        """Cria seção de verificação de arquivos"""
        files_frame = ttk.LabelFrame(parent, text="2. Verificação de Arquivos", padding=15)
        files_frame.pack(fill=tk.X, pady=10)
        
        # Grid de status dos arquivos
        self.files_labels = {}
        
        # Headers
        ttk.Label(files_frame, text="Arquivo", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 50))
        ttk.Label(files_frame, text="Status", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        ttk.Label(files_frame, text="Tipo", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W)
        
        # Arquivo clientes
        ttk.Label(files_frame, text="clientes.csv/xlsx").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.files_labels['clientes'] = ttk.Label(files_frame, text="❌ Não encontrado", style="Error.TLabel")
        self.files_labels['clientes'].grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text="Obrigatório").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Arquivo vendas
        ttk.Label(files_frame, text="vendas.csv/xlsx").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.files_labels['vendas'] = ttk.Label(files_frame, text="❌ Não encontrado", style="Error.TLabel")
        self.files_labels['vendas'].grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text="Obrigatório").grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # Arquivo enderecos
        ttk.Label(files_frame, text="enderecos.csv/xlsx").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.files_labels['enderecos'] = ttk.Label(files_frame, text="❓ Não encontrado", style="Status.TLabel")
        self.files_labels['enderecos'].grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text="Opcional").grid(row=3, column=2, sticky=tk.W, pady=5)
    
    def create_analysis_section(self, parent):
        """Cria seção de configuração da análise"""
        analysis_frame = ttk.LabelFrame(parent, text="3. Configuração da Análise", padding=15)
        analysis_frame.pack(fill=tk.X, pady=10)
        
        # Grid de configurações
        config_grid = ttk.Frame(analysis_frame)
        config_grid.pack(fill=tk.X)
        
        # Protocolo
        ttk.Label(config_grid, text="Protocolo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.protocolo_entry = ttk.Entry(config_grid, width=30, state="disabled")
        self.protocolo_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Setor
        ttk.Label(config_grid, text="Setor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.setor_entry = ttk.Entry(config_grid, width=30, state="disabled")
        self.setor_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Arquivo de resultado
        ttk.Label(config_grid, text="Arquivo Resultado:").grid(row=2, column=0, sticky=tk.W, pady=5)
        result_frame = ttk.Frame(config_grid)
        result_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.result_path_entry = ttk.Entry(result_frame, width=40, state="disabled")
        self.result_path_entry.pack(side=tk.LEFT)
        
        self.select_result_btn = ttk.Button(result_frame, 
                                           text="...",
                                           width=3,
                                           state="disabled",
                                           command=self.select_result_path)
        self.select_result_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão analisar
        analyze_frame = ttk.Frame(analysis_frame)
        analyze_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.analyze_button = ttk.Button(analyze_frame,
                                        text="ANALISAR",
                                        style="Analyze.TButton",
                                        state="normal",
                                        command=self.handle_analyze)
        self.analyze_button.pack()
        
        # Configurar estilo do botão
        self._setup_analyze_button_style()
        
        
 
        
    
    def create_executions_section(self, parent):
        """Cria seção de execuções"""
        exec_frame = ttk.LabelFrame(parent, text="4. Histórico de Execuções", padding=15)
        exec_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para mostrar execuções
        columns = ('ID', 'Protocolo', 'Setor', 'Data', 'Status')
        self.executions_tree = ttk.Treeview(exec_frame, columns=columns, show='headings', height=8)
        
        # Configurar colunas
        self.executions_tree.heading('ID', text='ID')
        self.executions_tree.heading('Protocolo', text='Protocolo')
        self.executions_tree.heading('Setor', text='Setor')
        self.executions_tree.heading('Data', text='Data')
        self.executions_tree.heading('Status', text='Status')
        
        self.executions_tree.column('ID', width=50)
        self.executions_tree.column('Protocolo', width=120)
        self.executions_tree.column('Setor', width=120)
        self.executions_tree.column('Data', width=150)
        self.executions_tree.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(exec_frame, orient=tk.VERTICAL, command=self.executions_tree.yview)
        self.executions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.executions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões para CRUD
        crud_frame = ttk.Frame(exec_frame)
        crud_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(crud_frame, text="Atualizar", command=self.refresh_executions).pack(side=tk.LEFT)
        ttk.Button(crud_frame, text="Deletar", command=self.delete_execution).pack(side=tk.LEFT, padx=(5, 0))
    
    def select_folder(self):
        """Seleciona pasta com os arquivos"""
        folder = filedialog.askdirectory(title="Selecione a pasta com os arquivos de dados")
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=f"Pasta: {folder}")
            self.check_files()
    
    def check_files(self):
        """Verifica se os arquivos necessários existem na pasta"""
        if not self.selected_folder:
            return
        
        # Reset status
        for key in self.files_status:
            self.files_status[key] = False
        
        # Verificar arquivos
        files_in_folder = os.listdir(self.selected_folder)
        
        for file_name in files_in_folder:
            name_lower = file_name.lower()
            if name_lower.startswith('clientes.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['clientes'] = True
                self.files_labels['clientes'].config(text="✅ Encontrado", style="Success.TLabel")
            elif name_lower.startswith('vendas.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['vendas'] = True
                self.files_labels['vendas'].config(text="✅ Encontrado", style="Success.TLabel") 
            elif name_lower.startswith('enderecos.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['enderecos'] = True
                self.files_labels['enderecos'].config(text="✅ Encontrado", style="Success.TLabel")
        
        # Atualizar labels para arquivos não encontrados
        if not self.files_status['clientes']:
            self.files_labels['clientes'].config(text="❌ Não encontrado", style="Error.TLabel")
        if not self.files_status['vendas']:
            self.files_labels['vendas'].config(text="❌ Não encontrado", style="Error.TLabel")
        if not self.files_status['enderecos']:
            self.files_labels['enderecos'].config(text="❓ Não encontrado", style="Status.TLabel")
        
        # Habilitar campos se arquivos obrigatórios foram encontrados
        self.update_form_state()
    
    def update_form_state(self):
        """Atualiza estado dos campos baseado na verificação de arquivos"""
        required_files_ok = self.files_status['clientes'] and self.files_status['vendas']
        
        state = "normal" if required_files_ok else "disabled"
        
        self.protocolo_entry.config(state=state)
        self.setor_entry.config(state=state)
        self.result_path_entry.config(state=state)
        self.select_result_btn.config(state=state)
        
    
    def select_result_path(self):
        """Seleciona caminho para arquivo resultado"""
        file_path = filedialog.asksaveasfilename(
            title="Salvar arquivo resultado como...",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.result_path_entry.delete(0, tk.END)
            self.result_path_entry.insert(0, file_path)
    
    def _setup_analyze_button_style(self):
        """Configura o estilo do botão analisar"""
        try:
            style = ttk.Style()
            
            # Configurar estilo personalizado para o botão analisar
            style.configure("Analyze.TButton",
                           font=("Arial", 14, "bold"),
                           background="#3498db",
                           foreground="white",
                           bordercolor="white",
                           focuscolor="white",
                           relief="solid",
                           borderwidth=3,
                           padding=(30, 15))
            
            # Mapear estados do botão
            style.map("Analyze.TButton",
                     background=[
                         ('active', '#2980b9'),
                         ('pressed', '#1f6391'),
                         ('focus', '#3498db')
                     ],
                     foreground=[
                         ('active', 'white'),
                         ('pressed', 'white'),
                         ('focus', 'white')
                     ])
            
        except Exception as e:
            print(f"Erro ao configurar estilo do botão: {e}")
    
    def handle_analyze(self):
        """Manipula clique no botão analisar"""
        
        # Validar campos obrigatórios
        errors = []
        
        # Verificar arquivos obrigatórios
        if not (self.files_status['clientes'] and self.files_status['vendas']):
            if not self.files_status['clientes']:
                errors.append("- Arquivo de clientes não encontrado")
            if not self.files_status['vendas']:
                errors.append("- Arquivo de vendas não encontrado")
        
        # Verificar campos do formulário
        protocolo = self.protocolo_entry.get().strip()
        if not protocolo:
            errors.append("- Campo 'Protocolo' é obrigatório")
        
        setor = self.setor_entry.get().strip()
        if not setor:
            errors.append("- Campo 'Setor' é obrigatório")
        
        arquivo_resultado = self.result_path_entry.get().strip()
        if not arquivo_resultado:
            errors.append("- Campo 'Caminho do arquivo resultado' é obrigatório")
        
        # Se há erros, mostrar mensagem e parar
        if errors:
            error_message = "Por favor, corrija os seguintes problemas:\n\n" + "\n".join(errors)
            messagebox.showerror("Erro de Validação", error_message)
            return
        
        # Se tudo está válido, pedir confirmação
        result = messagebox.askyesno(
            "Confirmar Análise",
            "Deseja realmente executar a análise dos dados?\n\nEsta operação pode levar alguns minutos.",
            icon="question"
        )
        
        if result and self.on_analyze:
            analysis_data = {
                'protocolo': protocolo,
                'setor': setor,
                'pasta_origem': self.selected_folder,
                'arquivo_resultado': arquivo_resultado,
                'files_status': self.files_status.copy()
            }
            self.on_analyze(analysis_data)
    
    def refresh_executions(self):
        """Atualiza lista de execuções"""
        try:
            # Limpar árvore
            for item in self.executions_tree.get_children():
                self.executions_tree.delete(item)
            
            # Chamar callback do controller se estiver disponível
            if self.on_refresh_executions:
                self.on_refresh_executions()
            else:
                messagebox.showwarning("Aviso", "Funcionalidade de atualização não disponível.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar execuções: {str(e)}")
    
    def delete_execution(self):
        """Deleta execução selecionada"""
        selected = self.executions_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma execução para deletar.")
            return
        
        # Obter ID da execução selecionada
        try:
            item = self.executions_tree.item(selected[0])
            execucao_id = item['values'][0]
            
            # Confirmação do usuário
            result = messagebox.askyesno(
                "Confirmar Exclusão", 
                f"Deseja realmente deletar a execução #{execucao_id}?\n\nEsta ação não pode ser desfeita.",
                icon="warning"
            )
            
            if result:
                # Se temos um callback para deletar (será definido pelo controller)
                if hasattr(self, 'on_delete_execution') and self.on_delete_execution:
                    self.on_delete_execution(execucao_id)
                else:
                    # Fallback se o controller não definiu o callback
                    messagebox.showinfo("Info", "Funcionalidade de deletar ainda não está conectada ao controller.")
                    
        except (IndexError, KeyError) as e:
            messagebox.showerror("Erro", f"Erro ao obter dados da execução selecionada: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def toggle_maximize(self):
        """Alterna entre maximizar e restaurar a janela"""
        if self.is_maximized:
            # Restaurar tamanho original
            self.restore_window()
        else:
            # Maximizar janela
            self.maximize_window()
    
    def maximize_window(self):
        """Maximiza a janela para tela cheia"""
        # Salvar posição e tamanho atuais
        self.root.update_idletasks()
        self.saved_geometry = self.root.geometry()
        
        # Tentar usar o método nativo do sistema primeiro
        try:
            self.root.state('zoomed')  # Windows
            self.is_maximized = True
            self.maximize_btn.config(text="🗗")  # Ícone de restaurar
        except tk.TclError:
            # Fallback para sistemas Unix/Linux
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Maximizar (deixar uma pequena margem para a barra de tarefas/dock)
            self.root.geometry(f"{screen_width}x{screen_height-60}+0+0")
            
            self.is_maximized = True
            self.maximize_btn.config(text="🗗")  # Ícone de restaurar
    
    def restore_window(self):
        """Restaura a janela ao tamanho original"""
        try:
            # Tentar restaurar usando o método nativo
            self.root.state('normal')
            
            # Restaurar geometria salva
            if hasattr(self, 'saved_geometry'):
                self.root.geometry(self.saved_geometry)
            else:
                # Fallback para tamanho padrão
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                width = int(screen_width * 0.8)
                height = int(screen_height * 0.8)
                pos_x = (screen_width // 2) - (width // 2)
                pos_y = (screen_height // 2) - (height // 2)
                self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
                
        except tk.TclError:
            # Fallback para sistemas que não suportam state('normal')
            if hasattr(self, 'saved_geometry'):
                self.root.geometry(self.saved_geometry)
            else:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                width = int(screen_width * 0.8)
                height = int(screen_height * 0.8)
                pos_x = (screen_width // 2) - (width // 2)
                pos_y = (screen_height // 2) - (height // 2)
                self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
        self.is_maximized = False
        self.maximize_btn.config(text="🗖")  # Ícone de maximizar

    def handle_logout(self):
        """Manipula logout"""
        if self.on_logout:
            self.on_logout()
    
    def on_closing(self):
        """Manipula fechamento da janela"""
        result = messagebox.askyesno("Sair", "Deseja realmente sair do aplicativo?")
        if result:
            self.destroy()
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        messagebox.showinfo("Sucesso", message)
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        messagebox.showerror("Erro", message)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(_('main.settings.title'))
        settings_window.geometry("400x500")
        settings_window.resizable(False, False)
        
        # Center the settings window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Load current settings
        current_config = self.load_current_settings()
        
        # Main frame
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language selection
        lang_frame = ttk.LabelFrame(main_frame, text=_('main.settings.language'), padding="10")
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.language_var = tk.StringVar(value=current_config.get('language', get_i18n().get_current_language()))
        ttk.Radiobutton(lang_frame, text=_('main.settings.languages.pt'), 
                       variable=self.language_var, value='pt').pack(anchor=tk.W)
        ttk.Radiobutton(lang_frame, text=_('main.settings.languages.en'), 
                       variable=self.language_var, value='en').pack(anchor=tk.W)
        
        # Theme selection
        theme_frame = ttk.LabelFrame(main_frame, text=_('main.settings.theme'), padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_var = tk.StringVar(value=current_config.get('theme', 'arc'))
        available_themes = ['arc', 'equilux', 'adapta', 'breeze', 'yaru']
        for theme in available_themes:
            ttk.Radiobutton(theme_frame, text=theme.capitalize(), 
                           variable=self.theme_var, value=theme).pack(anchor=tk.W)
        
        # Dark mode
        dark_frame = ttk.LabelFrame(main_frame, text=_('main.settings.appearance'), padding="10")
        dark_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dark_mode_var = tk.BooleanVar(value=current_config.get('dark_mode', False))
        ttk.Checkbutton(dark_frame, text=_('main.settings.dark_mode'), 
                       variable=self.dark_mode_var).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text=_('common.cancel'), 
                  command=settings_window.destroy).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text=_('common.save'), 
                  command=lambda: self.apply_settings(settings_window)).pack(side=tk.RIGHT)
    
    def apply_settings(self, settings_window):
        """Apply settings changes"""
        new_language = self.language_var.get()
        new_theme = self.theme_var.get()
        new_dark_mode = self.dark_mode_var.get()
        
        # Get current settings to compare
        current_settings = self.load_current_settings()
        
        # Change language if different
        if new_language != get_i18n().get_current_language():
            get_i18n().change_language(new_language)
            self.update_interface_text()
            messagebox.showinfo(_('common.info'), _('main.settings.restart_required'))
        
        # Change theme immediately if different
        if new_theme != current_settings.get('theme', 'arc'):
            if self.apply_theme(new_theme):
                messagebox.showinfo(_('common.success'), _('main.settings.theme_applied'))
            else:
                messagebox.showerror(_('common.error'), _('main.settings.theme_error'))
        
        # Apply dark mode immediately if different
        if new_dark_mode != current_settings.get('dark_mode', False):
            if self.apply_dark_mode(new_dark_mode):
                mode_text = _('main.settings.dark_mode_enabled') if new_dark_mode else _('main.settings.dark_mode_disabled')
                messagebox.showinfo(_('common.success'), mode_text)
            else:
                messagebox.showerror(_('common.error'), _('main.settings.dark_mode_error'))
        
        # Save settings to database
        if hasattr(self, 'on_settings_changed'):
            self.on_settings_changed(new_language, new_theme, new_dark_mode)
        
        settings_window.destroy()
    
    def load_current_settings(self):
        """Load current user settings"""
        if hasattr(self, 'get_current_settings') and callable(self.get_current_settings):
            return self.get_current_settings()
        return {
            'theme': 'arc',
            'language': get_i18n().get_current_language(),
            'dark_mode': False
        }
    
    def apply_theme(self, theme_name):
        """Apply theme dynamically"""
        try:
            self.root.set_theme(theme_name)
            return True
        except Exception as e:
            print(f"Error applying theme {theme_name}: {e}")
            return False
    
    def apply_dark_mode(self, dark_mode_enabled):
        """Apply dark mode colors to the interface"""
        try:
            style = ttk.Style()
            
            if dark_mode_enabled:
                # Dark mode colors
                bg_color = "#2c3e50"          # Dark blue-gray background
                fg_color = "#ecf0f1"          # Light gray text
                select_bg = "#34495e"         # Darker selection background
                button_bg = "#3498db"         # Blue buttons
                entry_bg = "#34495e"          # Dark entries
                frame_bg = "#2c3e50"          # Dark frames
                scrollbar_bg = "#34495e"      # Dark scrollbars
                
                # Configure root window
                self.root.configure(bg=bg_color)
                
                # Configure ALL frame types
                style.configure("TFrame", background=bg_color, relief="flat")
                style.configure("TLabelFrame", 
                               background=bg_color, 
                               foreground=fg_color,
                               borderwidth=1,
                               relief="solid")
                style.configure("TLabelFrame.Label", 
                               background=bg_color, 
                               foreground=fg_color, 
                               font=("Arial", 10, "bold"))
                
                # Configure ALL label types
                style.configure("TLabel", background=bg_color, foreground=fg_color)
                style.configure("Header.TLabel", 
                               background=bg_color, 
                               foreground=fg_color,
                               font=("Arial", 16, "bold"))
                style.configure("Section.TLabel",
                               background=bg_color, 
                               foreground=fg_color,
                               font=("Arial", 12, "bold"))
                style.configure("Status.TLabel",
                               background=bg_color, 
                               foreground=fg_color,
                               font=("Arial", 10),
                               padding=5)
                style.configure("Success.TLabel",
                               background=bg_color, 
                               foreground="#27ae60",
                               font=("Arial", 10))
                style.configure("Error.TLabel",
                               background=bg_color, 
                               foreground="#e74c3c",
                               font=("Arial", 10))
                
                # Configure ALL button types with enhanced styling
                style.configure("TButton", 
                               background=button_bg, 
                               foreground="white",
                               borderwidth=1,
                               focuscolor="white",
                               relief="solid")
                style.map("TButton",
                         background=[
                             ('active', '#2980b9'), 
                             ('pressed', '#1f6391'),
                             ('disabled', '#95a5a6'),
                             ('!disabled', button_bg)
                         ],
                         foreground=[
                             ('active', 'white'), 
                             ('pressed', 'white'),
                             ('disabled', '#7f8c8d'),
                             ('!disabled', 'white')
                         ],
                         bordercolor=[
                             ('active', 'white'),
                             ('pressed', 'white'),
                             ('disabled', '#bdc3c7'),
                             ('!disabled', 'white')
                         ])
                
                # Configure entry styles
                style.configure("TEntry", 
                               background=entry_bg, 
                               foreground=fg_color,
                               borderwidth=1,
                               insertcolor=fg_color,
                               relief="solid")
                style.map("TEntry",
                         background=[('focus', '#34495e'), ('!focus', entry_bg)],
                         foreground=[('focus', fg_color), ('!focus', fg_color)],
                         bordercolor=[('focus', '#3498db'), ('!focus', '#566e7e')])
                
                # Configure treeview with enhanced styling
                style.configure("Treeview", 
                               background=entry_bg, 
                               foreground=fg_color,
                               fieldbackground=entry_bg,
                               borderwidth=1,
                               relief="solid")
                style.configure("Treeview.Heading", 
                               background=select_bg, 
                               foreground=fg_color,
                               borderwidth=1,
                               relief="solid")
                style.map("Treeview",
                         background=[('selected', select_bg)],
                         foreground=[('selected', 'white')])
                style.map("Treeview.Heading",
                         background=[('active', '#3498db')],
                         foreground=[('active', 'white')])
                
                # Configure scrollbar
                style.configure("Vertical.TScrollbar",
                               background=scrollbar_bg,
                               troughcolor=bg_color,
                               borderwidth=1,
                               arrowcolor=fg_color)
                style.map("Vertical.TScrollbar",
                         background=[('active', '#3498db')],
                         arrowcolor=[('active', 'white')])
                
                # Configure checkbutton
                style.configure("TCheckbutton", 
                               background=bg_color, 
                               foreground=fg_color,
                               focuscolor=bg_color)
                style.map("TCheckbutton",
                         background=[('active', bg_color)],
                         foreground=[('active', fg_color)])
                
                # Configure radiobutton
                style.configure("TRadiobutton", 
                               background=bg_color, 
                               foreground=fg_color,
                               focuscolor=bg_color)
                style.map("TRadiobutton",
                         background=[('active', bg_color)],
                         foreground=[('active', fg_color)])
                
                # Configure separator
                style.configure("TSeparator", background=select_bg)
                
                # Apply direct widget configuration for resistant widgets
                self._apply_dark_mode_to_widgets(bg_color, fg_color, button_bg)
                
            else:
                # Light mode - reset to theme defaults
                current_theme = style.theme_use()
                style.theme_use('default')  # Reset to default first
                style.theme_use(current_theme)  # Then apply current theme
                
                # Reset root background with platform-appropriate color
                self.root.configure(bg=self._get_default_bg_color())
                
                # Reset custom styles to defaults
                self._reset_light_mode_styles(style)
                
                # Apply light mode to direct widgets
                self._apply_light_mode_to_widgets()
                
            # Botão analisar sempre habilitado, não precisa de atualização especial
            
            return True
            
        except Exception as e:
            print(f"Error applying dark mode: {e}")
            return False
    
    def _apply_dark_mode_to_widgets(self, bg_color, fg_color, button_bg):
        """Apply dark mode directly to specific widgets that resist style configuration"""
        try:
            # Function to recursively apply colors to all widgets
            def apply_to_widget(widget, is_dark_mode=True):
                try:
                    widget_class = widget.winfo_class()
                    
                    if is_dark_mode:
                        # Dark mode colors
                        if widget_class in ['Frame', 'Labelframe']:
                            widget.configure(bg=bg_color)
                        elif widget_class == 'Label':
                            widget.configure(bg=bg_color, fg=fg_color)
                        elif widget_class == 'Button':
                            if widget != self.analyze_button:  # Don't override analyze button
                                widget.configure(bg=button_bg, fg='white', activebackground='#2980b9', activeforeground='white')
                        elif widget_class == 'Entry':
                            widget.configure(bg='#34495e', fg=fg_color, insertbackground=fg_color)
                        elif widget_class == 'Text':
                            widget.configure(bg='#34495e', fg=fg_color, insertbackground=fg_color)
                        elif widget_class == 'Listbox':
                            widget.configure(bg='#34495e', fg=fg_color, selectbackground='#34495e')
                        elif widget_class == 'Checkbutton':
                            widget.configure(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
                        elif widget_class == 'Radiobutton':
                            widget.configure(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
                        elif widget_class == 'Toplevel':
                            widget.configure(bg=bg_color)
                    else:
                        # Light mode - reset to safe defaults
                        default_bg = self._get_default_bg_color()
                        default_fg = '#000000'  # Black text
                        
                        if widget_class in ['Frame', 'Labelframe']:
                            widget.configure(bg=default_bg)
                        elif widget_class == 'Label':
                            widget.configure(bg=default_bg, fg=default_fg)
                        elif widget_class == 'Button':
                            if widget != self.analyze_button:  # Don't override analyze button
                                widget.configure(bg='#e1e1e1', fg='#000000', activebackground='#d1d1d1', activeforeground='#000000')
                        elif widget_class == 'Entry':
                            widget.configure(bg='#ffffff', fg=default_fg, insertbackground=default_fg)
                        elif widget_class == 'Text':
                            widget.configure(bg='#ffffff', fg=default_fg, insertbackground=default_fg)
                        elif widget_class == 'Listbox':
                            widget.configure(bg='#ffffff', fg=default_fg, selectbackground='#0078d4')
                        elif widget_class == 'Checkbutton':
                            widget.configure(bg=default_bg, fg=default_fg, activebackground=default_bg, activeforeground=default_fg)
                        elif widget_class == 'Radiobutton':
                            widget.configure(bg=default_bg, fg=default_fg, activebackground=default_bg, activeforeground=default_fg)
                        elif widget_class == 'Toplevel':
                            widget.configure(bg=default_bg)
                    
                    # Recursively apply to all children
                    for child in widget.winfo_children():
                        apply_to_widget(child, is_dark_mode)
                        
                except Exception as e:
                    # Some widgets might not support certain configurations
                    pass
            
            # Apply to root and all children
            apply_to_widget(self.root, True)
            
        except Exception as e:
            print(f"Error applying dark mode to widgets: {e}")
    
    def _apply_light_mode_to_widgets(self):
        """Apply light mode directly to specific widgets"""
        try:
            # Use the same function but with is_dark_mode=False
            def apply_to_widget(widget):
                try:
                    widget_class = widget.winfo_class()
                    default_bg = self._get_default_bg_color()
                    default_fg = '#000000'  # Black text
                    
                    if widget_class in ['Frame', 'Labelframe']:
                        widget.configure(bg=default_bg)
                    elif widget_class == 'Label':
                        widget.configure(bg=default_bg, fg=default_fg)
                    elif widget_class == 'Button':
                        if widget != self.analyze_button:  # Don't override analyze button
                            widget.configure(bg='#e1e1e1', fg='#000000', activebackground='#d1d1d1', activeforeground='#000000')
                    elif widget_class == 'Entry':
                        widget.configure(bg='#ffffff', fg=default_fg, insertbackground=default_fg)
                    elif widget_class == 'Text':
                        widget.configure(bg='#ffffff', fg=default_fg, insertbackground=default_fg)
                    elif widget_class == 'Listbox':
                        widget.configure(bg='#ffffff', fg=default_fg, selectbackground='#0078d4')
                    elif widget_class == 'Checkbutton':
                        widget.configure(bg=default_bg, fg=default_fg, activebackground=default_bg, activeforeground=default_fg)
                    elif widget_class == 'Radiobutton':
                        widget.configure(bg=default_bg, fg=default_fg, activebackground=default_bg, activeforeground=default_fg)
                    elif widget_class == 'Toplevel':
                        widget.configure(bg=default_bg)
                    
                    # Recursively apply to all children
                    for child in widget.winfo_children():
                        apply_to_widget(child)
                        
                except Exception as e:
                    # Some widgets might not support certain configurations
                    pass
            
            # Apply to root and all children
            apply_to_widget(self.root)
            
        except Exception as e:
            print(f"Error applying light mode to widgets: {e}")
    
    def _get_default_bg_color(self):
        """Get default background color based on platform"""
        import platform
        system = platform.system().lower()
        
        try:
            if system == 'windows':
                # Try Windows system color first
                try:
                    return 'SystemButtonFace'
                except:
                    return '#f0f0f0'  # Windows-like gray
            elif system == 'darwin':  # macOS
                return '#ececec'  # macOS-like gray
            else:  # Linux and others
                return '#e8e8e8'  # Light gray for Linux
        except:
            # Ultimate fallback - safe light gray
            return '#f0f0f0'
    
    def _reset_light_mode_styles(self, style):
        """Reset styles for light mode"""
        try:
            # Reset all custom styles to default appearance
            default_styles = {
                "TFrame": {},
                "TLabel": {},
                "TButton": {},
                "TEntry": {},
                "TCheckbutton": {},
                "TRadiobutton": {},
                "TLabelFrame": {},
                "Treeview": {},
                "TSeparator": {},
                "Vertical.TScrollbar": {}
            }
            
            for style_name in default_styles:
                try:
                    style.configure(style_name, **default_styles[style_name])
                except:
                    pass
                    
        except Exception as e:
            print(f"Error resetting light mode styles: {e}")
    
    def destroy(self):
        """Destroy window"""
        if self.root:
            self.root.destroy()
    
    def run(self):
        """Executa o loop da interface"""
        if self.root:
            # Bind events para atualizar botão analisar
            self.protocolo_entry.bind('<KeyRelease>', lambda e: self.update_analyze_button())
            self.setor_entry.bind('<KeyRelease>', lambda e: self.update_analyze_button())
            
            # Carregar execuções iniciais (após 100ms para garantir que o controller já configurou os métodos)
            self.root.after(100, self.refresh_executions)
            
            self.root.mainloop()