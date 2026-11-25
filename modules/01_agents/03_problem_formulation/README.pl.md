[English](README.md) | **Polski**

# Lekcja 1.3 — Typy agentów i sformułowanie problemu

**Core** · Wymagania: 1.2 Agent i środowisko.

## Cele lekcji

Po tej lekcji:

- rozróżnisz pięć typów agentów i powiesz, czego każdy potrzebuje, żeby działać;
- sformułujesz zadanie jako problem przeszukiwania: stan, akcje, model przejść, test celu i koszt;
- wyjaśnisz, czym jest abstrakcja i po co z niej korzystamy;
- policzysz stany problemu i zobaczysz, jak szybko ich przybywa;
- zaimplementujesz sformułowanie problemu, które rozwiąże gotowy algorytm przeszukiwania.

## Problem

W lekcji 1.2 nawet agent z pamięcią błądził po hali, bo nie wiedział, gdzie leżą paczki. Załóżmy teraz, że system magazynowy przekazuje robotowi całą mapę z położeniem paczek. Wtedy robot może zaplanować całą sekwencję akcji, zanim ruszy z miejsca.

Żeby jednak komputer mógł taki plan znaleźć, zadanie trzeba najpierw **sformułować**: dokładnie powiedzieć, czym jest stan, jakie są akcje, co z nich wynika i kiedy osiągamy cel.

## Pięć typów agentów

| Typ agenta | Na podstawie czego decyduje | Gdzie w kursie |
|---|---|---|
| reaktywny | wyłącznie bieżąca percepcja i reguły „warunek → akcja” | lekcja 1.2 |
| z modelem | percepcja i **stan wewnętrzny**, czyli model świata budowany z dotychczasowych percepcji | agent z pamięcią z lekcji 1.2 |
| z celem | model świata i **cel**: szuka sekwencji akcji, która do celu prowadzi | ta lekcja i moduł 2 |
| z użytecznością | model świata i **funkcja użyteczności**: wybiera najlepszy oczekiwany wynik, nie tylko „jakikolwiek cel” | moduł 6 |
| uczący się | dowolny z powyższych, który dodatkowo poprawia się na podstawie doświadczenia | moduły 7 i 8 |

Agent z celem potrzebuje dwóch rzeczy, których nie ma agent reaktywny: modelu, czyli wiedzy, co dzieje się po każdej akcji, i opisu celu. Mając je, może przewidywać skutki akcji „w głowie” i szukać planu.

## Sformułowanie problemu

Problem przeszukiwania składa się z pięciu elementów:

| Element | Znaczenie | W problemie zbierania paczek |
|---|---|---|
| stan początkowy | od czego zaczynamy | `(pole startowe robota, zbiór wszystkich paczek)` |
| akcje | co można zrobić w danym stanie | ruchy N, E, S, W na wolne pola; `PICK`, gdy na polu robota leży paczka |
| model przejść | dokąd prowadzi akcja: `result(stan, akcja)` | ruch zmienia pole robota; `PICK` usuwa paczkę z jego pola |
| test celu | czy stan jest celem: `is_goal(stan)` | nie została żadna paczka |
| koszt akcji | ile kosztuje krok | każda akcja kosztuje 1 |

**Rozwiązanie** to sekwencja akcji, która prowadzi od stanu początkowego do celu. **Rozwiązanie optymalne** ma najniższy łączny koszt, czyli tutaj najmniej akcji.

W kodzie kursu problem jest klasą dziedziczącą po `Problem` (z `introai.search`). Ma atrybut `initial` i metody `actions`, `result` oraz `is_goal`. Koszt 1 za akcję jest dziedziczony. Takie sformułowanie umie rozwiązać każdy algorytm przeszukiwania z modułu 2.

## Abstrakcja

Prawdziwy robot ma dokładną pozycję w centymetrach, prędkość, baterię, chwytak, który trzeba opuścić i podnieść, a do tego czas potrzebny na każdy ruch. W naszym sformułowaniu nic z tego nie ma: jest tylko pole siatki i zbiór paczek. To **abstrakcja**, czyli celowe pominięcie szczegółów nieistotnych dla decyzji.

Dobra abstrakcja jest:

