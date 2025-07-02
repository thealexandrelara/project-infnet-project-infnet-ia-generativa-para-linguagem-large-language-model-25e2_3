Projeto de machine learning com o objetivo de demonstrar os conhecimentos teóricos e práticos em LLMs, NER, NLP, Engenharia de Prompts, Streamlit, LangChain, etc.

Link do repositório:

```
https://github.com/thealexandrelara/project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3
```

# Rúbricas do projeto

Para facilitar a avaliação, desenvolvi uma documentação estruturada com base nas rúbricas do projeto, contendo explicações detalhadas de como cada critério foi atendido ao longo do desenvolvimento:

Link: https://github.com/thealexandrelara/project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3/blob/main/docs/rubricas.md

⸻

# Instalação e Execução do Projeto

Este projeto foi desenvolvido em Python 3.13 e com diversas dependências que podem ser vistas no arquivo `pyproject.toml`. Para facilitar a gestão de dependências e o ambiente virtual, é recomendado o uso do `uv`.

## Pré-requisitos

    • Python 3.13 instalado
    • uv instalado (instruções para instalação podem ser encontradas (aqui)[https://docs.astral.sh/uv/getting-started/installation/#installing-uv])

#### Instalação do projeto

Clone o repositório e instale as dependências:

```bash
git clone git@github.com:thealexandrelara/project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3.git
```

```
cd project-infnet-project-infnet-ia-generativa-para-linguagem-large-language-model-25e2_3
```

#### Instale as dependências listadas em pyproject.toml

```bash
uv sync
```

#### Execução do projeto

Caso deseje fazer uso somente do `pip` sem o `uv`, modifique as células que usam "!uv pip install [dependencia]" por "!pip install [dependencia]", por exemplo:

```python

!pip install -q pandas
!pip install -q seaborn
```

#### Arquitetura do projeto

    |_ part-01.ipynb: Contém as respostas e implementações da Parte 01 do projeto.
    |_ part-02.ipynb: Contém as respostas e implementações da Parte 02 do projeto.
    |_ part-03.ipynb: Contém as respostas e implementações da Parte 03 do projeto.
    |_ part-04.ipynb: Contém as respostas e implementações da Parte 04 do projeto.
    |_ part-05.ipynb: Contém as respostas da Parte 05 do projeto.
    |_ part-05: Pasta contendo a implementação da Parte 05 do projeto.
    |_ assets: Contém imagens dos certificados, quiz e exemplos
    |_ docs: Contém o arquivo de rúbricas demonstrando como cada rúbrica está sendo atendida no projeto.
