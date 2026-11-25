[English](README.md) | **Polski**

# Rozwiązania wzorcowe

Ten katalog jest celowo publiczny. Ma tę samą strukturę co `modules/`: rozwiązanie lekcji `modules/02_search/02_bfs_dfs/` znajdziesz w `solutions/02_search/02_bfs_dfs/`.

## Jak z nich korzystać

1. Najpierw spróbuj samodzielnie: przeczytaj lekcję, uzupełnij `task.py` i uruchom testy.
2. Jeśli utkniesz, skorzystaj z podpowiedzi w sekcji „Jeśli utkniesz” w lekcji.
3. Dopiero potem porównaj swoją wersję z `task.py` z tego katalogu. Przeczytaj też `answers.pl.md` z odpowiedziami do pytań kontrolnych i listą tego, co powinna zawierać dobra odpowiedź.

Rozwiązanie wzorcowe to tylko jedna z poprawnych implementacji. Jeśli Twoja wygląda inaczej, a testy przechodzą, zwykle wszystko jest w porządku.

## Materiały dla autorów

- `mutants/` zawiera celowo błędne implementacje. Każda odpowiada typowemu błędowi opisanemu w lekcji, a testy lekcji muszą ją odrzucić.
- `alternatives/` zawiera inne poprawne implementacje. Testy lekcji muszą je przyjąć, więc nie narzucają jednego rozwiązania.

Testy lekcji możesz uruchomić na dowolnym z tych plików, na przykład na rozwiązaniu wzorcowym:

```bash
uv run pytest modules/02_search/02_bfs_dfs --impl=solution
```
