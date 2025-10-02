"""
File validation and processing utilities
"""

import os
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging

class FileValidator:
    """Class for validating CSV/XLSX files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def find_files(self, folder_path: str) -> Dict[str, Optional[str]]:
        """
        Find necessary files in folder
        
        Returns:
            Dict with paths of found files
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
            self.logger.error(f"Error listing files from folder {folder_path}: {e}")
        
        return files_found
    
    def _is_valid_extension(self, filename: str) -> bool:
        """Check if file extension is valid"""
        return filename.endswith('.csv') or filename.endswith('.xlsx')
    
    def validate_file_structure(self, file_path: str, expected_columns: List[str]) -> Tuple[bool, str]:
        """
        Validate if file has expected columns
        
        Returns:
            Tuple (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File not found"
        
        try:
            # Read header only
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=0)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, nrows=0)
            else:
                return False, "Unsupported file format"
            
            # Check columns
            missing_columns = []
            for col in expected_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                return False, f"Missing columns: {', '.join(missing_columns)}"
            
            return True, "Valid file"
            
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def validate_all_files(self, files_dict: Dict[str, Optional[str]]) -> Dict[str, Tuple[bool, str]]:
        """
        Validate all found files
        
        Returns:
            Dict with validation result for each file
        """
        validation_results = {}
        
        # Define expected columns for each file
        expected_columns = {
            'clientes': ['id', 'nome'],
            'vendas': ['cliente_id', 'produto', 'quantidade', 'preco_unitario', 'preco_final'],
            'enderecos': ['cliente_id', 'rua', 'bairro', 'cidade']
        }
        
        for file_type, file_path in files_dict.items():
            if file_path is None:
                if file_type in ['clientes', 'vendas']:  # Required
                    validation_results[file_type] = (False, "Required file not found")
                else:  # Optional
                    validation_results[file_type] = (True, "Optional file not found")
            else:
                validation_results[file_type] = self.validate_file_structure(
                    file_path, expected_columns[file_type]
                )
        
        return validation_results


class DataProcessor:
    """Class for data processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load CSV or XLSX file"""
        if not os.path.exists(file_path):
            return None
        
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                self.logger.error(f"Unsupported format: {file_path}")
                return None
        except Exception as e:
            self.logger.error(f"Error loading file {file_path}: {e}")
            return None
    
    def process_data(self, files_dict: Dict[str, Optional[str]]) -> Dict[str, any]:
        """
        Process file data and generate statistics
        
        Returns:
            Dict with processing results
        """
        results = {
            'success': False,
            'error_message': '',
            'statistics': {},
            'data_summary': {}
        }
        
        try:
            # Load required files
            clientes_df = self.load_file(files_dict['clientes'])
            vendas_df = self.load_file(files_dict['vendas'])
            
            if clientes_df is None or vendas_df is None:
                results['error_message'] = "Error loading required files"
                return results
            
            # Load optional file
            enderecos_df = None
            if files_dict['enderecos']:
                enderecos_df = self.load_file(files_dict['enderecos'])
            
            # Process data
            stats = self._calculate_statistics(clientes_df, vendas_df, enderecos_df)
            summary = self._generate_summary(clientes_df, vendas_df, enderecos_df)
            
            results['success'] = True
            results['statistics'] = stats
            results['data_summary'] = summary
            
        except Exception as e:
            results['error_message'] = f"Processing error: {str(e)}"
            self.logger.error(f"Data processing error: {e}")
        
        return results
    
    def _calculate_statistics(self, clientes_df: pd.DataFrame, 
                            vendas_df: pd.DataFrame, 
                            enderecos_df: Optional[pd.DataFrame]) -> Dict:
        """Calculate data statistics"""
        stats = {}
        
        # Basic statistics
        stats['total_clientes'] = len(clientes_df)
        stats['total_vendas'] = len(vendas_df)
        stats['total_enderecos'] = len(enderecos_df) if enderecos_df is not None else 0
        
        # Sales statistics
        stats['receita_total'] = vendas_df['preco_final'].sum()
        stats['ticket_medio'] = vendas_df['preco_final'].mean()
        stats['quantidade_total_produtos'] = vendas_df['quantidade'].sum()
        
        # Top products
        produtos_mais_vendidos = vendas_df.groupby('produto').agg({
            'quantidade': 'sum',
            'preco_final': 'sum'
        }).sort_values('quantidade', ascending=False).head(5)
        
        stats['top_produtos'] = produtos_mais_vendidos.to_dict('index')
        
        # Top customers
        clientes_vendas = vendas_df.groupby('cliente_id').agg({
            'preco_final': 'sum',
            'quantidade': 'sum'
        }).sort_values('preco_final', ascending=False).head(5)
        
        stats['top_clientes'] = clientes_vendas.to_dict('index')
        
        return stats
    
    def _generate_summary(self, clientes_df: pd.DataFrame,
                         vendas_df: pd.DataFrame,
                         enderecos_df: Optional[pd.DataFrame]) -> Dict:
        """Generate data summary"""
        summary = {}
        
        # Integrity validation
        clientes_ids = set(clientes_df['id'])
        vendas_cliente_ids = set(vendas_df['cliente_id'])
        
        # Customers without sales
        clientes_sem_vendas = clientes_ids - vendas_cliente_ids
        summary['clientes_sem_vendas'] = len(clientes_sem_vendas)
        
        # Sales with non-existent customer
        vendas_cliente_inexistente = vendas_cliente_ids - clientes_ids
        summary['vendas_cliente_inexistente'] = len(vendas_cliente_inexistente)
        
        # If addresses file exists, check coverage
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
        """Generate report text for resultado.txt"""
        from datetime import datetime
        
        report_lines = []
        report_lines.append("="*60)
        report_lines.append("SPREADSHEET ANALYSIS REPORT")
        report_lines.append("="*60)
        report_lines.append("")
        
        # Execution information
        report_lines.append("EXECUTION INFORMATION:")
        report_lines.append(f"Protocol: {protocolo}")
        report_lines.append(f"Department: {setor}")
        report_lines.append(f"Execution date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        report_lines.append(f"Source folder: {pasta_origem}")
        report_lines.append(f"Result file: {arquivo_resultado}")
        report_lines.append("")
        
        if not processing_results['success']:
            report_lines.append("PROCESSING ERROR:")
            report_lines.append(processing_results['error_message'])
            return "\n".join(report_lines)
        
        # General statistics
        stats = processing_results['statistics']
        report_lines.append("GENERAL STATISTICS:")
        report_lines.append(f"Total customers: {stats['total_clientes']:,}")
        report_lines.append(f"Total sales: {stats['total_vendas']:,}")
        report_lines.append(f"Total addresses: {stats['total_enderecos']:,}")
        report_lines.append(f"Total revenue: R$ {stats['receita_total']:,.2f}")
        report_lines.append(f"Average ticket: R$ {stats['ticket_medio']:,.2f}")
        report_lines.append(f"Total product quantity: {stats['quantidade_total_produtos']:,}")
        report_lines.append("")
        
        # Top products
        report_lines.append("TOP 5 BEST-SELLING PRODUCTS:")
        for produto, dados in stats['top_produtos'].items():
            report_lines.append(f"- {produto}: {dados['quantidade']:,} units, R$ {dados['preco_final']:,.2f}")
        report_lines.append("")
        
        # Top customers
        report_lines.append("TOP 5 CUSTOMERS (by revenue):")
        for cliente_id, dados in stats['top_clientes'].items():
            report_lines.append(f"- Customer {cliente_id}: R$ {dados['preco_final']:,.2f} ({dados['quantidade']:,} items)")
        report_lines.append("")
        
        # Integrity summary
        summary = processing_results['data_summary']
        report_lines.append("DATA INTEGRITY ANALYSIS:")
        report_lines.append(f"Customers without sales: {summary['clientes_sem_vendas']}")
        report_lines.append(f"Sales with non-existent customer: {summary['vendas_cliente_inexistente']}")
        report_lines.append(f"Customers without address: {summary['clientes_sem_endereco']}")
        report_lines.append(f"Address coverage: {summary['cobertura_enderecos']:.1f}%")
        report_lines.append("")
        
        report_lines.append("="*60)
        report_lines.append("Report generated by Sheetwise v1.0")
        report_lines.append("="*60)
        
        return "\n".join(report_lines)