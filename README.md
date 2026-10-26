# ANADIG — sklep internetowy

ANADIG to projekt sklepu internetowego stworzony w oparciu o framework Django. Aplikacja umożliwia przeglądanie produktów, zarządzanie koszykiem oraz składanie zamówień. Interfejs wykorzystuje Bootstrap i minimalistyczny design.

## Funkcjonalności

- Katalog dostępnych produktów.
- Wyświetlanie nazw, opisów, cen i zdjęć produktów.
- Dodawanie produktów do koszyka.
- Zmiana ilości produktów w koszyku.
- Usuwanie produktów z koszyka.
- Automatyczne obliczanie wartości koszyka.
- Formularz składania zamówienia z danymi klienta i adresem dostawy.
- Zapisywanie zamówień i ich pozycji w bazie danych.
- Panel administracyjny Django do zarządzania produktami.

## Technologie

- **Python 3.12**
- **Django 4.2**
- **Bootstrap 5.3**
- **HTML5 i CSS3**
- **SQLite**

## Wymagania

Do uruchomienia projektu potrzebujesz:
- Pythona 3.12.
- Gita.
- Menedżera pakietów pip.

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/damian-malec/django-blog.git
cd django-blog
```

### 2. Utwórz środowisko wirtualne

```bash
python3.12 -m venv .venv
```

Aktywuj je:

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Zainstaluj zależności

```bash
python -m pip install "Django==4.2.30"
```

### 4. Wykonaj migracje bazy danych

```bash
python manage.py migrate
```

### 5. Utwórz konto administratora

```bash
python manage.py createsuperuser
```

### 6. Uruchom serwer

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem:

http://127.0.0.1:8000/

Panel administracyjny:

http://127.0.0.1:8000/admin/

## Struktura projektu

- `blog/` — pierwotna aplikacja blogowa.
- `shop/` — aplikacja sklepu internetowego.
- `shop/models.py` — modele produktów i zamówień.
- `shop/views.py` — logika katalogu, koszyka i zamówień.
- `shop/templates/shop/` — szablony HTML sklepu.
- `mysite/settings.py` — konfiguracja projektu Django.
- `mysite/urls.py` — główne adresy URL.
- `manage.py` — narzędzie do zarządzania projektem.

## Status projektu

Projekt jest rozwijany. Aktualnie obejmuje podstawową funkcjonalność sklepu, zarządzanie koszykiem i składanie zamówień.

Płatności internetowe i automatyczna wysyłka wiadomości e-mail nie są jeszcze zaimplementowane.

## Autor

Damian Malec