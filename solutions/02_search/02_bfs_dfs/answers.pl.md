[English](answers.md) | **Polski**

# Lekcja 2.2 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/02_bfs_dfs/README.pl.md).

## Część A

### BFS

<!-- generated:trace-table algorithm=bfs example=exercise lang=pl -->
| Krok | Rozwijany węzeł | Frontier (w kolejności zdejmowania) | Zbiór osiągniętych (reached) |
|---|---|---|---|
| 1 | A | B, C | A, B, C |
| 2 | B | C, D | A, B, C, D |
| 3 | C | D, F | A, B, C, D, F |
| 4 | D | F, E | A, B, C, D, E, F |
| 5 | F | E | A, B, C, D, E, F |

Cel **H** znaleziony podczas rozwijania **F**. Ścieżka: A → C → F → H.
<!-- /generated -->

Odpowiedzi: `BFS_EXPANSION_ORDER = ["A", "B", "C", "D", "F"]` i `BFS_PATH = ["A", "C", "F", "H"]`.

BFS rozwija `D` przed `F`, bo `D` trafiło do kolejki wcześniej. Kiedy rozwija `F`, stan `E` jest już osiągnięty (dodało go rozwinięcie `D`), więc zostaje pominięty. Za to `H` jest nowe i jest celem.

### DFS

<!-- generated:trace-table algorithm=dfs example=exercise lang=pl -->
| Krok | Zdjęty węzeł | Wynik | Frontier (w kolejności zdejmowania) | Rozwinięte |
|---|---|---|---|---|
| 1 | A | rozwinięty | B, C | A |
| 2 | B | rozwinięty | C, D, C | A, B |
| 3 | C | rozwinięty | F, D, C | A, B, C |
| 4 | F | rozwinięty | E, H, D, C | A, B, C, F |
| 5 | E | rozwinięty | D, G, H, D, C | A, B, C, E, F |
| 6 | D | rozwinięty | G, H, D, C | A, B, C, D, E, F |
| 7 | G | rozwinięty | H, H, D, C | A, B, C, D, E, F, G |
| 8 | H | cel | H, D, C | A, B, C, D, E, F, G |

Ścieżka: A → B → C → F → E → G → H.
<!-- /generated -->

Odpowiedzi: `DFS_EXPANSION_ORDER = ["A", "B", "C", "F", "E", "D", "G"]` i `DFS_PATH = ["A", "B", "C", "F", "E", "G", "H"]`.

Warto zauważyć dwie rzeczy. Po rozwinięciu `F` cel `H` leży na stosie, ale pod `E`, bo `E` jest wcześniej w alfabecie. DFS schodzi więc najpierw w `E`. Potem `D` okazuje się ślepym zaułkiem, bo jego sąsiedzi są już rozwinięci, i algorytm wraca do `G`. Znaleziona ścieżka ma 6 kroków, a najkrótsza tylko 3.

## Pytania kontrolne

### 1. Wczesny test celu w BFS

BFS generuje węzły w kolejności niemalejącej głębokości. Zanim wygeneruje pierwszy węzeł o głębokości *k* + 1, rozwinął już wszystkie węzły o głębokości *k*. Gdyby jakiś cel leżał płycej, zostałby wygenerowany wcześniej. Pierwszy wygenerowany cel ma więc najmniejszą możliwą liczbę kroków, a czekanie z testem do momentu zdjęcia z frontier niczego nie poprawia. Przy różnych kosztach kroków to rozumowanie się załamuje: trasa z większą liczbą kroków może być tańsza. Wcześnie wygenerowany cel nie musi więc leżeć na najtańszej ścieżce i test celu trzeba przenieść na moment zdejmowania węzła z frontier (lekcja 2.3).

Dobra odpowiedź zawiera:

- informację, że BFS generuje węzły w kolejności głębokości;
- wniosek, że pierwszy wygenerowany cel ma najmniejszą głębokość;
- uwagę, że przy różnych kosztach mniej kroków nie oznacza niższego kosztu;
- wniosek, że wtedy cel trzeba sprawdzać przy zdejmowaniu z frontier.

### 2. Pamięć DFS

DFS bez zapamiętywania stanów trzyma tylko bieżącą ścieżkę i nierozwiniętych jeszcze sąsiadów węzłów na tej ścieżce, czyli około *b*·*m* węzłów. BFS trzyma całą falę, czyli około *b*<sup>*d*</sup> węzłów. Przewaga DFS jest ogromna w szerokich, głębokich drzewach. Znika w przeszukiwaniu grafu, bo zbiór rozwiniętych stanów rośnie z liczbą odwiedzonych stanów i może być tak duży jak pamięć BFS. Słabnie też wtedy, gdy maksymalna głębokość *m* jest dużo większa od głębokości celu *d*. Część przewagi da się zachować, sprawdzając cykle tylko na bieżącej ścieżce: pamięć zostaje O(*b*·*m*), a DFS zatrzymuje się na skończonych grafach, choć może wielokrotnie rozwijać te same stany.

