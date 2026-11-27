[English](README.md) | **Polski**

# Lekcja 2.5 — Porównanie strategii przeszukiwania

**Core** · Wymagania: 2.4 Heurystyki, greedy best-first i A* (zobacz [mapę kursu](../../../COURSE_MAP.pl.md)).

## Cele lekcji

Po tej lekcji:

- zestawisz własności BFS, DFS, UCS, greedy i A\* i każdą z nich uzasadnisz;
- dobierzesz strategię do problemu, zamiast sięgać zawsze po tę samą;
- zmierzysz, ile pracy i pamięci zużywa każdy algorytm na mapach z kosztami;
- zobaczysz, gdzie kończą się możliwości przeszukiwania dokładnego.

## Problem

Robot zna już pięć sposobów szukania trasy. Którego z nich powinien używać? Na to pytanie nie ma jednej odpowiedzi. Gdy wszystkie ruchy kosztują tyle samo, BFS w zupełności wystarczy. Gdy w magazynie są strefy wolnego ruchu, BFS zaczyna przepłacać. A\* jest zwykle najlepszy, ale tylko wtedy, gdy mamy dobrą heurystykę. Greedy bywa bardzo szybki, ale nie gwarantuje najtańszej trasy.

W tej lekcji nie piszesz nowego algorytmu. Zbierasz to, co już wiesz, w jedną tabelę, a potem sprawdzasz ją w eksperymentach na własnym kodzie z lekcji 2.2–2.4.

## Intuicja

Wszystkie pięć algorytmów robi to samo: zdejmuje węzeł z frontier, sprawdza go i rozwija. Różnią się tylko odpowiedzią na pytanie, **który węzeł zdjąć jako następny**. Każda odpowiedź ma swoją cenę:

- BFS bierze najpłytszy węzeł. Nie zgubi najkrótszej trasy, ale trzyma w pamięci całą falę.
- DFS bierze najgłębszy. Szybko schodzi w głąb, ale może się zapędzić w bardzo długą trasę.
- UCS bierze najtańszy. Znajduje najtańszą trasę, ale rozgląda się na wszystkie strony.
- Greedy bierze ten, który wygląda na najbliższy celu. Jest szybki, ale ślepy na koszt.
- A\* bierze ten o najmniejszym *g* + *h*. Łączy zalety UCS i greedy, o ile heurystyka nie przeszacowuje.

Przypomina to wybór środka transportu: najszybszy, najtańszy i najwygodniejszy to zwykle trzy różne odpowiedzi.

## Porównywane własności

Wszystkie algorytmy rozumiemy tak, jak napisaliśmy je w kursie: jako przeszukiwanie grafu, które pamięta osiągnięte albo rozwinięte stany. Koszty kroków są zawsze dodatnie. Heurystyka w A\* jest dopuszczalna, a w greedy może być dowolna. Porównujemy cztery własności:

| Klucz w `task.py` | Własność | Założenia |
|---|---|---|
| `complete_finite` | **kompletność na skończonej przestrzeni stanów**: jeśli rozwiązanie istnieje, algorytm je znajdzie; jeśli nie istnieje, zatrzyma się i zwróci `None` | stanów jest skończenie wiele |
| `complete_infinite` | **kompletność na nieskończonej przestrzeni stanów**: algorytm na pewno znajdzie rozwiązanie | stanów może być nieskończenie wiele, ale każdy stan ma skończenie wiele akcji, każdy krok kosztuje co najmniej pewne *ε* > 0, a rozwiązanie istnieje |
| `optimal_unit_costs` | **optymalność przy jednakowych kosztach**: zwrócona trasa ma najmniej kroków | każdy krok kosztuje tyle samo |
| `optimal_any_costs` | **optymalność przy dowolnych kosztach**: zwrócona trasa jest najtańsza | koszty kroków są dodatnie, ale mogą się różnić |

Odpowiedzi wynikają z lekcji 2.2–2.4. Żeby wpisać „nie”, wystarczy jeden kontrprzykład: mapa albo graf, na którym algorytm zawodzi. Żeby wpisać „tak”, trzeba przypomnieć sobie argument, dlaczego algorytm nie może zawieść.

