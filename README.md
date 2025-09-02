# 🎮 Análise e Visualização de Dados de Jogos Steam - Projeto Fase II

Este projeto evolui da Fase I, aprofundando a análise e visualização de dados de jogos da plataforma Steam. Agora, utilizando o poderoso ecossistema de ciência de dados em Python (`pandas`, `numpy`, `matplotlib` e `Jupyter Notebook`), ele oferece insights mais robustos sobre o mercado de jogos, focando na performance de títulos, tendências de mercado e comportamento de publishers.

## ✨ Recursos da Fase II

*   **Análise Abrangente de Dados:** Utiliza a biblioteca `pandas` para um pré-processamento eficiente e manipulação de grandes volumes de dados.
*   **Relatório Interativo com Jupyter:** O coração do projeto é o `relatorio_analise.ipynb`, um notebook Jupyter que apresenta de forma interativa todas as análises, resultados e gráficos.
*   **Novas Perguntas de Negócio (Q1-Q4 + Autoral):**
    *   **Q1: Top 10 Metacritic:** Identifica os jogos mais bem avaliados segundo o Metacritic, com critério de desempate por data de lançamento.
    *   **Q2: Métricas RPG:** Calcula médias e máximos de DLCs, avaliações e materiais de demonstração para jogos de Role-Playing.
    *   **Q3: Publishers de Jogos Pagos:** Encontra os principais publishers de jogos pagos e analisa suas métricas de avaliações positivas.
    *   **Q4: Suporte Linux:** Verifica o crescimento do suporte a Linux em jogos entre 2018 e 2022.
    *   **Pergunta Autoral:** Explora a correlação entre preço do jogo e recomendações para jogos recentes em gêneros populares.
*   **Novos Gráficos Exploratórios (G1-G2 + Autoral):**
    *   **G1: Suporte a SO:** Visualiza o percentual de jogos com suporte para Windows, Mac e Linux.
    *   **G2: Tendência de Gênero:** Apresenta a tendência de lançamento de jogos single-player Indie e Estratégia por ano (2010-2020).
    *   **Gráfico Autoral:** Gráfico comparativo de preço médio vs. recomendações por gênero para jogos pós-2019.
*   **Modularidade do Código:** A lógica do projeto está bem organizada em módulos Python separados (`data_processor.py`, `analysis_functions.py`, `chart_plotting.py`) para facilitar a manutenção e reusabilidade.
*   **Estilo de Gráficos Padronizado:** Todos os gráficos são gerados com um estilo visual customizado, garantindo consistência e profissionalismo.
*   **Testes Unitários Atualizados:** O `test_steam_analyzer.py` foi reescrito para testar as novas funções baseadas em `pandas`, garantindo a confiabilidade das análises.

## 🚀 Primeiros Passos

Siga as instruções abaixo para configurar e executar o projeto em sua máquina local.

### 📋 Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
Para a Fase II, as seguintes bibliotecas Python são essenciais: `pandas`, `numpy`, `matplotlib` e `jupyter`.

### 📦 Instalação e Configuração

1.  **Clone o Repositório:**
    Comece clonando este repositório para a sua máquina local:

    ```bash
    git clone https://github.com/SeuUsuario/SeuRepositorio.git # Substitua pelo seu usuário e nome do repositório
    cd SeuRepositorio # Navegue até o diretório do projeto
    ```

2.  **Configuração dos Dados (Passo CRÍTICO!):**
    O dataset completo `steam_games.csv` está compactado como `steam_games.zip` no diretório `data/dataset/`. **Você DEVE descompactá-lo antes de executar qualquer análise.**

    *   **Local do Arquivo Compactado:** `data/dataset/steam_games.zip`
    *   **Local de Destino (onde o arquivo descompactado deve ficar):** `data/dataset/steam_games.csv`

    Você pode usar sua ferramenta de descompactação de preferência. Em sistemas baseados em Unix (Linux/macOS) ou Git Bash no Windows, você pode usar:

    ```bash
    unzip data/dataset/steam_games.zip -d data/dataset/
    ```

    No Windows, você pode descompactar manualmente usando o Explorador de Arquivos ou via PowerShell:

    ```powershell
    Expand-Archive -LiteralPath "data/dataset/steam_games.zip" -DestinationPath "data/dataset/"
    ```

    **Verifique se, após a descompactação, o arquivo `steam_games.csv` existe em `data/dataset/`**.

