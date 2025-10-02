# 🎨 Migração para ttkbootstrap

## 📋 Resumo da Migração

Este documento descreve a migração completa de **ttkthemes** para **ttkbootstrap** no projeto Sheetwise.

## 🎯 Objetivos Alcançados

✅ **Substituição completa de ttkthemes por ttkbootstrap**
✅ **Remoção do sistema de dark mode** (agora cada tema é dark ou light)
✅ **Atualização do banco de dados** para armazenar apenas o tema
✅ **Simplificação da interface de configurações**
✅ **Atualização de todos os scripts de build**
✅ **Atualização de toda documentação**

---

## 🔄 Mudanças Principais

### 1. **Biblioteca de Interface Gráfica**

#### Antes (ttkthemes):
```python
from ttkthemes import ThemedTk
root = ThemedTk(theme="arc")
```

#### Depois (ttkbootstrap):
```python
import ttkbootstrap as ttk_boot
from ttkbootstrap import Window
root = Window(themename="cosmo")
```

---

### 2. **Sistema de Temas**

#### Antes:
- 5 temas básicos (arc, equilux, adapta, breeze, yaru)
- Sistema separado de dark mode (ON/OFF)
- Aplicação manual de cores dark mode

#### Depois:
- **18 temas ttkbootstrap** separados em:
  - **Light themes (13)**: cosmo, flatly, journal, litera, lumen, minty, pulse, sandstone, united, yeti, morph, simplex, cerculean
  - **Dark themes (5)**: solar, superhero, darkly, cyborg, vapor

---

### 3. **Banco de Dados**

#### Schema Antes:
```sql
CREATE TABLE configurations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    theme TEXT DEFAULT 'arc',
    language TEXT DEFAULT 'en',
    dark_mode INTEGER DEFAULT 0,  -- REMOVIDO
    last_updated TIMESTAMP
)
```

#### Schema Depois:
```sql
CREATE TABLE configurations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    theme TEXT DEFAULT 'cosmo',
    language TEXT DEFAULT 'en',
    last_updated TIMESTAMP
)
```

**Migração**: A coluna `dark_mode` foi removida. Agora o tema já define se é dark ou light.

---

### 4. **Interface de Configurações**

#### Antes:
- Seleção de tema (5 opções)
- Checkbox separado para Dark Mode
- Lógica complexa de aplicação de cores

#### Depois:
- Seleção de tema organizada por tipo:
  - **Light Themes** (13 opções)
  - **Dark Themes** (5 opções)
- Aplicação automática do tema pelo ttkbootstrap
- Código muito mais simples e limpo

---

### 5. **Arquivos Modificados**

#### Código Python:
- ✅ `src/models/database.py` - Schema e temas atualizados
- ✅ `src/views/login_view.py` - Import ttkbootstrap
- ✅ `src/views/main_view.py` - Import, temas, remoção dark mode
- ✅ `src/controllers/app_controller.py` - Remoção lógica dark mode

#### Scripts de Build:
- ✅ `scripts/build_linux.sh` - Removido ttkthemes
- ✅ `scripts/build_windows.bat` - Removido ttkthemes
- ✅ `.github/workflows/cd_linux_workflow.yml` - Removido ttkthemes
- ✅ `.github/workflows/cd_windows_workflow.yml` - Removido ttkthemes

#### Dependências:
- ✅ `pyproject.toml` - Removido ttkthemes, mantido apenas ttkbootstrap

#### Traduções:
- ✅ `src/static/i18n/en.json` - Removidas strings dark_mode
- ✅ `src/static/i18n/pt.json` - Removidas strings dark_mode

#### Documentação:
- ✅ `README.md` - Atualizado para ttkbootstrap
- ✅ Todos os arquivos `.md` - ttkthemes substituído por ttkbootstrap

---

## 🎨 Temas Disponíveis

### Light Themes:
1. **cosmo** (default) - Clean e moderno
2. **flatly** - Design plano e minimalista
3. **journal** - Estilo jornal
4. **litera** - Baseado no Bootstrap
5. **lumen** - Claro e limpo
6. **minty** - Verde menta
7. **pulse** - Roxo vibrante
8. **sandstone** - Terra/areia
9. **united** - Ubuntu-like
10. **yeti** - Azul claro
11. **morph** - Moderno gradiente
12. **simplex** - Simples e clean
13. **cerculean** - Azul oceano

