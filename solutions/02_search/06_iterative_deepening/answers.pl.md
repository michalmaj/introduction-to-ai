[English](answers.md) | **Polski**

# Lekcja 2.6 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/06_iterative_deepening/README.pl.md).

## Część A

<!-- generated:trace-table algorithm=ids example=exercise lang=pl -->
| Krok | Limit | Zdjęty (głębokość) | Wynik | Stos (od wierzchu) |
|---|---|---|---|---|
| 1 | 0 | A (0) | odcięty | — |
| 2 | 1 | A (0) | rozwinięty | B, C |
| 3 | 1 | B (1) | odcięty | C |
| 4 | 1 | C (1) | odcięty | — |
| 5 | 2 | A (0) | rozwinięty | B, C |
| 6 | 2 | B (1) | rozwinięty | A, C, D, C |
| 7 | 2 | A (2) | odcięty | C, D, C |
| 8 | 2 | C (2) | odcięty | D, C |
| 9 | 2 | D (2) | odcięty | C |
| 10 | 2 | C (1) | rozwinięty | A, B, F |
| 11 | 2 | A (2) | odcięty | B, F |
| 12 | 2 | B (2) | odcięty | F |
| 13 | 2 | F (2) | odcięty | — |
| 14 | 3 | A (0) | rozwinięty | B, C |
| 15 | 3 | B (1) | rozwinięty | A, C, D, C |
| 16 | 3 | A (2) | cykl | C, D, C |
| 17 | 3 | C (2) | rozwinięty | A, B, F, D, C |
| 18 | 3 | A (3) | odcięty | B, F, D, C |
| 19 | 3 | B (3) | odcięty | F, D, C |
| 20 | 3 | F (3) | odcięty | D, C |
| 21 | 3 | D (2) | rozwinięty | B, E, C |
| 22 | 3 | B (3) | odcięty | E, C |
| 23 | 3 | E (3) | odcięty | C |
| 24 | 3 | C (1) | rozwinięty | A, B, F |
| 25 | 3 | A (2) | cykl | B, F |
| 26 | 3 | B (2) | rozwinięty | A, C, D, F |
| 27 | 3 | A (3) | odcięty | C, D, F |
| 28 | 3 | C (3) | odcięty | D, F |
| 29 | 3 | D (3) | odcięty | F |
| 30 | 3 | F (2) | rozwinięty | C, E, H |
| 31 | 3 | C (3) | odcięty | E, H |
| 32 | 3 | E (3) | odcięty | H |
| 33 | 3 | H (3) | cel | — |

Cel **H** znaleziony przy limicie 3. Ścieżka: A → C → F → H.
<!-- /generated -->

Odpowiedź: `IDS_EXPANSIONS_PER_ITERATION = [0, 1, 3, 7]`.

W rundzie z limitem 3 rozwijane są: `A`, `B`, `C` (przez `B`), `D` (przez `B`), `C` (bezpośrednio z `A`), `B` (przez `C`) i `F` (przez `C`). Warto zauważyć dwie rzeczy:

- **Cykle pojawiają się dopiero przy limicie 3.** `A` na głębokości 2 (ścieżki A → B → A i A → C → A) to cykl. Przy limicie 2 ten sam węzeł leży na granicy, a limit sprawdzamy przed cyklem, więc liczy się jako odcięty.
- **Ścieżki nadmiarowe nie są cyklami.** `C` przez `B` i `B` przez `C` to stany, które pojawiają się w drzewie drugi raz, ale nie na tej samej ścieżce. IDS rozwija je, bo pamięta tylko bieżącą ścieżkę. To jest właśnie koszt, który w magazynie rośnie do tysięcy rozwinięć.

Typowe pomyłki: rozwijanie węzłów cyklu (w ostatniej rundzie wychodzi wtedy 9), liczenie odciętych węzłów jako rozwiniętych albo pominięcie rundy z limitem 0.

## Część B

Rozwiązanie wzorcowe używa stosu, jak DFS z lekcji 2.2, i sprawdza warunki w kolejności: cel, limit, cykl. Alternatywa [recursive_dls.py](alternatives/recursive_dls.py) to wersja rekurencyjna. Funkcja wywołuje się dla każdego dziecka, a odcięcie przekazuje w górę: jeśli któreś wywołanie zwróciło `CUTOFF`, cała gałąź zwraca `CUTOFF`. Przy głębokościach z tej lekcji rekurencja jest bezpieczna, bo stos wywołań Pythona ma limit około 1000 poziomów.

## Pytania kontrolne

### 1. `CUTOFF` a `None`

`CUTOFF` znaczy: przy tym limicie celu nie znalazłem, ale coś odciąłem, więc głębiej cel może istnieć. `None` znaczy: niczego nie odciąłem i celu nie ma nigdzie. Gdyby oba przypadki dawały ten sam wynik, IDS nie wiedziałby, czy szukać dalej. Jeśli oba oznaczałyby „szukaj dalej”, IDS na skończonym grafie bez celu nigdy by się nie zatrzymał. Jeśli oba oznaczałyby „koniec”, poddałby się już po rundzie z limitem 0.

Dobra odpowiedź zawiera:

- znaczenie obu wyników;
- skutek pomylenia ich w jedną albo w drugą stronę.

