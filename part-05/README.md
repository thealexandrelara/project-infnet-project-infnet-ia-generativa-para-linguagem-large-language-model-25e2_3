# 🎵 Wedding Song Checker

**Wedding Song Checker** é uma aplicação interativa baseada em IA que ajuda casais e organizadores de eventos a verificar se uma música é apropriada para ser tocada em cerimônias de casamento. O sistema analisa automaticamente a letra da música e retorna uma avaliação baseada em critérios como linguagem explícita, violência, infidelidade, tristeza ou temas que contradizem o espírito de amor e celebração.

## 🚀 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) – para criação da interface web interativa
- [LangChain](https://www.langchain.com/) – para estruturação dos agentes LLM e fluxo da aplicação
- [OpenAI GPT (via langchain-openai)](https://platform.openai.com/) – para análise semântica das letras
- [Genius API (via lyricsgenius)](https://docs.genius.com/) – para busca das letras de músicas
- [Transformers (Hugging Face)](https://huggingface.co/transformers/) – compatibilidade com modelos baseados em Torch
- `uv` – para gerenciamento de ambiente e dependências

## Pré-requisitos

    • Python 3.13 instalado
    • uv instalado (instruções para instalação podem ser encontradas (aqui)[https://docs.astral.sh/uv/getting-started/installation/#installing-uv])
    • obtenha sua API key no site do Genius (https://genius.com/api-clients)
    • obtenha sua API key no site da Open AI (https://platform.openai.com/)

## 📦 Instalação

1. Clone o repositório:

````bash
git clone git@github.com:thealexandrelara/project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3.git
cd project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3

2. Instale as dependências listadas em pyproject.toml

```bash
uv sync
````

3. Configure as variáveis de ambiente criando um arquivo .env:

```bash
GENIUS_API_CLIENT_ID="Your GENIUS API CLIENT ID"
GENIUS_API_CLIENT_SECRET="Your GENIUS API CLIENT SECRET"
GENIUS_API_CLIENT_ACCESS_TOKEN="Your GENIUS CLIENT ACCESS TOKEN"
OPENAI_API_KEY="Your OpenAI API Key"
```

4. Execute a aplicação:

```bash
streamlit run app.py
```

## Arquitetura do projeto

O projeto é composto por 4 arquivos principais:

- **app.py**: Implementação principal da interface com Streamlit. Gerencia as entradas do usuário e exibe o resultado da análise.
- **wedding_organizer_agent.py**: Lógica do agente LangChain. Define o prompt, o agente LLM, e registra a tool que busca a letra da música.
- **lyrics_searcher.py**: Wrapper sobre a Genius API para buscar letras de músicas com base no nome e artista fornecidos.
- **json_parser.py**: Responsável por realizar o parsing e limpeza do JSON de resposta da Genius API, garantindo que as informações necessárias sejam usada na análise ou retornadas na saída.

### Funcionalidades

- Análise automatizada de letras de músicas com IA
- Busca real de letras usando a Genius API
- Avaliação de adequação para cerimônias de casamento com explicações
- Interface simples, acessível e responsiva com Streamlit

## Exemplo de Uso

1. Informe o nome da música e o artista
2. A aplicação busca automaticamente a letra
3. A IA analisa a letra com base em critérios pré-definidos
4. O sistema exibe se a música é apropriada ou inapropriada, com justificativa
