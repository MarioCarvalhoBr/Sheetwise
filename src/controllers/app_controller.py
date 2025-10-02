"""
Controlador principal do aplicativo
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import logging
from datetime import datetime

# Adicionar src ao path se necessário
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from models.database import DatabaseManager, Usuario, Execucao, ConfiguracaoManager
from views.login_view import LoginView
from views.main_view import MainView
from utils.file_processor import FileValidator, DataProcessor
from utils.i18n_manager import init_i18n, get_i18n, _

class AppController:
    """Controlador principal do aplicativo"""
    
    def __init__(self):
        self.setup_logging()
        self.db_manager = DatabaseManager()
        self.usuario_model = Usuario(self.db_manager)
        self.execucao_model = Execucao(self.db_manager)
        self.config_manager = ConfiguracaoManager(self.db_manager)
        self.file_validator = FileValidator()
        self.data_processor = DataProcessor()
        
        self.current_user = None
        self.login_view = None
        self.main_view = None
        
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analisa_planilhas.log'),
                logging.StreamHandler()
            ]
        )
    
    def run(self):
        """Start application"""
        self.logger.info("Starting Sheetwise")
        # Initialize i18n with default language
        init_i18n('pt')
        self.show_login()
    
    def load_user_settings(self, user_id):
        """Load and apply user settings"""
        try:
            config = self.config_manager.get_configuracao_or_create(user_id)
            
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
                'language': 'pt',
                'dark_mode': False
            }
    
    def show_login(self):
        """Mostra tela de login"""
        if self.main_view:
            self.main_view.destroy()
            self.main_view = None
        
        self.login_view = LoginView(on_login_success=self.handle_login)
        self.login_view.run()
    
    def handle_login(self, email, username=None, is_new_user=False):
        """Manipula login/cadastro do usuário"""
        try:
            if is_new_user:
                # Verificar se usuário já existe
                existing_user = self.usuario_model.buscar_usuario_por_email(email)
                if existing_user:
                    self.login_view.show_error("Usuário já cadastrado com este email.")
                    return
                
                # Criar novo usuário
                user_id = self.usuario_model.criar_usuario(username, email)
                self.current_user = {
                    'id': user_id,
                    'username': username,
                    'email': email
                }
                self.login_view.show_success("Usuário cadastrado com sucesso!")
                
            else:
                # Buscar usuário existente
                user = self.usuario_model.buscar_usuario_por_email(email)
                if not user:
                    self.login_view.show_error("Usuário não encontrado. Cadastre-se primeiro.")
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
            self.logger.error(f"Erro no login: {e}")
            if self.login_view:
                self.login_view.show_error(f"Erro no sistema: {str(e)}")
            else:
                # Fallback if login_view is None
                import tkinter.messagebox as messagebox
                messagebox.showerror("Error", f"System error: {str(e)}")
    
    def show_main(self):
        """Mostra tela principal"""
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
        
        # Executar a view
        self.main_view.run()
    
    def handle_logout(self):
        """Manipula logout"""
        self.current_user = None
        if self.main_view:
            self.main_view.destroy()
            self.main_view = None
        self.show_login()
    
    def handle_analyze(self, analysis_data):
        """Manipula análise dos dados"""
        try:
            self.logger.info(f"Iniciando análise para protocolo: {analysis_data['protocolo']}")
            
            # Validar arquivos
            files_dict = self.file_validator.find_files(analysis_data['pasta_origem'])
            validation_results = self.file_validator.validate_all_files(files_dict)
            
            # Verificar se validação passou
            for file_type, (is_valid, message) in validation_results.items():
                if file_type in ['clientes', 'vendas'] and not is_valid:
                    self.main_view.show_error(f"Erro na validação do arquivo {file_type}: {message}")
                    return
            
            # Processar dados
            processing_results = self.data_processor.process_data(files_dict)
            
            if not processing_results['success']:
                self.main_view.show_error(f"Erro no processamento: {processing_results['error_message']}")
                return
            
            # Gerar relatório
            report_text = self.data_processor.generate_report_text(
                processing_results,
                analysis_data['protocolo'],
                analysis_data['setor'],
                analysis_data['pasta_origem'],
                analysis_data['arquivo_resultado']
            )
            
            # Salvar arquivo resultado
            with open(analysis_data['arquivo_resultado'], 'w', encoding='utf-8') as f:
                f.write(report_text)
            
            # Salvar execução no banco
            nome_arquivo = os.path.basename(analysis_data['arquivo_resultado'])
            execucao_id = self.execucao_model.criar_execucao(
                usuario_id=self.current_user['id'],
                protocolo=analysis_data['protocolo'],
                setor=analysis_data['setor'],
                nome_arquivo=nome_arquivo,
                caminho_pasta_origem=analysis_data['pasta_origem'],
                caminho_arquivo_resultado=analysis_data['arquivo_resultado'],
                observacoes=f"Análise concluída com sucesso. {processing_results['statistics']['total_vendas']} vendas processadas."
            )
            
            self.logger.info(f"Análise concluída com sucesso. ID da execução: {execucao_id}")
            
            # Atualizar lista de execuções
            self.handle_refresh_executions()
            
            # Mostrar sucesso
            self.main_view.show_success(
                f"Análise concluída com sucesso!\n\n"
                f"Arquivo salvo em: {analysis_data['arquivo_resultado']}\n"
                f"Total de vendas processadas: {processing_results['statistics']['total_vendas']:,}\n"
                f"Receita total: R$ {processing_results['statistics']['receita_total']:,.2f}"
            )
            
        except Exception as e:
            self.logger.error(f"Erro na análise: {e}")
            self.main_view.show_error(f"Erro durante a análise: {str(e)}")
    
    def handle_refresh_executions(self):
        """Manipula a atualização da lista de execuções"""
        try:
            self.logger.info("Atualizando lista de execuções...")
            
            
            # Limpa toda a lista
            for item in self.main_view.executions_tree.get_children():
                self.main_view.executions_tree.delete(item)
            
            # Carregar execuções do usuário atual
            execucoes = self.execucao_model.listar_execucoes(self.current_user['id'])
            self.logger.info(f"Encontradas {len(execucoes)} execuções para o usuário {self.current_user['id']}")
            
            for execucao in execucoes:
                # Formatar data
                data_exec = datetime.strptime(execucao['data_execucao'], '%Y-%m-%d %H:%M:%S')
                data_formatada = data_exec.strftime('%d/%m/%Y %H:%M')
                
                self.main_view.executions_tree.insert('', tk.END, values=(
                    execucao['id'],
                    execucao['protocolo'],
                    execucao['setor'],
                    data_formatada,
                    execucao['status'].title()
                ))
                
        except Exception as e:
            self.logger.error(f"Erro ao atualizar execuções: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar execuções: {str(e)}")
    
    def handle_delete_execution(self, execucao_id):
        """Manipula a deleção de uma execução"""
        try:
            self.logger.info(f"Tentando deletar execução ID: {execucao_id}")
            
            # Deletar do banco de dados
            if self.execucao_model.deletar_execucao(execucao_id):
                self.logger.info(f"Execução {execucao_id} deletada com sucesso do banco de dados")
                messagebox.showinfo("Sucesso", "Execução deletada com sucesso.")
                
                
                # Atualizar a lista de execuções
                self.handle_refresh_executions()
                return True
            else:
                self.logger.error(f"Falha ao deletar execução {execucao_id} do banco de dados")
                messagebox.showerror(_('common.error'), _('main.executions.delete_error'))
                return False
                    
        except Exception as e:
            self.logger.error(f"Erro ao deletar execução {execucao_id}: {e}")
            messagebox.showerror(_('common.error'), f"Erro ao deletar execução: {str(e)}")
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
            'language': 'pt',
            'dark_mode': False
        }
    
    def handle_settings_changed(self, language, theme, dark_mode):
        """Handle settings changes"""
        try:
            # Save settings to database
            success = self.config_manager.salvar_configuracao(
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
