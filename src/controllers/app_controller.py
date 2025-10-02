"""
Main application controller
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import logging
from datetime import datetime

# Add src to path if necessary
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from models.database import DatabaseManager, User, Execution, ConfigurationManager
from views.login_view import LoginView
from views.main_view import MainView
from utils.file_processor import FileValidator, DataProcessor
from utils.i18n_manager import init_i18n, get_i18n, _

class AppController:
    """Main application controller"""
    
    def __init__(self):
        self.setup_logging()
        self.db_manager = DatabaseManager()
        self.user_model = User(self.db_manager)
        self.execution_model = Execution(self.db_manager)
        self.config_manager = ConfigurationManager(self.db_manager)
        self.file_validator = FileValidator()
        self.data_processor = DataProcessor()
        
        self.current_user = None
        self.login_view = None
        self.main_view = None
        
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sheetwise.log'),
                logging.StreamHandler()
            ]
        )
    
    def run(self):
        """Start application"""
        self.logger.info("Starting Sheetwise")
        # Initialize i18n with default language (English)
        init_i18n('en')
        self.show_login()
    
    def load_user_settings(self, user_id):
        """Load and apply user settings"""
        try:
            config = self.config_manager.get_configuration_or_create(user_id)
            
            # Apply language setting
            if config['language'] != get_i18n().get_current_language():
                get_i18n().change_language(config['language'])
            
            # Store current config for later use
            self.current_config = config
            
            self.logger.info(f"User settings loaded: {config}")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading user settings: {e}")
            # Return default config
            return {
                'theme': 'arc',
                'language': 'en',
                'dark_mode': False
            }
    
    def show_login(self):
        """Show login screen"""
        if self.main_view:
            self.main_view.destroy()
            self.main_view = None
        
        self.login_view = LoginView(on_login_success=self.handle_login)
        self.login_view.run()
    
    def handle_login(self, email, username=None, is_new_user=False):
        """Handle user login/registration"""
        try:
            if is_new_user:
                # Check if user already exists
                existing_user = self.user_model.find_user_by_email(email)
                if existing_user:
                    self.login_view.show_error("User already registered with this email.")
                    return
                
                # Create new user
                user_id = self.user_model.create_user(username, email)
                self.current_user = {
                    'id': user_id,
                    'username': username,
                    'email': email
                }
                self.login_view.show_success("User registered successfully!")
                
            else:
                # Find existing user
                user = self.user_model.find_user_by_email(email)
                if not user:
                    self.login_view.show_error("User not found. Please register first.")
                    return
                
                self.current_user = user
            
            # Load user settings
            self.load_user_settings(self.current_user['id'])
            
            # Destroy login and show main screen
            login_view_temp = self.login_view
            self.login_view = None
            login_view_temp.destroy()
            self.show_main()
            
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            if self.login_view:
                self.login_view.show_error(f"System error: {str(e)}")
            else:
                # Fallback if login_view is None
                import tkinter.messagebox as messagebox
                messagebox.showerror("Error", f"System error: {str(e)}")
    
    def show_main(self):
        """Show main screen"""
        if not self.current_user:
            self.show_login()
            return
        
        # Get current theme and dark mode from settings
        current_config = self.get_current_settings()
        initial_theme = current_config.get('theme', 'arc')
        initial_dark_mode = current_config.get('dark_mode', False)
        
        self.main_view = MainView(
            usuario_data=self.current_user,
            initial_theme=initial_theme,
            initial_dark_mode=initial_dark_mode,
            on_logout=self.handle_logout,
            on_analyze=self.handle_analyze,
            on_delete_execution=self.handle_delete_execution,
            on_refresh_executions=self.handle_refresh_executions
        )
        
        # Add settings callbacks
        self.main_view.on_settings_changed = self.handle_settings_changed
        self.main_view.get_current_settings = self.get_current_settings
        
        # Run the view
        self.main_view.run()
    
    def handle_logout(self):
        """Handle logout"""
        self.current_user = None
        if self.main_view:
            self.main_view.destroy()
            self.main_view = None
        self.show_login()
    
    def handle_analyze(self, analysis_data):
        """Handle data analysis"""
        try:
            self.logger.info(f"Starting analysis for protocol: {analysis_data['protocolo']}")
            
            # Validate files
            files_dict = self.file_validator.find_files(analysis_data['pasta_origem'])
            validation_results = self.file_validator.validate_all_files(files_dict)
            
            # Check if validation passed
            for file_type, (is_valid, message) in validation_results.items():
                if file_type in ['clientes', 'vendas'] and not is_valid:
                    self.main_view.show_error(f"File validation error {file_type}: {message}")
                    return
            
            # Process data
            processing_results = self.data_processor.process_data(files_dict)
            
            if not processing_results['success']:
                self.main_view.show_error(f"Processing error: {processing_results['error_message']}")
                return
            
            # Generate report
            report_text = self.data_processor.generate_report_text(
                processing_results,
                analysis_data['protocolo'],
                analysis_data['setor'],
                analysis_data['pasta_origem'],
                analysis_data['arquivo_resultado']
            )
            
            # Save result file
            with open(analysis_data['arquivo_resultado'], 'w', encoding='utf-8') as f:
                f.write(report_text)
            
            # Save execution to database
            filename = os.path.basename(analysis_data['arquivo_resultado'])
            execution_id = self.execution_model.create_execution(
                user_id=self.current_user['id'],
                protocol=analysis_data['protocolo'],
                department=analysis_data['setor'],
                filename=filename,
                source_folder_path=analysis_data['pasta_origem'],
                result_file_path=analysis_data['arquivo_resultado'],
                notes=f"Analysis completed successfully. {processing_results['statistics']['total_vendas']} sales processed."
            )
            
            self.logger.info(f"Analysis completed successfully. Execution ID: {execution_id}")
            
            # Refresh executions list
            self.handle_refresh_executions()
            
            # Show success
            self.main_view.show_success(
                f"Analysis completed successfully!\n\n"
                f"File saved at: {analysis_data['arquivo_resultado']}\n"
                f"Total sales processed: {processing_results['statistics']['total_vendas']:,}\n"
                f"Total revenue: R$ {processing_results['statistics']['receita_total']:,.2f}"
            )
            
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            self.main_view.show_error(f"Error during analysis: {str(e)}")
    
    def handle_refresh_executions(self):
        """Handle executions list refresh"""
        try:
            self.logger.info("Refreshing executions list...")
            
            # Clear entire list
            for item in self.main_view.executions_tree.get_children():
                self.main_view.executions_tree.delete(item)
            
            # Load current user executions
            executions = self.execution_model.list_executions(self.current_user['id'])
            self.logger.info(f"Found {len(executions)} executions for user {self.current_user['id']}")
            
            for execution in executions:
                # Format date
                exec_date = datetime.strptime(execution['execution_date'], '%Y-%m-%d %H:%M:%S')
                formatted_date = exec_date.strftime('%d/%m/%Y %H:%M')
                
                self.main_view.executions_tree.insert('', tk.END, values=(
                    execution['id'],
                    execution['protocol'],
                    execution['department'],
                    formatted_date,
                    execution['status'].title()
                ))
                
        except Exception as e:
            self.logger.error(f"Error refreshing executions: {e}")
            messagebox.showerror("Error", f"Error refreshing executions: {str(e)}")
    
    def handle_delete_execution(self, execution_id):
        """Handle execution deletion"""
        try:
            self.logger.info(f"Attempting to delete execution ID: {execution_id}")
            
            # Delete from database
            if self.execution_model.delete_execution(execution_id):
                self.logger.info(f"Execution {execution_id} deleted successfully from database")
                messagebox.showinfo("Success", "Execution deleted successfully.")
                
                # Refresh executions list
                self.handle_refresh_executions()
                return True
            else:
                self.logger.error(f"Failed to delete execution {execution_id} from database")
                messagebox.showerror(_('common.error'), _('main.executions.delete_error'))
                return False
                    
        except Exception as e:
            self.logger.error(f"Error deleting execution {execution_id}: {e}")
            messagebox.showerror(_('common.error'), f"Error deleting execution: {str(e)}")
            return False
    
    def get_current_settings(self):
        """Get current user settings"""
        if hasattr(self, 'current_config') and self.current_config:
            return self.current_config
        
        # Load from database if not cached
        if self.current_user:
            return self.load_user_settings(self.current_user['id'])
        
        # Return defaults if no user
        return {
            'theme': 'arc',
            'language': 'en',
            'dark_mode': False
        }
    
    def handle_settings_changed(self, language, theme, dark_mode):
        """Handle settings changes"""
        try:
            # Save settings to database
            success = self.config_manager.save_configuration(
                self.current_user['id'], 
                theme, 
                language, 
                dark_mode
            )
            
            if success:
                self.logger.info(f"Settings saved: theme={theme}, language={language}, dark_mode={dark_mode}")
                
                # Update current config
                self.current_config = {
                    'theme': theme,
                    'language': language,
                    'dark_mode': dark_mode
                }
                
                messagebox.showinfo(_('common.success'), _('main.settings.settings_saved'))
            else:
                messagebox.showerror(_('common.error'), "Failed to save settings")
                
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            messagebox.showerror(_('common.error'), f"Error saving settings: {str(e)}")
