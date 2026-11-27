[English](README.md) | **Polski**

# Moduł 2 — Przeszukiwanie

Jak znaleźć drogę od stanu początkowego do celu, jeśli wiemy tylko, jakie akcje są dostępne i do czego prowadzą? Ten moduł pokazuje strategie przeszukiwania przestrzeni stanów: od przeszukiwania wszerz i w głąb, przez uwzględnianie kosztów kroków, po heurystyki i algorytm A*. Zadania rozgrywają się w magazynie, w którym robot szuka trasy do rampy.

## Cele modułu

Po tym module:

- sformułujesz problem jako przeszukiwanie przestrzeni stanów;
- zaimplementujesz i prześledzisz BFS, DFS, przeszukiwanie kosztowe, greedy best-first i A*;
- porównasz strategie pod względem kompletności, optymalności, czasu i pamięci;
- zaprojektujesz heurystykę i ocenisz, czy jest dopuszczalna.

## Lekcje

Listę lekcji modułu, ich zależności i stan przygotowania znajdziesz w [mapie kursu](../../COURSE_MAP.pl.md).

Ścieżka przez moduł:

- **lekcje core:** 2.1 → 2.2 → 2.3 → 2.4 → 2.5. Po lekcji 2.5 znasz pięć strategii przeszukiwania i wiesz, kiedy której użyć;
- **lekcje opcjonalne:** 2.6 o iteracyjnym pogłębianiu i 2.7 o projektowaniu heurystyk. Obie wymagają tylko lekcji 2.5 i można je robić w dowolnej kolejności.

## Dokąd to prowadzi

- **Moduł 3, gry i problemy z ograniczeniami.** Przeszukiwanie, w którym ruchy wykonuje też przeciwnik. Funkcja oceny pozycji w grze to bliska krewna heurystyki z lekcji 2.4 i 2.7.
- **Moduł 4, algorytmy inspirowane naturą.** Gdy robot ma odebrać wiele paczek, przestrzeń stanów rośnie wykładniczo i dokładne przeszukiwanie przestaje wystarczać. Zobaczysz, jak w rozsądnym czasie znaleźć dobrą, choć niekoniecznie najlepszą trasę.
- **Moduł 8, uczenie ze wzmocnieniem.** A* zakłada, że znamy model świata. Q-learning uczy robota dojeżdżać do celu bez tej wiedzy.