3.  **Instale as Dependências:**
    É altamente recomendado usar um ambiente virtual para gerenciar as dependências do projeto.

    ```bash
    # (Opcional) Crie e ative um ambiente virtual
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate

    # Instale as dependências necessárias para a Fase II
    pip install pandas numpy matplotlib jupyter
    ```

4.  **Prepare os Dados de Teste:**
    Para que os testes unitários (`test_steam_analyzer.py`) funcionem corretamente, você precisará preencher o arquivo `data/samples/all_expected_results.json` com os resultados esperados para cada uma das amostras e para cada nova pergunta de negócio e gráfico. Este arquivo deve conter a saída esperada das funções de `analysis_functions.py` para as amostras fornecidas.

## ⚙️ Uso

O principal artefato da Fase II é o **Jupyter Notebook** que contém o relatório completo. Um script `main_analysis.py` é fornecido para demonstração rápida via linha de comando.

### �� Como Utilizar o Relatório Interativo (Jupyter Notebook)

1.  **Inicie o Jupyter Notebook:**
    Com o ambiente virtual ativado e as dependências instaladas, execute:

    ```bash
    jupyter notebook
    ```
    Isso abrirá uma nova aba em seu navegador com a interface do Jupyter.

2.  **Abra o Notebook:**
    Navegue até o arquivo `relatorio_analise.ipynb` na interface do Jupyter e clique nele para abri-lo.

3.  **Execute as Células:**
    Execute todas as células do notebook em sequência (clique em "Cell" -> "Run All" ou execute-as uma por uma). O notebook carregará os dados, executará as análises, gerará os gráficos e exibirá os resultados e discussões diretamente no navegador.

### 🧪 Como Rodar os Testes Unitários

Para garantir a correção das funções de análise e pré-processamento, você pode rodar os testes unitários:

```bash
python -m unittest test_steam_analyzer.py

▶️ Como Utilizar o Script de Demonstração (main_analysis.py)
Este script serve como um exemplo de como orquestrar os módulos de análise via linha de comando. Ele realiza uma pequena amostra das análises e gera alguns gráficos para demonstração.

Analisar o dataset completo (steam_games.csv):

    ```bash
    python main_analysis.py -s full
    # ou
    python main_analysis.py --sample full
	
Analisar uma amostra específica (steam_games_sample_XX.csv): Substitua ID_DA_AMOSTRA por um número de 1 a 10. Por exemplo, para steam_games_sample_05.csv:

    ```bash
    python main_analysis.py -s 5
	# ou
	python main_analysis.py --sample 05

Analisar o dataset completo (comportamento padrão): Se nenhum argumento for fornecido, a análise será executada para o dataset completo.

	```bash
	python main_analysis.py
	
Mostrar Ajuda: Para ver as opções de uso e uma descrição detalhada:

	```bash
	python main_analysis.py -h
	# ou
	python main_analysis.py --help
	
🖼️ Saída dos Gráficos
Após a execução do relatorio_analise.ipynb ou do main_analysis.py, os gráficos gerados serão salvos no diretório data/plots/ como arquivos .png.

📁 Estrutura do Projeto
.
├── data/
│   ├── dataset/
│   │   ├── steam_games.csv       # Dataset completo (descompactar de steam_games.zip)
│   │   └── steam_games.zip       # Dataset completo compactado (no GitHub)
│   ├── samples/
│   │   ├── steam_games_sample_01.csv # Amostras de dataset
│   │   ├── ... (até sample_10.csv)
│   │   └── all_expected_results.json # Resultados esperados para testes unitários
│   └── plots/                    # Diretório onde os gráficos gerados serão salvos
├── analysis_functions.py         # Módulo com as funções de análise das perguntas de negócio (Fase II)
├── chart_plotting.py             # Módulo para geração e customização de gráficos (Fase II)
├── data_processor.py             # Módulo para carregar e pré-processar os dados com pandas (Fase II)
├── main_analysis.py              # Script de demonstração de uso dos módulos (herdado da Fase I, adaptado para Fase II)
├── relatorio_analise.ipynb       # **Principal relatório interativo da Fase II (Jupyter Notebook)**
├── test_steam_analyzer.py        # Testes unitários para as funções de análise (Fase II)
└── README.md                     # Este arquivo