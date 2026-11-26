[English](answers.md) | **Polski**

# Lekcja 2.3 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/03_uniform_cost_search/README.pl.md).

## Część A

<!-- generated:trace-table algorithm=ucs example=weighted_exercise lang=pl -->
| Krok | Zdjęty | g | f | Wynik | Frontier: stan f, w kolejności zdejmowania | Najlepsze znane g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 0 | rozwinięty | B 2, C 4 | A 0, B 2, C 4 |
| 2 | B | 2 | 2 | rozwinięty | C 3, C 4, D 9 | A 0, B 2, C 3, D 9 |
| 3 | C | 3 | 3 | rozwinięty | C 4, E 6, D 9 | A 0, B 2, C 3, D 9, E 6 |
| 4 | C | 4 | 4 | pominięty | E 6, D 9 | A 0, B 2, C 3, D 9, E 6 |
| 5 | E | 6 | 6 | rozwinięty | D 7, D 9, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 12, G 11 |
| 6 | D | 7 | 7 | rozwinięty | F 8, D 9, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11 |
| 7 | F | 8 | 8 | rozwinięty | D 9, H 10, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |
| 8 | D | 9 | 9 | pominięty | H 10, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |
| 9 | H | 10 | 10 | cel | G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |

Cel **H** osiągnięty kosztem 10. Ścieżka: A → B → C → E → D → F → H.
<!-- /generated -->

Odpowiedzi: `UCS_EXPANSION_ORDER = ["A", "B", "C", "E", "D", "F"]` i `UCS_PATH = ["A", "B", "C", "E", "D", "F", "H"]`.

Warto zauważyć trzy rzeczy:

- **Krok 2.** Rozwinięcie `B` daje drogę do `C` o koszcie 2 + 1 = 3, tańszą niż bezpośrednia krawędź A–C o koszcie 4. Wpis C 4 staje się nieaktualny i w kroku 4 zostaje pominięty.
- **Krok 5.** Rozwinięcie `E` daje drogę do `D` o koszcie 6 + 1 = 7, tańszą niż D 9 przez `B`. Ten wpis zostaje pominięty w kroku 8.
- **Krok 7.** Rozwinięcie `F` generuje cel `H` o koszcie 10. Zanim UCS go zdejmie, musi jeszcze zdjąć nieaktualny wpis D 9, bo 9 < 10.

Zwrócona ścieżka ma 6 kroków i koszt 2 + 1 + 3 + 1 + 1 + 2 = 10. Ścieżka przez `G` (A → B → C → E → G → H) ma tylko 5 kroków, ale kosztuje 2 + 1 + 3 + 5 + 1 = 12. Najczęstsza pomyłka to wpisanie pominiętych wpisów `C` i `D` do kolejności rozwijania.

## Część B

Rozwiązanie wzorcowe pomija nieaktualne wpisy, porównując koszt zdjętego węzła z najlepszym znanym kosztem w reached. Dwie alternatywy też są poprawne:

- [aima_style.py](alternatives/aima_style.py) to wersja z podręcznika Russella i Norviga. Nie pomija nieaktualnych wpisów, tylko rozwija je jeszcze raz. Żadne z ich dzieci nie jest tańsze niż to, co już znamy, więc nic nowego nie trafia do frontier. Wynik jest ten sam, a kilka rozwinięć się powtarza;
- [expanded_set.py](alternatives/expanded_set.py) to algorytm Dijkstry ze zbiorem rozwiniętych stanów. Na kopiec trafia każde dziecko, którego stan nie był jeszcze rozwinięty. Gdy stan pierwszy raz zejdzie z kopca, ma już najniższy koszt, a późniejsze kopie są pomijane.

## Pytania kontrolne

### 1. BFS przy różnych kosztach

BFS rozwija węzły w kolejności liczby kroków. Pierwsza znaleziona trasa ma najmniej kroków, ale przy różnych kosztach kroków mniej kroków nie znaczy taniej: dwa drogie kroki mogą kosztować więcej niż cztery tanie. W przykładzie z lekcji BFS zwraca S → B → G o koszcie 12, a najtańsza trasa S → A → B → C → G kosztuje 7.

Dobra odpowiedź zawiera:

- informację, że BFS porządkuje węzły według liczby kroków, a nie kosztu;
- uwagę, że trasa o mniejszej liczbie kroków może być droższa;
- przykład.

### 2. Test celu przy zdejmowaniu

Gdy węzeł celu zostaje wygenerowany, we frontier może jeszcze leżeć węzeł, przez który da się dojechać do celu taniej. Dopiero gdy cel zostaje zdjęty z frontier, każdy pozostały węzeł ma koszt co najmniej taki sam, a koszty kroków nie są ujemne, więc żadna droga przez nie nie będzie tańsza. Przykład: w grafie z lekcji rozwinięcie `B` generuje `G` o koszcie 9, a wczesny test celu zwróciłby S → A → B → G. Tymczasem `C` o koszcie 5 czeka jeszcze we frontier i prowadzi do `G` za 7.

Dobra odpowiedź zawiera:

- uwagę, że w chwili generowania nie wiadomo, czy tańsza droga nie czeka we frontier;
- argument, że przy zdejmowaniu wszystkie pozostałe węzły są co najmniej tak samo drogie;
- konkretny przykład z liczbami.

### 3. Licznik w kopcu

`heapq` porównuje krotki element po elemencie. Jeśli dwa wpisy mają ten sam koszt, porównuje kolejny element. Bez licznika byłby to węzeł, a obiektów `Node` nie da się porównywać, więc program zakończyłby się błędem `TypeError`. Licznik jest za każdym razem inny, więc porównanie zawsze rozstrzyga się na nim, i to w kolejności dodawania do frontier.

