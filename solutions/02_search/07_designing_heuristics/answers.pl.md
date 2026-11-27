[English](answers.md) | **Polski**

# Lekcja 2.7 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/02_search/07_designing_heuristics/README.pl.md).

## Część A

| Heurystyka | Dopuszczalna | Uzasadnienie |
|---|---|---|
| `h1`: liczba paczek | tak | Problem zrelaksowany: robot podnosi paczki z dowolnego miejsca, bez jazdy. Zostają same akcje `PICK`, po jednej na paczkę. |
| `h2`: najbliższa paczka + liczba paczek | tak | Robot musi dojechać przynajmniej do pierwszej paczki, którą podniesie, a ta jest co najmniej tak daleko jak najbliższa. Jazda po siatce bez ścian to co najmniej *M* ruchów. Do tego po jednej akcji `PICK` na paczkę. |
| `h3`: najdalsza paczka + liczba paczek | tak | Robot musi kiedyś stanąć na najdalszej paczce, a dojazd tam to co najmniej *M* ruchów, niezależnie od kolejności. Do tego akcje `PICK`. |
| `h4`: suma odległości + liczba paczek | nie | Kontrprzykład: robot w polu (1, 1), paczki w (1, 2) i (1, 3). Wystarczą 4 akcje: E, PICK, E, PICK. Heurystyka daje 1 + 2 + 2 = 5. Na mapie `parcels.txt` w stanie początkowym daje 13, a najkrótszy plan ma 11 akcji. |
| `h5`: odległość do rampy | nie | Cel nie wymaga dojazdu do rampy. W stanie celu, gdy robot stoi daleko od rampy, prawdziwy koszt to 0, a heurystyka jest dodatnia. |
| `h6`: dwa razy liczba paczek | nie | Robot stoi na ostatniej paczce: wystarczy jedna akcja `PICK`, a heurystyka daje 2. |

Zauważ łańcuch dominacji: *h*<sub>1</sub> ≤ *h*<sub>2</sub> ≤ *h*<sub>3</sub> w każdym stanie, bo najdalsza paczka jest co najmniej tak daleko jak najbliższa.

## Część B

Rozwiązanie wzorcowe to *h*<sub>3</sub>: odległość do najdalszej paczki plus liczba paczek. Dwie alternatywy też przechodzą testy:

- [nearest_parcel.py](alternatives/nearest_parcel.py) to *h*<sub>2</sub>. Jest dopuszczalna, ale słabsza: *h*<sub>3</sub> ją dominuje, więc A\* rozwija z nią więcej węzłów.
- [nearest_plus_spread.py](alternatives/nearest_plus_spread.py) jest najsilniejsza z trzech. Robot najpierw dojeżdża do jakiejś paczki, co najmniej najbliższej. Potem musi odwiedzić obie paczki z najbardziej oddalonej pary, co wymaga co najmniej ich odległości. Suma tych dwóch części i liczby paczek nie przeszacowuje. Dominuje *h*<sub>3</sub>, bo z nierówności trójkąta *M*(robot, najdalsza) ≤ *M*(robot, najbliższa) + *M*(najbliższa, najdalsza). Przy sześciu paczkach A\* rozwija z nią 657 węzłów zamiast 1814.

## Pytania kontrolne

### 1. Dlaczego problem zrelaksowany nie przeszacowuje

Problem zrelaksowany ma te same stany i co najmniej te same akcje co prawdziwy, a niektóre ograniczenia znikają. Każdy plan prawdziwego problemu jest więc też planem problemu zrelaksowanego, o tym samym albo niższym koszcie. Najtańszy plan problemu zrelaksowanego nie może być droższy od najtańszego planu prawdziwego.

Dobra odpowiedź zawiera:

- uwagę, że każdy prawdziwy plan jest też planem zrelaksowanym;
- wniosek, że optimum zrelaksowane jest nie większe niż prawdziwe.

### 2. Problemy zrelaksowane dla „liczby paczek” i *h*<sub>3</sub>

„Liczba paczek” to koszt problemu, w którym robot podnosi paczki bez jazdy, na przykład z dowolnego miejsca. *h*<sub>3</sub> wynika z problemu, w którym robot jeździ po siatce bez ścian i musi dojechać tylko do najdalszej paczki, a pozostałe może podnieść z daleka. Najtańszy plan to dojazd po najkrótszej drodze bez ścian (*M* ruchów) i podniesienie wszystkich paczek.

Dobra odpowiedź zawiera:

- dla liczby paczek: usunięcie potrzeby jazdy;
- dla *h*<sub>3</sub>: usunięcie ścian i wymogu odwiedzenia wszystkich paczek poza najdalszą.

