import unittest
import os
import json
import pandas as pd
from pandas.testing import assert_frame_equal

from data_processor import load_and_preprocess_data
from analysis_functions import (
    get_top_10_metacritic_games,
    analyze_role_playing_games_metrics,
    analyze_top_paid_game_publishers,
    check_linux_support_growth,
    analyze_price_vs_recommendations_by_genre
)

SAMPLES_DIR = 'data/samples'
ALL_EXPECTED_RESULTS_FILE = os.path.join(SAMPLES_DIR, 'all_expected_results.json')

class TestSteamAnalysisFunctions(unittest.TestCase):
    """
    Classe de testes para as funções de análise de dados da Steam (Fase 2).
    Utiliza múltiplas amostras de dados e um único arquivo JSON para resultados esperados.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura o ambiente de teste uma vez antes de todos os testes.
        Carrega o arquivo JSON de resultados esperados e prepara os DataFrames para teste.
        """
        cls.samples_data = []
        
        if not os.path.exists(SAMPLES_DIR):
            raise FileNotFoundError(f"O diretório de amostras '{SAMPLES_DIR}' não foi encontrado. "
                                    "Por favor, certifique-se de que ele foi criado e contém os arquivos de amostra e o JSON.")
        
        if not os.path.exists(ALL_EXPECTED_RESULTS_FILE):
            raise FileNotFoundError(f"O arquivo de resultados esperados '{ALL_EXPECTED_RESULTS_FILE}' não foi encontrado. "
                                    "Certifique-se de que ele foi criado e está no local correto, contendo os resultados para as funções da Fase 2.")
        
        try:
            with open(ALL_EXPECTED_RESULTS_FILE, 'r', encoding='utf-8') as f:
                cls.all_expected_results = json.load(f)
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar JSON de '{ALL_EXPECTED_RESULTS_FILE}': {e}. Verifique a sintaxe do JSON.")
        except Exception as e:
            raise Exception(f"Erro inesperado ao carregar '{ALL_EXPECTED_RESULTS_FILE}': {e}")
        
        for i in range(1, 11):
            sample_id_str = f"{i:02d}"
            filename = f'steam_games_sample_{sample_id_str}.csv'
            csv_path = os.path.join(SAMPLES_DIR, filename)
            
            if not os.path.exists(csv_path):
                print(f"Aviso: Arquivo de amostra '{csv_path}' não encontrado. Pulando esta amostra.")
                continue
            
            expected_data_for_this_sample = cls.all_expected_results.get(f'sample_{sample_id_str}')
            
            if expected_data_for_this_sample:
                try:
                    df = load_and_preprocess_data(csv_path)
                    cls.samples_data.append((sample_id_str, df, expected_data_for_this_sample))
                except Exception as e:
                    print(f"Erro ao carregar/pré-processar a amostra {sample_id_str} ('{csv_path}'): {e}. Pulando.")
            else:
                print(f"Aviso: Resultados esperados para 'sample_{sample_id_str}' não encontrados em '{ALL_EXPECTED_RESULTS_FILE}'. Pulando esta amostra.")
        
        if not cls.samples_data:
            raise Exception(f"Nenhuma amostra de teste válida foi carregada. "
                            "Verifique a nomeação dos arquivos CSV e do JSON, e se os dados são válidos.")
        
        print(f"\nTotal de {len(cls.samples_data)} amostras carregadas e pré-processadas para teste.")

    def test_get_top_10_metacritic_games(self):
        """
        Testa a função get_top_10_metacritic_games (Pergunta 1).
        Compara o DataFrame resultante com o DataFrame esperado.
        """
        for sample_id, df, expected_data in self.samples_data:
            with self.subTest(sample=sample_id):
                actual_result_df = get_top_10_metacritic_games(df)
                
                expected_q1_data = expected_data.get('q1_top_metacritic', [])
                
                if not expected_q1_data:
                    self.assertTrue(actual_result_df.empty, f"Esperava DataFrame vazio para Q1 em {sample_id}, mas obteve dados.")
                    continue
                
                expected_result_df = pd.DataFrame(expected_q1_data)
                
                if 'release_date' in expected_result_df.columns:
                    expected_result_df['release_date'] = pd.to_datetime(expected_result_df['release_date'])
                if 'metacritic_score' in expected_result_df.columns:
                    expected_result_df['metacritic_score'] = pd.to_numeric(expected_result_df['metacritic_score'])
                
                expected_result_df.sort_values(by=['metacritic_score', 'release_date'], ascending=[False, True], inplace=True)
                actual_result_df.sort_values(by=['metacritic_score', 'release_date'], ascending=[False, True], inplace=True)
                
                actual_result_df = actual_result_df.reset_index(drop=True)
                expected_result_df = expected_result_df.reset_index(drop=True)

                try:
                    assert_frame_equal(actual_result_df, expected_result_df, check_dtype=True, check_exact=False, atol=0.01)
                except AssertionError as e:
                    self.fail(f"Falha na Q1 (Top Metacritic) para amostra {sample_id}: {e}\n"
                              f"--- Esperado ---\n{expected_result_df.to_string()}\n"
                              f"--- Obtido ---\n{actual_result_df.to_string()}")
    
    def test_analyze_role_playing_games_metrics(self):
        """
        Testa a função analyze_role_playing_games_metrics (Pergunta 2).
        Compara o dicionário de métricas resultante com o dicionário esperado.
        """
        for sample_id, df, expected_data in self.samples_data:
            with self.subTest(sample=sample_id):
                actual_result = analyze_role_playing_games_metrics(df)
                expected_q2_data = expected_data.get('q2_rpg_metrics', {})
                
                if not expected_q2_data:
                    self.assertTrue("message" in actual_result or not actual_result, 
                                    f"Esperava mensagem de 'nenhum RPG encontrado' ou dict vazio para Q2 em {sample_id}, mas obteve: {actual_result}")
                    continue
                
                self.assertIsInstance(actual_result, dict, f"Q2 para amostra {sample_id}: O resultado não é um dicionário.")
                self.assertEqual(actual_result.keys(), expected_q2_data.keys(), f"Q2 para amostra {sample_id}: Chaves do dicionário diferentes.")

                for metric, values in expected_q2_data.items():
                    self.assertIn(metric, actual_result, f"Q2 para amostra {sample_id}: Métrica '{metric}' ausente no resultado real.")
                    self.assertAlmostEqual(actual_result[metric]['media'], values['media'], places=2,
                                           msg=f"Q2 para amostra {sample_id}: Média incorreta para '{metric}'.")
                    self.assertAlmostEqual(actual_result[metric]['maximo'], values['maximo'], places=0,
                                           msg=f"Q2 para amostra {sample_id}: Máximo incorreto para '{metric}'.")

    def test_analyze_top_paid_game_publishers(self):
        """
        Testa a função analyze_top_paid_game_publishers (Pergunta 3).
        Compara o DataFrame resultante com o DataFrame esperado.
        """
        for sample_id, df, expected_data in self.samples_data:
            with self.subTest(sample=sample_id):
                actual_result_df = analyze_top_paid_game_publishers(df)
                expected_q3_data = expected_data.get('q3_top_publishers', [])

                if not expected_q3_data:
                    self.assertTrue(actual_result_df.empty, f"Esperava DataFrame vazio para Q3 em {sample_id}, mas obteve dados.")
                    continue
                
                expected_result_df = pd.DataFrame(expected_q3_data)
                
                expected_result_df['num_paid_games'] = expected_result_df['num_paid_games'].astype(int)
                expected_result_df['avg_positive_reviews'] = pd.to_numeric(expected_result_df['avg_positive_reviews'])
                expected_result_df['median_positive_reviews'] = pd.to_numeric(expected_result_df['median_positive_reviews'])
                
                expected_result_df.sort_values(by='num_paid_games', ascending=False, inplace=True)
                actual_result_df.sort_values(by='num_paid_games', ascending=False, inplace=True)
                
                actual_result_df = actual_result_df.reset_index(drop=True)
                expected_result_df = expected_result_df.reset_index(drop=True)

                try:
                    assert_frame_equal(actual_result_df, expected_result_df, check_dtype=True, check_exact=False, atol=0.01)
                except AssertionError as e:
                    self.fail(f"Falha na Q3 (Top Publishers) para amostra {sample_id}: {e}\n"
                              f"--- Esperado ---\n{expected_result_df.to_string()}\n"
                              f"--- Obtido ---\n{actual_result_df.to_string()}")

    def test_check_linux_support_growth(self):
        """
        Testa a função check_linux_support_growth (Pergunta 4).
        Compara o DataFrame resultante com o DataFrame esperado.
        """
        for sample_id, df, expected_data in self.samples_data:
            with self.subTest(sample=sample_id):
                actual_result_df = check_linux_support_growth(df)
                
                expected_q4_data = expected_data.get('q4_linux_growth', [])
                if not expected_q4_data:
                    self.assertTrue(actual_result_df.empty, f"Esperava DataFrame vazio para Q4 em {sample_id}, mas obteve dados.")
                    continue

                expected_result_df = pd.DataFrame(expected_q4_data)
                
                expected_result_df['release_year'] = expected_result_df['release_year'].astype(int)
                expected_result_df['num_linux_games'] = expected_result_df['num_linux_games'].astype(int)
                
                expected_result_df.sort_values(by='release_year', inplace=True)
                actual_result_df.sort_values(by='release_year', inplace=True)
                
                actual_result_df = actual_result_df.reset_index(drop=True)
                expected_result_df = expected_result_df.reset_index(drop=True)

                try:
                    assert_frame_equal(actual_result_df, expected_result_df, check_dtype=True) 
                except AssertionError as e:
                    self.fail(f"Falha na Q4 (Suporte Linux) para amostra {sample_id}: {e}\n"
                              f"--- Esperado ---\n{expected_result_df.to_string()}\n"
                              f"--- Obtido ---\n{actual_result_df.to_string()}")

    def test_analyze_price_vs_recommendations_by_genre(self):
        """
        Testa a função analyze_price_vs_recommendations_by_genre (Pergunta Autoral).
        Compara o DataFrame resultante com o DataFrame esperado.
        """
        for sample_id, df, expected_data in self.samples_data:
            with self.subTest(sample=sample_id):
                actual_result_df = analyze_price_vs_recommendations_by_genre(df)
                expected_custom_q_data = expected_data.get('q_custom_price_recs', [])

                if not expected_custom_q_data:
                    self.assertTrue(actual_result_df.empty, f"Esperava DataFrame vazio para Pergunta Autoral em {sample_id}, mas obteve dados.")
                    continue
                
                expected_result_df = pd.DataFrame(expected_custom_q_data)
                
                expected_result_df['avg_price'] = pd.to_numeric(expected_result_df['avg_price'])
                expected_result_df['avg_total_recommendations'] = pd.to_numeric(expected_result_df['avg_total_recommendations'])
                
                if 'correlation_price_recs' in expected_result_df.columns:
                    expected_result_df['correlation_price_recs'] = pd.to_numeric(expected_result_df['correlation_price_recs'], errors='coerce')
                
                expected_result_df.sort_values(by='genre', inplace=True)
                actual_result_df.sort_values(by='genre', inplace=True)
                
                actual_result_df = actual_result_df.reset_index(drop=True)
                expected_result_df = expected_result_df.reset_index(drop=True)

                try:
                    assert_frame_equal(actual_result_df, expected_result_df, check_dtype=True, check_exact=False, atol=0.01)
                except AssertionError as e:
                    self.fail(f"Falha na Pergunta Autoral para amostra {sample_id}: {e}\n"
                              f"--- Esperado ---\n{expected_result_df.to_string()}\n"
                              f"--- Obtido ---\n{actual_result_df.to_string()}")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
