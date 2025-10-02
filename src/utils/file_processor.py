"""
Utilitários para validação e processamento de arquivos
"""

import os
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging

class FileValidator:
    """Classe para validar arquivos CSV/XLSX"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def find_files(self, folder_path: str) -> Dict[str, Optional[str]]:
        """
        Encontra os arquivos necessários na pasta
        
        Returns:
            Dict com os caminhos dos arquivos encontrados
        """
        files_found = {
            'clientes': None,
            'vendas': None,
            'enderecos': None
        }
        
        if not os.path.exists(folder_path):
            return files_found
        
        try:
            files_in_folder = os.listdir(folder_path)
            
            for file_name in files_in_folder:
                name_lower = file_name.lower()
                full_path = os.path.join(folder_path, file_name)
                
                if name_lower.startswith('clientes.') and self._is_valid_extension(name_lower):
                    files_found['clientes'] = full_path
                elif name_lower.startswith('vendas.') and self._is_valid_extension(name_lower):
                    files_found['vendas'] = full_path
                elif name_lower.startswith('enderecos.') and self._is_valid_extension(name_lower):
                    files_found['enderecos'] = full_path
                    
        except Exception as e:
            self.logger.error(f"Erro ao listar arquivos da pasta {folder_path}: {e}")
        
        return files_found
    
    def _is_valid_extension(self, filename: str) -> bool:
        """Verifica se a extensão do arquivo é válida"""
        return filename.endswith('.csv') or filename.endswith('.xlsx')
    
    def validate_file_structure(self, file_path: str, expected_columns: List[str]) -> Tuple[bool, str]:
        """
        Valida se o arquivo tem as colunas esperadas
        
        Returns:
            Tuple (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "Arquivo não encontrado"
        
        try:
            # Ler apenas o cabeçalho
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=0)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, nrows=0)
            else:
                return False, "Formato de arquivo não suportado"
            
            # Verificar colunas
            missing_columns = []
            for col in expected_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                return False, f"Colunas faltando: {', '.join(missing_columns)}"
            
            return True, "Arquivo válido"
            
        except Exception as e:
            return False, f"Erro ao ler arquivo: {str(e)}"
    
    def validate_all_files(self, files_dict: Dict[str, Optional[str]]) -> Dict[str, Tuple[bool, str]]:
        """
        Valida todos os arquivos encontrados
        
        Returns:
            Dict com resultado da validação para cada arquivo
        """
        validation_results = {}
        
        # Definir colunas esperadas para cada arquivo
        expected_columns = {
            'clientes': ['id', 'nome'],
            'vendas': ['cliente_id', 'produto', 'quantidade', 'preco_unitario', 'preco_final'],
            'enderecos': ['cliente_id', 'rua', 'bairro', 'cidade']
        }
        
        for file_type, file_path in files_dict.items():
            if file_path is None:
                if file_type in ['clientes', 'vendas']:  # Obrigatórios
                    validation_results[file_type] = (False, "Arquivo obrigatório não encontrado")
                else:  # Opcional
                    validation_results[file_type] = (True, "Arquivo opcional não encontrado")
            else:
                validation_results[file_type] = self.validate_file_structure(
                    file_path, expected_columns[file_type]
                )
        
        return validation_results