### 3. Łączenie heurystyk

Wziąć maksimum: *h*(*n*) = max(*h*<sub>a</sub>(*n*), *h*<sub>b</sub>(*n*)). W każdym stanie maksimum równa się jednej z dopuszczalnych heurystyk, więc nie przeszacowuje. Jest też większe lub równe każdej z nich, więc dominuje obie. Suma nie byłaby bezpieczna, bo dwie poprawne dolne granice mogą liczyć ten sam fragment kosztu.

Dobra odpowiedź zawiera:

- maksimum jako sposób łączenia;
- uzasadnienie dopuszczalności i dominacji;
- opcjonalnie: ostrzeżenie przed sumą.

### 4. Stan, w którym *h*<sub>6</sub> przeszacowuje

Robot stoi na polu ostatniej paczki. Prawdziwy koszt to 1, czyli jedna akcja `PICK`. *h*<sub>6</sub> daje 2.

Dobra odpowiedź zawiera:

- konkretny stan;
- prawdziwy koszt i wartość heurystyki.

### 5. Kiedy silniejsza heurystyka spowalnia

Gdy policzenie jej dla jednego węzła kosztuje więcej, niż oszczędza mniejsza liczba rozwinięć. Na przykład heurystyka, która dla każdego stanu rozwiązuje trudny podproblem (choćby dokładny objazd wszystkich paczek), może rozwijać bardzo mało węzłów, a mimo to działać dłużej niż prosta odległość. W eksperymencie 3 silniejsze heurystyki były też szybsze, bo liczy się je tanio, ale tak nie musi być zawsze.

Dobra odpowiedź zawiera:

- porównanie kosztu liczenia heurystyki z zaoszczędzoną pracą;
- przykład heurystyki drogiej w liczeniu.

## Eksperymenty

Wyniki implementacji wzorcowej na mapie z alejkami (rozwinięcia / długość planu). Twoja heurystyka da inne liczby, jeśli różni się od *h*<sub>3</sub>.

| Paczki | *h* = 0 | *h*<sub>1</sub> | *h*<sub>2</sub> | *h*<sub>3</sub> | *h*<sub>4</sub> |
|---|---|---|---|---|---|
| 1 | 101 / 14 | 89 / 14 | 18 / 14 | 18 / 14 | 18 / 14 |
| 2 | 181 / 19 | 159 / 19 | 51 / 19 | 36 / 19 | 23 / 19 |
| 3 | 803 / 42 | 767 / 42 | 476 / 42 | 262 / 42 | 112 / **46** |
| 4 | 1815 / 51 | 1697 / 51 | 1159 / 51 | 635 / 51 | 324 / **55** |
| 5 | 3672 / 56 | 3488 / 56 | 2395 / 56 | 1071 / 56 | 440 / **72** |
| 6 | 7377 / 57 | 6844 / 57 | 4844 / 57 | 1814 / 57 | 583 / **81** |

- **Eksperyment 1.** Kolejność od najwięcej do najmniej rozwinięć: *h* = 0, *h*<sub>1</sub>, *h*<sub>2</sub>, *h*<sub>3</sub>, *h*<sub>4</sub>. *h*<sub>4</sub> rozwija najmniej, bo przeszacowuje: A\* wierzy jej i pędzi do celu, ale od trzech paczek zwraca za długie plany (81 akcji zamiast 57 przy sześciu paczkach). Przy sześciu paczkach *h*<sub>3</sub> rozwija 1814 węzłów, a *h*<sub>2</sub> 4844, czyli 2,7 razy więcej.
- **Eksperyment 2.** *h*<sub>3</sub> jest większa od *h*<sub>2</sub> w 614 stanach, równa w 626 i nigdy mniejsza: dominuje ją. *h*<sub>2</sub> dominuje *h*<sub>1</sub> (większa w 1073 stanach, nigdy mniejsza). Heurystyka „najbliższa paczka + rozrzut paczek” jest większa od *h*<sub>3</sub> w 468 stanach i nigdy mniejsza. Gdy Twoja heurystyka jest w części stanów większa, a w części mniejsza od *h*<sub>3</sub>, warto wziąć maksimum obu.
- **Eksperyment 3.** Przy sześciu paczkach czas maleje razem z liczbą rozwinięć, od około 28 ms dla *h* = 0 do około 8 ms dla *h*<sub>3</sub>. Wszystkie te heurystyki liczy się tanio, więc oszczędzone rozwinięcia przekładają się na czas. Bezwzględne czasy zależą od komputera.
