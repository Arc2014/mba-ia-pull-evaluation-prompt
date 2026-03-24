"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull dos prompts do LangSmith Hub e salva localmente.

    Returns:
        True se sucesso, False caso contrário
    """
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    try:
        print("Puxando prompt 'leonanluppi/bug_to_user_story_v1' do LangSmith Hub...")
        prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
        print("   Prompt carregado com sucesso")

        system_prompt = ""
        user_prompt = ""

        for message in prompt.messages:
            if isinstance(message, SystemMessagePromptTemplate):
                system_prompt = message.prompt.template
            elif isinstance(message, HumanMessagePromptTemplate):
                user_prompt = message.prompt.template

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }

        raw_path = "prompts/raw_prompts.yml"
        v1_path = "prompts/bug_to_user_story_v1.yml"

        saved_raw = save_yaml(prompt_data, raw_path)
        saved_v1 = save_yaml(prompt_data, v1_path)

        if saved_raw:
            print(f"   Salvo em: {raw_path}")
        if saved_v1:
            print(f"   Salvo em: {v1_path}")

        return saved_raw and saved_v1

    except Exception as e:
        print(f"Erro ao puxar prompt do LangSmith: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    success = pull_prompts_from_langsmith()

    if success:
        print("\nPrompts salvos com sucesso!")
        print("Arquivos gerados:")
        print("  - prompts/raw_prompts.yml")
        print("  - prompts/bug_to_user_story_v1.yml")
        return 0
    else:
        print("\nFalha ao puxar prompts do LangSmith.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