class DataProcessor:
    """Classe para processamento dos dados"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Carrega arquivo CSV ou XLSX"""
        if not os.path.exists(file_path):
            return None
        
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                self.logger.error(f"Formato não suportado: {file_path}")
                return None
        except Exception as e:
            self.logger.error(f"Erro ao carregar arquivo {file_path}: {e}")
            return None
    
    def process_data(self, files_dict: Dict[str, Optional[str]]) -> Dict[str, any]:
        """
        Processa os dados dos arquivos e gera estatísticas
        
        Returns:
            Dict com os resultados do processamento
        """
        results = {
            'success': False,
            'error_message': '',
            'statistics': {},
            'data_summary': {}
        }
        
        try:
            # Carregar arquivos obrigatórios
            clientes_df = self.load_file(files_dict['clientes'])
            vendas_df = self.load_file(files_dict['vendas'])
            
            if clientes_df is None or vendas_df is None:
                results['error_message'] = "Erro ao carregar arquivos obrigatórios"
                return results
            
            # Carregar arquivo opcional
            enderecos_df = None
            if files_dict['enderecos']:
                enderecos_df = self.load_file(files_dict['enderecos'])
            
            # Processar dados
            stats = self._calculate_statistics(clientes_df, vendas_df, enderecos_df)
            summary = self._generate_summary(clientes_df, vendas_df, enderecos_df)
            
            results['success'] = True
            results['statistics'] = stats
            results['data_summary'] = summary
            
        except Exception as e:
            results['error_message'] = f"Erro no processamento: {str(e)}"
            self.logger.error(f"Erro no processamento dos dados: {e}")
        
        return results
    
    def _calculate_statistics(self, clientes_df: pd.DataFrame, 
                            vendas_df: pd.DataFrame, 
                            enderecos_df: Optional[pd.DataFrame]) -> Dict:
        """Calcula estatísticas dos dados"""
        stats = {}
        
        # Estatísticas básicas
        stats['total_clientes'] = len(clientes_df)
        stats['total_vendas'] = len(vendas_df)
        stats['total_enderecos'] = len(enderecos_df) if enderecos_df is not None else 0
        
        # Estatísticas de vendas
        stats['receita_total'] = vendas_df['preco_final'].sum()
        stats['ticket_medio'] = vendas_df['preco_final'].mean()
        stats['quantidade_total_produtos'] = vendas_df['quantidade'].sum()
        
        # Top produtos
        produtos_mais_vendidos = vendas_df.groupby('produto').agg({
            'quantidade': 'sum',
            'preco_final': 'sum'
        }).sort_values('quantidade', ascending=False).head(5)
        
        stats['top_produtos'] = produtos_mais_vendidos.to_dict('index')
        
        # Clientes com mais compras
        clientes_vendas = vendas_df.groupby('cliente_id').agg({
            'preco_final': 'sum',
            'quantidade': 'sum'
        }).sort_values('preco_final', ascending=False).head(5)
        
        stats['top_clientes'] = clientes_vendas.to_dict('index')
        
        return stats
    
    def _generate_summary(self, clientes_df: pd.DataFrame,
                         vendas_df: pd.DataFrame,
                         enderecos_df: Optional[pd.DataFrame]) -> Dict:
        """Gera resumo dos dados"""
        summary = {}
        
        # Validação de integridade
        clientes_ids = set(clientes_df['id'])
        vendas_cliente_ids = set(vendas_df['cliente_id'])
        
        # Clientes sem vendas
        clientes_sem_vendas = clientes_ids - vendas_cliente_ids
        summary['clientes_sem_vendas'] = len(clientes_sem_vendas)
        
        # Vendas com cliente inexistente
        vendas_cliente_inexistente = vendas_cliente_ids - clientes_ids
        summary['vendas_cliente_inexistente'] = len(vendas_cliente_inexistente)
        
        # Se há arquivo de endereços, verificar cobertura
        if enderecos_df is not None:
            enderecos_cliente_ids = set(enderecos_df['cliente_id'])
            clientes_sem_endereco = clientes_ids - enderecos_cliente_ids
            summary['clientes_sem_endereco'] = len(clientes_sem_endereco)
            summary['cobertura_enderecos'] = (len(enderecos_cliente_ids) / len(clientes_ids)) * 100
        else:
            summary['clientes_sem_endereco'] = len(clientes_ids)
            summary['cobertura_enderecos'] = 0
        
        return summary
    
    def generate_report_text(self, processing_results: Dict, 
                           protocolo: str, setor: str,
                           pasta_origem: str, arquivo_resultado: str) -> str:
        """Gera o texto do relatório resultado.txt"""
        from datetime import datetime
        
        report_lines = []
        report_lines.append("="*60)
        report_lines.append("RELATÓRIO DE ANÁLISE DE PLANILHAS")
        report_lines.append("="*60)
        report_lines.append("")
        
        # Informações da execução
        report_lines.append("INFORMAÇÕES DA EXECUÇÃO:")
        report_lines.append(f"Protocolo: {protocolo}")
        report_lines.append(f"Setor: {setor}")
        report_lines.append(f"Data de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        report_lines.append(f"Pasta de origem: {pasta_origem}")
        report_lines.append(f"Arquivo resultado: {arquivo_resultado}")
        report_lines.append("")
        
        if not processing_results['success']:
            report_lines.append("ERRO NO PROCESSAMENTO:")
            report_lines.append(processing_results['error_message'])
            return "\n".join(report_lines)
        
        # Estatísticas gerais
        stats = processing_results['statistics']
        report_lines.append("ESTATÍSTICAS GERAIS:")
        report_lines.append(f"Total de clientes: {stats['total_clientes']:,}")
        report_lines.append(f"Total de vendas: {stats['total_vendas']:,}")
        report_lines.append(f"Total de endereços: {stats['total_enderecos']:,}")
        report_lines.append(f"Receita total: R$ {stats['receita_total']:,.2f}")
        report_lines.append(f"Ticket médio: R$ {stats['ticket_medio']:,.2f}")
        report_lines.append(f"Quantidade total de produtos: {stats['quantidade_total_produtos']:,}")
        report_lines.append("")
        
        # Top produtos
        report_lines.append("TOP 5 PRODUTOS MAIS VENDIDOS:")
        for produto, dados in stats['top_produtos'].items():
            report_lines.append(f"- {produto}: {dados['quantidade']:,} unidades, R$ {dados['preco_final']:,.2f}")
        report_lines.append("")
        
        # Top clientes
        report_lines.append("TOP 5 CLIENTES (por receita):")
        for cliente_id, dados in stats['top_clientes'].items():
            report_lines.append(f"- Cliente {cliente_id}: R$ {dados['preco_final']:,.2f} ({dados['quantidade']:,} itens)")
        report_lines.append("")
        
        # Resumo de integridade
        summary = processing_results['data_summary']
        report_lines.append("ANÁLISE DE INTEGRIDADE DOS DADOS:")
        report_lines.append(f"Clientes sem vendas: {summary['clientes_sem_vendas']}")
        report_lines.append(f"Vendas com cliente inexistente: {summary['vendas_cliente_inexistente']}")
        report_lines.append(f"Clientes sem endereço: {summary['clientes_sem_endereco']}")
        report_lines.append(f"Cobertura de endereços: {summary['cobertura_enderecos']:.1f}%")
        report_lines.append("")
        
        report_lines.append("="*60)
        report_lines.append("Relatório gerado pelo Sheetwise v1.0")
        report_lines.append("="*60)
        
        return "\n".join(report_lines)