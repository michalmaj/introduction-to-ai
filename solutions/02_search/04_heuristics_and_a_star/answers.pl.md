[English](answers.md) | **Polski**

# Lekcja 2.4 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/04_heuristics_and_a_star/README.pl.md).

## Część A

### Greedy best-first

<!-- generated:trace-table algorithm=greedy example=astar_exercise lang=pl -->
| Krok | Zdjęty | g | f | Wynik | Frontier: stan f, w kolejności zdejmowania | Najlepsze znane g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 7 | rozwinięty | D 4, B 6, C 8 | A 0, B 2, C 1, D 3 |
| 2 | D | 3 | 4 | rozwinięty | G 0, B 6, C 8 | A 0, B 2, C 1, D 3, G 9 |
| 3 | G | 9 | 0 | cel | B 6, C 8 | A 0, B 2, C 1, D 3, G 9 |

Cel **G** osiągnięty kosztem 9. Ścieżka: A → D → G.
<!-- /generated -->

Odpowiedź: `GREEDY_PATH = ["A", "D", "G"]`.

Po rozwinięciu `A` najmniejsze *h* ma `D` (4), więc greedy idzie do `D`, a stamtąd bezpośrednio do celu. Trasa kosztuje 3 + 6 = 9, a najtańsza 8.

### A*

<!-- generated:trace-table algorithm=astar example=astar_exercise lang=pl -->
| Krok | Zdjęty | g | f | Wynik | Frontier: stan f, w kolejności zdejmowania | Najlepsze znane g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 7 | rozwinięty | D 7, B 8, C 9 | A 0, B 2, C 1, D 3 |
| 2 | D | 3 | 7 | rozwinięty | B 8, C 9, G 9 | A 0, B 2, C 1, D 3, G 9 |
| 3 | B | 2 | 8 | rozwinięty | F 8, C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 9 |
| 4 | F | 6 | 8 | rozwinięty | G 8, C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 8 |
| 5 | G | 8 | 8 | cel | C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 8 |

Cel **G** osiągnięty kosztem 8. Ścieżka: A → B → F → G.
<!-- /generated -->

Odpowiedzi: `ASTAR_EXPANSION_ORDER = ["A", "D", "B", "F"]` i `ASTAR_PATH = ["A", "B", "F", "G"]`.

A\* też najpierw rozwija `D`, bo ma ono najmniejsze *f* = 3 + 4 = 7. Wygenerowany wtedy cel ma jednak *f* = 9, a `B` tylko 2 + 6 = 8, więc A\* nie zatrzymuje się, tylko rozwija `B`, a potem `F`. Rozwinięcie `F` daje tańszą drogę do celu, o koszcie 8, i ten wpis zostaje zdjęty jako następny. Stanów `C` i `E` A\* w ogóle nie rozwija: `C` ma *f* = 1 + 8 = 9, czyli więcej niż koszt najtańszej trasy.

Najczęstsze pomyłki to porównywanie samych *h* zamiast *f* = *g* + *h*, pominięcie `D` w kolejności rozwijania (choć nie leży na zwróconej ścieżce, A\* je rozwija) i zatrzymanie się na pierwszym wygenerowanym celu.

### Dla porównania: UCS

<!-- generated:trace-table algorithm=ucs example=astar_exercise lang=pl -->
| Krok | Zdjęty | g | f | Wynik | Frontier: stan f, w kolejności zdejmowania | Najlepsze znane g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 0 | rozwinięty | C 1, B 2, D 3 | A 0, B 2, C 1, D 3 |
| 2 | C | 1 | 1 | rozwinięty | B 2, E 2, D 3 | A 0, B 2, C 1, D 3, E 2 |
| 3 | B | 2 | 2 | rozwinięty | E 2, D 3, F 6 | A 0, B 2, C 1, D 3, E 2, F 6 |
| 4 | E | 2 | 2 | rozwinięty | D 3, F 6 | A 0, B 2, C 1, D 3, E 2, F 6 |
| 5 | D | 3 | 3 | rozwinięty | F 6, G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 9 |
| 6 | F | 6 | 6 | rozwinięty | G 8, G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 8 |
| 7 | G | 8 | 8 | cel | G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 8 |

Cel **G** osiągnięty kosztem 8. Ścieżka: A → B → F → G.
<!-- /generated -->

UCS rozwija 6 węzłów, w tym `C` i `E`, które leżą w przeciwnym kierunku niż cel, ale są tanie. A\* rozwija tylko 4.

## Część B

Rozwiązanie wzorcowe ma jedną funkcję pomocniczą `best_first(problem, f)`, którą wywołują greedy i A\* z różnymi priorytetami. To jest UCS z lekcji 2.3, w którym koszt ścieżki zastąpiła funkcja priorytetu. Dwie alternatywy też są poprawne:

