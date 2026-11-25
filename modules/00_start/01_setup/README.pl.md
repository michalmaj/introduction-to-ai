[English](README.md) | **Polski**

# Lekcja 0.1 — Instalacja i praca z samouczkiem

**Core** · Wymagania: brak. To pierwsza lekcja kursu.

## Cele lekcji

Po tej lekcji:

- uruchomisz kurs na swoim komputerze;
- będziesz wiedzieć, z czego składa się każda lekcja i jak z nią pracować;
- uruchomisz testy lekcji i odczytasz ich komunikaty;
- poznasz świat zadań, czyli mapę magazynu i konwencję współrzędnych `(wiersz, kolumna)`.

## Instalacja

### 1. Git i uv

Potrzebujesz dwóch narzędzi:

- **Git** do pobrania kursu: [git-scm.com/downloads](https://git-scm.com/downloads);
- **uv** do Pythona i bibliotek: [instrukcja instalacji](https://docs.astral.sh/uv/getting-started/installation/).

Instalacja uv na macOS i Linuksie:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Instalacja uv na Windowsie, w PowerShellu:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Po instalacji otwórz **nowe** okno terminala i sprawdź, czy wszystko działa: `uv --version`.

### 2. Kurs

```bash
git clone https://github.com/michalmaj/introduction-to-ai.git
cd introduction-to-ai
uv sync
```

`uv sync` pobiera odpowiednią wersję Pythona i biblioteki do katalogu `.venv` wewnątrz projektu. Nic nie instaluje w systemie i nie zmienia innych projektów.

### 3. Pierwsze uruchomienie testów

Z głównego katalogu kursu:

```bash
uv run pytest modules/00_start/01_setup
```

Spodziewany wynik: **testy oblewają**. Tak ma być, bo zadanie z tej lekcji nie jest jeszcze rozwiązane. Jeśli zamiast listy testów widzisz błąd w rodzaju „command not found”, zajrzyj do sekcji „Jeśli utkniesz”.

### 4. Jupyter

```bash
uv run jupyter lab
```

W przeglądarce otworzy się JupyterLab. Notebooki z eksperymentami leżą w katalogach lekcji, na przykład `modules/00_start/01_setup/experiments.pl.ipynb`.

## Jak zbudowana jest lekcja

Każda lekcja to katalog w `modules/`:

| Plik | Do czego służy |
|---|---|
| `README.pl.md` | teoria, przykłady i treść zadań; czytasz go najpierw |
| `task.py` | jedyny plik, który edytujesz: część A to odpowiedzi „na papierze”, część B to kod |
| `test_task.py` | testy, które sprawdzają `task.py`; nie musisz ich czytać ani zmieniać |
| `experiments.pl.ipynb` | eksperymenty: najpierw przewidujesz, potem uruchamiasz i porównujesz |

Rozwiązania i odpowiedzi do pytań leżą w osobnym katalogu `solutions/`. Są publiczne, ale zaglądaj do nich dopiero po własnej próbie.

Rytm pracy jest zawsze ten sam:

1. Przeczytaj `README.pl.md`.
2. Uzupełnij `task.py`.
3. Uruchom testy lekcji i poprawiaj, aż przejdą.
4. Wykonaj eksperymenty w notebooku.
5. Odpowiedz na pytania kontrolne, a dopiero potem porównaj się z `solutions/`.

Lekcje **core** tworzą ścieżkę minimalną, a lekcje **opcjonalne** ją rozszerzają. Pełną listę znajdziesz w [mapie kursu](../../../COURSE_MAP.pl.md).

## Jak czytać komunikaty testów

Przykładowy wynik na nierozwiązanym zadaniu:

```text
FAILED modules/00_start/01_setup/test_task.py::test_part_a_start - Part A: fill in START in task.py
```

- Nazwa testu (`test_part_a_start`) mówi, co jest sprawdzane. Testy `test_part_a_...` sprawdzają odpowiedzi z części A, a pozostałe sprawdzają kod.
- Po myślniku jest wskazówka. Komunikaty są po angielsku, jak cały kod kursu.
- Komunikaty nigdy nie zdradzają poprawnej odpowiedzi do części A. Mówią tylko, że jeszcze jej nie ma albo że jest błędna.

Przechodzące testy oznaczają, że kod spełnia wymagania zadania. Nie dowodzą, że rozumiesz, dlaczego działa. Do tego służą eksperymenty i pytania kontrolne.

## Świat zadań: magazyn

Większość zadań w kursie rozgrywa się w zautomatyzowanym magazynie. Mapa to zwykły plik tekstowy, na przykład `data/maps/small.txt`:

```text
#######
#R..#.#
#.#...#
#...#D#
#######
```

- `#` to przeszkoda, czyli ściana albo regał;
- `.` to wolna podłoga;
- `R` to pole, na którym startuje robot;
- `D` to rampa, do której robot często ma dojechać.

W dalszych lekcjach dojdą jeszcze paczki, oznaczane `P`.

**Współrzędne.** Pole opisujemy parą `(wiersz, kolumna)`. Wiersze liczymy od góry, kolumny od lewej, oba od zera:

```text
          kolumna
          0123456
wiersz 0  #######
       1  #R..#.#
       2  #.#...#
       3  #...#D#
       4  #######
```

Lewy górny róg to `(0, 0)`, a pole `(2, 3)` leży w wierszu 2 i kolumnie 3. Najpierw zawsze podajemy wiersz. Tak samo jak przy indeksowaniu list w Pythonie: najpierw wiersz, potem element w wierszu.

**Kierunki.** Robot porusza się w czterech kierunkach:

- `N` (północ): wiersz − 1;
- `E` (wschód): kolumna + 1;
- `S` (południe): wiersz + 1;
- `W` (zachód): kolumna − 1.

W kodzie mapę wczytasz poleceniem `WarehouseMap.from_file(...)`. Wywołanie `warehouse.is_free(pole)` mówi, czy robot może stanąć na danym polu: czy leży ono na mapie i czy nie jest przeszkodą.

## Częste błędy

1. **Zamiana wiersza z kolumną.** Kto myśli o polu jak o punkcie `(x, y)` na wykresie, łatwo zapisze najpierw kolumnę. Wtedy wszystkie kierunki obracają się o 90°.
2. **Zapominanie o przeszkodach.** Pole obok robota nie jest wolne tylko dlatego, że leży na mapie.
3. **Wychodzenie poza mapę.** Mapa nie musi mieć ścian na brzegach. Pole spoza mapy nie istnieje, więc nie może być wolnym sąsiadem. `is_free` sprawdza to za Ciebie.

## Zadanie

### Część A: odczytaj mapę

W `task.py` wpisz współrzędne pól `R` i `D` z mapy `data/maps/small.txt`: `START` i `DOCK`, każde jako para `(wiersz, kolumna)`.

### Część B: wolni sąsiedzi

Zaimplementuj `free_neighbours(warehouse, cell)`. Funkcja zwraca listę wolnych pól sąsiadujących z `cell` w kolejności N, E, S, W. Do sprawdzania, czy pole jest wolne, użyj `warehouse.is_free`.

### Jak sprawdzić

```bash
uv run pytest modules/00_start/01_setup
```

### Kryteria akceptacji

- Wszystkie testy lekcji przechodzą.
- Potrafisz odpowiedzieć na pytania kontrolne.

## Czego testy nie sprawdzają

- **Zrozumienia rytmu pracy.** Testy sprawdzają tylko kod i odpowiedzi.
- **Wszystkich możliwych map.** Testy sprawdzają kilka pól na mapie `small` i na małej mapie bez ścian na brzegach.
- **Stylu i czytelności kodu.**

## Eksperymenty

Otwórz [experiments.pl.ipynb](experiments.pl.ipynb). Notebook sprawdza, czy środowisko działa, rysuje mapę i pokazuje wolnych sąsiadów pola startowego. Przed uruchomieniem zapisz, których sąsiadów się spodziewasz.

## Pytania kontrolne

1. Dlaczego zaraz po pobraniu kursu testy lekcji oblewają i dlaczego to dobrze?
2. Które pole ma współrzędne `(0, 0)`? Dlaczego zapisujemy `(wiersz, kolumna)`, a nie `(x, y)`?
3. Czym różni się `uv run pytest modules/00_start/01_setup` od samego `uv run pytest` uruchomionego z głównego katalogu?

## Jeśli utkniesz

<details>
<summary>„uv: command not found” albo „uv nie jest rozpoznawany”</summary>

Zamknij terminal i otwórz nowy, bo instalator dopisuje uv do ścieżki dopiero dla nowych okien. Jeśli to nie pomoże, wróć do [instrukcji instalacji uv](https://docs.astral.sh/uv/getting-started/installation/) dla swojego systemu.

</details>

<details>
<summary>pytest uruchamia nie te testy albo nie znajduje lekcji</summary>

Sprawdź, czy jesteś w głównym katalogu kursu (tym, w którym leży `pyproject.toml`), i czy podajesz ścieżkę do lekcji: `uv run pytest modules/00_start/01_setup`. Samo `uv run pytest` uruchamia testy samego kursu, a nie lekcji.

</details>

<details>
<summary>Testy nie widzą moich zmian</summary>

Zapisz `task.py` przed uruchomieniem testów. W notebooku pierwsza komórka włącza automatyczne przeładowanie, więc zmiany w `task.py` są widoczne bez restartu.

</details>

## Co zapamiętać

- Kurs uruchamiasz trzema poleceniami: `git clone`, `uv sync`, `uv run ...`.
- Każda lekcja ma ten sam rytm: README, `task.py`, testy, eksperymenty, pytania kontrolne, rozwiązania.
- Pole to para `(wiersz, kolumna)` liczona od zera od lewego górnego rogu.
- Przechodzące testy to warunek konieczny, ale nie dowód zrozumienia.

## Co dalej

- Po własnej próbie porównaj się z [rozwiązaniem i odpowiedziami](../../../solutions/00_start/01_setup/).
- Następna lekcja: [1.1 Czym jest AI](../../01_agents/01_what_is_ai/README.pl.md).
