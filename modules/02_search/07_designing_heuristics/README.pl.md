[English](README.md) | **Polski**

# Lekcja 2.7 — Projektowanie heurystyk

**Opcjonalna** · Wymagania: 2.5 Porównanie strategii przeszukiwania (zobacz [mapę kursu](../../../COURSE_MAP.pl.md)).

## Cele lekcji

Po tej lekcji:

- zbudujesz heurystykę metodą problemu zrelaksowanego i wyjaśnisz, dlaczego jest dopuszczalna;
- porównasz dwie heurystyki pojęciem dominacji;
- rozpoznasz heurystykę, która przeszacowuje, i podasz stan, w którym to robi;
- zaprojektujesz własną heurystykę dla problemu zbierania paczek i sprawdzisz, ile pracy oszczędza A\*.

## Problem

W lekcji 2.5 A\* zbierał paczki w magazynie z alejkami. Z każdą paczką liczba rozwinięć mniej więcej się podwajała, a heurystyka „liczba paczek, które jeszcze leżą” prawie nic nie pomagała: przy sześciu paczkach 6844 rozwinięcia zamiast 7377. Ta heurystyka liczy tylko podnoszenie paczek, a większość kosztu to jazda.

Lepsza heurystyka musi uwzględniać odległości. Ale ostrożnie: jeśli choć raz przeszacuje, A\* może zwrócić za długi plan. Jak projektować heurystyki, które są silne, a przy tym na pewno dopuszczalne?

## Intuicja

Dobre oszacowanie dostaniesz, rozwiązując **łatwiejszą wersję** problemu. Jeśli usuniesz jakieś ograniczenie, robot ma więcej możliwości, więc najtańsze rozwiązanie łatwiejszego problemu nie może być droższe niż rozwiązanie prawdziwego. Jest więc dolnym oszacowaniem, czyli heurystyką dopuszczalną.

Tak liczymy w życiu codziennym. „Do sklepu jest co najmniej dziesięć minut, bo tyle zajmuje sama droga prosto przez park” to oszacowanie z łatwiejszego świata, w którym nie trzeba obchodzić płotów. Prawdziwy czas nie może być krótszy.

## Model formalny

### Problemy zrelaksowane

**Problem zrelaksowany** (*relaxed problem*) powstaje z prawdziwego przez usunięcie części ograniczeń akcji. Każde rozwiązanie prawdziwego problemu jest wtedy też rozwiązaniem problemu zrelaksowanego, a może się pojawić jeszcze tańsze. Stąd:

$$h^*_{\text{zrelaksowany}}(n) \le h^*(n),$$

więc dokładny koszt rozwiązania problemu zrelaksowanego jest heurystyką dopuszczalną. Co więcej, taka heurystyka jest spójna: w problemie zrelaksowanym dokładne koszty spełniają nierówność trójkąta, a każda akcja prawdziwego problemu jest też akcją zrelaksowanego.

Żeby to się opłacało, problem zrelaksowany musi dać się rozwiązać **szybko**, najlepiej wzorem. Inaczej liczenie heurystyki kosztuje więcej, niż oszczędza.

### Dominacja

Heurystyka *h*<sub>2</sub> **dominuje** heurystykę *h*<sub>1</sub>, jeśli obie są dopuszczalne i dla każdego stanu *h*<sub>2</sub>(*n*) ≥ *h*<sub>1</sub>(*n*). Jeśli obie są też spójne, A\* z *h*<sub>2</sub> nie rozwija więcej węzłów niż z *h*<sub>1</sub>, nie licząc remisów. Uzasadnienie: przy spójnej heurystyce A\* rozwija każdy węzeł o *f*(*n*) < *C*\*, czyli o *h*(*n*) < *C*\* − *g*(*n*). Im większe *h*, tym mniej węzłów spełnia ten warunek.

**Maksimum heurystyk.** Gdy masz kilka dopuszczalnych heurystyk i żadna nie dominuje pozostałych, weź ich maksimum: *h*(*n*) = max(*h*<sub>1</sub>(*n*), …, *h*<sub>k</sub>(*n*)). Maksimum też nie przeszacowuje, bo żadna ze składowych tego nie robi, a dominuje każdą z nich.

### Koszt heurystyki

Silniejsza heurystyka oszczędza rozwinięcia, ale sama też kosztuje: liczysz ją przy każdym wygenerowanym węźle. Heurystyka, która przegląda wszystkie pary paczek (*p*, *q*), przy dziesięciu paczkach liczy sto odległości na każdy węzeł. Zwykle to się opłaca, bo każde zaoszczędzone rozwinięcie to wiele wygenerowanych węzłów mniej, ale warto to zmierzyć, a nie zakładać.

## Prześledź ręcznie

### Przykład rozwiązany

