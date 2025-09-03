import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class ChartGenerator:
    """
    Classe responsável por gerar e salvar gráficos para as análises de dados.
    """
    def __init__(self, output_dir='data/plots'):
        """
        Inicializa o gerador de gráficos.
        Cria o diretório de saída se ele não existir.
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self._setup_custom_plot_style()

    def _setup_custom_plot_style(self):
        """
        Define um estilo customizado para todos os gráficos, padronizando cores, fontes, etc.
        """
        
        plt.style.use('seaborn-v0_8-darkgrid')

        self.colors = [
            '#1f77b4',  # Azul Metálico (primary)
            '#ff7f0e',  # Laranja Vívido
            '#2ca02c',  # Verde Esmeralda (para "gratuitos")
            '#d62728',  # Vermelho Vivo (para destaques ou "pagos")
            '#9467bd',  # Roxo
            '#8c564b',  # Marrom
            '#e377c2',  # Rosa Magenta
            '#7f7f7f',  # Cinza Neutro
            '#bcbd22',  # Verde Amarelo
            '#17becf'   # Ciano
        ]

        plt.rcParams.update({
            'font.family': 'sans-serif',    # Fonte mais limpa
            'font.size': 10,                # Tamanho de fonte padrão
            'axes.labelsize': 12,           # Tamanho da fonte dos rótulos dos eixos
            'axes.titlesize': 14,           # Tamanho da fonte dos títulos dos eixos
            'xtick.labelsize': 10,          # Tamanho da fonte dos ticks do eixo X
            'ytick.labelsize': 10,          # Tamanho da fonte dos ticks do eixo Y
            'legend.fontsize': 10,          # Tamanho da fonte da legenda
            'figure.titlesize': 16,         # Tamanho da fonte do título principal da figura
            'axes.edgecolor': '#cccccc',    # Cor da borda dos eixos
            'axes.facecolor': '#e0e0e0',    # Cor de fundo da área de plotagem
            'grid.color': '#cccccc',        # Cor da grade
            'grid.linestyle': '--',         # Estilo da linha da grade
            'grid.linewidth': 0.5,          # Espessura da linha da grade
            'lines.linewidth': 2,           # Espessura das linhas (para gráficos de linha)
            'lines.marker': 'o',            # Marcador padrão para gráficos de linha
            'figure.facecolor': 'white',    # Fundo da figura (fora da área de plotagem)
            'text.color': 'black',          # Cor geral do texto
            'axes.labelcolor': 'black',     # Cor dos rótulos dos eixos
            'xtick.color': 'black',         # Cor dos ticks do eixo X
            'ytick.color': 'black',         # Cor dos ticks do eixo Y
            'axes.spines.left': True,       # Manter linha da esquerda
            'axes.spines.bottom': True,     # Manter linha de baixo
            'axes.spines.right': False,     # Remover linha da direita
            'axes.spines.top': False,       # Remover linha de cima
            'savefig.dpi': 300              # Resolução ao salvar figuras
        })

        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=self.colors)

    def _save_plot(self, filename):
        """
        Salva o gráfico atual e fecha a figura para liberar memória.
        """
        full_path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(full_path)
        plt.close()

    def generate_q1_pie_chart(self, free_percentage, paid_percentage, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de pizza para o percentual de jogos gratuitos vs. pagos.
        """
        labels = ['Gratuitos', 'Pagos']
        sizes = [free_percentage, paid_percentage]
        colors = [self.colors[2], self.colors[0]]
        explode = (0.1, 0)

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                           colors=colors, shadow=False, startangle=90, wedgeprops={'edgecolor': 'black'})
        ax1.axis('equal')
        ax1.set_title(f'Percentual de Jogos Gratuitos vs. Pagos - {title_suffix}', fontsize=plt.rcParams['axes.titlesize'])

        plt.setp(autotexts, size=plt.rcParams['font.size'] + 2, weight='bold', color='white')
        plt.setp(texts, size=plt.rcParams['font.size'], color='black')

        self._save_plot(f'q1_{filename_suffix}.png')

    def generate_q2_bar_chart(self, year_counts, max_years, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de barras para o número de jogos lançados por ano,
        destacando o(s) ano(s) com mais lançamentos.
        """
        if not year_counts:
            print(f"Não há dados de anos para plotar para Q2 - {title_suffix}.")
            return

        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]

        plt.figure(figsize=(12, 7))
        bars = plt.bar(years, counts, color=self.colors[0])
        
        for i, year in enumerate(years):
            if year in max_years:
                bars[i].set_color(self.colors[3])

        plt.xlabel('Ano de Lançamento', fontsize=plt.rcParams['axes.labelsize'])
        plt.ylabel('Número de Jogos', fontsize=plt.rcParams['axes.labelsize'])
        plt.title(f'Número de Jogos Lançados por Ano - {title_suffix}', fontsize=plt.rcParams['axes.titlesize'])
        plt.xticks(years, rotation=45, ha='right', fontsize=plt.rcParams['xtick.labelsize'])
        plt.yticks(fontsize=plt.rcParams['ytick.labelsize'])
        
        self._save_plot(f'q2_{filename_suffix}.png')

    def generate_q3_bar_chart(self, top_genres_data, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de barras para os top N gêneros com a maior média de recomendações,
        destacando o(s) gênero(s) com a maior média.
        """
        if not top_genres_data:
            print(f"Não há dados de gênero para plotar para Q3 - {title_suffix}.")
            return

        genres = [item['genre'] for item in top_genres_data]
        avg_recommendations_values = [item['average_recommendations'] for item in top_genres_data]

        max_avg_value = 0.0
        if avg_recommendations_values:
            max_avg_value = max(avg_recommendations_values)

        plt.figure(figsize=(12, 7))
        bars = plt.bar(genres, avg_recommendations_values, color=self.colors[1])
        
        for i, bar in enumerate(bars):
            if avg_recommendations_values[i] == max_avg_value:
                bar.set_color(self.colors[3])

        plt.xlabel('Gênero', fontsize=plt.rcParams['axes.labelsize'])
        plt.ylabel('Média de Recomendações', fontsize=plt.rcParams['axes.labelsize'])
        plt.title(f'Top {len(genres)} Gêneros por Média de Recomendações (Filtrado) - {title_suffix}', fontsize=plt.rcParams['axes.titlesize'])
        plt.xticks(rotation=45, ha='right', fontsize=plt.rcParams['xtick.labelsize'])
        plt.yticks(fontsize=plt.rcParams['ytick.labelsize'])
        
        self._save_plot(f'q3_{filename_suffix}.png')
    

    def generate_g1_os_support_chart(self, os_percentages: dict, title_suffix: str, filename_suffix: str):
        """
        Gráfico 1: Percentual de jogos que possuem suporte para cada sistema operacional.
        (Barras com percentuais).
        """
        if not os_percentages:
            print(f"Não há dados de suporte a SO para plotar para G1 - {title_suffix}.")
            return

        labels = list(os_percentages.keys())
        sizes = list(os_percentages.values())

        plt.figure(figsize=(10, 7))
        
        colors_for_os = {
            'Windows': self.colors[0], # Azul
            'Mac': self.colors[1],     # Laranja
            'Linux': self.colors[2]    # Verde
        }
        
        bar_colors = [colors_for_os.get(label, self.colors[7]) for label in labels]

        bars = plt.bar(labels, sizes, color=bar_colors)
        
        plt.xlabel('Sistema Operacional', fontsize=plt.rcParams['axes.labelsize'])
        plt.ylabel('Percentual de Jogos (%)', fontsize=plt.rcParams['axes.labelsize'])
        plt.title(f'Percentual de Jogos por Suporte a SO - {title_suffix}', fontsize=plt.rcParams['axes.titlesize'])
        plt.ylim(0, 100)
        plt.yticks(fontsize=plt.rcParams['ytick.labelsize'])
        plt.xticks(fontsize=plt.rcParams['xtick.labelsize'])
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontsize=plt.rcParams['font.size'] - 1)

        self._save_plot(f'g1_{filename_suffix}.png')

    
    def generate_g2_genre_trend_chart(self, genre_data: pd.DataFrame, title_suffix: str, filename_suffix: str):
        """
        Gráfico 2: Número total de jogos single-player do gênero Indie e estratégia
        lançados por ano entre 2010 e 2020.
        (mostrar tendência para cada gênero separadamente, mas no mesmo gráfico).
        """
        
        if genre_data.empty or 'year' not in genre_data.columns or 'Indie' not in genre_data.columns or 'Strategy' not in genre_data.columns:
            print(f"Dados insuficientes para plotar o Gráfico 2 para {title_suffix}.")
            return
        
        plt.figure(figsize=(12, 7))
        plt.plot(genre_data['year'], genre_data['Indie'], label='Indie', color=self.colors[4], marker='o')
        plt.plot(genre_data['year'], genre_data['Strategy'], label='Strategy', color=self.colors[5], marker='s')

        plt.xlabel('Ano de Lançamento', fontsize=plt.rcParams['axes.labelsize'])
        plt.ylabel('Número de Jogos Single-Player', fontsize=plt.rcParams['axes.labelsize'])
        plt.title(f'Jogos Single-Player por Gênero (2010-2020) - {title_suffix}', fontsize=plt.rcParams['axes.titlesize'])
        plt.xticks(genre_data['year'], rotation=45, ha='right', fontsize=plt.rcParams['xtick.labelsize'])
        plt.yticks(fontsize=plt.rcParams['ytick.labelsize'])
        plt.legend(fontsize=plt.rcParams['legend.fontsize'])
        plt.grid(True, linestyle=plt.rcParams['grid.linestyle'], alpha=plt.rcParams['grid.linewidth'])
        
        self._save_plot(f'g2_{filename_suffix}.png')

    
    def generate_g3_custom_chart_price_vs_recs(self, analysis_data: pd.DataFrame, title_suffix: str, filename_suffix: str):
        """
        Gráfico Autoral: Comparação de Preço Médio e Recomendações Médias por Gênero
        (para jogos pós-2019). Utiliza dois eixos Y para comparar métricas com escalas diferentes.
        """
        if analysis_data.empty or 'genre' not in analysis_data.columns:
            print(f"Dados insuficientes para plotar o Gráfico Autoral para {title_suffix}.")
            return
        
        genres = analysis_data['genre']
        avg_prices = analysis_data['avg_price']
        avg_total_recommendations = analysis_data['avg_total_recommendations']

        x = np.arange(len(genres))
        width = 0.35

        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        rects1 = ax1.bar(x - width/2, avg_prices, width, label='Preço Médio (USD)', color=self.colors[6])
        ax1.set_xlabel('Gênero', fontsize=plt.rcParams['axes.labelsize'])
        ax1.set_ylabel('Preço Médio (USD)', color=self.colors[6], fontsize=plt.rcParams['axes.labelsize'])
        ax1.tick_params(axis='y', labelcolor=self.colors[6])
        ax1.set_xticks(x)
        ax1.set_xticklabels(genres, rotation=45, ha='right', fontsize=plt.rcParams['xtick.labelsize'])
        
        ax2 = ax1.twinx()
        rects2 = ax2.bar(analysis_data['genre'], analysis_data['avg_total_recommendations'], color=self.colors[7], alpha=0.6, width=0.4, align='edge', label='Média de Recomendações')
        ax2.set_ylabel('Média de Recomendações', color=self.colors[7], fontsize=plt.rcParams['axes.labelsize'])
        ax2.tick_params(axis='y', labelcolor=self.colors[7])

        fig.suptitle(f'Preço Médio vs. Média de Recomendações por Gênero (Jogos Pós-2019) - {title_suffix}', fontsize=plt.rcParams['figure.titlesize'])
        
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=plt.rcParams['legend.fontsize'])
        
        def autolabel(rects, ax_target):
            for rect in rects:
                height = rect.get_height()
                ax_target.annotate(f'{height:.0f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=plt.rcParams['font.size'] - 2)

        autolabel(rects1, ax1)
        autolabel(rects2, ax2)

        self._save_plot(f'g3_{filename_suffix}.png')