- [aima_style.py](alternatives/aima_style.py) nie pomija nieaktualnych wpisów, tylko rozwija je jeszcze raz;
- [expanded_set.py](alternatives/expanded_set.py) rozwija każdy stan co najwyżej raz. Dla A\* jest to poprawne, gdy heurystyka jest spójna, a odległość Manhattan w magazynie jest spójna.

## Pytania kontrolne

### 1. Greedy a A*

Greedy best-first porządkuje frontier według *h*, czyli tylko według oszacowania odległości do celu. A\* porządkuje go według *g* + *h*, więc bierze pod uwagę także to, ile już kosztowała droga. Greedy może więc wybrać drogę, która wygląda na bliską celu, ale jest droga. W przykładzie z lekcji greedy idzie z `S` do `B`, bo *h*(`B`) = 3 < *h*(`A`) = 5, i zwraca trasę o koszcie 12, choć najtańsza kosztuje 7. Na mapie `congested.txt` greedy jedzie korytarzem pełnym stref wolnego ruchu i płaci 52 zamiast 24.

Dobra odpowiedź zawiera:

- priorytety obu algorytmów: *h* i *g* + *h*;
- wyjaśnienie, że greedy ignoruje koszt już przebytej drogi;
- przykład, w którym greedy zwraca droższą trasę.

### 2. Dopuszczalność odległości Manhattan

Heurystyka jest dopuszczalna, jeśli nigdy nie przeszacowuje prawdziwego kosztu dojścia do celu: *h*(*n*) ≤ *h*\*(*n*). Każdy ruch robota zmienia wiersz albo kolumnę o 1, więc do rampy potrzeba co najmniej tylu ruchów, ile wynosi odległość Manhattan. Każdy ruch kosztuje co najmniej 1: zwykłe pole 1, strefa wolnego ruchu 3. Prawdziwy koszt jest więc co najmniej równy liczbie ruchów, a ta co najmniej równa odległości Manhattan. Przeszkody i strefy wolnego ruchu mogą prawdziwy koszt tylko podnieść.

Dobra odpowiedź zawiera:

- definicję *h*(*n*) ≤ *h*\*(*n*);
- argument o liczbie ruchów: każdy ruch zmienia odległość najwyżej o 1;
- argument o koszcie: każdy ruch kosztuje co najmniej 1.

### 3. Ruchy po skosie

Nie. Jeden ruch po skosie zmienia jednocześnie wiersz i kolumnę, więc zmniejsza odległość Manhattan o 2, a kosztuje tylko 1. Pole leżące po skosie obok rampy ma odległość Manhattan 2, a prawdziwy koszt 1: heurystyka przeszacowuje, więc nie jest dopuszczalna. W takim świecie dopuszczalna jest odległość Czebyszewa, max(|*w*<sub>1</sub> − *w*<sub>2</sub>|, |*k*<sub>1</sub> − *k*<sub>2</sub>|), bo tyle co najmniej ruchów potrzeba, gdy ruch po skosie jest dozwolony.

Dobra odpowiedź zawiera:

- odpowiedź „nie”;
- przykład pola, dla którego Manhattan przeszacowuje;
- opcjonalnie: heurystykę, która w takim świecie jest dopuszczalna.

### 4. Niemalejące f

Gdy *n′* jest dzieckiem *n*, to *g*(*n′*) = *g*(*n*) + *c*(*n*, *a*, *n′*), więc *f*(*n′*) = *g*(*n*) + *c* + *h*(*n′*). Ze spójności *c* + *h*(*n′*) ≥ *h*(*n*), więc *f*(*n′*) ≥ *g*(*n*) + *h*(*n*) = *f*(*n*). Dzieci mają więc *f* co najmniej takie jak rodzic. Frontier zawsze oddaje węzeł o najmniejszym *f*, a nowe węzły nie mają mniejszego *f* niż ten, który właśnie zdjęto, więc kolejne zdejmowane wartości nie maleją.

Dobra odpowiedź zawiera:

- rachunek *f*(*n′*) ≥ *f*(*n*) z nierówności spójności;
- uwagę, że frontier zawsze zdejmuje najmniejsze *f*;
- wniosek, że kolejne rozwijane *f* nie maleją.

### 5. Skrajne heurystyki

Przy *h* = 0 mamy *f* = *g*, czyli A\* jest dokładnie UCS. Przy *h* = *h*\*, czyli prawdziwym koszcie do celu, wszystkie węzły na najtańszych ścieżkach mają *f* = *C*\*, a wszystkie inne większe *f*. A\* rozwija wtedy tylko węzły na najtańszych ścieżkach (przy wielu równie tanich ścieżkach może zajrzeć na kilka z nich). Taka heurystyka jest jednak równie trudna do policzenia jak samo rozwiązanie.