- **poprawna:** każdy plan znaleziony w abstrakcyjnym problemie da się wykonać w prawdziwym świecie;
- **użyteczna:** abstrakcyjne akcje są na tyle proste, że ich wykonanie samo nie jest trudnym problemem.

## Ten sam świat, dwie reprezentacje

| | Lekcja 1.2: agent | Lekcja 1.3: problem przeszukiwania |
|---|---|---|
| Co wiadomo | percepcja: paczka na polu i wolne kierunki | pełny stan: pole robota i wszystkie pozostałe paczki |
| Kiedy decyzja | w każdym kroku, na bieżąco | całą sekwencję planujemy z góry |
| Co jest potrzebne | reguły (i ewentualnie pamięć) | model przejść i test celu |

To ta sama hala i te same paczki, ale reprezentacja decyduje, co agent może zrobić. Właśnie o to chodzi w pytaniu przewodnim kursu.

## Prześledź ręcznie

Mała mapa: korytarz z jedną paczką.

```text
######
#RP.D#
######
```

- **Wolne pola:** `(1, 1)`, `(1, 2)`, `(1, 3)`, `(1, 4)`, czyli 4 pola.
- **Zbiory paczek:** paczka może jeszcze leżeć albo być zebrana, więc są 2 możliwe zbiory: `{(1, 2)}` i `{}`.
- **Liczba stanów:** 4 · 2 = **8**.
- **Stan początkowy:** `((1, 1), frozenset({(1, 2)}))`.
- **Akcje na starcie:** `["E"]`, bo N, S i W prowadzą w ścianę, a na polu startu nie ma paczki.
- **Po akcji `E`:** stan `((1, 2), frozenset({(1, 2)}))`. Akcje to `["E", "W", "PICK"]`.
- **Po akcji `PICK`:** stan `((1, 2), frozenset())`. To cel, bo nie została żadna paczka.

Optymalny plan to `E`, `PICK`, czyli dwie akcje. Rampa `D` nie ma tu znaczenia: celem jest zebranie paczek, a nie dojechanie do rampy.

## Ile jest stanów

Ogólnie stanów jest tyle, ile par „wolne pole × podzbiór paczek”:

> liczba stanów = (liczba wolnych pól) · 2<sup>(liczba paczek)</sup>

Mapa `aisles` ma 155 wolnych pól:

| Liczba paczek | Liczba stanów |
|---|---|
| 1 | 310 |
| 5 | 4 960 |
| 10 | 158 720 |
| 20 | 162 529 280 |

Każda dodatkowa paczka podwaja liczbę stanów. Nie wszystkie stany są osiągalne, ale algorytm szukający najlepszego planu musi wiele z nich odwiedzić. To **eksplozja przestrzeni stanów**, z którą zmierzymy się w modułach 2 i 4.

## Częste błędy

1. **PICK bez paczki.** Akcja `PICK` jest możliwa tylko na polu, na którym leży paczka.
2. **Ruch w przeszkodę.** Akcje to wyłącznie ruchy na wolne pola: robot nie przenika przez regały.
3. **Zły test celu.** Celem jest zebranie wszystkich paczek, a nie dojechanie do rampy.
4. **Zmienny zbiór paczek.** Jeśli paczki są w `set` i `result` zmienia go w miejscu, poprzedni stan też się zmienia. Na dodatek `set` nie da się wstawić do zbioru, więc algorytm przeszukiwania nie zapamięta stanu. Używaj `frozenset` i twórz nowy zbiór: `parcels - {cell}`.

Testy lekcji wykrywają każdy z tych błędów.

## Zadanie

### Część A: liczba stanów

W `task.py` wpisz `NUM_STATES`, czyli liczbę stanów problemu dla mapy `data/maps/parcels.txt`. Liczysz wszystkie kombinacje wolnego pola robota i zbioru paczek, które jeszcze leżą. Pamiętaj, że pola `R`, `D` i `P` też są wolne.

### Część B: sformułowanie problemu

Zaimplementuj klasę `ParcelPickupProblem(warehouse)`:

