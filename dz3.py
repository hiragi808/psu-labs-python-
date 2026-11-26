import json
from collections import defaultdict


def load_library(path='library.json'):
    """
    читат данные с jsona
    """
    with open('library.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    books_by_id = {book['id']: book for book in data.get('books', [])}
    readers_by_id = {reader['id']: reader for reader in data.get('readers', [])}
    loans = data.get('loans', [])
    print("=" * 40)
    print("СТАТИСТИКА БИБЛИОТЕКИ")
    print("=" * 40)
    print(f"Книг в каталоге:     {len(books_by_id)}")
    print(f"Читателей:           {len(readers_by_id)}")
    print(f"Выдач книг:          {len(loans)}")
    print("=" * 40)
    return books_by_id, readers_by_id, loans

def create_stats(readers_by_id):
    """
    cоздаёт словарь статистики с нулями для каждого читателя
    """
    return {
        rid: {
            "name":           reader.get('name', f'Читатель {rid}'),
            "total":          0,
            "returned":       0,
            "active":         0,
            "active_cost":    0,
            "most_expensive": None,   # (title, price)
        }
        for rid, reader in readers_by_id.items()
    }

def compute_stats(books_by_id, readers_by_id, loans):
    """
    Возвращает {reader_id: {total, returned, active, active_cost, most_expensive, name}}
    """
    stats = create_stats(readers_by_id)

    for loan in loans:
        rid = loan.get('reader_id')

        s = stats[rid]
        s["total"] += 1

        status = loan.get('status')
        if status == "returned":
            s["returned"] += 1
            continue
        s["active"] += 1

        book = books_by_id.get(loan.get('book_id'))

        price = int(book.get('price', 0) or 0)
        s["active_cost"] += price

        if s["most_expensive"] is None or price > s["most_expensive"][1]:
            s["most_expensive"] = (book.get('title'), price)

    return stats

def print_report(stats):
    header = (f"{'Читатель':<25}{'Всего':>6}{'Возвр.':>8}"
              f"{'Актив.':>8}{'Стоимость':>12}   Самая дорогая (активная)")
    print(header)
    print("-" * len(header))
    c=0
    for s in stats.values():
        c=c+1
        me = s["most_expensive"]
        me_str = f"{me[0]} ({me[1]} ₽)" if me else "—"
        print(f"{s['name']:<25}{s['total']:>6}{s['returned']:>8}"
              f"{s['active']:>8}{s['active_cost']:>12}   {me_str}")
        if c==5:
            break
    print("-" * 40)
    print("Должники")
    print("-" * 40)
    deb=[]
    for s in stats.values():
        if s["total"] > 0 and s["returned"] == 0 :
            deb.append(s)
    if len(deb)==0:
        print("Должников нету")
    else:
        for s in deb:
            print(f"{s['name']:<25}{s['total']:>6}{s['returned']:>8}")
def all_genres(books_by_id):
    """
    Жанры, которые есть в библиотеке
    """
    return {b.get('genre') for b in books_by_id.values() if b.get('genre')}
def authors_with_more_than(books_by_id, t=3):
    """
    Авторы, у которых больше t книг. Возвращает {author: count}.
    """
    counts = defaultdict(int)
    for b in books_by_id.values():
        author = b.get('author')
        if author:
            counts[author] += 1
    return {a: c for a, c in counts.items() if c > t}
def readers_each(readers_by_id,loans,books_by_id):
    """
    Читатели которые взяли книгу каждого жанра
    """
    res={}
    genres = all_genres(books_by_id)
    readers = defaultdict(set)
    for loan in loans:
        rid = loan.get('reader_id')
        book = books_by_id.get(loan.get('book_id'))
        genre = book.get('genre')
        if genre:
            readers[rid].add(genre)
    for r in readers:
        if readers[r]==genres:
            res = res.add(readers[r])
    return res
def genre_analis(books_by_id):
    genres = all_genres(books_by_id)
    stats=dict()
    for b in books_by_id.values():
        stats[b.get('genre')] = {"count": 0, "cost": 0, "popular": 0}
    for b in books_by_id.values():
        genre = b.get('genre')
        stats[genre]["count"] += 1
        stats[genre]["cost"] += int(b.get('price', 0))

        # 2. проход по выдачам: популярность
    for loan in loans:
        book = books_by_id.get(loan.get('book_id'))
        genre = book.get('genre')
        if genre:
            stats[genre]["popular"] += 1
    return stats
def most_popular(books_by_id):
    """
    Возвращает (title, times) — книгу с максимальным числом выдач
    """
    counts = defaultdict(int)
    for loan in loans:
        bid = loan.get('book_id')
        if bid in books_by_id:
            counts[bid] += 1
    top_id = None
    top_times = -1
    for bid, times in counts.items():
        if times > top_times:
            top_id = bid
            top_times = times
    title = books_by_id[top_id].get('title')
    return title, counts[top_id]
def genre_all(readers_by_id,loans,books_by_id):
    readers = defaultdict(set)
    for loan in loans:
        rid = loan.get('reader_id')
        book = books_by_id.get(loan.get('book_id'))
        genre = book.get('genre')
        if genre:
            readers[rid].add(genre)
    return set.intersection(*readers.values())
def authors_with_more_than(books_by_id, t=3):
    """{author: count} для авторов, у которых больше t книг."""
    counts = defaultdict(int)
    for b in books_by_id.values():
        author = b.get('author')
        if author:
            counts[author] += 1
    return {a: c for a, c in counts.items() if c > t}

def reportjson(books_by_id,readers_by_id,loans,):
    readers = compute_stats(books_by_id, readers_by_id, loans)
    activeloans = sum(v["active"] for v in readers.values())
    debt = sum(v["active_cost"] for v in readers.values())
    summary = {
        "total_books":len(books_by_id),
        "total_readers":len(readers_by_id),
        "total_loans":len(loans),
        "active_loans": activeloans,
        "total_debt": debt
    }
    readers_sorted = sorted(
        readers.items(),
        key=lambda a: a[1]["active_cost"],
        reverse=True,
    )
    top_readers = []
    for rid, s in readers_sorted[:5]:
        me = s["most_expensive"]
        top_readers.append({
            "name": s["name"],
            "active_books": s["active"],
            "total_cost": s["active_cost"],
            "most_expensive_book": me[0] if me else None,
        })
    popu = genre_analis(books_by_id)
    genre_statistic = []
    genre_statistic.append(popu)
    debtors = []

    stats = compute_stats(books_by_id, readers_by_id, loans)
    for s in stats.values():
        if s["total"] > 0 and s["returned"] == 0:
            debtors.append({
                "name": s["name"],
                "books_taken": s["total"],
                "books_not_returned": s["active"],
                "debt_amount": s["active_cost"],
            })
    report = {
        "summary": summary,
        "top_readers": top_readers,
        "genre_statistics": genre_statistic,
        "debtors": debtors,
    }

    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report
books_by_id, readers_by_id, loans = load_library("library.json")
stats = compute_stats(books_by_id, readers_by_id, loans)
print_report(stats)
print("Все жанры:", *all_genres(books_by_id))
print("Читатели почитавшие все жанры:", *readers_each(readers_by_id, loans, books_by_id))
print(genre_analis(books_by_id))
print(most_popular(books_by_id))
print(genre_all(readers_by_id, loans, books_by_id))
print(authors_with_more_than(books_by_id,2))
reportjson(books_by_id,readers_by_id,loans)

