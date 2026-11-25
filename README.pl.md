[English](README.md) | **Polski**

# Podstawy sztucznej inteligencji

Samodzielny samouczek podstaw sztucznej inteligencji w Pythonie. Cały kurs krąży wokół jednego pytania: **jak maszyna reprezentuje problemy, rozumuje, podejmuje decyzje i rozwiązuje problemy?**

Samouczek obejmuje przeszukiwanie, gry i problemy z ograniczeniami, algorytmy inspirowane naturą, wiedzę i wnioskowanie, niepewność, podstawy uczenia maszynowego, uczenie ze wzmocnieniem oraz współczesną AI. Większość lekcji łączy teorię, przykład prześledzony krok po kroku, zadanie programistyczne z samodzielnym sprawdzaniem i eksperymenty. Lekcje koncepcyjne składają się z tekstu, pytań i odpowiedzi wzorcowych. Zadania rozgrywają się w jednym świecie: w zautomatyzowanym magazynie, po którym jeździ robot dostawczy.

**Zacznij tutaj:** [lekcja 0.1 Instalacja i praca z samouczkiem](modules/00_start/01_setup/README.pl.md).

## Dla kogo

Dla osób, które znają Pythona na poziomie programowania obiektowego i mają za sobą podstawy statystyki. Potrzebną matematykę, na przykład logikę i rachunek prawdopodobieństwa, samouczek wprowadza sam.

## Przygotowanie

Potrzebujesz narzędzia [uv](https://docs.astral.sh/uv/getting-started/installation/). Samo pobierze odpowiednią wersję Pythona.

```bash
git clone https://github.com/michalmaj/introduction-to-ai.git
cd introduction-to-ai
uv sync
```

Notebooki z eksperymentami otworzysz poleceniem:

```bash
uv run jupyter lab
```

## Jak pracować z lekcją

Każda lekcja to katalog w `modules/`, na przykład `modules/02_search/02_bfs_dfs/`.

1. Przeczytaj `README.pl.md` lekcji: teorię, przykład prześledzony krok po kroku i treść zadań.
2. Uzupełnij `task.py`. To jedyny plik, który edytujesz.
3. Sprawdź swoją pracę z głównego katalogu repozytorium:

   ```bash
   uv run pytest modules/02_search/02_bfs_dfs
   ```

4. Otwórz `experiments.pl.ipynb` i wykonaj eksperymenty. Przed uruchomieniem każdej komórki zapisz, czego się spodziewasz.
5. Dopiero po własnej próbie porównaj się z rozwiązaniem w `solutions/`.

Przechodzące testy oznaczają, że implementacja spełnia wymagania zadania. Nie są dowodem zrozumienia, dlatego każda lekcja opisuje też, czego jej testy nie sprawdzają.

## Mapa kursu

Lekcje dzielą się na **core**, które tworzą ścieżkę minimalną, oraz **opcjonalne**, które ją rozszerzają. Pełną listę modułów i lekcji, ich zależności i stan przygotowania znajdziesz w [mapie kursu](COURSE_MAP.pl.md).

## Rozwiązania

Rozwiązania wzorcowe są publiczne i leżą w katalogu [`solutions/`](solutions/README.pl.md). Zadania służą nauce, a nie ocenie. Najwięcej zyskasz, jeśli porównasz rozwiązanie wzorcowe z własną próbą, zamiast czytać je w jej miejsce.

## Licencje

- Kod: [MIT](LICENSE).
- Treści dydaktyczne, czyli teksty lekcji, treści zadań, odpowiedzi i tekst w notebookach: [CC BY-SA 4.0](LICENSE-CONTENT.md).