- **stan:** `(pole_robota, frozenset_pozostałych_paczek)`;
- **`initial`:** `(warehouse.start, frozenset(warehouse.parcels))`. Ustaw go wywołaniem `super().__init__(...)`;
- **`actions(stan)`:** ruchy `"N"`, `"E"`, `"S"`, `"W"` prowadzące na wolne pola (`warehouse.is_free`) oraz `"PICK"`, jeśli na polu robota leży paczka; kolejność akcji jest dowolna;
- **`result(stan, akcja)`:** ruch zmienia pole robota; `"PICK"` usuwa paczkę z pola robota; stan wejściowy pozostaje bez zmian;
- **`is_goal(stan)`:** prawda, gdy nie została żadna paczka.

### Jak sprawdzić

```bash
uv run pytest modules/01_agents/03_problem_formulation
```

Jeden z testów uruchamia na Twoim sformułowaniu wzorcowy BFS i porównuje długość planu z optymalną.

### Kryteria akceptacji

- Wszystkie testy lekcji przechodzą.
- Potrafisz odpowiedzieć na pytania kontrolne.

## Czego testy nie sprawdzają

- **Wydajności.** Wolne, ale poprawne sformułowanie przejdzie testy.
- **Kolejności akcji.** Testy porównują akcje jako zbiory.
- **Zachowania przy niedozwolonej akcji.** Testy nie sprawdzają, co robi `result`, gdy dostanie akcję, której nie ma w `actions`.
- **Jakości Twojej abstrakcji.** Sformułowanie jest podane; o abstrakcji myślisz w pytaniach kontrolnych.

## Eksperymenty

Otwórz [experiments.pl.ipynb](experiments.pl.ipynb). Notebook uruchamia BFS na Twoim sformułowaniu dla mapy z alejkami i od 1 do 8 paczek, a potem rysuje wykres liczby rozwinięć. Zanim go uruchomisz, przewidź, ile razy wzrośnie praca BFS po dodaniu jednej paczki.

## Pytania kontrolne

1. Czym różni się agent z celem od agenta z modelem? Którego potrzebujemy, żeby zaplanować trasę do wszystkich paczek, zanim robot ruszy?
2. Dlaczego stan zawiera zbiór pozostałych paczek, a nie tylko liczbę zebranych?
3. Dlaczego zbiór paczek w stanie powinien być `frozenset`, a nie `set`?
4. Jakie szczegóły prawdziwego magazynu pominęliśmy w sformułowaniu? Kiedy takie uproszczenie mogłoby zawieść?

## Jeśli utkniesz

<details>
<summary>Podpowiedź 1: konstruktor</summary>

`super().__init__(stan_początkowy)` zapisuje stan w atrybucie `initial`. Zapamiętaj też mapę, na przykład w `self.warehouse`, bo będzie potrzebna w `actions`.

</details>

<details>
<summary>Podpowiedź 2: ruchy</summary>

Słownik `{"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}` zamienia nazwę ruchu na przesunięcie `(wiersz, kolumna)`. Ruch jest możliwy, jeśli pole docelowe jest wolne.

</details>

<details>
<summary>Podpowiedź 3: PICK</summary>

`parcels - {cell}` tworzy nowy `frozenset` bez paczki z pola robota i nie zmienia starego.

</details>

## Co zapamiętać

- Typy agentów różnią się tym, co wiedzą i na jakiej podstawie decydują: od reguł, przez model świata i cel, po użyteczność i uczenie.
- Sformułowanie problemu to stan początkowy, akcje, model przejść, test celu i koszt. Rozwiązanie to sekwencja akcji.
- Abstrakcja pomija szczegóły nieistotne dla decyzji. Musi pozostać poprawna i użyteczna.
- Liczba stanów rośnie wykładniczo z liczbą paczek, czyli z liczbą niezależnych elementów świata.

## Co dalej

- Po własnej próbie porównaj się z [rozwiązaniem i odpowiedziami](../../../solutions/01_agents/03_problem_formulation/).
- Moduł 2 pokazuje, jak algorytmy przeszukiwania znajdują rozwiązania takich problemów i ile to kosztuje. Mapę modułów znajdziesz w [mapie kursu](../../../COURSE_MAP.pl.md).
- Opcjonalnie: [1.4 Krótka historia AI](../04_history_of_ai/README.pl.md).

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 2 i 3.1–3.2.
