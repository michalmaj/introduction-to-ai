[English](answers.md) | **Polski**

# Lekcja 1.3 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/01_agents/03_problem_formulation/README.pl.md).

## Część A

Mapa `parcels.txt` ma 12 wolnych pól. Po 4 w każdym z trzech środkowych wierszy, licząc pola `R`, `D` i `P`. Paczki są 3, więc zbiorów pozostałych paczek jest 2³ = 8. Stąd `NUM_STATES = 12 · 8 = 96`.

## Pytania kontrolne

### 1. Agent z celem a agent z modelem

Agent z modelem utrzymuje stan wewnętrzny, czyli wie, gdzie był i co widział, ale nadal reaguje krok po kroku. Agent z celem używa modelu świata, żeby przewidzieć skutki *sekwencji* akcji, i szuka takiej, która prowadzi do celu. Żeby zaplanować trasę do wszystkich paczek, zanim robot ruszy, potrzebujemy agenta z celem. Musi on mieć pełny model, czyli mapę i położenie paczek, oraz opis celu.

Dobra odpowiedź zawiera:

- informację, że agent z modelem pamięta, ale decyduje na bieżąco;
- informację, że agent z celem przewiduje skutki akcji i szuka planu;
- wniosek, że do planowania z góry potrzebny jest agent z celem i pełny model.

### 2. Zbiór pozostałych paczek zamiast ich liczby

Stan musi zawierać wszystko, co jest potrzebne do przewidzenia skutków akcji. Sama liczba zebranych paczek nie mówi, *które* paczki jeszcze leżą. Nie da się więc ustalić, czy `PICK` jest możliwy na danym polu ani dokąd jechać. Dwa stany z tą samą liczbą zebranych paczek, ale z różnymi paczkami do zebrania, wymagają różnych planów. Zbiór paczek odróżnia je od siebie, a sama liczba nie.

Dobra odpowiedź zawiera:

- zasadę, że stan musi wystarczać do przewidzenia skutków akcji;
- przykład dwóch sytuacji, których liczba paczek nie odróżnia.

### 3. `frozenset` zamiast `set`

Z dwóch powodów:

- **Niezmienność.** `result` musi tworzyć nowy stan, a nie zmieniać stary. Algorytm przeszukiwania przechowuje wiele stanów naraz, na przykład we frontier, więc zmiana jednego w miejscu psułaby inne.
- **Hashowalność.** Przeszukiwanie grafu zapamiętuje odwiedzone stany w zbiorze, a krotka zawierająca `set` nie ma skrótu (*hash*), więc nie da się jej tam wstawić.

Dobra odpowiedź zawiera:

- argument o niezmienności i o stanach przechowywanych jednocześnie;
- argument o zapamiętywaniu stanów w zbiorze, który wymaga hashowalności.

### 4. Co pominęliśmy i kiedy to zawodzi

Pominęliśmy między innymi:

- dokładną pozycję i prędkość robota;
- czas potrzebny na ruch i podniesienie paczki;
- baterię;
- inne roboty;
- możliwość, że chwytak nie złapie paczki.

Uproszczenie zawodzi, gdy któryś z tych szczegółów zmienia wykonalność planu. Bateria może się wyczerpać przed końcem planu. Inny robot może zablokować alejkę, a wtedy środowisko jest dynamiczne. `PICK` może się nie udać, a wtedy środowisko jest stochastyczne. Wtedy plan trzeba poprawiać w trakcie działania albo wzbogacić model.

Dobra odpowiedź zawiera:

- przynajmniej dwa konkretne pominięte szczegóły;
- sytuację, w której plan z abstrakcyjnego modelu przestaje być wykonalny;
- sposób zaradzenia: zmianę planu w trakcie działania albo bogatszy model.

## Eksperymenty

BFS na wzorcowym sformułowaniu. Mapa `aisles` ma 155 wolnych pól. Paczki dokładane są po kolei z listy w notebooku.

| Paczki | Stanów | Rozwinięcia BFS | Długość planu |
|---|---|---|---|
| 1 | 310 | 89 | 14 |
| 2 | 620 | 163 | 19 |
| 3 | 1 240 | 776 | 42 |
| 4 | 2 480 | 1 738 | 51 |
| 5 | 4 960 | 3 519 | 56 |
| 6 | 9 920 | 7 065 | 57 |
| 7 | 19 840 | 16 901 | 66 |
| 8 | 39 680 | 36 140 | 73 |

Twoje sformułowanie może dać nieco inne liczby rozwinięć, jeśli zwraca akcje w innej kolejności (na przykład `PICK` na początku listy), ale długość planu będzie taka sama.

Od trzech paczek liczba rozwinięć mniej więcej podwaja się z każdą kolejną, tak jak liczba stanów. Długość planu rośnie przy tym powoli. Plan jest krótki, ale jego znalezienie robi się bardzo drogie. Przy 20 paczkach przestrzeń ma ponad 162 miliony stanów. Moduł 2 pokazuje mądrzejsze przeszukiwanie (heurystyki, A*), a moduł 4 metody przybliżone.
