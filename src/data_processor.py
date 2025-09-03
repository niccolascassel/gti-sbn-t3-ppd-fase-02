import pandas as pd
import numpy as np

def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Carrega e pré-processa os dados do arquivo CSV especificado,
    retornando um DataFrame do pandas pronto para análise.

    Args:
        filepath (str): O caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: O DataFrame com os dados carregados e pré-processados.

    Raises:
        FileNotFoundError: Se o arquivo especificado não for encontrado.
        Exception: Para outros erros que possam ocorrer durante o carregamento ou pré-processamento.
    """
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(filepath)
        print(f"Dados de '{filepath}' carregados. Total de registros: {len(df)}")

        # 1. Limpar nomes das colunas de forma mais segura
        # Converte para minúsculas, remove espaços extras e substitui espaços por underscores
        # Remove a parte do regex que era muito agressiva ([^\w])
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False)
        
        # Mapeamento de nomes de colunas esperados para padronização
        column_rename_map = {
            'positive': 'positive_reviews',
            'negative': 'negative_reviews',
            # Adicione mapeamentos explícitos para 'publisher' e 'developer'
            # caso seus nomes originais no CSV sejam diferentes de 'publisher' ou 'developer'
            'publisher_name': 'publisher', # Exemplo: se a coluna for 'Publisher Name'
            'game_publisher': 'publisher', # Exemplo: se a coluna for 'Game Publisher'
            'developer_name': 'developer', # Exemplo: se a coluna for 'Developer Name'
            'game_developer': 'developer', # Exemplo: se a coluna for 'Game Developer'
        }
        # Renomeia as colunas apenas se elas existirem no DataFrame
        df.rename(columns={k: v for k, v in column_rename_map.items() if k in df.columns}, inplace=True)

        # 2. Converter tipos de dados e tratar valores ausentes/inválidos

        # release_date: Converter para datetime e extrair o ano
        # 'errors="coerce"' converterá valores inválidos para NaT (Not a Time)
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce', format='%b %d, %Y')
        df['release_year'] = df['release_date'].dt.year # Extrai o ano para fácil filtragem

        # price: Converter para float, preencher NaNs com 0.0 (assumindo jogo gratuito)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)

        # Colunas Booleanas (windows, mac, linux): Converter para bool
        for col in ['windows', 'mac', 'linux']:
            if col in df.columns: # Garante que a coluna existe antes de tentar converter
                df[col] = df[col].astype(bool)

        # Colunas Numéricas Inteiras:
        # Remove caracteres não numéricos, converte para número e preenche NaNs com 0
        numeric_cols_to_int = [
            'dlc_count', 'reviews', 'positive_reviews', 'negative_reviews', 'achievements',
            'recommendations', 'average_playtime_forever', 'average_playtime_two_weeks',
            'median_playtime_forever', 'median_playtime_two_weeks', 'screenshots', 'movies'
        ]
        for col in numeric_cols_to_int:
            if col in df.columns: # Garante que a coluna existe
                # Remove todos os caracteres não-dígitos da string antes da conversão
                df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # estimated_owners: Tratamento específico para strings com ranges (e.g., '500,000 - 1,000,000')
        if 'estimated_owners' in df.columns:
            def clean_estimated_owners(owner_str):
                if pd.isna(owner_str) or not isinstance(owner_str, str): 
                    return np.nan
                # Remove vírgulas, divide por ' - ', pega a primeira parte (o menor número do range),
                # e tenta converter para float.
                parts = owner_str.replace(',', '').split(' - ')
                try:
                    return float(parts[0])
                except ValueError:
                    return np.nan # Retorna NaN para valores que não podem ser convertidos
            
            df['estimated_owners'] = df['estimated_owners'].apply(clean_estimated_owners)
            df['estimated_owners'].fillna(0, inplace=True) # Preenche NaNs restantes com 0

        # metacritic_score: Converter para float. NaNs serão mantidos para que a análise
        # de jogos mais bem avaliados possa filtrá-los.
        if 'metacritic_score' in df.columns: # Garante que a coluna existe
            df['metacritic_score'] = pd.to_numeric(df['metacritic_score'], errors='coerce')
        
        # Colunas tipo lista (genres, categories, tags): Garantir que são strings e preencher NaNs com vazio
        # Para facilitar operações como str.contains() em funções de análise
        for col in ['genres', 'categories', 'tags']:
            if col in df.columns: # Garante que a coluna existe
                df[col] = df[col].astype(str).str.strip().fillna('')
        
        print("Pré-processamento de dados concluído.")
        return df

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado. Verifique o caminho e se o arquivo foi descompactado.")
        raise # Levanta a exceção novamente para ser tratada em um nível superior
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o carregamento e pré-processamento dos dados: {e}")
        raise # Levanta a exceção novamente