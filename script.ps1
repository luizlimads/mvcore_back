# --- CONFIGURAÇÕES ---
$Origem = "$env:USERPROFILE\Documents\mvcore\mvcore-api" # Define caminho de origem
$Destino = $PSScriptRoot # Define caminho atual (onde o script está rodando)
$NomeScript = $MyInvocation.MyCommand.Name # Nome deste arquivo script


Write-Host "--- INICIANDO PROCESSO ---" -ForegroundColor Cyan


# 1. VERIFICAÇÃO DE SEGURANÇA
if (!(Test-Path "$Origem")) {
    Write-Error "A pasta de origem '$Origem' não foi encontrada."
    exit
}


# 2. LIMPEZA (Preservando .git e o próprio script)
Write-Host "Limpando diretório atual (mantendo .git)..." -ForegroundColor Yellow
Get-ChildItem -Path $Destino -Exclude ".git", $NomeScript | Remove-Item -Recurse -Force



# 3. CÓPIA DOS ARQUIVOS
Write-Host "Copiando arquivos de '$Origem'..." -ForegroundColor Yellow
Copy-Item -Path "$Origem\*" -Destination $Destino -Recurse -Force


# 4. GIT AUTOMATION
Write-Host "Executando comandos GIT..." -ForegroundColor Green
# Add
git add .
$Data = Get-Date -Format "yyyy-MM-dd HH:mm:ss" # Commit (com timestamp para diferenciar)
# Commit
git commit -m "Auto-update: $Data"
# Push Force
Write-Host "Enviando para o repositório (FORCE)..." -ForegroundColor Red
git push origin main --force

Write-Host "--- CONCLUÍDO COM SUCESSO ---" -ForegroundColor Cyan
Pause