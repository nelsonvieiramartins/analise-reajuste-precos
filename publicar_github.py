import os
import json
import subprocess
import sys

CONFIG_FILE = ".github_config.json"
REPO_NAME = "analise-reajuste-precos"

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

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def is_git_initialized():
    return os.path.exists(".git")

def init_git():
    print("Inicializando repositório Git...")
    returncode, stdout, stderr = run_command("git init")
    if returncode != 0:
        print(f"Erro ao inicializar git: {stderr}")
        return False
    print("Repositório Git inicializado com sucesso!")
    return True

def configure_git_user():
    run_command('git config user.email "nelsonvieiramartins@email.com"')
    run_command('git config user.name "Nelson Vieira Martins"')

def get_files_to_commit():
    returncode, stdout, stderr = run_command("git status --porcelain")
    if returncode != 0:
        return []
    files = [line[3:] for line in stdout.strip().split('\n') if line.strip()]
    return files

def commit_changes(message=None):
    files = get_files_to_commit()
    if not files:
        print("Não há alterações para commit.")
        return True
    
    if message is None:
        message = f"Atualização automática - {len(files)} arquivo(s) modificado(s)"
    
    print(f"Arquivos alterados: {files}")
    print(f"Mensagem: {message}")
    
    for f in files:
        run_command(f'git add "{f}"')
    
    returncode, stdout, stderr = run_command(f'git commit -m "{message}"')
    if returncode != 0:
        print(f"Erro ao fazer commit: {stderr}")
        return False
    print("Commit realizado com sucesso!")
    return True

def check_remote_exists():
    returncode, stdout, stderr = run_command("git remote -v")
    return "origin" in stdout

def create_github_repo():
    print("\n=== PRIMEIRA VEZ: Criando repositório no GitHub ===")
    print("Você será solicitado a fazer login no GitHub via navegador.")
    
    returncode, stdout, stderr = run_command(f'gh repo create {REPO_NAME} --public --source=. --description "Análise de Reajuste de Preços - Projeto de controle de receitas e despesas"')
    
    if returncode != 0:
        print(f"Erro ao criar repositório (gh pode não estar instalado): {stderr}")
        print("\nAlternativa: Use o VS Code para publicar:")
        print("1. Abra o VS Code neste diretório")
        print("2. Vá para Source Control (Ctrl+Shift+G)")
        print("3. Clique em 'Publish to GitHub'")
        print("4. Siga as instruções na tela")
        return False
    
    print(f"Repositório criado com sucesso: https://github.com/nelsonvieiramartins/{REPO_NAME}")
    return True

def push_to_github():
    returncode, stdout, stderr = run_command("git push -u origin main")
    if returncode != 0:
        returncode, stdout, stderr = run_command("git push -u origin master")
        if returncode != 0:
            print(f"Erro ao fazer push: {stderr}")
            return False
    print("Push realizado com sucesso!")
    return True

def update_github():
    if not commit_changes():
        return False
    
    if not push_to_github():
        return False
    
    print("\n=== Repositório atualizado com sucesso! ===")
    print(f"Veja em: https://github.com/nelsonvieiramartins/{REPO_NAME}")
    return True

def main():
    print("=" * 60)
    print("  PUBLICAR NO GITHUB - Análise Reajuste de Preços")
    print("=" * 60)
    
    config = load_config()
    repo_published = config.get("published", False)
    
    if not is_git_initialized():
        print("\nRepositório Git não encontrado. Inicializando...")
        if not init_git():
            return
        configure_git_user()
    
    if not check_remote_exists():
        print("\nRepositório GitHub não configurado.")
        if not create_github_repo():
            return
        
        config["published"] = True
        config["repo_name"] = REPO_NAME
        save_config(config)
        
        commit_changes("Primeiro commit - Initial")
        push_to_github()
        
        print("\n=== PRIMEIRA PUBLICAÇÃO CONCLUÍDA! ===")
        print(f"Repositório: https://github.com/nelsonvieiramartins/{REPO_NAME}")
    else:
        print("\nRepositório já configurado. Atualizando...")
        update_github()
    
    print("\nPara próximas atualizações, basta rodar este mesmo script!")
    print("python publicar_github.py")

if __name__ == "__main__":
    main()
