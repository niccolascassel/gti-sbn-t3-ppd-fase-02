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
        df = pd.read_csv(filepath)
        print(f"Dados de '{filepath}' carregados. Total de registros: {len(df)}")

        # 1. Limpar nomes das colunas
        # Converte para minúsculas, substitui espaços por underscores e remove caracteres não alfanuméricos
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False).str.replace(r'[^\w]', '', regex=True)
        
        # Renomear colunas 'positive' e 'negative' para 'positive_reviews' e 'negative_reviews'
        if 'positive' in df.columns:
            df.rename(columns={'positive': 'positive_reviews'}, inplace=True)
        if 'negative' in df.columns:
            df.rename(columns={'negative': 'negative_reviews'}, inplace=True)

        # 2. Converter tipos de dados e tratar valores ausentes/inválidos

        # release_date: Converter para datetime e extrair o ano
        # 'errors="coerce"' converterá valores inválidos para NaT (Not a Time)
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce', format='%b %d, %Y')
        df['release_year'] = df['release_date'].dt.year

        # price: Converter para float, preencher NaNs com 0.0 (assumindo jogo gratuito)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)

        # Colunas Booleanas (windows, mac, linux): Converter para bool
        for col in ['windows', 'mac', 'linux']:
            if col in df.columns:
                df[col] = df[col].astype(bool)

        # Colunas Numéricas Inteiras:
        # Remove caracteres não numéricos, converte para número e preenche NaNs com 0
        numeric_cols_to_int = [
            'dlc_count', 'reviews', 'positive_reviews', 'negative_reviews', 'achievements',
            'recommendations', 'average_playtime_forever', 'average_playtime_two_weeks',
            'median_playtime_forever', 'median_playtime_two_weeks', 'screenshots', 'movies'
        ]
        for col in numeric_cols_to_int:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # estimated_owners: Tratamento específico para strings com ranges (e.g., '500,000 - 1,000,000')
        if 'estimated_owners' in df.columns:
            def clean_estimated_owners(owner_str):
                if pd.isna(owner_str) or not isinstance(owner_str, str): 
                    return np.nan
                parts = owner_str.replace(',', '').split(' - ')
                try:
                    return float(parts[0])
                except ValueError:
                    return np.nan
            
            df['estimated_owners'] = df['estimated_owners'].apply(clean_estimated_owners)
            df['estimated_owners'].fillna(0, inplace=True) # Preenche NaNs restantes com 0

        # metacritic_score: Converter para float. NaNs serão mantidos para que a análise
        # de jogos mais bem avaliados possa filtrá-los.
        if 'metacritic_score' in df.columns:
            df['metacritic_score'] = pd.to_numeric(df['metacritic_score'], errors='coerce')
        
        # Colunas tipo lista (genres, categories, tags): Garantir que são strings e preencher NaNs com vazio
        for col in ['genres', 'categories', 'tags']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().fillna('')
        
        print("Pré-processamento de dados concluído.")
        return df

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado. Verifique o caminho e se o arquivo foi descompactado.")
        raise
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o carregamento e pré-processamento dos dados: {e}")
        raise