# ❓ Release System - FAQ

## Perguntas Frequentes sobre Releases

### 🤔 Como funciona o sistema de releases?

Quando você cria uma **release** no GitHub:
1. O GitHub Actions detecta automaticamente
2. Inicia uma máquina virtual Windows
3. Instala Python, Poetry e dependências
4. Executa PyInstaller para gerar `Sheetwise_v1.exe`
5. Faz upload do executável na release
6. Fica disponível para download público

**Tempo total:** 5-10 minutos ⏱️

---

### 📝 Qual a diferença entre Tag e Release?

- **Tag**: Apenas um marcador no Git (ex: `v1.0.0`)
- **Release**: Tag + página pública + assets anexados

**Para o workflow funcionar, você precisa criar uma RELEASE, não apenas uma tag!**

---

### 🪟 Por que só Windows?

O executável `.exe` só funciona em Windows. O workflow usa `runs-on: windows-latest` para garantir compatibilidade.

Para Linux/macOS, os usuários devem:
- Baixar o código fonte
- Instalar Python e dependências
- Rodar com `python src/main.py`

---

### 💰 Isso custa dinheiro?

**Não!** GitHub Actions é **gratuito** para repositórios públicos:
- 2000 minutos/mês grátis
- Cada build usa ~5-10 minutos
- Você pode fazer ~200-400 releases por mês gratuitamente

---

### 🔄 Posso editar uma release depois de criada?

**Sim!** Você pode:
- Editar descrição
- Adicionar/remover assets manualmente
- Mudar de draft para published

**Mas:** O workflow só executa quando a release é **criada** pela primeira vez.

---

### 🧪 Como testar sem criar release pública?

1. Vá em **Actions**
2. Selecione **"CD - Build and Release"**
3. Clique **"Run workflow"**
4. Escolha branch `main`
5. Execute

O executável será gerado como **artifact** (disponível por 90 dias), mas **não** será anexado a nenhuma release.

---

### 📦 O que são artifacts?

**Artifacts** são arquivos temporários salvos pelo GitHub Actions:
- Disponíveis por 90 dias
- Acessíveis apenas via Actions (não públicos)
- Úteis para debug e testes

O workflow cria 2 versões do executável:
1. **Artifact**: Backup temporário (90 dias)
2. **Release asset**: Download público permanente

---

### ❌ O workflow falhou. E agora?

1. Vá em **Actions** → workflow com erro
2. Clique no job **"Build Windows Executable"**
3. Veja qual step falhou
4. Leia os logs para identificar o erro

**Erros comuns:**
- `assets/icon.ico` não encontrado
- Dependência faltando em `pyproject.toml`
- Problema de permissão (token)

---

### 🔐 Preciso configurar tokens?

**Não!** O `GITHUB_TOKEN` é fornecido automaticamente pelo GitHub.

O workflow já está configurado com:
```yaml
permissions:
  contents: write  # Para anexar arquivo na release
```

---

### 📊 Posso ver o tamanho do executável?

**Sim!** No workflow, o step "Verify executable" mostra:
```
✅ Executable built successfully!
File size: 123456789 bytes
```

Tamanho esperado: **~80-150 MB** (PyInstaller empacota Python + todas as libs)

---

### 🚀 Posso usar em repositório privado?

**Sim**, mas tem limitações:
- GitHub Free: 2000 minutos/mês
- GitHub Pro: 3000 minutos/mês

Windows usa multiplicador de **2x** nos minutos:
- 10 min de build = 20 min consumidos

---

### 🔄 Posso fazer rollback de uma release?

**Sim!** Você pode:
1. Deletar a release ruim
2. Criar nova release apontando para commit anterior
3. O workflow gerará novo executável automaticamente

```bash
# Exemplo: voltar para v1.0.0
git tag -a v1.0.1-fix -m "Fix release" <commit-hash-antigo>
git push origin v1.0.1-fix
# Criar release no GitHub
```

---

### 📝 Posso personalizar o nome do executável?

**Sim!** No workflow, altere:
```yaml
--name "Sheetwise_v1"  # Mude aqui
```

Para nome com versão dinâmica:
```yaml
--name "Sheetwise_${{ github.ref_name }}"
```

---

### 🐛 E se o executável não funcionar no Windows?

Possíveis causas:
1. **Antivírus bloqueou**: Adicione exceção
2. **DLL faltando**: PyInstaller deve incluir tudo
3. **Versão Windows antiga**: Requer Windows 10+

**Debug:**
- Execute via terminal: `Sheetwise_v1.exe` (ver erros)
- Teste em máquina virtual Windows
- Verifique logs do PyInstaller no workflow

---

### 📈 Posso ver histórico de releases?

**Sim!** Em:
- `github.com/MarioCarvalhoBr/Sheetwise/releases` - Todas as releases
- `github.com/MarioCarvalhoBr/Sheetwise/actions` - Todos os builds

---

### 🔔 Posso receber notificação quando build completar?

**Sim!** Configure em:
1. GitHub → Settings → Notifications
2. Marque **"Actions"**
3. Escolha email ou app

Ou use **GitHub Mobile** para notificações push.

---

### 🌍 Posso gerar executável para Linux também?

**Sim!** Adicione outro job no workflow:

```yaml
build-linux:
  runs-on: ubuntu-latest
  steps:
    # Similar ao Windows, mas com PyInstaller para Linux
```

**Mas:** Executável Linux só funciona em Linux (não é universal).

---

### 💡 Outras perguntas?

- 📚 Veja [RELEASE_SETUP.md](.github/RELEASE_SETUP.md) - Guia completo
- 💡 Veja [RELEASE_EXAMPLE.md](.github/RELEASE_EXAMPLE.md) - Exemplo prático
- 🇧🇷 Veja [RELEASE.md](.github/RELEASE.md) - Instruções em português
- 🇺🇸 Veja [RELEASE_EN.md](.github/RELEASE_EN.md) - English instructions

---

**Última atualização:** 02/10/2025