### 2. Dlaczego IDS znajduje najkrótszą trasę

Runda z limitem *L* sprawdza test celu dla każdego węzła o głębokości co najwyżej *L*. Jeśli runda z limitem *L* − 1 skończyła się odcięciem, to żaden stan na głębokości mniejszej niż *L* nie jest celem. Cel znaleziony w rundzie *L* leży więc na głębokości dokładnie *L*, a krótszej trasy nie ma. Kolejność w obrębie rundy (w głąb) nie ma znaczenia, bo liczy się tylko to, że rundy idą po kolei.

Dobra odpowiedź zawiera:

- uwagę, że limity rosną po kolei;
- argument, że wcześniejsza runda wykluczyła płytsze cele;
- wniosek o najkrótszej trasie przy jednakowych kosztach.

### 3. Koszt powtórzeń

Najwięcej węzłów leży na najgłębszym poziomie, a ten IDS przechodzi tylko raz. Poziomy płytsze są powtarzane, ale są małe: każdy jest *b* razy mniejszy od następnego. Łączna praca IDS to w przybliżeniu praca BFS pomnożona przez 1 + 1/*b* + 1/*b*<sup>2</sup> + … = *b*/(*b* − 1). Dla *b* = 2 stosunek dąży do 2: IDS rozwija mniej więcej dwa razy więcej węzłów niż BFS. W eksperymencie przy *d* = 8 wyszło 502 wobec 255, czyli 1,97.

Dobra odpowiedź zawiera:

- uwagę, że najgłębszy poziom dominuje i jest przechodzony raz;
- szereg geometryczny albo wzór *b*/(*b* − 1);
- wynik dla *b* = 2.

### 4. IDS w magazynie

Na drzewie do każdego węzła prowadzi jedna droga, więc IDS powtarza tylko płytkie poziomy. W magazynie do pola prowadzi bardzo wiele dróg bez powtórzeń (ścieżek nadmiarowych z lekcji 2.1). IDS sprawdza cykle tylko na bieżącej ścieżce, więc każdą z tych dróg przechodzi osobno, i to w każdej rundzie. BFS pamięta osiągnięte stany i każde pole rozwija raz. Na otwartej podłodze IDS rozwinął 9097 węzłów wobec 89 w BFS.

Dobra odpowiedź zawiera:

- różnicę: jedna droga w drzewie, wiele dróg w siatce;
- informację, że IDS nie pamięta odwiedzonych stanów;
- wniosek, że ścieżki nadmiarowe mnożą jego pracę.

### 5. Pamięć dla *b* = 10 i *d* = 10

IDS trzyma na stosie bieżącą ścieżkę i rodzeństwo jej węzłów, czyli około *b*·*d* = 100 węzłów. BFS w najgorszym razie trzyma całą falę na głębokości *d*, czyli rzędu *b*<sup>*d*</sup> = 10<sup>10</sup> węzłów. Przy kilkudziesięciu bajtach na węzeł to setki gigabajtów, a więc więcej, niż ma zwykły komputer.

Dobra odpowiedź zawiera:

- oszacowanie O(*b*·*d*) dla IDS i O(*b*<sup>*d*</sup>) dla BFS;
- konkretne liczby;
- wniosek, że BFS nie zmieści się w pamięci.

## Eksperymenty

Wyniki implementacji wzorcowych. Liczby rozwinięć IDS na drzewach nie zależą od sposobu zapisu, a w magazynie mogą się nieco różnić, jeśli Twoja wersja inaczej rozstrzyga kolejność dzieci.

| *b* | *d* | BFS | IDS | IDS / BFS | Frontier BFS | Frontier IDS |
|---|---|---|---|---|---|---|
| 2 | 8 | 255 | 502 | 1,97 | 255 | 9 |
| 3 | 8 | 3280 | 4916 | 1,50 | 6559 | 17 |
| 4 | 8 | 21 845 | 29 124 | 1,33 | 65 533 | 25 |

| Mapa | Kroki trasy | BFS | IDS (rundy) |
|---|---|---|---|
| `small` | 6 | 10 | 32 (7) |
| `aisles` | 21 | 144 | 3497 (22) |
| `open_floor` | 10 | 89 | 9097 (11) |
| `depot` | 32 | 137 | 12 388 (33) |

- **Eksperyment 1.** Stosunki pracy dążą do 2, 1,5 i 1,33, czyli dokładnie do *b*/(*b* − 1). Frontier BFS rośnie *b* razy z każdym poziomem, a frontier IDS tylko o *b* − 1 węzłów: przy *b* = 3 i *d* = 8 to 6559 wobec 17.
- **Eksperyment 2.** W magazynie IDS przegrywa z BFS wielokrotnie: od 3 razy na małej mapie do ponad 100 razy na otwartej podłodze. Na otwartej podłodze z prawie każdego pola można jechać w czterech kierunkach, więc liczba dróg bez powtórzeń rośnie prawie tak szybko jak drzewo z lekcji 2.1. W alejkach wybór jest mniejszy, więc wykres rośnie wolniej. IDS opłaca się tam, gdzie ścieżek nadmiarowych jest mało, a pamięci brakuje: w drzewach i w ogromnych przestrzeniach, w których BFS nie zmieściłby się w pamięci.