## Czas i pamięć

Oznaczenia jak w poprzednich lekcjach: *b* to współczynnik rozgałęzienia, *d* to głębokość najpłytszego celu, *m* to największa głębokość, *C*\* to koszt optymalnego rozwiązania, a *ε* to najmniejszy koszt kroku.

| Algorytm | Czas w najgorszym razie | Pamięć w najgorszym razie |
|---|---|---|
| BFS | O(*b*<sup>*d*</sup>) | O(*b*<sup>*d*</sup>) |
| DFS | O(*b*<sup>*m*</sup>); w przeszukiwaniu grafu najwyżej liczba stanów | O(*b*·*m*) dla frontier; zbiór rozwiniętych stanów może urosnąć do liczby stanów |
| UCS | O(*b*<sup>1 + ⌊*C*\*/*ε*⌋</sup>) | O(*b*<sup>1 + ⌊*C*\*/*ε*⌋</sup>) |
| Greedy | O(*b*<sup>*m*</sup>), z dobrą heurystyką zwykle dużo mniej | jak czas |
| A\* | zależy od heurystyki; rozwija każdy węzeł o *f* < *C*\* | jak czas |

**Jak mierzyć pamięć?** Najprostsza miara to **największy rozmiar frontier** w trakcie przeszukiwania. Do niego dochodzi zbiór osiągniętych stanów, który w przeszukiwaniu grafu rośnie aż do liczby odwiedzonych stanów. W eksperymentach mierzymy oba: rozwinięcia i największy frontier.

Uwaga na DFS. Jego mała pamięć O(*b*·*m*) to zaleta tylko wtedy, gdy *m*, czyli głębokość, na którą schodzi, jest niewielka. Na otwartej podłodze DFS potrafi zejść na głębokość ponad stu kroków, a wtedy jego frontier jest większy niż fala BFS.

## Jak wybrać strategię

- **Wszystkie kroki kosztują tyle samo, a przestrzeń nie jest ogromna:** BFS. Jest prosty i znajduje najkrótszą trasę.
- **Kroki mają różne koszty:** UCS, a jeśli masz dopuszczalną heurystykę, to A\*. A\* znajduje tę samą trasę co UCS, ale zwykle rozwija dużo mniej węzłów.
- **Wystarczy jakakolwiek trasa, byle szybko:** greedy z dobrą heurystyką. Trzeba się jednak liczyć z tym, że trasa bywa dużo droższa.
- **Brakuje pamięci, a głębokość celu jest nieznana:** iteracyjne pogłębianie (lekcja 2.6). Zużywa pamięć jak DFS, a znajduje najkrótszą trasę jak BFS.
- **Przestrzeń stanów jest gigantyczna,** na przykład przy kilkudziesięciu paczkach: żaden z tych algorytmów nie wystarczy. Potrzebne są metody przybliżone z modułu 4.

## Prześledź ręcznie

### Przykład rozwiązany

Nie ma tu śladu krok po kroku, bo żaden algorytm nie jest nowy. Ćwiczymy za to uzasadnianie własności. Weźmy szósty algorytm, którego nie ma w tabeli: **DFS bez pamiętania stanów**, czyli przeszukiwanie drzewa w głąb z lekcji 2.1.

- **Kompletność na skończonej przestrzeni: nie.** Kontrprzykład: graf z cyklem A–B–A. DFS bez pamięci może chodzić tam i z powrotem w nieskończoność i nigdy nie zbadać reszty grafu.
- **Kompletność na nieskończonej przestrzeni: nie.** Ten sam kontrprzykład działa i tutaj, bo definicja dopuszcza też skończoną przestrzeń: w grafie z cyklem, w którym rozwiązanie istnieje, DFS bez pamięci może krążyć w cyklu i nigdy do rozwiązania nie dojść.
- **Optymalność przy jednakowych kosztach: nie.** Kontrprzykład bez cykli: ze startu `S` prowadzą krawędzie do `A` i `B`, z `A` do `C`, a z `C` i z `B` do celu `G`. DFS, który najpierw próbuje `A`, zwraca S → A → C → G (3 kroki), choć istnieje S → B → G (2 kroki).
- **Optymalność przy dowolnych kosztach: nie.** Jeśli algorytm nie jest optymalny nawet wtedy, gdy wszystkie koszty są równe, nie będzie optymalny także przy kosztach różnych.

