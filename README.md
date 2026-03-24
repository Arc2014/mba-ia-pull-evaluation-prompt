# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v1a
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
================================
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v2_optimized
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/raw_prompts.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/desafio-prompt-engineer/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com ≥ 20 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Tecnicas Aplicadas (Fase 2)

### 1. Role Prompting

**O que e:** Definir uma persona especialista para o modelo, fornecendo contexto profissional e expertise.

**Por que escolhi:** O prompt v1 usava uma persona generica ("Voce e um assistente"). Ao definir o modelo como um "Product Manager Senior com 10 anos de experiencia em metodologias ageis", as respostas passaram a ter tom profissional, vocabulario adequado e foco em valor de negocio — exatamente o que as metricas de Tone e Format exigiam.

**Como apliquei:** No inicio do system_prompt, defini a persona completa:
> "Voce e um Product Manager Senior com 10 anos de experiencia em metodologias ageis (Scrum/Kanban). Sua especialidade e transformar relatos tecnicos em User Stories centradas no usuario."

### 2. Few-shot Learning

**O que e:** Fornecer exemplos concretos de entrada/saida para o modelo aprender o padrao esperado.

**Por que escolhi:** A metrica de Acceptance Criteria Score e User Story Format Score exigiam formato muito especifico (Given-When-Then, "Como um... eu quero... para que..."). Sem exemplos, o modelo produzia formatos inconsistentes. Com 3 exemplos cobrindo diferentes niveis de complexidade, o modelo passou a replicar o formato com alta fidelidade.

**Como apliquei:** Inclui 3 exemplos completos no system_prompt:
- **Exemplo 1 (Bug Simples):** Botao de login no mobile — demonstra user story basica com 5 criterios Given-When-Then
- **Exemplo 2 (Bug Medio):** Campo de busca com acentos — demonstra user story com tratamento de normalizacao
- **Exemplo 3 (Bug Complexo):** Sistema de pagamento com timeout — demonstra user story com secoes adicionais (Contexto Tecnico, Tasks Tecnicas Sugeridas)

### 3. Chain of Thought (CoT)

**O que e:** Instruir o modelo a seguir um raciocinio passo a passo antes de gerar a resposta final.

**Por que escolhi:** A metrica de Completeness Score exigia que a user story cobrisse todos os aspectos do bug (usuario afetado, funcionalidade, valor, edge cases). Sem CoT, o modelo frequentemente omitia aspectos importantes. O raciocinio estruturado garantiu cobertura completa.

**Como apliquei:** Defini 4 passos obrigatorios de analise antes da escrita:
1. Identificar o usuario afetado
2. Entender a acao/funcionalidade quebrada
3. Determinar o valor de negocio
4. Pensar em edge cases e criterios testaveis

---

## Resultados Finais

### Prompt publicado no LangSmith Hub

- **v1 (original):** [leonanluppi/bug_to_user_story_v1](https://smith.langchain.com/hub/leonanluppi/bug_to_user_story_v1)
- **v2 (otimizado):** [primeiro/bug_to_user_story_v2](https://smith.langchain.com/hub/primeiro/bug_to_user_story_v2)

### Resultados da Avaliacao (v2 otimizado)

| Metrica | Score | Status |
|---|---|---|
| Tone Score | **0.98** | >=0.9 |
| Acceptance Criteria Score | **0.98** | >=0.9 |
| User Story Format Score | **0.98** | >=0.9 |
| Completeness Score | **0.98** | >=0.9 |
| **Media** | **0.98** | **>=0.9** |

### Metricas adicionais

| Metrica | Score |
|---|---|
| Helpfulness | 0.95 |
| Clarity | 0.93 |
| Precision | 0.98 |
| F1-Score | 0.74 |
| Correctness | 0.86 |

### Tabela Comparativa: v1 vs v2

| Aspecto | v1 (Original) | v2 (Otimizado) |
|---|---|---|
| Persona | Generica ("assistente") | Product Manager Senior especializado |
| Formato | Sem formato definido | Template "Como um... eu quero... para que..." |
| Exemplos | Nenhum | 3 exemplos (simples, medio, complexo) |
| Criterios de Aceitacao | Nao mencionados | Given-When-Then obrigatorio |
| Edge Cases | Nao tratados | 4 cenarios documentados |
| Raciocinio | Nenhum | Chain of Thought em 4 passos |
| Tamanho do system_prompt | ~200 caracteres | ~4900 caracteres |

---

## Como Executar

### Pre-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com) com API Key
- API Key do [Google Gemini](https://aistudio.google.com/app/apikey) (gratuito) ou [OpenAI](https://platform.openai.com/api-keys) (pago)

### 1. Setup do ambiente

```bash
# Clonar o repositorio
git clone https://github.com/seu-usuario/mba-ia-pull-evaluation-prompt.git
cd mba-ia-pull-evaluation-prompt

# Criar e ativar virtualenv
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variaveis de ambiente

```bash
cp .env.example .env
```

Preencher no `.env`:
- `LANGSMITH_API_KEY` - Sua chave do LangSmith
- `USERNAME_LANGSMITH_HUB` - Seu handle publico do LangSmith Hub
- `GOOGLE_API_KEY` ou `OPENAI_API_KEY` - Chave do provider LLM
- `LLM_PROVIDER` - `google` ou `openai`
- `LLM_MODEL` / `EVAL_MODEL` - Modelos a utilizar

### 3. Pull do prompt original

```bash
python src/pull_prompts.py
```

### 4. Push do prompt otimizado

```bash
python src/push_prompts.py
```

### 5. Executar avaliacao

```bash
python src/evaluate.py
```

### 6. Executar testes

```bash
pytest tests/test_prompts.py -v
```

---

## Dicas Finais

- **Lembre-se da importancia da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** e excelente para tarefas que exigem raciocinio complexo
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug
- **Nao altere os datasets de avaliacao** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - e normal precisar de 3-5 iteracoes para atingir 0.9 em todas as metricas
- **Documente seu processo** - a jornada de otimizacao e tao importante quanto o resultado final
