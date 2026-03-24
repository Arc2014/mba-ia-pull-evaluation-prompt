"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        username = os.getenv("USERNAME_LANGSMITH_HUB", "")
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])

        full_prompt_name = f"{username}/{prompt_name}" if username else prompt_name

        print(f"   Fazendo push do prompt: {full_prompt_name}")
        hub.push(full_prompt_name, prompt, new_repo_is_public=True)

        print(f"   Prompt publicado com sucesso!")
        print(f"   URL: https://smith.langchain.com/hub/{username}/{prompt_name}")

        return True

    except Exception as e:
        print(f"   Erro ao fazer push do prompt '{prompt_name}': {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = ['system_prompt', 'user_prompt']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    system_prompt = prompt_data.get('system_prompt', '').strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    if '[TODO]' in system_prompt:
        errors.append("system_prompt contém [TODO] não resolvido")

    techniques = prompt_data.get('techniques_applied', [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    prompts_file = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompts_file)

    if not data:
        print(f"Erro ao carregar arquivo: {prompts_file}")
        return 1

    all_passed = True

    for prompt_name, prompt_data in data.items():
        print(f"\nProcessando prompt: {prompt_name}")

        is_valid, errors = validate_prompt(prompt_data)

        if not is_valid:
            print(f"   Prompt inválido:")
            for error in errors:
                print(f"   - {error}")
            all_passed = False
            continue

        print(f"   Validação OK")

        success = push_prompt_to_langsmith(prompt_name, prompt_data)

        if not success:
            all_passed = False

    if all_passed:
        print("\nTodos os prompts foram publicados com sucesso!")
        return 0
    else:
        print("\nAlguns prompts falharam ao ser publicados.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
