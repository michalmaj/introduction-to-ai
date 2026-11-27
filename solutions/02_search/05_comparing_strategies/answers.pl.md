[English](answers.md) | **Polski**

# Lekcja 2.5 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/05_comparing_strategies/README.pl.md).

## Część A

| | `complete_finite` | `complete_infinite` | `optimal_unit_costs` | `optimal_any_costs` |
|---|---|---|---|---|
| BFS | tak | tak | tak | nie |
| DFS | tak | nie | nie | nie |
| UCS | tak | tak | tak | tak |
| greedy | tak | nie | nie | nie |
| A\* | tak | tak | tak | tak |

Uzasadnienia, kolumna po kolumnie:

- **Zupełność na skończonej przestrzeni.** Wszystkie pięć algorytmów to przeszukiwanie grafu: każdy stan rozwijają najwyżej raz (albo, w UCS i A\*, ponownie tylko wtedy, gdy znajdą do niego tańszą drogę, a takich poprawek jest skończenie wiele). Na skończonej przestrzeni każdy z nich w końcu albo znajdzie cel, albo opróżni frontier i zwróci `None`.
- **Zupełność na nieskończonej przestrzeni.**
  - BFS bada przestrzeń warstwami. Cel leży na skończonej głębokości *d*, a każda warstwa jest skończona, bo *b* jest skończone, więc BFS do niego dotrze.
  - UCS rozwija węzły w kolejności kosztu. Węzłów tańszych niż *C*\* jest skończenie wiele, bo każdy krok kosztuje co najmniej *ε*.
  - A\* rozwija tylko węzły o *f* ≤ *C*\*, a ponieważ *f* ≥ *g*, jest ich też skończenie wiele.
  - DFS może zejść w nieskończoną gałąź, w której stany się nie powtarzają.
  - Greedy może iść w nieskończoność za węzłami, które wyglądają na coraz bliższe celu albo równie bliskie.
- **Optymalność przy jednakowych kosztach.**
  - BFS znajduje trasę o najmniejszej liczbie kroków.
  - UCS i A\* znajdują najtańszą trasę, a przy jednakowych kosztach najtańsza to najkrótsza.
  - DFS zwraca pierwszą znalezioną trasę, na przykład pięciokrokową zamiast trzykrokowej w lekcji 2.2.
  - Greedy ignoruje przebyty koszt: na grafie z lekcji 2.4 wybrał trasę o koszcie 12 zamiast 7, a takie kontrprzykłady da się też zbudować przy jednakowych kosztach.
- **Optymalność przy dowolnych kosztach.** Zostają tylko UCS i A\*. BFS minimalizuje liczbę kroków, nie koszt; na mapie `congested.txt` zapłacił 52 zamiast 24.

## Pytania kontrolne

### 1. Dwa różne DFS

DFS z lekcji 2.2 pamięta rozwinięte stany i nie rozwija żadnego stanu drugi raz. Na skończonej przestrzeni stanów może więc wykonać tylko skończenie wiele rozwinięć, a potem albo znajdzie cel, albo opróżni stos. DFS z przykładu rozwiązanego nie pamięta niczego, więc w grafie z cyklem może wracać do tych samych stanów bez końca.

Dobra odpowiedź zawiera:

- różnicę: pamięć rozwiniętych stanów albo jej brak;
- argument o skończonej liczbie rozwinięć;
- przykład cyklu, w którym DFS bez pamięci się zapętla.

### 2. Nieskończona przestrzeń

Przykład: stan to liczba całkowita *n*. Z każdego stanu prowadzą dwie akcje: „+1” i „cel”, gdzie „cel” prowadzi do stanu docelowego. Jeśli DFS najpierw próbuje akcji „+1”, schodzi w nieskończoną gałąź 0, 1, 2, 3, … i nigdy nie wraca. BFS rozwija warstwami, więc już na głębokości 1 znajdzie cel. Ten sam schemat pasuje do magazynu, w którym stan zawiera licznik przejechanych pól.

Dobra odpowiedź zawiera:

- nieskończoną gałąź, w której stany się nie powtarzają;
- wyjaśnienie, dlaczego DFS z niej nie wraca;
- wyjaśnienie, dlaczego BFS znajduje płytki cel.

### 3. A\* a greedy

A\* porządkuje frontier według *g* + *h*. Gdy *h* nie przeszacowuje, węzeł na najtańszej ścieżce ma *f* ≤ *C*\*, więc zostanie zdjęty, zanim A\* zwróci droższy cel. Gdyby *h* przeszacowywała, ten węzeł mógłby czekać we frontier, a A\* zdjąłby wcześniej droższy cel. Greedy w ogóle nie bierze pod uwagę *g*, czyli tego, ile już zapłacił. Nawet idealna heurystyka nie pomaga, jeśli algorytm ignoruje koszt drogi, którą już przebył.

Dobra odpowiedź zawiera:

- rolę dopuszczalności w argumencie optymalności A\*;
- informację, że greedy ignoruje *g*;
- wniosek, że sama dobra heurystyka nie wystarcza do optymalności.