Weźmy problem trasy z lekcji 2.4: robot jedzie do rampy, ruch na zwykłe pole kosztuje 1, a na pole strefy wolnego ruchu 3. Zrelaksujmy go na trzy sposoby:

1. **Robot się teleportuje.** Każde pole jest osiągalne jedną darmową akcją, więc koszt dojazdu wynosi 0. Dostajemy *h* = 0, czyli UCS.
2. **Robot lata w linii prostej.** Nie ma ścian ani stref, a robot może poruszać się w dowolnym kierunku. Najtańsza trasa to odcinek, więc *h* to **odległość euklidesowa**.
3. **Robot jedzie po siatce, ale przez ściany.** Zostają ruchy N, E, S, W, każdy za 1, ale znikają przeszkody i strefy wolnego ruchu. Najtańsza trasa ma tyle ruchów, ile wynosi **odległość Manhattan**.

Każdy kolejny problem zrelaksowany jest bliższy prawdziwemu, więc daje większe oszacowanie: 0 ≤ odległość euklidesowa ≤ odległość Manhattan ≤ *h*\*. Odległość Manhattan dominuje euklidesową, a ta dominuje *h* = 0. Eksperyment z lekcji 2.4 to potwierdził: na mapie z alejkami A\* rozwinął 147 pól z *h* = 0, 66 z odległością euklidesową i 48 z odległością Manhattan.

### Twoja kolej

Wróć do problemu zbierania paczek z lekcji 1.3. Stan to para (pole robota, zbiór paczek, które jeszcze leżą). Ruch na sąsiednie wolne pole kosztuje 1 i podniesienie paczki (`PICK`) też kosztuje 1. Cel: zebrać wszystkie paczki. Odległość Manhattan między polami oznaczamy *M*.

Oto sześciu kandydatów na heurystykę:

| Klucz | Heurystyka |
|---|---|
| `h1` | liczba paczek, które jeszcze leżą |
| `h2` | *M* od robota do najbliższej paczki, plus liczba paczek |
| `h3` | *M* od robota do najdalszej paczki, plus liczba paczek |
| `h4` | suma *M* od robota do każdej paczki, plus liczba paczek |
| `h5` | *M* od robota do rampy |
| `h6` | dwa razy liczba paczek |

Gdy nie ma już paczek, „najbliższa” i „najdalsza” paczka nie istnieją; wtedy ten składnik wynosi 0. Dla każdej heurystyki zdecyduj, czy jest dopuszczalna, i wpisz `True` albo `False` w słowniku `ADMISSIBLE` w części A pliku `task.py`.

Dla heurystyki dopuszczalnej znajdź problem zrelaksowany, z którego ona wynika. Dla niedopuszczalnej znajdź stan, w którym obiecuje więcej, niż robot naprawdę musi zrobić.

## Częste błędy

1. **Ta sama droga liczona kilka razy.** Jeśli heurystyka składa się z części, z których każda zakłada osobny przejazd, łatwo policzyć jeden odcinek drogi wielokrotnie. Jadąc do jednej paczki, robot często mija inne. Taka heurystyka przeszacowuje.
2. **Mnożenie przez liczbę paczek.** Odległość do najbliższej paczki razy liczba paczek wygląda rozsądnie, ale gdy paczki leżą obok siebie, robot nie musi jechać tak daleko do każdej z nich.
3. **Heurystyka bez odległości.** Heurystyka, która pomija jazdę, czyli największą część kosztu, prawie nie pomaga A\*. Testy wymagają, żeby Twoja oszczędzała więcej pracy niż samo liczenie paczek.
4. **Pominięty stan bez paczek.** `max()` ani `min()` ze zbioru pustego nie działa. W stanie celu heurystyka musi zwrócić 0, a nie zgłosić błąd.

Testy lekcji wykrywają każdy z tych błędów.

## Zadanie

### Część A: które heurystyki są dopuszczalne

Wypełnij w `task.py` słownik `ADMISSIBLE` dla heurystyk `h1`–`h6` z sekcji „Twoja kolej”.

### Część B: własna heurystyka

Zaimplementuj w `task.py` funkcję `parcel_heuristic(state)`, gdzie `state = (pole robota, frozenset paczek)`. Heurystyka:

- zwraca 0 w stanie celu, czyli gdy nie ma już paczek;
- nigdy nie przeszacowuje prawdziwego kosztu zebrania wszystkich paczek;
- sprawia, że A\* rozwija mniej węzłów niż z heurystyką „liczba paczek”.

Funkcję odległości Manhattan napisz w `task.py` sam albo przepisz swoją z lekcji 2.4. `task.py` nie importuje `introai.world.reference`.

### Jak sprawdzić

Z głównego katalogu repozytorium:

```bash
uv run pytest modules/02_search/07_designing_heuristics
```