Dobra odpowiedź zawiera:

- *h* = 0 daje UCS;
- *h* = *h*\* prowadzi prosto po najtańszej ścieżce;
- uwagę, że *h*\* zwykle nie znamy.

### 6. Heurystyka przeszacowująca

Większe *h* sprawia, że A\* bardziej ufa oszacowaniu, a mniej przebytej drodze, i zachowuje się coraz bardziej jak greedy. Rozwija wtedy mniej węzłów, bo wcześniej skreśla kierunki, które wyglądają na dalekie. Traci jednak gwarancję optymalności: może zdjąć cel, zanim zbada tańszą drogę, którą heurystyka niesłusznie uznała za drogą. W eksperymencie 2 odległość Manhattan razy 3 zmniejszyła liczbę rozwinięć z 53 do 18, ale trasa zdrożała z 24 do 52. Dla A\* z heurystyką *w* · *h*, gdzie *h* jest dopuszczalna, wiadomo, że koszt trasy jest co najwyżej *w* razy większy od optymalnego.

Dobra odpowiedź zawiera:

- uwagę, że większe *h* to mniej rozwinięć;
- informację, że przeszacowanie odbiera gwarancję najtańszej trasy;
- przykład albo ograniczenie, o ile trasa może zdrożeć.

## Eksperymenty

Wyniki implementacji wzorcowych. Twoja implementacja może rozwinąć nieco inną liczbę pól, jeśli inaczej rozstrzyga remisy, ale koszty tras A\* z dopuszczalną heurystyką muszą być takie same.

| Mapa | Algorytm i heurystyka | Kroki | Koszt | Rozwinięcia |
|---|---|---|---|---|
| `congested` | UCS | 22 | 24 | 94 |
| `congested` | greedy, Manhattan | 18 | 52 | 18 |
| `congested` | A\*, *h* = 0 | 22 | 24 | 94 |
| `congested` | A\*, euklidesowa | 22 | 24 | 53 |
| `congested` | A\*, Manhattan | 22 | 24 | 53 |
| `congested` | A\*, 2 × Manhattan | 22 | 24 | 32 |
| `congested` | A\*, 3 × Manhattan | 18 | 52 | 18 |
| `aisles` | UCS | 21 | 21 | 147 |
| `aisles` | A\*, euklidesowa | 21 | 21 | 66 |
| `aisles` | A\*, Manhattan | 21 | 21 | 48 |
| `open_floor` | UCS | 10 | 10 | 104 |
| `open_floor` | A\*, euklidesowa | 10 | 10 | 37 |
| `open_floor` | A\*, Manhattan | 10 | 10 | 34 |

- **Eksperyment 1.** Greedy jedzie korytarzem, bo każdy krok w nim zmniejsza odległość Manhattan do rampy o 1. Koszt kroków greedy nie interesuje. A\* jedzie objazdem jak UCS, ale rozwija 53 pola zamiast 94. W magazynie po lewej rozwija tylko 9 pól tuż przy starcie: na przykład pole `(3, 9)` ma *g* = 1 i *h* = 19, czyli *f* = 20 < 24, a pole `(3, 5)` ma *g* = 5 i *h* = 23, czyli *f* = 28 > 24, więc A\* do niego nie zagląda.
- **Eksperyment 2.** *h* = 0 to UCS. Odległość euklidesowa i Manhattan są dopuszczalne i obie dają najtańszą trasę. Na tej mapie rozwijają tyle samo pól, bo o liczbie rozwinięć decydują tu głównie pola przy starcie i alejki, a nie ich drobne różnice. Odległość Manhattan razy 2 nie jest dopuszczalna, na przykład w polu tuż przed rampą daje 2, a prawdziwy koszt to 1. Tutaj A\* miał z nią szczęście i nadal znalazł trasę za 24. Razy 3 heurystyka tak przeważa nad kosztem, że A\* zachowuje się jak greedy i jedzie korytarzem za 52.
- **Eksperyment 3.** Na obu mapach A\* z odległością Manhattan rozwija około trzy razy mniej pól niż UCS. Na otwartej podłodze odległość Manhattan jest prawie równa prawdziwemu kosztowi, a w alejkach regały wymuszają objazdy, więc heurystyka zaniża koszt bardziej. Odległość euklidesowa nigdy nie jest większa od odległości Manhattan, a obie są dopuszczalne, więc A\* z odległością euklidesową rozwija więcej pól: 66 zamiast 48 w alejkach. Większa dopuszczalna heurystyka oznacza mniej pracy. Mówimy, że odległość Manhattan dominuje odległość euklidesową (lekcja 2.7).
