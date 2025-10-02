"""
Modelos de dados para o AnalisaPlanilhas
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    """Gerenciador de conexão com o banco de dados SQLite"""
    
    def __init__(self, db_path: str = "database/analisa_planilhas.db"):
        self.db_path = db_path
        self._ensure_database_directory()
        self._create_tables()
    
    def _ensure_database_directory(self):
        """Garante que o diretório do banco existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _create_tables(self):
        """Cria as tabelas necessárias no banco"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Migração: renomear coluna 'nome' para 'username' se existir
            self._migrate_nome_to_username(cursor)
            
            # Tabela de execuções
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execucoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    protocolo TEXT NOT NULL,
                    setor TEXT NOT NULL,
                    nome_arquivo TEXT NOT NULL,
                    caminho_pasta_origem TEXT NOT NULL,
                    caminho_arquivo_resultado TEXT NOT NULL,
                    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'concluido',
                    observacoes TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabela de configurações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    theme TEXT DEFAULT 'arc',
                    language TEXT DEFAULT 'pt',
                    dark_mode INTEGER DEFAULT 0,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                    UNIQUE(usuario_id)
                )
            ''')
            
            conn.commit()
    
    def _migrate_nome_to_username(self, cursor):
        """Migra a coluna 'nome' para 'username' se necessário"""
        try:
            # Verificar se a coluna 'nome' existe
            cursor.execute("PRAGMA table_info(usuarios)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Se a coluna 'nome' existe e 'username' não existe, fazer a migração
            if 'nome' in columns and 'username' not in columns:
                print("Migrando coluna 'nome' para 'username'...")
                
                # Criar nova tabela temporária
                cursor.execute('''
                    CREATE TABLE usuarios_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Copiar dados da tabela antiga para a nova
                cursor.execute('''
                    INSERT INTO usuarios_temp (id, username, email, data_cadastro)
                    SELECT id, nome, email, data_cadastro FROM usuarios
                ''')
                
                # Remover tabela antiga
                cursor.execute('DROP TABLE usuarios')
                
                # Renomear tabela temporária
                cursor.execute('ALTER TABLE usuarios_temp RENAME TO usuarios')
                
                print("Migração concluída com sucesso!")
                
        except Exception as e:
            print(f"Erro na migração: {e}")
            # Se houve erro, manter estrutura original
            pass
    
    def get_connection(self):
        """Retorna uma conexão com o banco"""
        return sqlite3.connect(self.db_path)


class Usuario:
    """Modelo para usuário"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def criar_usuario(self, username: str, email: str) -> int:
        """Cria um novo usuário"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, email) VALUES (?, ?)",
                (username, email)
            )
            return cursor.lastrowid
    
    def buscar_usuario_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, data_cadastro FROM usuarios WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'data_cadastro': row[3]
                }
        return None
    
    def listar_usuarios(self) -> List[Dict[str, Any]]:
        """Lista todos os usuários"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, data_cadastro FROM usuarios ORDER BY username"
            )
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'data_cadastro': row[3]
                }
                for row in rows
            ]


