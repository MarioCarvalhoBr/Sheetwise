# 🎯 Sistema de Release Automático - Resumo Visual

## ✅ O que foi configurado

```
📁 .github/
├── 📄 workflows/cd_workflow.yml      → Workflow principal (Windows build)
├── 📄 RELEASE.md                      → Instruções em português
├── 📄 RELEASE_EN.md                   → Instruções em inglês  
├── 📄 RELEASE_SETUP.md                → Guia completo de configuração
├── 📄 RELEASE_EXAMPLE.md              → Exemplo prático de release
├── 📄 release-template.md             → Template para releases
└── 📄 release-drafter.yml             → Config de draft automático

📄 README.md                           → Atualizado com seção de releases
```

## 🔄 Fluxo Automático

```mermaid
graph LR
    A[Criar Release] --> B[GitHub Actions]
    B --> C[VM Windows]
    C --> D[Instalar Python]
    D --> E[Instalar Poetry]
    E --> F[Instalar Deps]
    F --> G[Build .exe]
    G --> H[Upload Artifact]
    H --> I[Anexar na Release]
    I --> J[Download Público]
```

## 🚀 Como usar (3 passos)

### 1️⃣ Criar Release no GitHub

```
🌐 GitHub → Releases → Draft a new release

📝 Preencher:
   Tag: v1.0.0
   Title: Sheetwise v1.0.0
   Description: [O que mudou]
   
🎯 Publish release
```

### 2️⃣ Aguardar Build (5-10 min)

```
⏳ GitHub Actions inicia automaticamente
🖥️  Máquina Windows configurada
📦 Poetry + dependências instaladas
🔨 PyInstaller gera Sheetwise_v1.exe
✅ Build completo
```

### 3️⃣ Download Disponível

```
📦 Release Assets:
   ✅ Source code (zip)
   ✅ Source code (tar.gz)
   ✅ Sheetwise_v1.exe  ← Executável Windows!
```

## 📊 Status do Workflow

Veja o progresso em **Actions**:

```
✅ Checkout code                    # Baixa código
✅ Set up Python                    # Python 3.12
✅ Install Poetry                   # Gerenciador
✅ Install dependencies             # pandas, tkinter, etc
✅ Install PyInstaller              # Gerador de .exe
✅ Build Windows executable         # Cria Sheetwise_v1.exe
✅ Verify executable                # Verifica arquivo
✅ Upload executable as artifact    # Backup 90 dias
✅ Upload to Release                # Anexa na release
```

## 🎨 Versões Recomendadas

```
v1.0.0 → Primeira versão estável
v1.1.0 → Nova funcionalidade
v1.1.1 → Correção de bug
v2.0.0 → Mudança incompatível
```

## 🧪 Teste Rápido

```bash
# 1. Criar tag de teste
git tag -a v0.1.0-beta -m "Test release"
git push origin v0.1.0-beta

# 2. Criar release no GitHub (web)

# 3. Aguardar build em Actions

# 4. Baixar .exe da release
```

## 📁 Onde está cada coisa

| Arquivo | Descrição |
|---------|-----------|
| `.github/workflows/cd_workflow.yml` | 🤖 Workflow principal |
| `.github/RELEASE_SETUP.md` | 📚 Guia completo (este arquivo) |
| `.github/RELEASE.md` | 🇧🇷 Instruções PT |
| `.github/RELEASE_EN.md` | 🇺🇸 Instruções EN |
| `.github/RELEASE_EXAMPLE.md` | 💡 Exemplo prático |
| `README.md` | 📖 Documentação principal |
| `scripts/build_windows.bat` | 🪟 Build local Windows |

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| ❌ Workflow não executou | Criar **release**, não só tag |
| ❌ Build falhou | Ver logs em Actions |
| ❌ .exe não aparece | Aguardar 5-10 min |
| ❌ Erro de dependência | Verificar `pyproject.toml` |
| ❌ Icon não encontrado | Verificar `assets/icon.ico` |

## 🎯 Checklist para Release

```
✅ Código testado e funcionando
✅ Version atualizada (se necessário)
✅ Changelog preparado
✅ Tag criada (vX.Y.Z)
✅ Release publicada no GitHub
✅ Workflow executado com sucesso
✅ Executável anexado na release
✅ Download testado
```

## 📞 Recursos

- 📚 [Guia Completo](.github/RELEASE_SETUP.md)
- 🇧🇷 [Instruções PT](.github/RELEASE.md)
- 🇺🇸 [Instructions EN](.github/RELEASE_EN.md)
- 💡 [Exemplo Prático](.github/RELEASE_EXAMPLE.md)
- 🤖 [Workflow](.github/workflows/cd_workflow.yml)

## 🎉 Pronto!

Agora sempre que você criar uma release:

1. ✨ GitHub Actions inicia automaticamente
2. 🪟 VM Windows faz o build
3. 📦 `Sheetwise_v1.exe` é gerado
4. 🚀 Executável anexado na release
5. 💾 Download público disponível!

**Sem esforço manual! Totalmente automatizado! 🤖✨**

---

**Criado por:** GitHub Copilot  
**Data:** 02/10/2025  
**Status:** ✅ Pronto para uso
