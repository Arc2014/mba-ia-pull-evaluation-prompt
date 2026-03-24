"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_v2_prompt():
    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get("bug_to_user_story_v2", {})

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = load_v2_prompt()
        assert "system_prompt" in prompt
        assert isinstance(prompt["system_prompt"], str)
        assert len(prompt["system_prompt"].strip()) > 100

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt = load_v2_prompt()
        system_prompt = prompt.get("system_prompt", "")
        role_keywords = ["Você é", "Product Manager", "especialista", "especializado", "experiência"]
        assert any(kw in system_prompt for kw in role_keywords), \
            f"Prompt deve definir uma persona. Palavras-chave esperadas: {role_keywords}"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt = load_v2_prompt()
        system_prompt = prompt.get("system_prompt", "")
        format_keywords = ["Markdown", "User Story", "Como um", "eu quero", "para que"]
        assert any(kw in system_prompt for kw in format_keywords), \
            f"Prompt deve mencionar formato. Palavras-chave esperadas: {format_keywords}"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt = load_v2_prompt()
        system_prompt = prompt.get("system_prompt", "")
        few_shot_keywords = ["Exemplo", "EXEMPLO", "Input:", "Output:", "Bug:"]
        assert any(kw in system_prompt for kw in few_shot_keywords), \
            "Prompt deve conter exemplos de entrada/saída (Few-shot)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = load_v2_prompt()
        system_prompt = prompt.get("system_prompt", "")
        user_prompt = prompt.get("user_prompt", "")
        assert "[TODO]" not in system_prompt, "system_prompt contém [TODO] não resolvido"
        assert "[TODO]" not in user_prompt, "user_prompt contém [TODO] não resolvido"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt = load_v2_prompt()
        techniques = prompt.get("techniques_applied", [])
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, \
            f"Mínimo 2 técnicas requeridas, encontradas: {len(techniques)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