Test dopuszczalności liczy dokładny koszt dla każdego osiągalnego stanu na trzech małych mapach i porównuje go z Twoją heurystyką. Jeśli heurystyka gdzieś przeszacowuje, komunikat pokazuje ten stan.

### Kryteria akceptacji

- Wszystkie testy lekcji przechodzą.
- Dla swojej heurystyki potrafisz wskazać problem zrelaksowany albo inny argument, dlaczego nie przeszacowuje.
- Potrafisz odpowiedzieć na pytania kontrolne, zanim zajrzysz do odpowiedzi.

## Czego testy nie sprawdzają

- **Dowodu dopuszczalności.** Testy sprawdzają wszystkie stany na trzech mapach, ale nie na każdej możliwej mapie. Heurystyka, która przechodzi testy, może przeszacowywać gdzie indziej. Argument musisz podać sam.
- **Spójności.** A\* z tego kursu wraca do stanów, gdy znajdzie tańszą drogę, więc wystarcza mu dopuszczalność. Czy Twoja heurystyka jest też spójna, testy nie sprawdzają.
- **Kosztu liczenia heurystyki.** Testy liczą rozwinięcia, a nie czas. Bardzo kosztowna heurystyka może oszczędzać rozwinięcia, a mimo to spowalniać przeszukiwanie.

## Eksperymenty

Otwórz [experiments.pl.ipynb](experiments.pl.ipynb). Przed każdym eksperymentem zapisz swoje przewidywanie, a potem je sprawdź:

1. Ile rozwinięć potrzebuje A\* z każdą heurystyką, także z Twoją, przy 1–6 paczkach? Która heurystyka daje za długi plan?
2. Czy *h*<sub>3</sub> jest większa lub równa *h*<sub>2</sub> we wszystkich stanach? Jak wypada w tym porównaniu Twoja heurystyka?
3. Czy heurystyka, która oszczędza najwięcej rozwinięć, jest też najszybsza?

## Pytania kontrolne

1. Dlaczego dokładny koszt problemu zrelaksowanego nigdy nie przeszacowuje kosztu prawdziwego problemu?
2. Wybierz z części A heurystykę, którą uznałeś za dopuszczalną, i podaj problem zrelaksowany albo inny argument, z którego to wynika.
3. Masz dwie dopuszczalne heurystyki, z których żadna nie dominuje drugiej. Jak je połączyć, żeby nadal była dopuszczalna i nie gorsza od żadnej z nich?
4. Wybierz z części A heurystykę, którą uznałeś za niedopuszczalną, i podaj stan, w którym przeszacowuje.
5. Kiedy silniejsza heurystyka może spowolnić przeszukiwanie, choć zmniejsza liczbę rozwinięć?

## Jeśli utkniesz

<details>
<summary>Podpowiedź 1: co musi zrobić robot</summary>

Zanim robot skończy, musi podnieść każdą paczkę (po jednej akcji na paczkę) i dojechać do każdej z nich. Czego co najmniej wymaga to drugie? Do której paczki musi dojechać na pewno najdalej?

</details>

<details>
<summary>Podpowiedź 2: stan celu</summary>

Gdy zbiór paczek jest pusty, zwróć 0, zanim policzysz `max()` albo `min()`. Możesz też użyć `max(..., default=0)`.

</details>

<details>
<summary>Podpowiedź 3: test pokazuje stan, w którym przeszacowujesz</summary>

Narysuj ten stan na mapie: gdzie stoi robot i gdzie leżą paczki. Policz ręcznie najkrótszy plan i porównaj go z każdą częścią swojej heurystyki. Któraś z nich liczy coś dwa razy.

</details>

## Co zapamiętać

- Heurystyki najłatwiej budować z problemów zrelaksowanych: usuń ograniczenie, rozwiąż łatwiejszy problem, a jego koszt będzie dopuszczalny, a nawet spójny.
- Heurystyka dominująca (większa, ale wciąż dopuszczalna) oznacza mniej rozwinięć.
- Maksimum dopuszczalnych heurystyk jest dopuszczalne i dominuje każdą z nich.
- Żeby wykazać, że heurystyka nie jest dopuszczalna, wystarczy jeden stan, w którym przeszacowuje.
- Silna heurystyka musi też być tania w liczeniu.

## Co dalej

- Po własnej próbie porównaj się z rozwiązaniem i odpowiedziami w [solutions/02_search/07_designing_heuristics/](../../../solutions/02_search/07_designing_heuristics/).
- Moduł 3 przenosi przeszukiwanie do gier. Funkcja oceny pozycji w grze to bliska krewna heurystyki.

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 3.6 (funkcje heurystyczne, problemy zrelaksowane, dominacja).
- J. Pearl, *Heuristics: Intelligent Search Strategies for Computer Problem Solving*, Addison-Wesley, 1984.
