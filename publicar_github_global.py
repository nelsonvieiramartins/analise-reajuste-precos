import os
import json
import subprocess
import sys

CONFIG_FILE = ".github_config.json"

def run_command(cmd, cwd=None):
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True, 
        cwd=cwd,
        encoding='utf-8',
        errors='replace'
    )
    return result.returncode, result.stdout, result.stderr

def load_config(cwd):
    config_path = os.path.join(cwd, CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(cwd, config):
    config_path = os.path.join(cwd, CONFIG_FILE)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def is_git_initialized(cwd):
    return os.path.exists(os.path.join(cwd, ".git"))

def init_git(cwd):
    print(f"Inicializando repositório Git em: {cwd}")
    returncode, stdout, stderr = run_command("git init", cwd=cwd)
    if returncode != 0:
        print(f"Erro ao inicializar git: {stderr}")
        return False
    run_command('git config user.email "nelsonvieiramartins@email.com"', cwd=cwd)
    run_command('git config user.name "Nelson Vieira Martins"', cwd=cwd)
    print("Repositório Git inicializado!")
    return True

def get_files_to_commit(cwd):
    returncode, stdout, stderr = run_command("git status --porcelain", cwd=cwd)
    if returncode != 0:
        return []
    files = [line[3:] for line in stdout.strip().split('\n') if line.strip()]
    return files

def commit_changes(cwd, message=None):
    files = get_files_to_commit(cwd)
    if not files:
        print("Não há alterações para commit.")
        return True
    
    if message is None:
        message = f"Atualização automática - {len(files)} arquivo(s)"
    
    for f in files:
        run_command(f'git add "{f}"', cwd=cwd)
    
    returncode, stdout, stderr = run_command(f'git commit -m "{message}"', cwd=cwd)
    if returncode != 0:
        print(f"Erro ao fazer commit: {stderr}")
        return False
    print(f"Commit: {message}")
    return True

def check_remote_exists(cwd):
    returncode, stdout, stderr = run_command("git remote -v", cwd=cwd)
    return "origin" in stdout

def create_github_repo(cwd, repo_name):
    print("\n" + "=" * 50)
    print("CRIANDO REPOSITÓRIO NO GITHUB")
    print("=" * 50)
    print("Você será solicitado a fazer login no GitHub.")
    print("Nota: Se gh não estiver instalado, use o VS Code:")
    print("  1. Abra a pasta no VS Code")
    print("  2. Ctrl+Shift+G > Publish to GitHub")
    print("")
    
    returncode, stdout, stderr = run_command(
        f'gh repo create {repo_name} --public --source="{cwd}" --description "Projeto automaticamente"',
        cwd=cwd
    )
    
    if returncode != 0:
        print(f"Aviso: {stderr}")
        print("\nPara continuar manualmente no VS Code:")
        print(f"  1. Abra: {cwd}")
        print("  2. Ctrl+Shift+G > Initialize Repository")
        print("  3. Publish to GitHub")
        return False
    
    print(f"Repositório criado!")
    return True

def push_to_github(cwd):
    for branch in ["main", "master"]:
        returncode, stdout, stderr = run_command(f"git push -u origin {branch}", cwd=cwd)
        if returncode == 0:
            print("Push realizado!")
            return True
    print(f"Erro ao fazer push: {stderr}")
    return False

def update_github(cwd):
    if not commit_changes(cwd):
        return False
    if not push_to_github(cwd):
        return False
    return True

def get_repo_name(path):
    folder_name = os.path.basename(path)
    repo_name = folder_name.lower().replace(" ", "-").replace("_", "-")
    repo_name = ''.join(c for c in repo_name if c.isalnum() or c == '-')
    return repo_name

def main():
    print("=" * 60)
    print("  PUBLICAR NO GITHUB - Script Global")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        cwd = os.getcwd()
    else:
        cwd = sys.argv[1]
    
    cwd = os.path.abspath(cwd)
    print(f"Diretório: {cwd}")
    
    config = load_config(cwd)
    repo_name = config.get("repo_name") or get_repo_name(cwd)
    
    if not is_git_initialized(cwd):
        print("\nRepositório Git não encontrado.")
        init_git(cwd)
    
    if not check_remote_exists(cwd):
        print("\nRepositório GitHub não configurado.")
        if create_github_repo(cwd, repo_name):
            commit_changes(cwd, "Primeiro commit - Initial")
            push_to_github(cwd)
            config["published"] = True
            config["repo_name"] = repo_name
            save_config(cwd, config)
            print("\n" + "=" * 50)
            print(f"PRIMEIRA PUBLICAÇÃO CONCLUÍDA!")
            print(f"https://github.com/nelsonvieiramartins/{repo_name}")
            print("=" * 50)
    else:
        print("\nAtualizando repositório...")
        update_github(cwd)
    
    print("\nPara atualizar novamente, rode:")
    print(f"  python publicar_github_global.py \"{cwd}\"")
    print("Ou apenas clique no atalho que vamos criar!")

if __name__ == "__main__":
    main()
