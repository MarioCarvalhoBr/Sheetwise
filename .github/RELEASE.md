# Release Instructions

## Como criar uma nova release

### 1. Via GitHub Web Interface (Recomendado)

1. Acesse a página do repositório no GitHub
2. Clique em **"Releases"** no menu lateral direito
3. Clique em **"Draft a new release"**
4. Preencha:
   - **Tag version**: Ex: `v1.0.0`, `v1.1.0`, `v2.0.0`
   - **Release title**: Ex: `Sheetwise v1.0.0`
   - **Description**: Descreva as mudanças da versão
5. Clique em **"Publish release"**

### 2. Via Git Command Line

```bash
# Criar e enviar tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Depois criar a release no GitHub pela interface web
```

## O que acontece automaticamente

Quando você criar uma release, o workflow de CD será executado automaticamente e irá:

1. ✅ Configurar ambiente Windows no GitHub Actions
2. ✅ Instalar Python 3.12
3. ✅ Instalar Poetry e todas as dependências
4. ✅ Instalar PyInstaller
5. ✅ Executar o build do executável Windows
6. ✅ Verificar se o arquivo `Sheetwise_v1.exe` foi gerado
7. ✅ Fazer upload do executável como artifact (disponível por 90 dias)
8. ✅ Anexar o executável à release para download público

## Download do executável

Após a release ser criada e o workflow concluído (cerca de 5-10 minutos):

1. Acesse a página da release no GitHub
2. Na seção **"Assets"**, você verá:
   - `Source code (zip)`
   - `Source code (tar.gz)`
   - **`Sheetwise_v1.exe`** ← Executável Windows pronto para download

## Verificar status do build

1. Acesse a aba **"Actions"** do repositório
2. Procure pelo workflow **"CD - Build and Release"**
3. Clique no workflow da sua release para ver os logs
4. Verifique se todos os steps foram concluídos com sucesso ✅

## Versionamento Semântico

Recomendamos usar [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (ex: `v1.2.3`)
- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs

Exemplos:
- `v1.0.0` - Primeira versão estável
- `v1.1.0` - Nova funcionalidade adicionada
- `v1.1.1` - Correção de bug
- `v2.0.0` - Mudança que quebra compatibilidade

## Troubleshooting

### Workflow não executou
- Verifique se criou uma **release**, não apenas uma tag
- Verifique em Actions se o workflow está habilitado

### Build falhou
- Acesse Actions → workflow com erro → logs detalhados
- Verifique se todas as dependências estão em `pyproject.toml`
- Verifique se o arquivo `assets/icon.ico` existe

### Executável não aparece na release
- Aguarde o workflow completar (5-10 minutos)
- Recarregue a página da release
- Verifique os logs do step "Upload to Release"

## Testar o workflow manualmente

Você pode testar o workflow sem criar uma release:

1. Acesse **Actions** no GitHub
2. Selecione **"CD - Build and Release"**
3. Clique em **"Run workflow"**
4. Selecione a branch `main`
5. Clique em **"Run workflow"**

O executável será gerado e disponibilizado como artifact (mas não anexado a nenhuma release).
