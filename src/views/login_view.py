"""
User login/registration screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_boot
from ttkbootstrap import Window
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
    
    def __init__(self, on_login_success=None, root_window=None, initial_theme="cosmo"):
        self.on_login_success = on_login_success
        self.root_window = root_window  # Existing window from main view
        self.initial_theme = initial_theme  # Theme to apply
        self.root = None
        self.setup_window()
    
    def setup_window(self):
        """Configure main window"""
        if self.root_window:
            # Reuse existing window from main view
            self.root = self.root_window
            
            # Clear all existing widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Update title
            self.root.title(_('app.login_title'))
            
            # Apply theme (may be different from the one used in main view)
            import ttkbootstrap as ttk_boot
            self.style = ttk_boot.Style(theme=self.initial_theme)
            
            # Resize window for login view
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            min_width, min_height = 500, 400
            if screen_width < 800:
                min_width = int(screen_width * 0.9)
            if screen_height < 600:
                min_height = int(screen_height * 0.8)
            
            max_width = int(screen_width * 0.4)
            max_height = int(screen_height * 0.5)
            
            window_width = max(min_width, min(max_width, 600))
            window_height = max(min_height, min(max_height, 500))
            
            pos_x = (screen_width - window_width) // 2
            pos_y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
            self.root.resizable(True, True)  # Allow resizing
            
        else:
            # Create new window (first run) with the theme from last user
            self.root = Window(themename=self.initial_theme)
            self.root.title(_('app.login_title'))
            
            # Calculate window size based on screen resolution
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Intelligent sizing system for login screen
            # Goals: window large enough for interaction, but not excessive
            min_width, min_height = 500, 400  # Minimum sizes for usability
            
            # Adaptation for small screens (netbooks, tablets, etc.)
            if screen_width < 800:
                min_width = int(screen_width * 0.9)  # 90% of width on small screens
            if screen_height < 600:
                min_height = int(screen_height * 0.8)  # 80% of height on small screens
            
            # Calculate ideal size based on screen
            max_width = int(screen_width * 0.4)   # Maximum 40% of width
            max_height = int(screen_height * 0.5)  # Maximum 50% of height
            
            # Determine final size (between minimum and maximum, with upper limit)
            window_width = max(min_width, min(max_width, 600))   # Maximum limit: 600px
            window_height = max(min_height, min(max_height, 500)) # Maximum limit: 500px
            
            # Calculate position to center
            pos_x = (screen_width - window_width) // 2
            pos_y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
            self.root.resizable(True, True)  # Allow resizing
        
        # Ensure window is updated
        self.root.update_idletasks()
        
        # Configure styles
        self.setup_styles()
        
        # Create interface
        self.create_widgets()
    
    def center_window(self):
        """Center window on screen (fallback method)"""
        self.root.update_idletasks()
        
        # Get current window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # If size is too small, use default values
        if width < 100:
            width = 500
        if height < 100:
            height = 400
        
        # Calculate center position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        
        # Title style
        style.configure("Title.TLabel", 
                       font=("Arial", 18, "bold"),
                       foreground="#2c3e50")
        
        # Subtitle style
        style.configure("Subtitle.TLabel",
                       font=("Arial", 10),
                       foreground="#7f8c8d")
        
        # Entry style
        style.configure("Custom.TEntry",
                       font=("Arial", 11),
                       padding=10)
    
    def create_widgets(self):
        """Create interface widgets"""
        # Create canvas with scrollbars for scrollable content
        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure canvas
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Main frame inside canvas
        main_frame = ttk.Frame(canvas, padding="30")
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # Update scroll region when frame size changes
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Center the frame horizontally if it's smaller than canvas
            canvas_width = canvas.winfo_width()
            frame_width = main_frame.winfo_reqwidth()
            if frame_width < canvas_width:
                x_position = (canvas_width - frame_width) // 2
                canvas.coords(canvas_window, x_position, 0)
            else:
                # Reset to left if frame is wider
                canvas.coords(canvas_window, 0, 0)
        
        main_frame.bind('<Configure>', configure_scroll_region)
        canvas.bind('<Configure>', configure_scroll_region)
        
        # Force update on window state changes
        def on_window_configure(event):
            canvas.update_idletasks()
            configure_scroll_region()
        
        self.root.bind('<Configure>', on_window_configure)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_shift_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)
        
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
        # Pre-fill with default value for testing
        self.username_entry.insert(0, "testuser")
        
        # Email field
        ttk.Label(form_frame, text=_('login.email'), font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.email_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 20))
        # Pre-fill with default value for testing
        self.email_entry.insert(0, "test@example.com")

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.login_button = ttk.Button(button_frame,
                                      text=_('login.login_button'),
                                      command=self.handle_login)
        self.login_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.register_button = ttk.Button(button_frame,
                                         text=_('login.register_button'),
                                         command=self.handle_register)
        self.register_button.pack(side=tk.RIGHT)
        
        # Bind Enter for login
        self.root.bind('<Return>', lambda e: self.handle_login())
        
        # Focus on username field
        self.username_entry.focus()
    
    def validate_email(self, email):
        """Validate email format"""
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
        """Show success message"""
        messagebox.showinfo("Success", message)
    
    def destroy(self):
        """Destroy window"""
        if self.root:
            self.root.destroy()
    
    def run(self):
        """Run interface loop"""
        if self.root:
            self.root.mainloop()