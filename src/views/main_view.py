"""
Main application screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
try:
    from tkinter import filedialog
except ImportError:
    import tkinter.filedialog as filedialog
import ttkbootstrap as ttk_boot
from ttkbootstrap import Window
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
    
    def __init__(self, usuario_data, initial_theme="cosmo", root_window=None, on_logout=None, on_analyze=None, on_delete_execution=None, on_refresh_executions=None):
        self.usuario_data = usuario_data
        self.initial_theme = initial_theme
        self.root_window = root_window  # Existing window from login
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
        if self.root_window:
            # Reuse existing window from login
            self.root = self.root_window
            
            # Clear all existing widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Update title
            self.root.title(_('app.main_title') + f" - {self.usuario_data['username']}")
            
            # Apply theme if different from current
            self.style = ttk_boot.Style(theme=self.initial_theme)
            
            # Resize window for main view (80% of screen)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            self.root.geometry(f"{window_width}x{window_height}")
        else:
            # Create new window (fallback, shouldn't happen normally)
            self.root = Window(themename=self.initial_theme)
            self.root.title(_('app.main_title') + f" - {self.usuario_data['username']}")
            self.style = ttk_boot.Style(theme=self.initial_theme)
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            self.root.geometry(f"{window_width}x{window_height}")
        
        self.root.resizable(True, True)
        
        # Variable to control maximize state
        self.is_maximized = False
        
        # Center on screen
        ## self.center_window()
        
        # Configurar estilo
        self.setup_styles()
        
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
        """Center window on screen"""
        self.root.update_idletasks()
        
        # Get current window dimensions
        self.root.geometry("")  # Reset geometry to get natural size
        self.root.update_idletasks()
        
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # If not defined yet, use calculated dimensions
        if width < 100:  # Very small value indicates it hasn't been defined yet
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
    
    def setup_keyboard_shortcuts(self):
        """Configure keyboard shortcuts"""
        # F11 to maximize/restore
        self.root.bind('<F11>', lambda e: self.toggle_maximize())
        
        # Ctrl+M to maximize/restore  
        self.root.bind('<Control-m>', lambda e: self.toggle_maximize())
        
        # Escape to restore if maximized
        self.root.bind('<Escape>', lambda e: self.restore_window() if self.is_maximized else None)
    
    def create_tooltip(self, widget, text):
        """Create tooltip for a widget"""
        return ToolTip(widget, text)
    
    def create_widgets(self):
        """Create interface widgets"""
        # Main frame with scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Folder selection section
        self.create_folder_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # File verification section
        self.create_files_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Analysis configuration section
        self.create_analysis_section(main_frame)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Executions section
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
        self.create_tooltip(self.maximize_btn, _('tooltips.maximize_restore'))
        
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
        
        # Add tooltip to settings button
        self.create_tooltip(settings_btn, _('tooltips.settings'))
        
        self.logout_button = ttk.Button(user_frame, 
                               text=_('main.logout'),
                               command=self.handle_logout)
        self.logout_button.pack(side=tk.RIGHT)
    
    def create_folder_section(self, parent):
        """Create folder selection section"""
        folder_frame = ttk.LabelFrame(parent, text=_('main_view.folder_section.title'), padding=15)
        folder_frame.pack(fill=tk.X, pady=10)
        
        # Button to select folder
        select_frame = ttk.Frame(folder_frame)
        select_frame.pack(fill=tk.X, pady=5)
        
        self.browse_button = ttk.Button(select_frame,
                  text=_('main_view.folder_section.select_folder'),
                  command=self.select_folder)
        self.browse_button.pack(side=tk.LEFT)
        
        # Label to show selected folder
        self.folder_label = ttk.Label(select_frame,
                                     text=_('main_view.folder_section.no_folder'),
                                     foreground="#7f8c8d")
        self.folder_label.pack(side=tk.LEFT, padx=(15, 0))
    
    def create_files_section(self, parent):
        """Create file verification section"""
        files_frame = ttk.LabelFrame(parent, text=_('main_view.files_section.title'), padding=15)
        files_frame.pack(fill=tk.X, pady=10)
        
        # File status grid
        self.files_labels = {}
        
        # Headers
        ttk.Label(files_frame, text=_('main_view.files_section.file_header'), font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 50))
        ttk.Label(files_frame, text=_('main_view.files_section.status_header'), font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        ttk.Label(files_frame, text=_('main_view.files_section.type_header'), font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W)
        
        # Clients file
        ttk.Label(files_frame, text=_('main_view.files_section.clients_file')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.files_labels['clientes'] = ttk.Label(files_frame, text=_('main_view.files_section.not_found_required'), style="Error.TLabel")
        self.files_labels['clientes'].grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text=_('main_view.files_section.required')).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Sales file
        ttk.Label(files_frame, text=_('main_view.files_section.sales_file')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.files_labels['vendas'] = ttk.Label(files_frame, text=_('main_view.files_section.not_found_required'), style="Error.TLabel")
        self.files_labels['vendas'].grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text=_('main_view.files_section.required')).grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # Addresses file
        ttk.Label(files_frame, text=_('main_view.files_section.addresses_file')).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.files_labels['enderecos'] = ttk.Label(files_frame, text=_('main_view.files_section.not_found_optional'), style="Status.TLabel")
        self.files_labels['enderecos'].grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(files_frame, text=_('main_view.files_section.optional')).grid(row=3, column=2, sticky=tk.W, pady=5)
    
    def create_analysis_section(self, parent):
        """Create analysis configuration section"""
        analysis_frame = ttk.LabelFrame(parent, text=_('main_view.analysis_section.title'), padding=15)
        analysis_frame.pack(fill=tk.X, pady=10)
        
        # Configuration grid
        config_grid = ttk.Frame(analysis_frame)
        config_grid.pack(fill=tk.X)
        
        # Protocol
        ttk.Label(config_grid, text=_('main_view.analysis_section.protocol_label')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.protocolo_entry = ttk.Entry(config_grid, width=30, state="disabled")
        self.protocolo_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Sector
        ttk.Label(config_grid, text=_('main_view.analysis_section.sector_label')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.setor_entry = ttk.Entry(config_grid, width=30, state="disabled")
        self.setor_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Result file
        ttk.Label(config_grid, text=_('main_view.analysis_section.result_file_label')).grid(row=2, column=0, sticky=tk.W, pady=5)
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
        
        # Analyze button
        analyze_frame = ttk.Frame(analysis_frame)
        analyze_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.analyze_button = ttk.Button(analyze_frame,
                                        text=_('main_view.analysis_section.analyze_button'),
                                        state="normal",
                                        width=10,
                                        command=self.handle_analyze)
        self.analyze_button.pack()
        
        
        # Configure button style
        self._setup_analyze_button_style()
        
        
 
        
    
    def create_executions_section(self, parent):
        """Create executions section"""
        exec_frame = ttk.LabelFrame(parent, text=_('main_view.executions_section.title'), padding=15)
        exec_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview to show executions
        columns = ('ID', 'Protocolo', 'Setor', 'Data', 'Status')
        self.executions_tree = ttk.Treeview(exec_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.executions_tree.heading('ID', text=_('main.executions.columns.id'))
        self.executions_tree.heading('Protocolo', text=_('main.executions.columns.protocol'))
        self.executions_tree.heading('Setor', text=_('main.executions.columns.sector'))
        self.executions_tree.heading('Data', text=_('main.executions.columns.date'))
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
        
        # Buttons for CRUD
        crud_frame = ttk.Frame(exec_frame)
        crud_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(crud_frame, text=_('main.refresh'), command=self.refresh_executions).pack(side=tk.LEFT)
        ttk.Button(crud_frame, text=_('main.executions.delete'), command=self.delete_execution).pack(side=tk.LEFT, padx=(5, 0))
    
    def select_folder(self):
        """Select folder with files"""
        folder = filedialog.askdirectory(title=_('main.folder_selection.description'))
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=f"{_('main_view.folder_section.selected_folder')}: {folder}")
            self.check_files()
    
    def check_files(self):
        """Check if necessary files exist in folder"""
        if not self.selected_folder:
            return
        
        # Reset status
        for key in self.files_status:
            self.files_status[key] = False
        
        # Check files
        files_in_folder = os.listdir(self.selected_folder)
        
        for file_name in files_in_folder:
            name_lower = file_name.lower()
            if name_lower.startswith('clientes.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['clientes'] = True
                self.files_labels['clientes'].config(text=_('main_view.files_section.found'), style="Success.TLabel")
            elif name_lower.startswith('vendas.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['vendas'] = True
                self.files_labels['vendas'].config(text=_('main_view.files_section.found'), style="Success.TLabel") 
            elif name_lower.startswith('enderecos.') and (name_lower.endswith('.csv') or name_lower.endswith('.xlsx')):
                self.files_status['enderecos'] = True
                self.files_labels['enderecos'].config(text=_('main_view.files_section.found'), style="Success.TLabel")
        
        # Update labels for files not found
        if not self.files_status['clientes']:
            self.files_labels['clientes'].config(text=_('main_view.files_section.not_found_required'), style="Error.TLabel")
        if not self.files_status['vendas']:
            self.files_labels['vendas'].config(text=_('main_view.files_section.not_found_required'), style="Error.TLabel")
        if not self.files_status['enderecos']:
            self.files_labels['enderecos'].config(text=_('main_view.files_section.not_found_optional'), style="Status.TLabel")
        
        # Enable fields if required files were found
        self.update_form_state()
    
    def update_form_state(self):
        """Update field states based on file verification"""
        required_files_ok = self.files_status['clientes'] and self.files_status['vendas']
        
        state = "normal" if required_files_ok else "disabled"
        
        self.protocolo_entry.config(state=state)
        self.setor_entry.config(state=state)
        self.result_path_entry.config(state=state)
        self.select_result_btn.config(state=state)
        
    
    def select_result_path(self):
        """Select path for result file"""
        file_path = filedialog.asksaveasfilename(
            title=_('main_view.file_dialog.save_result_title'),
            defaultextension=".txt",
            filetypes=[(_('main_view.file_dialog.text_files'), "*.txt"), (_('main_view.file_dialog.all_files'), "*.*")]
        )
        if file_path:
            self.result_path_entry.delete(0, tk.END)
            self.result_path_entry.insert(0, file_path)
    
    def _setup_analyze_button_style(self):
        """Configure analyze button style"""
        try:
            style = ttk.Style()
            
        except Exception as e:
            print(f"Error configuring button style: {e}")
    
    def handle_analyze(self):
        """Handle analyze button click"""
        
        # Validate required fields
        errors = []
        
        # Check required files
        if not (self.files_status['clientes'] and self.files_status['vendas']):
            if not self.files_status['clientes']:
                errors.append(_('main_view.validation.clients_file_missing'))
            if not self.files_status['vendas']:
                errors.append(_('main_view.validation.sales_file_missing'))
        
        # Check form fields
        protocolo = self.protocolo_entry.get().strip()
        if not protocolo:
            errors.append(_('main_view.validation.protocol_required'))
        
        setor = self.setor_entry.get().strip()
        if not setor:
            errors.append(_('main_view.validation.sector_required'))
        
        arquivo_resultado = self.result_path_entry.get().strip()
        if not arquivo_resultado:
            errors.append(_('main_view.validation.result_path_required'))
        
        # If there are errors, show message and stop
        if errors:
            error_message = _('main_view.validation.correction_needed') + "\n\n" + "\n".join(errors)
            messagebox.showerror(_('main_view.validation.validation_error'), error_message)
            return
        
        # If everything is valid, ask for confirmation
        result = messagebox.askyesno(
            _('main_view.confirmation.analyze_title'),
            _('main_view.confirmation.analyze_message'),
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
        """Refresh executions list"""
        try:
            # Clear tree
            for item in self.executions_tree.get_children():
                self.executions_tree.delete(item)
            
            # Call controller callback if available
            if self.on_refresh_executions:
                self.on_refresh_executions()
            else:
                messagebox.showwarning(_('common.warning'), _('main_view.messages.update_unavailable'))
        except Exception as e:
            messagebox.showerror(_('common.error'), _('main_view.messages.update_error', error=str(e)))
    
    def delete_execution(self):
        """Delete selected execution"""
        selected = self.executions_tree.selection()
        if not selected:
            messagebox.showwarning(_('common.warning'), _('main_view.messages.select_execution'))
            return
        
        # Get selected execution ID
        try:
            item = self.executions_tree.item(selected[0])
            execucao_id = item['values'][0]
            
            # User confirmation
            result = messagebox.askyesno(
                _('main_view.messages.confirm_delete_title'), 
                _('main_view.messages.confirm_delete_message', id=execucao_id),
                icon="warning"
            )
            
            if result:
                # If we have a callback to delete (will be defined by controller)
                if hasattr(self, 'on_delete_execution') and self.on_delete_execution:
                    self.on_delete_execution(execucao_id)
                else:
                    # Fallback if controller didn't define callback
                    messagebox.showinfo(_('common.info'), _('main_view.messages.delete_not_connected'))
                    
        except (IndexError, KeyError) as e:
            messagebox.showerror(_('common.error'), _('main_view.messages.selection_error', error=str(e)))
        except Exception as e:
            messagebox.showerror(_('common.error'), _('main_view.messages.unexpected_error', error=str(e)))
    
    def toggle_maximize(self):
        """Toggle between maximize and restore window"""
        if self.is_maximized:
            # Restore original size
            self.restore_window()
        else:
            # Maximize window
            self.maximize_window()
    
    def maximize_window(self):
        """Maximize window to fullscreen"""
        # Save current position and size
        self.root.update_idletasks()
        self.saved_geometry = self.root.geometry()
        
        # Try using native system method first
        try:
            self.root.state('zoomed')  # Windows
            self.is_maximized = True
            self.maximize_btn.config(text="🗗")  # Restore icon
        except tk.TclError:
            # Fallback for Unix/Linux systems
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Maximize (leave small margin for taskbar/dock)
            self.root.geometry(f"{screen_width}x{screen_height-60}+0+0")
            
            self.is_maximized = True
            self.maximize_btn.config(text="🗗")  # Restore icon
    
    def restore_window(self):
        """Restore window to original size"""
        try:
            # Try to restore using native method
            self.root.state('normal')
            
            # Restore saved geometry
            if hasattr(self, 'saved_geometry'):
                self.root.geometry(self.saved_geometry)
            else:
                # Fallback to default size
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                width = int(screen_width * 0.8)
                height = int(screen_height * 0.8)
                pos_x = (screen_width // 2) - (width // 2)
                pos_y = (screen_height // 2) - (height // 2)
                self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
                
        except tk.TclError:
            # Fallback for systems that don't support state('normal')
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
        self.maximize_btn.config(text="🗖")  # Maximize icon

    def handle_logout(self):
        """Manipula logout"""
        if self.on_logout:
            self.on_logout()
    
    def on_closing(self):
        """Manipula fechamento da janela"""
        result = messagebox.askyesno(_('main_view.messages.exit_title'), _('main_view.messages.exit_message'))
        if result:
            self.destroy()
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        messagebox.showinfo(_('common.success'), message)
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        messagebox.showerror(_('common.error'), message)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(_('main.settings.title'))
        settings_window.geometry("450x600")
        settings_window.resizable(False, False)
        
        # Center the settings window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Load current settings
        current_config = self.load_current_settings()
        
        # Main frame with scrollbar
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
        
        # Get available themes from database
        from models.database import DatabaseManager, ConfigurationManager
        db_manager = DatabaseManager()
        config_manager = ConfigurationManager(db_manager)
        available_themes = config_manager.get_available_themes()
        
        self.theme_var = tk.StringVar(value=current_config.get('theme', 'cosmo'))
        
        # Separate light and dark themes
        light_label = ttk.Label(theme_frame, text="Light Themes:", font=("Arial", 9, "bold"))
        light_label.pack(anchor=tk.W, pady=(5, 2))
        
        for theme_key, theme_name in available_themes.items():
            if '(Light)' in theme_name:
                ttk.Radiobutton(theme_frame, text=theme_name, 
                               variable=self.theme_var, value=theme_key).pack(anchor=tk.W, padx=(10, 0))
        
        dark_label = ttk.Label(theme_frame, text="Dark Themes:", font=("Arial", 9, "bold"))
        dark_label.pack(anchor=tk.W, pady=(10, 2))
        
        for theme_key, theme_name in available_themes.items():
            if '(Dark)' in theme_name:
                ttk.Radiobutton(theme_frame, text=theme_name, 
                               variable=self.theme_var, value=theme_key).pack(anchor=tk.W, padx=(10, 0))
        
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
        
        # Get current settings to compare
        current_settings = self.load_current_settings()
        
        # Change language if different
        if new_language != get_i18n().get_current_language():
            get_i18n().change_language(new_language)
            self.update_interface_text()
            messagebox.showinfo(_('common.info'), _('main.settings.restart_required'))
        
        # Change theme immediately if different
        if new_theme != current_settings.get('theme', 'cosmo'):
            if self.apply_theme(new_theme):
                messagebox.showinfo(_('common.success'), _('main.settings.theme_applied'))
            else:
                messagebox.showerror(_('common.error'), _('main.settings.theme_error'))
        
        # Save settings to database
        if hasattr(self, 'on_settings_changed'):
            self.on_settings_changed(new_language, new_theme)
        
        settings_window.destroy()
    
    def load_current_settings(self):
        """Load current user settings"""
        if hasattr(self, 'get_current_settings') and callable(self.get_current_settings):
            return self.get_current_settings()
        return {
            'theme': 'cosmo',
            'language': get_i18n().get_current_language()
        }
    
    def apply_theme(self, theme_name):
        """Apply theme dynamically"""
        try:
            # Use the stored style instance to change theme
            self.style.theme_use(theme_name)
            return True
        except Exception as e:
            print(f"Error applying theme {theme_name}: {e}")
            return False
    
    def destroy(self):
        """Destroy window"""
        if self.root:
            self.root.destroy()
    
    def run(self):
        """Execute interface loop"""
        if self.root:
            # Bind events to update analyze button
            self.protocolo_entry.bind('<KeyRelease>', lambda e: self.update_analyze_button())
            self.setor_entry.bind('<KeyRelease>', lambda e: self.update_analyze_button())
            
            # Load initial executions (after 100ms to ensure controller has configured methods)
            self.root.after(100, self.refresh_executions)
            
            self.root.mainloop()