Zwróć uwagę na ostatni krok. Optymalność przy dowolnych kosztach pociąga optymalność przy kosztach jednakowych, bo jednakowe koszty to szczególny przypadek dowolnych. Z kompletnością tak prosto nie jest. Na skończonej przestrzeni algorytm musi się też zatrzymać, gdy rozwiązania nie ma, a tego definicja kompletności na nieskończonej przestrzeni nie wymaga. Każdą z tych dwóch własności trzeba więc sprawdzić osobno.

### Twoja kolej

Wypełnij tabelę `PROPERTIES` w części A pliku `task.py` dla pięciu algorytmów z tego kursu: BFS, DFS, UCS, greedy i A\*. Pamiętaj, że to przeszukiwanie grafu, a nie drzewa, więc odpowiedzi dla DFS różnią się od tych z przykładu.

## Częste błędy

1. **Mylenie DFS z przeszukiwaniem drzewa.** DFS z przykładu rozwiązanego nie pamięta żadnych stanów, a DFS z lekcji 2.2 pamięta rozwinięte stany. To dwa różne algorytmy o różnych własnościach. Sprawdź, o który chodzi w tabeli.
2. **Jedna odpowiedź dla obu rodzajów przestrzeni.** Kompletność na skończonej i na nieskończonej przestrzeni to dwie różne własności. Algorytm może mieć jedną, a nie mieć drugiej, więc dla każdej szukaj osobnego argumentu albo kontrprzykładu.
3. **Mylenie szybkości z optymalnością.** To, że algorytm szybko dociera do celu, nic nie mówi o koszcie znalezionej trasy. Optymalność trzeba uzasadnić osobno.
4. **Mylenie liczby kroków z kosztem.** Gdy kroki mają różne koszty, trasa o najmniejszej liczbie kroków nie musi być najtańsza. Sprawdź, co dokładnie minimalizuje każdy algorytm.

Testy lekcji wykrywają każdy z tych błędów.

## Zadanie

### Część A: tabela własności

Wpisz w `task.py` wartość `True` albo `False` w każdym z 20 pól tabeli `PROPERTIES`. Dokładne znaczenie każdej własności i jej założenia znajdziesz w sekcji „Porównywane własności”.

Ta lekcja nie ma części B. Notebook porównuje algorytmy, które napisałeś w lekcjach 2.2–2.4.

### Jak sprawdzić

Z głównego katalogu repozytorium:

```bash
uv run pytest modules/02_search/05_comparing_strategies
```

Każda własność ma osobny test. Gdy coś się nie zgadza, test podaje tylko, ile z pięciu odpowiedzi w danym wierszu jest błędnych, a nie które. Dzięki temu musisz jeszcze raz przemyśleć cały wiersz.

### Kryteria akceptacji

- Wszystkie testy lekcji przechodzą.
- Każdą odpowiedź w tabeli potrafisz uzasadnić argumentem albo kontrprzykładem.
- Potrafisz odpowiedzieć na pytania kontrolne, zanim zajrzysz do odpowiedzi.

## Czego testy nie sprawdzają

- **Uzasadnień.** Test sprawdza tylko wartości w tabeli. Czy wiesz, *dlaczego* tak jest, sprawdzisz w pytaniach kontrolnych.
- **Wniosków z eksperymentów.** Interpretację wyników porównaj z odpowiedziami w rozwiązaniach.
- **Czasu działania.** Czasy w notebooku zależą od komputera i są bardzo małe, więc wahają się z uruchomienia na uruchomienie.

## Eksperymenty

