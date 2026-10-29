[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot "backend\.venv\Scripts\python.exe"
$frontendPath = Join-Path $projectRoot "frontend"

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "Ambiente Python ausente. Siga a preparacao em README_IMPLEMENTACAO_SPRINT1.md."
}
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot ".env") -PathType Leaf)) {
    throw "Copie .env.example para .env na raiz e configure o PostgreSQL local."
}
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw "Instale o Node.js com npm e abra novamente o terminal."
}
if (-not (Test-Path -LiteralPath (Join-Path $frontendPath "node_modules") -PathType Container)) {
    throw "Dependencias do frontend ausentes. Execute npm install na pasta frontend."
}

Push-Location -LiteralPath $frontendPath
try {
    Write-Host "Compilando a interface React..."
    & npm.cmd run build
    if ($LASTEXITCODE -ne 0) {
        throw "A compilacao do React falhou. O servidor nao foi iniciado."
    }
}
finally {
    Pop-Location
}

Push-Location -LiteralPath (Join-Path $projectRoot "backend")
try {
    Write-Host "Aplicando migracoes no PostgreSQL..."
    & $pythonPath manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        throw "As migracoes falharam. Confira o servico PostgreSQL e as variaveis DB_* no .env."
    }

    Write-Host "Feneme: http://localhost:8000 (Ctrl+C para encerrar)"
    & $pythonPath manage.py runserver
    if ($LASTEXITCODE -ne 0) {
        throw "O servidor Django foi encerrado com erro."
    }
}
finally {
    Pop-Location
}
