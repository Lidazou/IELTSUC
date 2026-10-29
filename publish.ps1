$ErrorActionPreference='Stop'
$repo='Lidazou/IELTSUC'
$gh=Get-Command gh -ErrorAction SilentlyContinue
if(-not $gh){throw 'Install GitHub CLI and run gh auth login first.'}
Set-Location $PSScriptRoot
& gh auth status
if($LASTEXITCODE -ne 0){throw 'Run gh auth login first.'}
& gh auth setup-git
if(-not (Test-Path '.git')){git init -b main}
git add --all
git diff --cached --quiet
if($LASTEXITCODE -ne 0){git commit -m 'Publish IELTSUC desktop companion and deployment documentation'}
& gh repo view $repo *> $null
if($LASTEXITCODE -ne 0){& gh repo create $repo --public --description 'IELTSUC · IELTS Success — 本地雅思陪考桌面应用与 Ollama AI 教练' --source . --remote origin}
if(-not (git remote get-url origin 2>$null)){git remote add origin "https://github.com/$repo.git"}
git push -u origin main
if($LASTEXITCODE -ne 0){throw 'Git push failed'}
$exe='dist/IELTSUC-1.3.1-win-x64.exe'
if(-not (Test-Path $exe)){throw 'Build EXE with npm run portable first.'}
$hash=(Get-FileHash $exe -Algorithm SHA256).Hash.ToLower()
"$hash  IELTSUC-1.3.1-win-x64.exe" | Set-Content dist/SHA256SUMS.txt -Encoding ascii
& gh release view v1.3.1 --repo $repo *> $null
if($LASTEXITCODE -ne 0){& gh release create v1.3.1 --repo $repo --target main --title 'IELTSUC 1.3.1 · Windows 公开版' --notes-file docs/RELEASE.md}
& gh release upload v1.3.1 --repo $repo $exe dist/SHA256SUMS.txt docs/DEPLOYMENT.md docs/VOCABULARY.md docs/OLLAMA.md --clobber
if($LASTEXITCODE -ne 0){throw 'Release upload failed'}
& gh release view v1.3.1 --repo $repo --json url,assets