Otwórz [experiments.pl.ipynb](experiments.pl.ipynb). W trybie `"mine"` notebook uruchamia Twoje implementacje z lekcji 2.2, 2.3 i 2.4. Jeśli któraś jeszcze nie działa, przełącz się na `"reference"`. Przed każdym eksperymentem zapisz przewidywanie:

1. Na mapach `congested.txt` i `depot.txt`: który algorytm znajdzie najtańszą trasę, który rozwinie najmniej pól, a który najwięcej?
2. Który algorytm potrzebuje więcej pamięci, BFS czy DFS? Czy odpowiedź zależy od mapy?
3. Ile pracy kosztuje A\* zebranie 1, 2, …, 6 paczek? Co by było przy dwudziestu?

## Pytania kontrolne

1. Czym różni się DFS z lekcji 2.2 od DFS z przykładu rozwiązanego? Jak ta różnica wpływa na kompletność na skończonej przestrzeni stanów?
2. Zbuduj nieskończoną przestrzeń stanów, w której istnieje rozwiązanie. Które z pięciu algorytmów na pewno je znajdą? Uzasadnij jedno „tak” i jedno „nie”.
3. Która część argumentu optymalności A\* korzysta z dopuszczalności heurystyki? Czy ten argument da się przenieść na greedy?
4. Na mapie `open_floor.txt` DFS ma większy frontier niż BFS. Jak to pogodzić z tym, że DFS „zużywa mało pamięci”?
5. Masz mapę magazynu bez stref wolnego ruchu i bardzo mało pamięci. Który algorytm wybierzesz i dlaczego?

## Jeśli utkniesz

<details>
<summary>Podpowiedź 1: od czego zacząć</summary>

Zacznij od kolumny UCS. Wszystkie jej własności udowodniliśmy w lekcji 2.3. Potem przejdź do BFS (lekcja 2.2) i zastanów się, co się zmienia, gdy kroki mają różne koszty.

</details>

<details>
<summary>Podpowiedź 2: szukaj kontrprzykładów</summary>

Żeby odpowiedzieć „nie”, wystarczy jeden graf, na którym algorytm zawodzi. Dobre źródła kontrprzykładów: grafy z lekcji 2.3 i 2.4, mapa `congested.txt` oraz nieskończona przestrzeń, w której stan zawiera licznik rosnący bez końca.

</details>

<details>
<summary>Podpowiedź 3: własności zależą od siebie</summary>

Algorytm optymalny przy dowolnych kosztach jest też optymalny przy kosztach jednakowych. To pozwala sprawdzić, czy dwie ostatnie kolumny są spójne. Z kompletnością tak prosto nie jest: na skończonej przestrzeni algorytm musi się też zatrzymać, gdy rozwiązania nie ma.

</details>

## Co zapamiętać

- Pięć algorytmów różni się tylko tym, który węzeł zdejmują z frontier jako następny.
- Kompletność i optymalność zależą od założeń: skończona czy nieskończona przestrzeń, jednakowe czy różne koszty, dopuszczalna czy dowolna heurystyka.
- Żeby wpisać „tak”, potrzebny jest argument; żeby wpisać „nie”, wystarczy jeden kontrprzykład.
- Szybkość, optymalność i pamięć to trzy różne kryteria. Żaden algorytm nie wygrywa we wszystkich.
- Pamięć to osobny zasób: mierzymy ją największym frontier i zbiorem osiągniętych stanów.
- Przy wielu paczkach przestrzeń stanów rośnie wykładniczo i przeszukiwanie dokładne przestaje wystarczać.

## Co dalej

- Po własnej próbie porównaj się z odpowiedziami w [solutions/02_search/05_comparing_strategies/](../../../solutions/02_search/05_comparing_strategies/).
- Lekcje opcjonalne: 2.6 o iteracyjnym pogłębianiu i 2.7 o projektowaniu heurystyk.
- Moduł 3 przenosi przeszukiwanie do gier, w których ruch wykonuje też przeciwnik.

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 3.4–3.5 (porównanie strategii przeszukiwania).
