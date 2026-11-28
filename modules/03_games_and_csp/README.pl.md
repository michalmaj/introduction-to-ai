[English](README.md) | **Polski**

# Moduł 3 — Gry i problemy z ograniczeniami

W module 2 agent sam decydował o każdym kroku i szukał ciągu akcji, który prowadzi do celu. Ten moduł pokazuje dwa rodzaje problemów, w których takie przeszukiwanie nie wystarcza. W **grach** ruchy na zmianę wykonuje przeciwnik, który chce wygrać, więc agent potrzebuje strategii na każdą jego odpowiedź. W **problemach z ograniczeniami** (CSP, *constraint satisfaction problems*) liczy się nie droga do celu, lecz sam wynik: przypisanie wartości zmiennym, które spełnia wszystkie warunki naraz. Gry rozgrywamy w kółko i krzyżyk oraz w „cztery w rzędzie” na planszy 5 × 5. Problemy z ograniczeniami wracają do magazynu: trzeba ułożyć harmonogram dostaw.

## Cele modułu

Po tym module:

- opiszesz grę dwuosobową jako problem przeszukiwania i znajdziesz optymalny ruch algorytmem minimax;
- przytniesz drzewo gry algorytmem alfa-beta i zmierzysz, jak bardzo zależy to od kolejności ruchów;
- przerwiesz przeszukiwanie na zadanej głębokości i zaprojektujesz własną funkcję oceny pozycji;
- opiszesz problem jako zmienne, dziedziny i ograniczenia i rozwiążesz go przeszukiwaniem z nawrotami, wspieranym heurystykami i propagacją ograniczeń.

## Lekcje

Listę lekcji modułu, ich zależności i stan przygotowania znajdziesz w [mapie kursu](../../COURSE_MAP.pl.md).

Moduł ma dwie części, które można robić w dowolnej kolejności:

- **gry, lekcje core:** 3.1 → 3.2 → 3.3. Po lekcji 3.3 Twój program gra w „cztery w rzędzie” z własną funkcją oceny;
- **problemy z ograniczeniami, lekcje core:** 3.4 → 3.5. Wymagają tylko lekcji 2.5. Są w przygotowaniu;
- **lekcje opcjonalne:** 3.6 o propagacji ograniczeń AC-3 (po 3.5) oraz 3.7 o grach z losowością i 3.8 o przeszukiwaniu drzewa metodą Monte Carlo (obie po 3.3). Są w przygotowaniu.

## Dokąd to prowadzi

- **Moduł 4, algorytmy inspirowane naturą.** Przeszukiwanie lokalne ocenia stany funkcją celu, podobnie jak funkcja oceny ocenia pozycję w grze, i nie szuka drogi do celu. Harmonogram dostaw z lekcji o ograniczeniach wraca tam w lekcji 4.5, rozwiązywany algorytmem genetycznym.
- **Moduł 8, uczenie ze wzmocnieniem.** Przeszukiwanie drzewa metodą Monte Carlo (lekcja 3.8) wybiera ruchy, ważąc to, co już wiadomo, i to, czego warto jeszcze spróbować. Ten sam dylemat eksploracji i eksploatacji otwiera moduł 8.