Dobra odpowiedź zawiera:

- opis porównywania krotek element po elemencie;
- skutek braku licznika: `TypeError` przy równych kosztach;
- informację, że licznik rozstrzyga remisy według kolejności dodania.

### 4. Nieaktualne wpisy

Nieaktualny wpis to węzeł, który leży we frontier, choć później znaleźliśmy tańszą drogę do jego stanu. Tańszy węzeł też trafił do frontier i zostanie zdjęty wcześniej. Gdy w końcu zdejmujemy stary wpis, jego koszt jest wyższy niż ten zapisany w reached. Wszystko, co dałoby się z niego osiągnąć, da się osiągnąć taniej z nowszego węzła, który już rozwinęliśmy, więc pominięcie go niczego nie zmienia.

Dobra odpowiedź zawiera:

- definicję: wpis, którego koszt jest wyższy niż najlepszy znany koszt jego stanu;
- uwagę, że tańszy węzeł z tym samym stanem został zdjęty i rozwinięty wcześniej;
- wniosek, że rozwinięcie starego wpisu nie dałoby nic tańszego.

### 5. UCS a BFS przy równych kosztach

Gdy każdy krok kosztuje tyle samo, koszt ścieżki jest proporcjonalny do jej długości, więc UCS rozwija węzły w tej samej kolejności głębokości co BFS i znajduje trasę tej samej długości. Różnica tkwi w teście celu: BFS kończy, gdy cel zostanie wygenerowany, a UCS dopiero wtedy, gdy zostanie zdjęty z frontier. UCS rozwija więc zwykle więcej węzłów, mianowicie jeszcze część węzłów z głębokości celu. Do tego operacje na kopcu są wolniejsze niż na zwykłej kolejce.

Dobra odpowiedź zawiera:

- uwagę, że przy równych kosztach UCS rozwija węzły w kolejności głębokości, jak BFS;
- informację, że obie metody znajdują trasy tej samej długości;
- wniosek, że UCS rozwija więcej węzłów z powodu późnego testu celu.

### 6. Koszty zerowe i ujemne

Przy kosztach zerowych argument z optymalności nadal działa, bo koszty ścieżek nie maleją. Kłopot jest z kompletnością: jeśli przestrzeń stanów jest nieskończona, a pewne kroki są darmowe, UCS może bez końca rozwijać nowe stany o tym samym koszcie i nigdy nie dojść do celu. Dlatego warunek kompletności wymaga, żeby każdy krok kosztował co najmniej pewne *ε* > 0. Przy kosztach ujemnych zawodzi sam argument optymalności: cel zdjęty z frontier może później okazać się osiągalny taniej, przez krok o ujemnym koszcie. Gdy w grafie jest cykl o ujemnym koszcie, najtańsza droga w ogóle nie istnieje. Do grafów z ujemnymi wagami służą inne algorytmy, na przykład algorytm Bellmana-Forda.

Dobra odpowiedź zawiera:

- uwagę, że koszty zerowe zagrażają zatrzymaniu się algorytmu na nieskończonych przestrzeniach, a nie optymalności;
- wyjaśnienie, dlaczego koszty ujemne psują argument optymalności;
- wzmiankę o cyklu o ujemnym koszcie albo o innym algorytmie.

## Eksperymenty

Wyniki implementacji wzorcowych. Twoja implementacja może rozwinąć nieco inną liczbę pól, jeśli inaczej rozstrzyga remisy, ale koszty tras muszą być takie same.

| Mapa | Algorytm | Kroki | Koszt | Rozwinięcia |
|---|---|---|---|---|
| `congested` | BFS | 18 | 52 | 94 |
| `congested` | UCS | 22 | 24 | 94 |

- **Eksperyment 1.** BFS jedzie prosto korytarzem: 18 kroków, ale koszt 52. UCS wybiera objazd górną alejką: 22 kroki i koszt 24. Trasa UCS przejeżdża przez jedno pole strefy wolnego ruchu, pierwsze pole korytarza, bo tylko przez nie da się wyjechać ze strefy startowej do alejek. Oba algorytmy rozwijają po 94 pola: BFS, bo do celu jest 18 kroków, a prawie wszystkie pola mapy leżą bliżej; UCS, bo prawie wszystkie pola da się osiągnąć taniej niż za 24.
- **Eksperyment 2.** Korytarz, w którym strefa wolnego ruchu ma *k* pól, kosztuje 18 + 2*k*, a objazd 22 (dopóki pierwsze pole korytarza jest zwykłą podłogą). UCS jedzie korytarzem przy *k* ≤ 2, a od *k* = 3 wybiera objazd. Przy *k* = 2 obie trasy kosztują 22; wzorcowy UCS wybiera wtedy korytarz, bo przy remisie zdejmuje węzeł dodany wcześniej. Inna implementacja może wybrać objazd i też będzie poprawna. Przy *k* = 17 do strefy należy także pierwsze pole korytarza, przez które prowadzi objazd, więc objazd drożeje do 24.
- **Eksperyment 3.** UCS rozwinął 94 ze 104 wolnych pól, w tym wszystkie 45 pól magazynu po lewej stronie, choć rampa jest po prawej. Najdroższy rozwinięty węzeł kosztuje 24, tyle co trasa. UCS rozwija każde pole, do którego da się dojechać taniej niż do celu, bo nic nie wie o położeniu celu: rozchodzi się jednakowo we wszystkich kierunkach. Pomogłoby mu oszacowanie, jak daleko z danego pola jest do rampy. To jest heurystyka z lekcji 2.4.
