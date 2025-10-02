# 🚀 Sistema de Release Automático - Sheetwise

## ✅ O que foi configurado

### 1. **Workflows de CD** (`.github/workflows/`)
   
   **A) Windows Build** (`cd_windows_workflow.yml`)
   - Executa automaticamente quando você cria uma **release** no GitHub
   - Usa máquina **Windows** no GitHub Actions
   - Instala Python 3.12 + Poetry + PyInstaller
   - Gera executável `Sheetwise_v1.exe`
   - Faz upload como artifact (90 dias)
   - **Anexa automaticamente** o `.exe` na release
   
   **B) Linux Build** (`cd_linux_workflow.yml`)
   - Executa automaticamente quando você cria uma **release** no GitHub
   - Usa máquina **Ubuntu 24.04** no GitHub Actions
   - Instala Python 3.12 + Poetry + PyInstaller
   - Gera executável `Sheetwise_v1` (Linux)
   - Faz upload como artifact (90 dias)
   - **Anexa automaticamente** o executável na release

### 2. **Documentação de Release**
   - `.github/RELEASE.md` - Instruções em português
   - `.github/RELEASE_EN.md` - Instruções em inglês
   - `.github/release-template.md` - Template para notas de release
   - `.github/release-drafter.yml` - Configuração para geração automática de notas

### 3. **README Atualizado**
   - Seção "Quick Start" para usuários Windows e Linux
   - Link direto para releases
   - Instruções sobre releases automatizadas

## 📝 Como criar uma nova release

### Método 1: GitHub Web (Recomendado)

1. Vá para o repositório no GitHub
2. Clique em **"Releases"** (menu direito)
3. Clique em **"Draft a new release"**
4. Preencha:
   ```
   Tag version: v1.0.0
   Release title: Sheetwise v1.0.0 - [Nome da Release]
   Description: 
   - ✨ Nova funcionalidade X
   - 🐛 Correção de bug Y
   - 📚 Documentação atualizada
   ```
5. Clique em **"Publish release"**

### Método 2: Via Git CLI

```bash
# Criar tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# Depois criar release no GitHub pela interface
```

## ⚙️ O que acontece automaticamente

Quando você cria uma release, **2 workflows são executados em paralelo**:

### 🪟 Windows Build
1. **GitHub Actions detecta** a criação da release
2. **Inicia VM Windows** no GitHub Actions
3. **Instala** Python 3.12, Poetry, dependências
4. **Executa** PyInstaller para gerar `Sheetwise_v1.exe`
5. **Verifica** se o arquivo foi gerado corretamente
6. **Faz upload** como artifact (backup por 90 dias)
7. **Anexa** o `.exe` na release automaticamente

### 🐧 Linux Build
1. **GitHub Actions detecta** a criação da release
2. **Inicia VM Ubuntu 24.04** no GitHub Actions
3. **Instala** dependências do sistema (python3-tk, python3-dev)
4. **Instala** Python 3.12, Poetry, dependências
5. **Executa** PyInstaller para gerar `Sheetwise_v1` (Linux)
6. **Verifica** se o arquivo foi gerado corretamente
7. **Faz upload** como artifact (backup por 90 dias)
8. **Anexa** o executável na release automaticamente

**Tempo total:** ~5-10 minutos

## 📦 Onde encontrar o executável

Após a release ser publicada e o workflow completar:

1. Vá para a página da release
2. Role até a seção **"Assets"**
3. Você verá:
   - ✅ `Source code (zip)`
   - ✅ `Source code (tar.gz)`
   - ✅ **`Sheetwise_v1.exe`** ← Executável Windows

## 🔍 Como verificar o status do build

1. Vá para **Actions** no repositório
2. Procure pelo workflow **"CD - Build and Release"**
3. Clique no workflow da sua release
4. Veja os logs de cada step:
   - ✅ Checkout code
   - ✅ Set up Python
   - ✅ Install Poetry
   - ✅ Install dependencies
   - ✅ Install PyInstaller
   - ✅ Build Windows executable
   - ✅ Verify executable
   - ✅ Upload to Release

## 🧪 Testar sem criar release

Para testar o workflow sem criar uma release real:

1. Vá para **Actions**
2. Selecione **"CD - Build and Release"**
3. Clique em **"Run workflow"**
4. Selecione branch `main`
5. Clique em **"Run workflow"**

O executável será gerado e disponibilizado como **artifact** (mas não anexado a nenhuma release).

## 📋 Versionamento recomendado

Use **Semantic Versioning** (`MAJOR.MINOR.PATCH`):

- **v1.0.0** - Primeira versão estável
- **v1.1.0** - Nova funcionalidade (compatível)
- **v1.1.1** - Correção de bug
- **v2.0.0** - Mudança incompatível (breaking change)

## 🔧 Troubleshooting

### ❌ Workflow não executou
**Solução:** Certifique-se de criar uma **release**, não apenas uma tag

### ❌ Build falhou
**Solução:** 
1. Veja os logs em Actions
2. Verifique se todas as dependências estão em `pyproject.toml`
3. Verifique se `assets/icon.ico` existe

### ❌ Executável não aparece
**Solução:**
1. Aguarde 5-10 minutos (tempo do build)
2. Recarregue a página da release
3. Verifique se o workflow completou com sucesso

## 📁 Arquivos criados/modificados

```
.github/
├── workflows/
│   └── cd_windows_workflow.yml           # Workflow principal de CD
├── RELEASE.md                     # Instruções em português
├── RELEASE_EN.md                  # Instruções em inglês
├── release-template.md            # Template de release
└── release-drafter.yml            # Config para draft automático

README.md                          # Atualizado com seção de releases
```

## 🎯 Próximos passos

1. **Teste o workflow:**
   ```bash
   # Crie uma release de teste
   git tag -a v0.1.0-beta -m "Test release"
   git push origin v0.1.0-beta
   # Depois crie release no GitHub
   ```

2. **Monitore o build** em Actions

3. **Baixe o executável** da release

4. **Teste o .exe** no Windows

5. **Crie a v1.0.0 oficial** quando estiver pronto!

## 📞 Suporte

- **Instruções completas:** [RELEASE_EN.md](.github/RELEASE_EN.md)
- **Workflow logs:** GitHub → Actions → CD - Build and Release
- **Template de release:** Use ao criar nova release

---

**✨ Pronto!** Agora sempre que você criar uma release, o executável Windows será gerado e disponibilizado automaticamente! 🎉