class Execucao:
    """Modelo para execução"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def criar_execucao(self, usuario_id: int, protocolo: str, setor: str, 
                      nome_arquivo: str, caminho_pasta_origem: str,
                      caminho_arquivo_resultado: str, observacoes: str = "") -> int:
        """Cria uma nova execução"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO execucoes 
                (usuario_id, protocolo, setor, nome_arquivo, caminho_pasta_origem,
                 caminho_arquivo_resultado, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id, protocolo, setor, nome_arquivo, caminho_pasta_origem,
                  caminho_arquivo_resultado, observacoes))
            return cursor.lastrowid
    
    def listar_execucoes(self, usuario_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista execuções, opcionalmente filtradas por usuário"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            if usuario_id:
                cursor.execute('''
                    SELECT e.id, e.protocolo, e.setor, e.nome_arquivo,
                           e.caminho_pasta_origem, e.caminho_arquivo_resultado,
                           e.data_execucao, e.status, e.observacoes,
                           u.username as usuario_username
                    FROM execucoes e
                    JOIN usuarios u ON e.usuario_id = u.id
                    WHERE e.usuario_id = ?
                    ORDER BY e.data_execucao DESC
                ''', (usuario_id,))
            else:
                cursor.execute('''
                    SELECT e.id, e.protocolo, e.setor, e.nome_arquivo,
                           e.caminho_pasta_origem, e.caminho_arquivo_resultado,
                           e.data_execucao, e.status, e.observacoes,
                           u.username as usuario_username
                    FROM execucoes e
                    JOIN usuarios u ON e.usuario_id = u.id
                    ORDER BY e.data_execucao DESC
                ''')
            
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'protocolo': row[1],
                    'setor': row[2],
                    'nome_arquivo': row[3],
                    'caminho_pasta_origem': row[4],
                    'caminho_arquivo_resultado': row[5],
                    'data_execucao': row[6],
                    'status': row[7],
                    'observacoes': row[8],
                    'usuario_username': row[9]
                }
                for row in rows
            ]
    
    def buscar_execucao_por_id(self, execucao_id: int) -> Optional[Dict[str, Any]]:
        """Busca execução por ID"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.id, e.protocolo, e.setor, e.nome_arquivo,
                       e.caminho_pasta_origem, e.caminho_arquivo_resultado,
                       e.data_execucao, e.status, e.observacoes,
                       u.username as usuario_username, e.usuario_id
                FROM execucoes e
                JOIN usuarios u ON e.usuario_id = u.id
                WHERE e.id = ?
            ''', (execucao_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'protocolo': row[1],
                    'setor': row[2],
                    'nome_arquivo': row[3],
                    'caminho_pasta_origem': row[4],
                    'caminho_arquivo_resultado': row[5],
                    'data_execucao': row[6],
                    'status': row[7],
                    'observacoes': row[8],
                    'usuario_username': row[9],
                    'usuario_id': row[10]
                }
        return None
    
    def deletar_execucao(self, execucao_id: int) -> bool:
        """Deleta uma execução"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM execucoes WHERE id = ?", (execucao_id,))
            return cursor.rowcount > 0
    
    def atualizar_status_execucao(self, execucao_id: int, status: str, 
                                 observacoes: str = "") -> bool:
        """Atualiza status de uma execução"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE execucoes 
                SET status = ?, observacoes = ?
                WHERE id = ?
            ''', (status, observacoes, execucao_id))
            return cursor.rowcount > 0


class ConfiguracaoManager:
    """Gerenciador de configurações do usuário"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_configuracao(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca configurações do usuário"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT theme, language, dark_mode, data_atualizacao
                FROM configuracoes 
                WHERE usuario_id = ?
            ''', (usuario_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'theme': row[0],
                    'language': row[1],
                    'dark_mode': bool(row[2]),
                    'data_atualizacao': row[3]
                }
        return None
    
    def get_configuracao_or_create(self, usuario_id: int) -> Dict[str, Any]:
        """Busca configurações ou cria padrão se não existir"""
        config = self.get_configuracao(usuario_id)
        if config is None:
            # Criar configuração padrão
            self.salvar_configuracao(usuario_id, 'arc', 'pt', False)
            config = {
                'theme': 'arc',
                'language': 'pt',
                'dark_mode': False,
                'data_atualizacao': datetime.now().isoformat()
            }
        return config
    
    def salvar_configuracao(self, usuario_id: int, theme: str, 
                           language: str, dark_mode: bool) -> bool:
        """Salva configurações do usuário"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se configuração já existe
            existing = self.get_configuracao(usuario_id)
            
            if existing:
                # Atualizar configuração existente
                cursor.execute('''
                    UPDATE configuracoes 
                    SET theme = ?, language = ?, dark_mode = ?, 
                        data_atualizacao = CURRENT_TIMESTAMP
                    WHERE usuario_id = ?
                ''', (theme, language, int(dark_mode), usuario_id))
            else:
                # Inserir nova configuração
                cursor.execute('''
                    INSERT INTO configuracoes 
                    (usuario_id, theme, language, dark_mode)
                    VALUES (?, ?, ?, ?)
                ''', (usuario_id, theme, language, int(dark_mode)))
            
            return cursor.rowcount > 0
    
    def atualizar_theme(self, usuario_id: int, theme: str) -> bool:
        """Atualiza apenas o tema"""
        config = self.get_configuracao_or_create(usuario_id)
        return self.salvar_configuracao(usuario_id, theme, 
                                      config['language'], config['dark_mode'])
    
    def atualizar_language(self, usuario_id: int, language: str) -> bool:
        """Atualiza apenas o idioma"""
        config = self.get_configuracao_or_create(usuario_id)
        return self.salvar_configuracao(usuario_id, config['theme'], 
                                      language, config['dark_mode'])
    
    def atualizar_dark_mode(self, usuario_id: int, dark_mode: bool) -> bool:
        """Atualiza apenas o modo escuro"""
        config = self.get_configuracao_or_create(usuario_id)
        return self.salvar_configuracao(usuario_id, config['theme'], 
                                      config['language'], dark_mode)
    
    def get_available_themes(self) -> Dict[str, str]:
        """Retorna temas disponíveis"""
        return {
            'arc': 'Arc',
            'equilux': 'Equilux (Dark)',
            'adapta': 'Adapta',
            'breeze': 'Breeze',
            'yaru': 'Yaru'
        }