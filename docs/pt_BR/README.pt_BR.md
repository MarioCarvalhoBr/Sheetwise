# Sheetwise

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/Package%20Manager-Poetry-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![i18n](https://img.shields.io/badge/i18n-PT%20%7C%20EN-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descrição

Sheetwise é um software desktop desenvolvido em Python com interface gráfica moderna usando Tkinter. O sistema permite analisar planilhas CSV/XLSX contendo dados de clientes e vendas, gerando relatórios detalhados com estatísticas e análises de integridade dos dados.

### 🌍 Internacionalização (i18n)

- **Português** (padrão)
- **English** (completo)
- Sistema de configurações para troca de idioma em tempo real

### 🚀 Principais Funcionalidades

- **Interface Gráfica Moderna**: Design limpo e intuitivo usando temas ttk
- **Sistema de Configurações**: Temas, idiomas e modo escuro
- **Internacionalização**: Suporte completo para Português e Inglês
- **Janela Inteligente**: Tamanho inicial com 80% da tela (10% padding lateral) + botão maximizar
- **Atalhos de Teclado**: F11, Ctrl+M para maximizar/restaurar, ESC para restaurar
- **Suporte Multi-formato**: Aceita arquivos CSV e XLSX
- **Cadastro de Usuários**: Sistema de login/cadastro com SQLite
- **CRUD de Execuções**: Gerenciamento completo do histórico de análises
- **Validação de Dados**: Verificação automática da estrutura dos arquivos
- **Relatórios Detalhados**: Geração de relatórios com estatísticas completas
- **Executável Windows**: Geração de .exe standalone com todas as dependências
- **Gerenciamento com Poetry**: Dependências e ambientes virtuais modernos

## 📁 Estrutura do Projeto


```bash
Sheetwise/
├── main.py                      # Arquivo principal do aplicativo
├── pyproject.toml               # Configuração Poetry
├── poetry.lock                  # Lock file das dependências
├── requirements.txt             # Dependências Python (legado)
├── setup_poetry.sh              # Script de configuração Poetry
├── build_exe_poetry.sh          # Script para gerar executável
├── README.md                    # Documentação do projeto
├── .venv/                       # Ambiente virtual Poetry
├── 
├── src/                         # Código fonte
│   ├── models/                  # Modelos de dados
│   │   ├── __init__.py
│   │   └── database.py          # Gerenciador SQLite + Models
│   ├── views/                   # Interfaces gráficas
│   │   ├── __init__.py
│   │   ├── login_view.py        # Tela de login/cadastro
│   │   └── main_view.py         # Tela principal
│   ├── controllers/             # Controladores
│   │   ├── __init__.py
│   │   └── app_controller.py    # Controlador principal
│   ├── utils/                   # Utilitários
│   │   ├── __init__.py
│   │   ├── file_processor.py    # Processamento de arquivos
│   │   └── i18n_manager.py      # Gerenciador de traduções
│   └── static/                  # Recursos estáticos
│       └── i18n/                # Arquivos de tradução
│           ├── pt.json          # Traduções em português
│           └── en.json          # Traduções em inglês
├── 
├── database/                    # Banco de dados SQLite
├── assets/                      # Recursos (ícones, imagens)
├── tests/                       # Testes unitários
└── docs/                        # Documentação adicional
```

## � Instalação e Configuração

### 1. Pré-requisitos

- Python 3.8+ instalado no sistema
- Poetry instalado ([instruções](https://python-poetry.org/docs/#installation))
- Ubuntu 24.04 ou sistema Linux compatível
- 4GB RAM mínimo
- 1GB espaço em disco

### 2. Instalação com Poetry (Recomendado)

```bash
# Clonar o repositório (ou extrair ZIP)
cd Sheetwise

# Configurar e instalar dependências automaticamente
python3 -m venv .venv
source .venv/bin/activate

pip install poetry

# Verificar Poetry instalado
poetry --version

# Instalar dependências
poetry install
```

### 4. Executar o Aplicativo

#### Com Poetry (Recomendado)
```bash
# Opção 1: Executar diretamente
poetry run python main.py

# Opção 2: Ativar shell e executar
poetry shell
python main.py
```

#### Método Legado (venv tradicional)
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar aplicativo
python main.py
```

## 📊 Formato dos Arquivos de Entrada

O sistema espera encontrar os seguintes arquivos na pasta selecionada:

### Arquivos Obrigatórios

#### 1. clientes.csv/xlsx
```csv
id,nome
1,João Silva
2,Maria Santos
3,Pedro Costa
```

#### 2. vendas.csv/xlsx
```csv
cliente_id,produto,quantidade,preco_unitario,preco_final
1,Notebook,1,2500.00,2500.00
2,Mouse,2,50.00,100.00
3,Teclado,1,150.00,150.00
```

### Arquivo Opcional

#### 3. enderecos.csv/xlsx
```csv
cliente_id,rua,bairro,cidade
1,Rua A 123,Centro,São Paulo
2,Av B 456,Jardins,São Paulo
```

## 🎯 Como Usar

### 1. Controles de Janela
- **Tamanho Inicial**: A janela inicia com 80% do tamanho da tela, centralizada
- **Botão Maximizar**: Clique no botão 🗖 no canto superior direito
- **Atalhos de Teclado**:
  - `F11` - Maximizar/Restaurar janela
  - `Ctrl+M` - Maximizar/Restaurar janela
  - `ESC` - Restaurar janela (quando maximizada)
- **Tooltip**: Passe o mouse sobre o botão maximizar para ver as opções

### 2. Primeiro Acesso
1. Execute o aplicativo
2. Cadastre-se com nome e email
3. Ou faça login se já tiver cadastro

### 3. Realizar Análise
1. Clique em "Selecionar Pasta" e escolha a pasta com os arquivos
2. Verifique se todos os arquivos obrigatórios foram encontrados (✅)
3. Preencha o protocolo e setor
4. Selecione onde salvar o arquivo resultado.txt
5. Clique em "ANALISAR"
6. Confirme a operação

### 4. Visualizar Resultados
- O arquivo resultado.txt será gerado com todas as estatísticas
- A execução ficará salva no histórico
- Você pode visualizar/deletar execuções antigas

## 🏗️ Gerando Executável para Windows

### Requisitos
- PyInstaller instalado (incluído no requirements.txt)
- Todos os arquivos do projeto

### Processo Automático

#### Com Poetry (Recomendado)
```bash
# Executar script de build Poetry
chmod +x build_exe_poetry.sh
poetry run ./build_exe_poetry.sh
```

#### Método Direto com Poetry
```bash
# Gerar executável usando Poetry
poetry run pyinstaller \
    --name="Sheetwise_v1" \
    --onefile \
    --windowed \
    --icon="assets/icon.ico" \
    --add-data="src:src" \
    --add-data="database:database" \
    --hidden-import="pandas" \
    --hidden-import="openpyxl" \
    --hidden-import="ttkbootstrap" \
    --hidden-import="PIL" \
    --hidden-import="sqlite3" \
    main.py
```

#### Método Legado
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar script de build legado
chmod +x build_exe.sh
./build_exe.sh
```

### Resultado
- O executável `Sheetwise_v1.exe` será criado na pasta `dist/`
- Este arquivo contém todas as dependências necessárias
- Pode ser executado em qualquer Windows sem instalações adicionais
- **Tamanho aproximado**: 80-120MB (com todas as dependências)

## 📈 Funcionalidades do Relatório

O arquivo resultado.txt gerado contém:

### Informações da Execução
- Protocolo e setor
- Data/hora da execução
- Caminhos dos arquivos

### Estatísticas Gerais
- Total de clientes, vendas e endereços
- Receita total e ticket médio
- Quantidade total de produtos vendidos

### Top Rankings
- Top 5 produtos mais vendidos
- Top 5 clientes por receita

### Análise de Integridade
- Clientes sem vendas
- Vendas com cliente inexistente
- Cobertura de endereços
- Clientes sem endereço cadastrado

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Poetry**: Gerenciamento de dependências e ambientes virtuais
- **Tkinter + ttkbootstrap**: Interface gráfica moderna
- **SQLite**: Banco de dados embutido
- **Pandas**: Processamento de dados
- **OpenPyXL**: Suporte a arquivos Excel
- **PyInstaller**: Geração de executável
- **Pillow**: Processamento de imagens
- **Sistema i18n**: Internacionalização completa

## 🔒 Arquitetura do Software

### Padrão MVC
- **Models**: Gerenciamento de dados (SQLite)
- **Views**: Interfaces gráficas (Tkinter)
- **Controllers**: Lógica de negócio

### Clean Code
- Código modular e organizado
- Separação de responsabilidades
- Documentação completa
- Tratamento de erros robusto

## 🐛 Resolução de Problemas

### Erro: "Módulo não encontrado"

#### Com Poetry (Recomendado)
```bash
# Verificar ambiente virtual
poetry env info

# Reinstalar dependências
poetry install

# Executar aplicativo
poetry run python main.py
```

#### Método Legado
```bash
# Verifique se o ambiente virtual está ativo
source .venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: Poetry não encontrado
```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"

# Verificar instalação
poetry --version
```

### Erro: "Arquivo não encontrado"
- Verifique se os arquivos CSV/XLSX estão na pasta correta
- Confirme se os nomes dos arquivos seguem o padrão: clientes.csv, vendas.csv, enderecos.csv

### Erro na Geração do Executável
```bash
# Limpe arquivos temporários
rm -rf build/ dist/ *.spec

# Com Poetry
poetry run ./build_exe_poetry.sh

# Execute novamente o build
poetry run ./build_exe_poetry.sh
```

## 📦 Comandos Poetry Úteis

### Gerenciamento de Dependências
```bash
# Adicionar nova dependência
poetry add <package>

# Adicionar dependência de desenvolvimento
poetry add --group dev <package>

# Remover dependência
poetry remove <package>

# Atualizar dependências
poetry update

# Listar dependências
poetry show
```

### Ambiente Virtual
```bash
# Ativar shell do Poetry
poetry shell

# Executar comando no ambiente
poetry run <command>

# Mostrar informações do ambiente
poetry env info

# Limpar cache do Poetry
poetry cache clear pypi --all
```

### Build e Distribuição
```bash
# Executar aplicativo
poetry run python main.py

# Gerar executável
poetry run ./build_exe_poetry.sh

# Executar testes (se configurados)
poetry run pytest
```

## 📝 Logs e Debugging

- Logs são salvos automaticamente em `analisa_planilhas.log`
- Nível de log configurável (INFO por padrão)
- Rastreamento completo de erros e operações

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ usando Python e Tkinter

---

### 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de resolução de problemas
2. Consulte os logs em `analisa_planilhas.log`
3. Abra uma issue no repositório do projeto

### 🔄 Versões

- **v1.0**: Versão inicial com todas as funcionalidades principais
  - Suporte a CSV e XLSX
  - Interface gráfica moderna
  - Geração de executável Windows
  - **Sistema i18n completo** (Português/English)
  - **Gerenciamento com Poetry**
  - **Interface de configurações** (temas, idiomas, dark mode)
  - **Banco de dados expandido** com configurações persistentes
  - **Código totalmente em inglês** com documentação atualizada

---

**Sheetwise v1.0** - Sistema de Análise de Planilhas Profissional