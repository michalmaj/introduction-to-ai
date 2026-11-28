[English](answers.md) | **Polski**

# Lekcja 3.3 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/03_games_and_csp/03_evaluation_functions/README.pl.md).

## Część A

Odpowiedź:

```python
EVAL_VALUES = [-1, 3, 1]
DEPTH_ONE_MOVE = (2, 0)
```

**Wartości *e*.** Linii jest 8. Dla X otwarte są linie bez kółka, a dla O linie bez krzyżyka.

| Pozycja | Otwarte dla X | Otwarte dla O | *e* |
|---|---|---|---|
| `X..` / `.O.` / `...` | 8 − 4 = 4 (kółko w środku leży na 4 liniach) | 8 − 3 = 5 (krzyżyk w rogu leży na 3) | −1 |
| `X.O` / `.X.` / `...` | 8 − 3 = 5 | 8 − 6 = 2 (krzyżyki w rogu i w środku leżą razem na 6 liniach) | 3 |
| `X..` / `.O.` / `..X` | 8 − 4 = 4 | 8 − 5 = 3 (dwa krzyżyki w przeciwległych rogach: 5 linii, bo przekątną dzielą) | 1 |

Najczęstsza pomyłka to pominięcie pustych linii, które są otwarte dla obu graczy, albo dwukrotne liczenie przekątnej, na której leżą oba krzyżyki z trzeciej pozycji.

**Ruch przy głębokości 1.** X ma pięć ruchów. *e* pozycji po każdym z nich:

| Ruch X | Pozycja po ruchu | Otwarte dla X | Otwarte dla O | *e* |
|---|---|---|---|---|
| (0, 1) | `XX.` / `.OX` / `.O.` | 3 | 2 | 1 |
| (0, 2) | `X.X` / `.OX` / `.O.` | 3 | 2 | 1 |
| (1, 0) | `X..` / `XOX` / `.O.` | 3 | 3 | 0 |
| (2, 0) | `X..` / `.OX` / `XO.` | 3 | 1 | 2 |
| (2, 2) | `X..` / `.OX` / `.OX` | 3 | 2 | 1 |

Największe *e* = 2 daje ruch (2, 0), więc to on jest odpowiedzią. Nie jest to jednak dobry ruch, o czym mówi pytanie kontrolne 3.

## Część B

Rozwiązanie wzorcowe to alfa-beta z lekcji 3.2 z parametrem głębokości: najpierw test końca gry, potem test `d == 0`. Ocena to linie ważone. Każda linia, na której stoją tylko znaki jednego gracza, daje 10<sup>*n* − 1</sup> punktów, gdzie *n* to liczba tych znaków: plus dla gracza, minus dla przeciwnika. Suma *x* jest ściskana do przedziału (−1, 1) wzorem *x* / (1 + |*x*|).

W meczu z testu ta ocena wygrywa 11 partii, remisuje 1 i nie przegrywa żadnej.

Alternatywy:

- [negamax_h_search.py](alternatives/negamax_h_search.py) to negamax z limitem głębokości. Na granicy ocenia pozycję dla gracza, który ma w niej ruch, a rodzic zmienia znak. Przy ocenie symetrycznej, w której to, co dobre dla X, jest tak samo złe dla O, daje to ten sam wynik.
- [open_lines_eval.py](alternatives/open_lines_eval.py) ocenia przez linie otwarte, jak w części A, podzielone przez liczbę linii plus 1. Wygrywa 7 partii, remisuje 5 i nie przegrywa żadnej, więc test przechodzi. Zwraca liczbę typu `numpy.float64`, co jest w porządku.

## Pytania kontrolne

### 1. Użyteczność stanu końcowego na granicy

Stan końcowy ma pewny wynik: wygraną, remis albo przegraną. Ocena to tylko oszacowanie i może się mylić, a jej wartości leżą między −1 a 1, więc pewna wygrana oceniona na przykład na 0,9 przegrałaby z niepewną pozycją ocenioną na 0,95. Przeszukiwanie, które najpierw sprawdza głębokość, potrafi przegapić wygraną w jednym ruchu.

Dobra odpowiedź zawiera:

- różnicę między wynikiem pewnym a oszacowaniem;
- skutek odwrotnej kolejności testów, np. przegapioną wygraną.

### 2. Zakres oceny

Wygrana jest warta 1, a przegrana −1. Gdyby ocena mogła wynosić 50, każda niezakończona pozycja z dobrą oceną wyglądałaby lepiej niż pewna wygrana, a każda słaba gorzej niż przegrana. Program wolałby budować „obiecujące” pozycje, zamiast wygrać od razu, i mógłby wejść w pewną przegraną, żeby uniknąć pozycji z oceną −50.

Dobra odpowiedź zawiera:

- porównanie z wartościami wygranej i przegranej;
- konkretny zły wybór, do którego prowadzi zbyt duża ocena.

### 3. Czy ruch (2, 0) jest dobry?

Nie. O ma kółka w polach (1, 1) i (2, 1), a pole (0, 1) jest wolne, więc grozi ułożeniem środkowej kolumny. Jedynym dobrym ruchem X jest blokada (0, 1). Po każdym innym ruchu O wygrywa. Ocena *e* tej groźby nie widzi, bo liczy tylko linie otwarte, a nie to, ile brakuje do ich zamknięcia. Przeszukiwanie na głębokość 2 widzi odpowiedź O: po (2, 0) O stawia kółko w (0, 1) i wygrywa, co daje użyteczność −1. Dlatego przy głębokości 2 i 3 przeszukiwanie wybiera (0, 1).

