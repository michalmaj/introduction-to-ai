[English](answers.md) | **Polski**

# Lekcja 0.1 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/00_start/01_setup/README.pl.md).

## Część A

`START = (1, 1)` i `DOCK = (3, 5)`. `R` leży w wierszu 1 (drugim od góry) i kolumnie 1. `D` leży w wierszu 3 i kolumnie 5.

## Pytania kontrolne

### 1. Dlaczego testy oblewają zaraz po pobraniu kursu

Plik `task.py` w nowo pobranym kursie jest szkieletem: odpowiedzi z części A są puste, a funkcje zgłaszają `NotImplementedError`. Testy sprawdzają Twoją pracę, więc dopóki jej nie ma, muszą oblewać. Gdyby przechodziły na pustym szkielecie, niczego by nie sprawdzały. Przejście od czerwonych do zielonych testów pokazuje, że to Twój kod spełnia wymagania.

Dobra odpowiedź zawiera:

- informację, że `task.py` jest na początku nieuzupełniony;
- wniosek, że testy, które przechodzą na pustym szkielecie, byłyby bezwartościowe.

### 2. Współrzędne `(0, 0)` i kolejność `(wiersz, kolumna)`

`(0, 0)` to lewy górny róg mapy, czyli pierwszy znak pierwszej linii pliku. Zapisujemy `(wiersz, kolumna)`, bo tak indeksuje się dane ułożone w wiersze: mapa to lista linii, więc najpierw wybieramy linię (wiersz), a potem znak w niej (kolumnę). Zapis `(x, y)` z wykresów ma odwrotną kolejność i oś *y* skierowaną w górę. Pomylenie tych konwencji obraca kierunki.

Dobra odpowiedź zawiera:

- `(0, 0)` jako lewy górny róg;
- uzasadnienie przez indeksowanie wierszy, a potem znaków;
- uwagę, że `(x, y)` ma inną kolejność i inny kierunek osi.

### 3. `uv run pytest modules/...` a samo `uv run pytest`

Polecenie ze ścieżką uruchamia testy tej jednej lekcji, które sprawdzają Twój `task.py`. Samo `uv run pytest` w katalogu głównym uruchamia testy samego kursu, czyli jego narzędzi i biblioteki, a nie lekcji. Przejdą nawet wtedy, gdy żadna lekcja nie jest rozwiązana, dlatego pytest wypisuje wtedy przypomnienie, jak sprawdzić lekcję.

Dobra odpowiedź zawiera:

- informację, że ścieżka wybiera testy konkretnej lekcji;
- informację, że samo `uv run pytest` sprawdza kurs, a nie Twoją pracę.
