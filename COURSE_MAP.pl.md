[English](COURSE_MAP.md) | **Polski**

# Mapa kursu

Plik generowany z `course.toml` — nie edytuj go ręcznie. Lekcje **core** tworzą ścieżkę minimalną, lekcje **opcjonalne** ją rozszerzają. Lekcje „w przygotowaniu” jeszcze nie istnieją.

## M0 · Start

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 0.1 | [Instalacja i praca z samouczkiem](modules/00_start/01_setup/README.pl.md) | core | — | gotowa |

## M1 · Agenci i reprezentacja problemu

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 1.1 | [Czym jest AI](modules/01_agents/01_what_is_ai/README.pl.md) | core | 0.1 | gotowa |
| 1.2 | [Agent i środowisko](modules/01_agents/02_agents_and_environments/README.pl.md) | core | 1.1 | gotowa |
| 1.3 | [Typy agentów i sformułowanie problemu](modules/01_agents/03_problem_formulation/README.pl.md) | core | 1.2 | gotowa |
| 1.4 | [Krótka historia AI](modules/01_agents/04_history_of_ai/README.pl.md) | opcjonalna | 1.3 | gotowa |

## M2 · Przeszukiwanie

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 2.1 | [Przestrzeń stanów i drzewo przeszukiwania](modules/02_search/01_state_space/README.pl.md) | core | 1.3 | gotowa |
| 2.2 | [BFS i DFS](modules/02_search/02_bfs_dfs/README.pl.md) | core | 2.1 | gotowa |
| 2.3 | [Przeszukiwanie kosztowe (UCS)](modules/02_search/03_uniform_cost_search/README.pl.md) | core | 2.2 | gotowa |
| 2.4 | [Heurystyki, greedy best-first i A*](modules/02_search/04_heuristics_and_a_star/README.pl.md) | core | 2.3 | gotowa |
| 2.5 | [Porównanie strategii przeszukiwania](modules/02_search/05_comparing_strategies/README.pl.md) | core | 2.4 | gotowa |
| 2.6 | [Iteracyjne pogłębianie](modules/02_search/06_iterative_deepening/README.pl.md) | opcjonalna | 2.5 | gotowa |
| 2.7 | [Projektowanie heurystyk](modules/02_search/07_designing_heuristics/README.pl.md) | opcjonalna | 2.5 | gotowa |

## M3 · Gry i problemy z ograniczeniami

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 3.1 | [Gry i minimax](modules/03_games_and_csp/01_minimax/README.pl.md) | core | 2.5 | gotowa |
| 3.2 | [Przycinanie alfa-beta](modules/03_games_and_csp/02_alpha_beta/README.pl.md) | core | 3.1 | gotowa |
| 3.3 | [Funkcje oceny i ograniczona głębokość](modules/03_games_and_csp/03_evaluation_functions/README.pl.md) | core | 3.2 | gotowa |
| 3.4 | Modelowanie problemów z ograniczeniami | core | 2.5 | w przygotowaniu |
| 3.5 | Backtracking z heurystykami i forward checking | core | 3.4 | w przygotowaniu |
| 3.6 | Propagacja ograniczeń AC-3 | opcjonalna | 3.5 | w przygotowaniu |
| 3.7 | Expectimax: gry z losowością | opcjonalna | 3.3 | w przygotowaniu |
| 3.8 | Monte Carlo Tree Search | opcjonalna | 3.3 | w przygotowaniu |

## M4 · Algorytmy inspirowane naturą

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 4.1 | Przeszukiwanie lokalne i symulowane wyżarzanie | core | 2.5 | w przygotowaniu |
| 4.2 | Algorytmy genetyczne | core | 4.1 | w przygotowaniu |
| 4.3 | Optymalizacja mrowiskowa (ACO) | core | 4.2 | w przygotowaniu |
| 4.4 | Optymalizacja rojem cząstek (PSO) | opcjonalna | 4.3 | w przygotowaniu |
| 4.5 | Algorytm genetyczny dla harmonogramu | opcjonalna | 4.3, 3.5 | w przygotowaniu |
| 4.6 | Boidy i emergencja | opcjonalna | 4.3 | w przygotowaniu |
| 4.7 | Krytycznie o „zoo metafor” | opcjonalna | 4.3 | w przygotowaniu |

## M5 · Wiedza, logika i wnioskowanie

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 5.1 | Reprezentacja wiedzy i logika zdań | core | 1.3 | w przygotowaniu |
| 5.2 | Reguły i wnioskowanie w przód | core | 5.1 | w przygotowaniu |
| 5.3 | Wnioskowanie wstecz i system ekspertowy | core | 5.2 | w przygotowaniu |
| 5.4 | Rezolucja | opcjonalna | 5.3 | w przygotowaniu |
| 5.5 | Wprowadzenie do logiki pierwszego rzędu | opcjonalna | 5.3 | w przygotowaniu |

## M6 · Niepewność i prawdopodobieństwo

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 6.1 | Prawdopodobieństwo warunkowe i twierdzenie Bayesa | core | 0.1 | w przygotowaniu |
| 6.2 | Wnioskowanie probabilistyczne i sieci bayesowskie | core | 6.1 | w przygotowaniu |
| 6.3 | Decyzje przy niepewności | core | 6.2 | w przygotowaniu |
| 6.4 | Lokalizacja robota filtrem Bayesa | opcjonalna | 6.3 | w przygotowaniu |
| 6.5 | Wartość informacji | opcjonalna | 6.3 | w przygotowaniu |
| 6.6 | Naiwny klasyfikator Bayesa | opcjonalna | 6.3 | w przygotowaniu |

## M7 · Podstawy uczenia maszynowego i sieci neuronowych

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 7.1 | Uczenie z danych i kNN | core | 5.3 | w przygotowaniu |
| 7.2 | Generalizacja i przeuczenie | core | 7.1 | w przygotowaniu |
| 7.3 | Perceptron i mała sieć neuronowa | core | 7.2 | w przygotowaniu |
| 7.4 | Grupowanie k-means | opcjonalna | 7.3 | w przygotowaniu |
| 7.5 | Drzewa decyzyjne | opcjonalna | 7.3 | w przygotowaniu |
| 7.6 | Regresja liniowa | opcjonalna | 7.3 | w przygotowaniu |
| 7.7 | Neuroewolucja | opcjonalna | 7.3, 4.2 | w przygotowaniu |

## M8 · Uczenie ze wzmocnieniem

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 8.1 | Eksploracja i eksploatacja: wielorękie bandyty | core | 2.5, 6.3 | w przygotowaniu |
| 8.2 | MDP i Q-learning | core | 8.1 | w przygotowaniu |
| 8.3 | Iteracja wartości | opcjonalna | 8.2 | w przygotowaniu |
| 8.4 | Kształtowanie nagrody i niezamierzone zachowania | opcjonalna | 8.2 | w przygotowaniu |

## M9 · Współczesna AI i odpowiedzialność

| ID | Lekcja | Rodzaj | Wymaga | Status |
|---|---|---|---|---|
| 9.1 | Modele generatywne i językowe | core | 6.3, 7.3 | w przygotowaniu |
| 9.2 | Ograniczenia i odpowiedzialność | core | 9.1 | w przygotowaniu |
| 9.3 | Tokenizacja | opcjonalna | 9.2 | w przygotowaniu |
| 9.4 | Ocena odpowiedzi systemów AI | opcjonalna | 9.2 | w przygotowaniu |