### 4. Pamięć DFS na otwartej podłodze

Wzór O(*b*·*m*) mówi, że frontier DFS rośnie z głębokością *m*, na którą algorytm schodzi. Na otwartej podłodze trasa DFS ma 138 kroków, a przy każdym węźle na tej ścieżce zostaje na stosie kilku niezbadanych sąsiadów. To daje 120 węzłów we frontier. BFS dociera do rampy po 10 krokach i jego fala nie zdąży urosnąć. „Mała pamięć DFS” jest prawdą tylko wtedy, gdy DFS nie schodzi głęboko, a w przeszukiwaniu grafu dochodzi do tego jeszcze zbiór rozwiniętych stanów.

Dobra odpowiedź zawiera:

- zależność frontier DFS od głębokości *m*;
- porównanie z małą głębokością celu dla BFS;
- wniosek, że przewaga DFS zależy od kształtu przestrzeni.

### 5. Mało pamięci, jednakowe koszty

Najlepszy jest wtedy algorytm iteracyjnego pogłębiania (lekcja 2.6). Pamięta tylko bieżącą ścieżkę i jej rodzeństwo, czyli O(*b*·*d*), a przy jednakowych kosztach znajduje najkrótszą trasę, tak jak BFS. Rozsądne są też odpowiedzi: BFS, jeśli mapa jest mała, albo A\* z odległością Manhattan, jeśli zależy nam na szybkości i pamięć wystarczy. Odpowiedź powinna jednak ważyć pamięć i optymalność, a nie tylko szybkość.

Dobra odpowiedź zawiera:

- wybór algorytmu z uzasadnieniem przez pamięć i optymalność;
- świadomość, że DFS jest oszczędny w pamięci, ale nie optymalny;
- najlepiej: iteracyjne pogłębianie.

## Eksperymenty

Wyniki implementacji wzorcowych. Twoje implementacje mogą rozwinąć nieco inną liczbę pól, jeśli inaczej rozstrzygają remisy, ale koszty tras UCS i A\* muszą być takie same.

| Mapa | Algorytm | Kroki | Koszt | Rozwinięcia | Największy frontier |
|---|---|---|---|---|---|
| `congested` | BFS | 18 | 52 | 94 | 8 |
| `congested` | DFS | 22 | 24 | 22 | 4 |
| `congested` | UCS | 22 | 24 | 94 | 8 |
| `congested` | greedy | 18 | 52 | 18 | 4 |
| `congested` | A\* | 22 | 24 | 53 | 8 |
| `depot` | BFS | 32 | 50 | 137 | 6 |
| `depot` | DFS | 48 | 48 | 152 | 23 |
| `depot` | UCS | 38 | 38 | 150 | 9 |
| `depot` | greedy | 32 | 50 | 33 | 14 |
| `depot` | A\* | 38 | 38 | 124 | 16 |

- **Eksperyment 1.** Najtańszą trasę znajdują UCS i A\*, zgodnie z tabelą. BFS i greedy jadą przez zatłoczoną alejkę. Na `depot.txt` DFS znalazł trasę tańszą niż BFS (48 zamiast 50), ale to przypadek kolejności akcji, a nie gwarancja: tabela mówi o tym, co algorytm obiecuje na *każdej* mapie. A\* oszczędza na `congested.txt` 41 pól, a na `depot.txt` tylko 26. Na `depot.txt` aż 125 pól ma *f* ≤ 38, z czego 76 dokładnie *f* = 38: regularna siatka alejek daje mnóstwo równie tanich objazdów, a przy remisach *f* A\* zagląda prawie we wszystkie (to samo zjawisko co w eksperymencie 3 lekcji 2.4). Na `congested.txt` tylko 54 pola mają *f* ≤ 24, bo magazyn po lewej to ślepy zaułek, w który opłaca się zajrzeć tylko tuż przy starcie.
- **Eksperyment 2.** Największy frontier BFS i DFS:

  | Mapa | BFS | DFS |
  |---|---|---|
  | `aisles` | 12 | 23 |
  | `open_floor` | 17 | 120 |
  | `congested` | 8 | 4 |
  | `depot` | 6 | 23 |

  DFS ma mniejszy frontier tylko na `congested.txt`, gdzie jego trasa jest krótka. Na otwartej podłodze schodzi na głębokość 138 kroków i trzyma na stosie rodzeństwo prawie każdego węzła na tej ścieżce.
- **Eksperyment 3.** Liczba rozwinięć rośnie mniej więcej dwukrotnie z każdą paczką: od 101 przy jednej paczce do 7377 przy sześciu (z *h* = 0). Na wykresie logarytmicznym to prawie prosta. Przy 20 paczkach byłoby to rzędu 155 · 2<sup>20</sup>, czyli ponad 160 milionów stanów. Heurystyka „liczba paczek” prawie nic nie daje (6844 zamiast 7377), bo jest bardzo mała w porównaniu z prawdziwym kosztem, który składa się głównie z jazdy. Lepsze heurystyki zaprojektujesz w lekcji 2.7. Na naprawdę duże problemy potrzeba jednak innych metod, opisanych w module 4.
