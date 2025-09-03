import pandas as pd
import numpy as np

def get_top_10_metacritic_games(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pergunta 1: Retorna os dez jogos mais bem avaliados, de acordo com o Metacritic.
    Em caso de notas repetidas, ordena os jogos de acordo com suas datas de lançamento
    (do mais velho para o mais recente).

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos jogos Steam.

    Returns:
        pd.DataFrame: DataFrame com os 10 jogos mais bem avaliados e colunas relevantes.
    """
    # Garante que 'metacritic_score' é numérico e remove NaNs
    df_filtered = df.dropna(subset=['metacritic_score']).copy()
    df_filtered['metacritic_score'] = pd.to_numeric(df_filtered['metacritic_score'], errors='coerce')
    df_filtered.dropna(subset=['metacritic_score'], inplace=True)

    # Garante que 'release_date' é datetime e remove NaNs
    if not pd.api.types.is_datetime64_any_dtype(df_filtered['release_date']):
        df_filtered['release_date'] = pd.to_datetime(df_filtered['release_date'], errors='coerce')
    df_filtered.dropna(subset=['release_date'], inplace=True)

    # Ordena por metacritic_score (desc) e release_date (asc)
    top_games = df_filtered.sort_values(
        by=['metacritic_score', 'release_date'],
        ascending=[False, True]
    ).head(10)

    # Seleciona as colunas mais relevantes para exibição
    return top_games[['name', 'metacritic_score', 'release_date', 'publishers', 'developers']]

def analyze_role_playing_games_metrics(df: pd.DataFrame) -> dict:
    """
    Pergunta 2: Para jogos de role-playing, calcula o número médio e máximo de:
    DLCs, avaliações positivas, avaliações negativas e materiais de demonstração
    (número de capturas de tela e filmes, somados).

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos jogos Steam.

    Returns:
        dict: Dicionário com as métricas calculadas para jogos de role-playing.
    """
    # Certifica-se de que a coluna 'genres' é string e preenche NaNs para evitar erros
    df_filtered = df.copy()
    df_filtered['genres'] = df_filtered['genres'].astype(str).fillna('')

    # Filtra jogos que contêm "RPG" ou "Role-playing" em seus gêneros
    rpg_games = df_filtered[
        df_filtered['genres'].str.contains('RPG|Role-playing', case=False, na=False)
    ].copy()

    if rpg_games.empty:
        return {
            "message": "Nenhum jogo de role-playing encontrado com dados válidos para análise."
        }

    # Calcula materiais de demonstração: screenshots + movies
    rpg_games['total_demo_materials'] = rpg_games['screenshots'].fillna(0) + rpg_games['movies'].fillna(0)

    # Converte colunas para numéricas (após preencher NaN para evitar erros de conversão)
    numeric_cols = ['dlc_count', 'positive_reviews', 'negative_reviews', 'total_demo_materials']
    for col in numeric_cols:
        rpg_games[col] = pd.to_numeric(rpg_games[col], errors='coerce').fillna(0) # Trata NaN como 0 para média/max

    results = {
        "dlc_count": {
            "media": rpg_games['dlc_count'].mean(),
            "maximo": rpg_games['dlc_count'].max()
        },
        "positive_reviews": {
            "media": rpg_games['positive_reviews'].mean(),
            "maximo": rpg_games['positive_reviews'].max()
        },
        "negative_reviews": {
            "media": rpg_games['negative_reviews'].mean(),
            "maximo": rpg_games['negative_reviews'].max()
        },
        "total_demo_materials": {
            "media": rpg_games['total_demo_materials'].mean(),
            "maximo": rpg_games['total_demo_materials'].max()
        }
    }
    return results

def analyze_top_paid_game_publishers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pergunta 3: Encontra as cinco empresas que mais publicam jogos pagos na plataforma.
    Para tais empresas, calcula o número médio e mediano de avaliações positivas de seus jogos pagos.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos jogos Steam.

    Returns:
        pd.DataFrame: DataFrame com as 5 principais editoras, contagem de jogos pagos,
                      e média/mediana de avaliações positivas.
    """
    # Garante que 'price' é numérico e 'publishers' é string
    df_filtered = df.copy()
    df_filtered['price'] = pd.to_numeric(df_filtered['price'], errors='coerce')
    df_filtered['publishers'] = df_filtered['publishers'].astype(str).fillna('Desconhecido')
    df_filtered['positive_reviews'] = pd.to_numeric(df_filtered['positive_reviews'], errors='coerce')
    
    paid_games = df_filtered[(df_filtered['price'] > 0) & (df_filtered['price'].notna())].copy()

    if paid_games.empty:
        return pd.DataFrame(columns=['publishers', 'num_paid_games', 'avg_positive_reviews', 'median_positive_reviews'])

    top_publishers = paid_games['publishers'].value_counts().nlargest(5).index.tolist()

    results = []
    for publisher in top_publishers:
        publisher_games = paid_games[paid_games['publishers'] == publisher]
        num_paid_games = len(publisher_games)
        avg_positive = publisher_games['positive_reviews'].mean()
        median_positive = publisher_games['positive_reviews'].median()
        results.append({
            'publishers': publisher,
            'num_paid_games': num_paid_games,
            'avg_positive_reviews': avg_positive,
            'median_positive_reviews': median_positive
        })

    return pd.DataFrame(results).sort_values(by='num_paid_games', ascending=False)

def check_linux_support_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pergunta 4: Verifica se o número de jogos que suportam o sistema operacional Linux
    cresceu entre 2018 e 2022.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos jogos Steam.

    Returns:
        pd.DataFrame: DataFrame mostrando a contagem de jogos com suporte Linux por ano,
                      entre 2018 e 2022.
    """
    df_filtered = df.copy()

    # Garante que 'release_date' é datetime e extrai o ano
    if not pd.api.types.is_datetime64_any_dtype(df_filtered['release_date']):
        df_filtered['release_date'] = pd.to_datetime(df_filtered['release_date'], errors='coerce')
    df_filtered['release_year'] = df_filtered['release_date'].dt.year

    # Garante que 'linux' é booleano (True/False)
    df_filtered['linux'] = df_filtered['linux'].astype(bool)

    # Filtra jogos com suporte Linux entre 2018 e 2022
    linux_games_period = df_filtered[
        (df_filtered['linux'] == True) &
        (df_filtered['release_year'] >= 2018) &
        (df_filtered['release_year'] <= 2022)
    ].copy()

    if linux_games_period.empty:
        return pd.DataFrame(columns=['release_year', 'num_linux_games'])

    # Conta o número de jogos Linux por ano
    linux_growth = linux_games_period['release_year'].value_counts().sort_index().reset_index()
    linux_growth.columns = ['release_year', 'num_linux_games']

    # Garante que todos os anos no intervalo (2018-2022) estejam presentes, mesmo que com 0 jogos
    full_year_range = pd.DataFrame({'release_year': range(2018, 2023)})
    linux_growth = pd.merge(full_year_range, linux_growth, on='release_year', how='left').fillna(0)
    linux_growth['num_linux_games'] = linux_growth['num_linux_games'].astype(int)


    return linux_growth

def analyze_price_vs_recommendations_by_genre(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pergunta Autoral: Qual a correlação entre o preço do jogo e o número médio de
    recomendações (positivas + negativas) para jogos lançados após 2019 em gêneros populares,
    e como isso varia por gênero?

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos jogos Steam.

    Returns:
        pd.DataFrame: DataFrame com as médias de preço, recomendações e correlação por gênero.
    """
    df_filtered = df.copy()

    # Garante que 'release_date' é datetime e extrai o ano
    if not pd.api.types.is_datetime64_any_dtype(df_filtered['release_date']):
        df_filtered['release_date'] = pd.to_datetime(df_filtered['release_date'], errors='coerce')
    df_filtered['release_year'] = df_filtered['release_date'].dt.year

    # Garante que colunas são numéricas
    numeric_cols = ['price', 'positive_reviews', 'negative_reviews']
    for col in numeric_cols:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

    # Filtra jogos lançados após 2019 e com dados válidos de preço e avaliações
    recent_games = df_filtered[
        (df_filtered['release_year'] > 2019) &
        (df_filtered['price'].notna()) &
        (df_filtered['positive_reviews'].notna()) &
        (df_filtered['negative_reviews'].notna())
    ].copy()

    if recent_games.empty:
        return pd.DataFrame(columns=['genre', 'avg_price', 'avg_total_recommendations', 'correlation_price_recs'])

    recent_games['total_recommendations'] = recent_games['positive_reviews'] + recent_games['negative_reviews']

    # Descompacta gêneros para análise individual
    recent_games['genres'] = recent_games['genres'].astype(str).fillna('')
    all_genres = recent_games['genres'].str.split(';|,', expand=True).stack()
    all_genres = all_genres.str.strip() # Remove espaços extras
    genre_counts = all_genres.value_counts()

    popular_genres = genre_counts[genre_counts.index != ''].nlargest(5).index.tolist()
    
    results = []
    for genre in popular_genres:

        genre_games = recent_games[recent_games['genres'].str.contains(genre, case=False, na=False)].copy()

        if genre_games.empty:
            continue

        avg_price = genre_games['price'].mean()
        avg_total_recommendations = genre_games['total_recommendations'].mean()

        correlation = np.nan
        if genre_games['price'].nunique() > 1 and genre_games['total_recommendations'].nunique() > 1:
            correlation = genre_games['price'].corr(genre_games['total_recommendations'])

        results.append({
            'genre': genre,
            'avg_price': avg_price,
            'avg_total_recommendations': avg_total_recommendations,
            'correlation_price_recs': correlation
        })

    return pd.DataFrame(results).sort_values(by='avg_total_recommendations', ascending=False)