Dobra odpowiedź zawiera:

- groźbę O w środkowej kolumnie;
- wyjaśnienie, dlaczego *e* jej nie widzi;
- obserwację, że głębokość 2 dociera do wygranej O i zmienia wybór na (0, 1).

### 4. Efekt horyzontu

Przeszukiwanie nie widzi niczego za granicą głębokości. Jeśli zagrożenie pojawia się tuż za nią, pozycja wygląda na bezpieczną. Przykład z notebooka: w pozycji z dwoma kółkami w pierwszej kolumnie przeszukiwanie na głębokość 1 rozwija własne linie, bo nie widzi, że O dostawi trzecie kółko i będzie miało dwa wolne końce. W szachach klasyczny przykład to odwlekanie nieuniknionej straty figury kolejnymi szachami.

Dobra odpowiedź zawiera:

- definicję: przeszukiwanie nie widzi niczego za granicą głębokości;
- przykład, w którym groźba albo strata leży tuż za horyzontem.

### 5. Głębokość przy limicie czasu

Najlepiej nie wybierać jej z góry, tylko użyć iteracyjnego pogłębiania: szukać na głębokość 1, 2, 3 i tak dalej, aż skończy się czas, i zagrać najlepszy ruch z ostatniego ukończonego przeszukiwania. Każdy kolejny półruch kosztuje kilka do kilkunastu razy więcej niż poprzedni, więc ostatnie, nieukończone przeszukiwanie i tak zajęłoby większość czasu. Powtórzona praca kosztuje mało, a płytsze przeszukiwanie podpowiada kolejność ruchów dla głębszego.

Dobra odpowiedź zawiera:

- iteracyjne pogłębianie z limitem czasu;
- argument, że powtórzona praca jest tania (jak w lekcji 2.6);
- uwagę o kolejności ruchów z płytszego przeszukiwania.

## Eksperymenty

Wyniki implementacji wzorcowej. W trybie `"mine"` wiersz „yours” zależy od Twojej oceny, a pozostałe wiersze powinny wyjść tak samo, jeśli Twoje przeszukiwanie odcina przy ≥ i ogląda ruchy w kolejności `game.actions`.

| Ocena | Głębokość 1 | Głębokość 2 | Głębokość 3 |
|---|---|---|---|
| zerowa | 1 / 2 / 9 | 3 / 6 / 3 | 9 / 1 / 2 |
| linie otwarte | 4 / 4 / 4 | 7 / 5 / 0 | 11 / 1 / 0 |
| linie ważone | 11 / 0 / 1 | 11 / 1 / 0 | 12 / 0 / 0 |

Liczby to wygrane / remisy / porażki w 12 partiach z przeciwnikiem, który szuka na głębokość 2 z oceną zerową.

| Głębokość | Ruch | Ocena | Pozycje (pusta plansza) | Czas ruchu (pusta plansza) |
|---|---|---|---|---|
| 1 | (1, 3) | +0,964 | 26 | < 0,001 s |
| 2 | (3, 0) | −0,800 | 236 | ok. 0,002 s |
| 3 | (3, 0) | +0,976 | 2 360 | ok. 0,02 s |
| 4 | (3, 0) | +0,750 | 21 788 | ok. 0,18 s |

Kolumny „Ruch” i „Ocena” dotyczą pozycji z groźbą z eksperymentu 2, a kolumny „Pozycje” i „Czas” pierwszego ruchu na pustej planszy z eksperymentu 3.

- **Eksperyment 1.** Ocena zerowa z głębokością 1 przegrywa 9 partii, bo wybiera po prostu pierwszy wolny ruch. Z głębokością 3 wygrywa 9, bo widzi wygrane i groźby, których przeciwnik z głębokością 2 nie widzi. Dobra ocena daje więcej niż dodatkowa głębokość: linie ważone wygrywają 11 partii już przy głębokości 1. Najlepiej działa jedno i drugie naraz: linie ważone z głębokością 3 wygrywają wszystkie partie.
- **Eksperyment 2.** Jeśli O dostawi kółko w (3, 0), będzie mieć trzy w kolumnie i dwa wolne końce, a X zablokuje tylko jeden. Jedynie ruch (3, 0) zamyka obie linie, w których O może jeszcze ułożyć cztery. Przeszukiwanie na głębokość 1 widzi tylko pozycję po własnym ruchu, więc wybiera ruch, który najlepiej rozwija linie X. Od głębokości 2 widzi odpowiedź O i blokuje. Oceny skaczą z parzystością głębokości. Przy głębokości nieparzystej ostatni ruch przed horyzontem należy do X, więc ocena jest optymistyczna. Przy parzystej ostatni ruch ma O, więc ocena jest pesymistyczna. To też jest efekt horyzontu.
- **Eksperyment 3.** Każdy kolejny półruch kosztuje około 10 razy więcej pozycji i czasu. To mniej niż liczba ruchów na planszy (około 24), ale więcej niż jej pierwiastek (około 5), więc kolejność ruchów jest daleka od idealnej. Ruch na głębokość 8 kosztowałby około 10<sup>4</sup> razy więcej niż na głębokość 4, czyli około pół godziny. W ciągu sekundy przeszukiwanie zdąży zejść na głębokość 4. Głębokość 5 zajmuje już prawie 2 sekundy.
