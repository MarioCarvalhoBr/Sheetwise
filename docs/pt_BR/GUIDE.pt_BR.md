# Guia de Uso - Sheetwise

## Instalação Rápida

1. **Configurar Ambiente:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Executar Aplicativo:**
   ```bash
   source venv/bin/activate
   python main.py
   ```

3. **Testar Funcionalidades:**
   ```bash
   python test_features.py
   ```

## Novos Recursos v1.1

- **🖥️ Janela Inteligente**: Inicia com 80% da tela (10% padding)
- **🗖 Botão Maximizar**: No canto superior direito
- **⌨️ Atalhos**: F11, Ctrl+M para maximizar, ESC para restaurar
- **💡 Tooltips**: Dicas ao passar o mouse

## Gerar Executável Windows

```bash
chmod +x build_exe.sh
./build_exe.sh
```

O arquivo `Sheetwise_v1.exe` será criado em `dist/`

## Arquivos de Exemplo

Na pasta `docs/exemplos/` você encontra arquivos de teste:
- `clientes.csv` - Dados de clientes
- `vendas.csv` - Dados de vendas  
- `enderecos.csv` - Endereços (opcional)

## Estrutura dos Dados

### clientes.csv/xlsx
- `id`: ID único do cliente
- `nome`: Nome completo do cliente

### vendas.csv/xlsx  
- `cliente_id`: Referência ao ID do cliente
- `produto`: Nome do produto
- `quantidade`: Quantidade vendida
- `preco_unitario`: Preço por unidade
- `preco_final`: Valor total da venda

### enderecos.csv/xlsx (opcional)
- `cliente_id`: Referência ao ID do cliente
- `rua`: Endereço completo
- `bairro`: Bairro
- `cidade`: Cidade

## Troubleshooting

### Problema: Erro ao executar
**Solução:** Verifique se o ambiente virtual está ativo
```bash
source venv/bin/activate
```

### Problema: Módulo não encontrado
**Solução:** Reinstale as dependências
```bash
pip install -r requirements.txt
```

### Problema: Arquivos não encontrados
**Solução:** Verifique se os nomes dos arquivos estão corretos:
- clientes.csv ou clientes.xlsx
- vendas.csv ou vendas.xlsx
- enderecos.csv ou enderecos.xlsx (opcional)