Dobra odpowiedź zawiera:

- informację, że DFS pamięta tylko ścieżkę i rodzeństwo węzłów na niej;
- porównanie O(*b*·*m*) z O(*b*<sup>*d*</sup>);
- uwagę, że zapamiętywanie odwiedzonych stanów odbiera tę przewagę.

### 3. DFS na nieskończonej przestrzeni stanów

Jeśli stan zawiera licznik, który może rosnąć bez końca, każdy krok prowadzi do nowego stanu. DFS może wtedy schodzić coraz głębiej jedną gałęzią i nigdy nie wrócić, nawet jeśli płytki cel istnieje w innej gałęzi. Zbiór odwiedzonych stanów nie pomaga, bo stany się nie powtarzają. DFS nie jest więc zupełny. BFS znajdzie cel na skończonej głębokości, o ile współczynnik rozgałęzienia jest skończony. Lekarstwem jest ograniczenie głębokości albo iteracyjne pogłębianie (lekcja 2.6).

Dobra odpowiedź zawiera:

- opis nieskończonej gałęzi, w której stany się nie powtarzają;
- uwagę, że zbiór odwiedzonych stanów tu nie pomaga;
- wniosek, że DFS nie jest zupełny, a BFS jest;
- przynajmniej jeden sposób zaradzenia.

### 4. Kluczące trasy DFS

DFS nie wie, gdzie jest rampa: przeszukuje bez informacji o celu. Idzie pierwszą dostępną akcją tak daleko, jak się da, i zwraca pierwszą znalezioną trasę, a nie najkrótszą. Kształt trasy wynika więc z kolejności akcji (na przykład najpierw północ, potem wschód), a nie z położenia celu. Robot okrąża całe bloki regałów, zanim przypadkiem trafi na rampę.

Dobra odpowiedź zawiera:

- uwagę, że DFS nie korzysta z żadnej wiedzy o położeniu celu;
- informację, że zwraca pierwszą znalezioną trasę, a nie najkrótszą;
- wniosek, że kształt trasy zależy od kolejności akcji.

### 5. Zbiór odwiedzonych stanów w magazynie

W drzewie do każdego stanu prowadzi dokładnie jedna ścieżka, więc żaden stan nie pojawi się dwa razy. W magazynie ruchy są odwracalne (północ, potem południe wraca na to samo pole), a wokół bloków regałów są cykle. Bez zbioru odwiedzonych stanów DFS może bez końca chodzić tam i z powrotem, a BFS rozwija te same pola coraz więcej razy i liczba rozwinięć rośnie wykładniczo. Zbiór gwarantuje, że każdy stan zostanie rozwinięty co najwyżej raz.

Dobra odpowiedź zawiera:

- informację, że w drzewie każdy stan ma jedną ścieżkę dojścia;
- uwagę, że w magazynie są cykle i ruchy odwracalne;
- skutki braku zbioru: krążenie DFS albo wielokrotne rozwijanie w BFS;
- wniosek, że zbiór daje rozwinięcie każdego stanu co najwyżej raz.

## Eksperymenty

Wyniki implementacji wzorcowych. Twoja implementacja może dać inną liczbę rozwinięć, jeśli na przykład sprawdza cel w innym momencie, ale ogólny obraz powinien być ten sam.

| Mapa | Kolejność akcji | BFS: długość trasy | BFS: rozwinięcia | DFS: długość trasy | DFS: rozwinięcia |
|---|---|---|---|---|---|
| `aisles` | N, E, S, W | 21 | 144 | 91 | 127 |
| `aisles` | W, S, E, N | 21 | 142 | 25 | 25 |
| `open_floor` | N, E, S, W | 10 | 89 | 138 | 141 |

- **Eksperyment 1.** BFS zawsze znajduje najkrótszą trasę. DFS przy kolejności N, E, S, W jedzie najpierw na wschód, oddalając się od rampy, i znajduje trasę ponad czterokrotnie dłuższą.
- **Eksperyment 2.** Długość trasy BFS się nie zmienia. DFS przy kolejności W, S, E, N trafia od razu w dobrym kierunku: 25 kroków przy zaledwie 25 rozwinięciach. To przypadek, a nie zasługa algorytmu.
- **Eksperyment 3.** Na otwartej przestrzeni BFS zalewa pola wokół startu, aż dotrze do bliskiej rampy. DFS przechodzi niemal całą halę wężykiem: trasa ma 138 kroków, choć wystarczy 10.