### Dark Themes:
1. **solar** - Dark amarelado
2. **superhero** - Dark azul/laranja
3. **darkly** - Dark clássico
4. **cyborg** - Dark tech
5. **vapor** - Dark roxo/rosa

---

## 🚀 Como Usar os Novos Temas

### No Código:
```python
# Criar janela com tema específico
root = Window(themename="darkly")  # Tema dark
root = Window(themename="cosmo")   # Tema light

# Trocar tema dinamicamente
root.style.theme_use("superhero")
```

### Na Interface:
1. Abrir **Configurações** (⚙️)
2. Escolher tema na seção **Light Themes** ou **Dark Themes**
3. Clicar em **Save**
4. Tema aplicado imediatamente!

---

## 📦 Build do Executável

### Dependências Incluídas:
```bash
--hidden-import ttkbootstrap
--collect-all ttkbootstrap
```

### Dependências Removidas:
```bash
--hidden-import ttkthemes    # REMOVIDO
--collect-all ttkthemes      # REMOVIDO
```

---

## ⚠️ Breaking Changes

### Para usuários existentes:
1. **Configurações serão resetadas** na primeira execução após migração
2. **Tema padrão**: Será `cosmo` (light)
3. **Dark mode**: Removido - escolher tema dark diretamente
4. **Banco de dados**: Coluna `dark_mode` será ignorada (sem impacto)

### Para desenvolvedores:
1. Imports devem usar `ttkbootstrap` ao invés de `ttkthemes`
2. `ThemedTk` foi substituído por `Window`
3. Funções de dark mode foram removidas
4. Tema é aplicado via `root.style.theme_use()`

---

## 📈 Benefícios da Migração

### ✨ Para Usuários:
- 🎨 **18 temas** ao invés de 5
- 🌓 **5 temas dark** nativos
- 🚀 Aplicação **instantânea** de temas
- 🎯 Interface mais **limpa e moderna**

### 💻 Para Desenvolvedores:
- 📦 **Menos dependências** (removido ttkthemes)
- 🔧 **Código mais simples** (sem lógica dark mode manual)
- 🐛 **Menos bugs** (temas nativos bem testados)
- 📚 **Melhor documentação** (ttkbootstrap bem mantido)

---

## 🔍 Verificação Pós-Migração

Execute os seguintes testes:

```bash
# 1. Verificar imports
python -c "import ttkbootstrap; print('✅ ttkbootstrap OK')"

# 2. Testar aplicação
python src/main.py

# 3. Testar troca de temas
# Abrir app > Configurações > Selecionar tema > Salvar

# 4. Build executável
bash scripts/build_linux.sh
# ou
scripts/build_windows.bat
```

---

## 📝 Checklist de Migração

- [x] Atualizar imports Python
- [x] Modificar schema do banco de dados
- [x] Remover lógica de dark mode
- [x] Atualizar interface de configurações
- [x] Adicionar todos os temas ttkbootstrap
- [x] Atualizar scripts de build
- [x] Atualizar workflows CI/CD
- [x] Remover ttkthemes do pyproject.toml
- [x] Atualizar traduções (i18n)
- [x] Atualizar documentação
- [x] Testar todos os temas
- [x] Validar builds Windows/Linux

---

## 🆘 Troubleshooting

### Problema: Tema não aplica
**Solução**: Verificar se o nome do tema está correto (case-sensitive)

### Problema: Erro de import ttkbootstrap
**Solução**: 
```bash
pip install ttkbootstrap
# ou
poetry install
```

### Problema: Executável não abre
**Solução**: Verificar se `--collect-all ttkbootstrap` está nos parâmetros do PyInstaller

---

## 📅 Data da Migração

**Migração realizada em**: 02/10/2025

**Versão**: v1.0.0 (pós-migração)

---

## 👥 Responsáveis

- **Desenvolvedor**: Mario Carvalho
- **Ferramenta de Apoio**: GitHub Copilot

---

## 📚 Referências

- [ttkbootstrap Documentação](https://ttkbootstrap.readthedocs.io/)
- [ttkbootstrap Temas](https://ttkbootstrap.readthedocs.io/en/latest/themes/)
- [Migração de ttkthemes](https://github.com/israel-dryer/ttkbootstrap/discussions)

---

✨ **Migração concluída com sucesso!** ✨
