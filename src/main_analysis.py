import os
import sys
import argparse
import pandas as pd

from data_processor import load_and_preprocess_data
from analysis_functions import (
    get_top_10_metacritic_games,
    check_linux_support_growth,
)
from chart_plotting import ChartGenerator

FULL_DATA_PATH = 'data/dataset/steam_games.csv'
SAMPLE_PATH_TEMPLATE = 'data/samples/steam_games_sample_{:02d}.csv'
PLOTS_DIR = 'data/plots'

chart_generator = ChartGenerator(output_dir=PLOTS_DIR)

CUSTOM_HELP_MESSAGE = """
Como utilizar o main_analysis.py:

Este script demonstra o uso dos módulos de análise de dados Steam.
Para o relatório completo, consulte o arquivo 'relatorio_analise.ipynb'.

python main_analysis.py [OPÇÕES]

Opções:
  -s DATASET_ID, --s DATASET_ID, -sample DATASET_ID, --sample DATASET_ID
                        Define qual dataset será analisado.
                        Pode ser um número de 1 a 10 para usar uma amostra
                        (e.g., '1' para sample_01, '10' para sample_10),
                        ou 'full' para usar o dataset completo.
                        Se esta opção não for especificada ou for vazia/inválida,
                        a análise será executada para o dataset COMPLETO por padrão.
  -h, --help, --h, -help
                        Mostra esta mensagem de ajuda e sai.

Exemplos de uso:
  - Analisar a amostra 'sample_05':
    python main_analysis.py -s 5

  - Analisar o dataset completo (comportamento padrão):
    python main_analysis.py
"""

def print_custom_help():
    """Imprime a mensagem de ajuda personalizada no console e sai."""
    print(CUSTOM_HELP_MESSAGE)
    sys.exit(0)

def run_analysis(file_path: str, data_type_label: str, filename_prefix: str):
    """
    Executa uma análise de demonstração utilizando os novos módulos
    (data_processor, analysis_functions, chart_plotting).

    Args:
        file_path (str): Caminho para o arquivo CSV a ser analisado.
        data_type_label (str): Rótulo para identificação no título dos gráficos
                                (e.g., "Dataset Completo", "Amostra (Sample 01)").
        filename_prefix (str): Prefixo para o nome dos arquivos de gráficos salvos
                               (e.g., "full", "sample_01").
    """
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo de dados '{file_path}' não foi encontrado.")
        print("Por favor, verifique se o arquivo está no diretório correto ou atualize o caminho.")
        return

    try:
        # --- 1. Carregar e Pré-processar Dados usando o novo data_processor ---
        print(f"\n--- Carregando e pré-processando dados de: {file_path} ---")
        df = load_and_preprocess_data(file_path)
        print(f"DataFrame carregado e pronto para análise. Total de jogos: {len(df)}")

        # --- 2. Demonstrar algumas análises (exemplo) ---
        print("\n--- Demonstração de Análise: Top 10 Jogos Metacritic ---")
        top_10_metacritic = get_top_10_metacritic_games(df)
        print("Top 10 Jogos Mais Bem Avaliados (Metacritic):")
        
        print(top_10_metacritic[['name', 'metacritic_score', 'release_date']].to_string()) 
        print("\nPara uma análise detalhada e todos os resultados, consulte 'relatorio_analise.ipynb'.")

        print("\n--- Demonstração de Análise: Crescimento de Suporte Linux (2018-2022) ---")
        linux_growth_data = check_linux_support_growth(df)
        print("Contagem de jogos com suporte Linux por ano (2018-2022):")
        print(linux_growth_data.to_string(index=False))
        print("\nPara uma análise detalhada e todos os resultados, consulte 'relatorio_analise.ipynb'.")

        # --- 3. Demonstrar a geração de um gráfico (exemplo) ---
        print("\n--- Demonstração de Geração de Gráfico: Suporte a SO (Gráfico 1) ---")
        
        total_games = len(df)
        if total_games > 0:
            os_support = {
                'Windows': (df['windows'].sum() / total_games) * 100,
                'Mac': (df['mac'].sum() / total_games) * 100,
                'Linux': (df['linux'].sum() / total_games) * 100,
            }
            chart_generator.generate_g1_os_support_chart(
                os_support,
                data_type_label,
                f'{filename_prefix}_os_support'
            )
            print(f"Gráfico de suporte a SO gerado e salvo em '{PLOTS_DIR}/g1_{filename_prefix}_os_support.png'.")
        else:
            print("Não foi possível gerar o gráfico de suporte a SO: DataFrame vazio.")


    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o arquivo CSV está no local correto e descompactado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a análise de demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if any(arg in ['-h', '--h', '-help', '--help'] for arg in sys.argv[1:]):
        print_custom_help()
        
    parser = argparse.ArgumentParser(
        description="Script para análise de dados de jogos Steam e geração de gráficos.",
        add_help=False
    )
    
    parser.add_argument(
        '-s', '--s', '-sample', '--sample',
        dest='dataset_id',
        type=str,
        default='full',
        help="ID do dataset a ser analisado (1-10 para samples, 'full' para o dataset completo)."
    )

    args = parser.parse_args()

    selected_id = args.dataset_id
    file_to_analyze = FULL_DATA_PATH
    data_label = 'Dataset Completo'
    file_prefix = 'full'
    
    if isinstance(selected_id, str):
        if selected_id.isdigit():
            sample_num = int(selected_id)
            if 1 <= sample_num <= 10:
                file_to_analyze = SAMPLE_PATH_TEMPLATE.format(sample_num)
                data_label = f'Amostra (Sample {sample_num:02d})'
                file_prefix = f'sample_{sample_num:02d}'
            else:
                print(f"Aviso: ID de amostra '{selected_id}' fora do intervalo (1-10). Analisando o dataset COMPLETO por padrão.")
        elif selected_id.lower() == 'full':
            pass
        else:
            print(f"Aviso: Parâmetro '{selected_id}' inválido para a opção -s/--sample. Analisando o dataset COMPLETO por padrão.")

    print(f"\n--- Iniciando Análise de Demonstração para: {data_label} ---")
    run_analysis(file_to_analyze, data_label, file_prefix)

    print(f"\nDemonstração concluída. Gráficos salvos em '{PLOTS_DIR}'.")
    print("Para o relatório completo e detalhado, por favor, execute e revise 'relatorio_analise.ipynb'.")
