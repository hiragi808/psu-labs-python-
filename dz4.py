"""Лабораторная работа №4, задание dz4: остатки склада.

Часть 1. Генерация данных и сезонность.
Часть 2. Поиск дефицита.
Часть 3. Векторизованное пополнение.
Часть 4. Квартальная агрегация и стабильность.
Отчёт по задачам со звёздочкой сохраняется в dz4_report.txt.
"""

from pathlib import Path

import numpy as np

REPORT_PATH = Path(__file__).with_name("dz4_report.txt")

MONTHS = ["янв", "фев", "мар", "апр", "май", "июн",
          "июл", "авг", "сен", "окт", "ноя", "дек"]


def part1_report(stock, seasonality, stock_seasonal):
    lines = []

    lines.append("ОТЧЁТ ПО ЗАДАНИЮ dz4 (лабораторная работа №4)")
    lines.append("Часть 1. Генерация данных и сезонность")
    lines.append("=" * 60)
    lines.append("")

    lines.append("ЗАДАЧА 2*. Базовый массив остатков stock")
    lines.append("-" * 60)
    lines.append("Сначала зафиксировал seed = 42, чтобы при каждом запуске")
    lines.append("получались одни и те же данные.")
    lines.append("Затем сгенерировал массив 50x12: 50 товаров на 12 месяцев.")
    lines.append("Значения - целые числа от 30 до 80.")
    lines.append("")
    lines.append(f"shape = {stock.shape}, dtype = {stock.dtype}")
    lines.append(f"минимум = {stock.min()}, максимум = {stock.max()}")
    lines.append(f"суммарный остаток за все месяцы = {stock.sum()} шт.")
    lines.append("")
    lines.append("Массив stock (строки - товары, столбцы - месяцы):")
    for row in stock:
        lines.append("  " + " ".join(f"{value:3d}" for value in row))
    lines.append("")

    lines.append("ЗАДАЧА 3. Сезонные множители seasonality")
    lines.append("-" * 60)
    lines.append("Сделал массив из 12 множителей:")
    lines.append("  зима  (1-3 месяцы)  -> 1.5")
    lines.append("  весна (4-6 месяцы)  -> 0.8")
    lines.append("  лето  (7-9 месяцы)  -> 1.2")
    lines.append("  осень (10-12 месяцы)-> 1.0")
    lines.append("seasonality = [" + ", ".join(f"{v:.1f}" for v in seasonality) + "]")
    lines.append("")

    lines.append("ЗАДАЧА 4*. Остатки с учётом сезонности")
    lines.append("-" * 60)
    lines.append("Умножил каждый столбец stock на свой множитель: столбец j")
    lines.append("умножается на seasonality[j]. NumPy делает это сам, потому что")
    lines.append("массив (50, 12) умножается на массив (12,).")
    lines.append("Результат округлил через np.round, чтобы остаток остался целым")
    lines.append("числом штук, и привёл тип к int через astype(int).")
    lines.append("")
    lines.append(f"shape = {stock_seasonal.shape}, dtype = {stock_seasonal.dtype}")
    lines.append(f"минимум = {stock_seasonal.min()}, максимум = {stock_seasonal.max()}")
    lines.append(f"суммарный остаток с сезонностью = {stock_seasonal.sum()} шт.")
    lines.append("")
    lines.append("Массив stock_seasonal (строки - товары, столбцы - месяцы):")
    for row in stock_seasonal:
        lines.append("  " + " ".join(f"{value:4d}" for value in row))
    lines.append("")

    lines.append("Остатки по месяцам (сумма по всем товарам), шт.:")
    lines.append(f"  {'месяц':<6}{'базовый':>10}{'с сезоном':>12}{'разница':>10}")
    base_totals = stock.sum(axis=0)
    seasonal_totals = stock_seasonal.sum(axis=0)
    for month, base_total, seasonal_total in zip(MONTHS, base_totals, seasonal_totals):
        diff = int(seasonal_total) - int(base_total)
        lines.append(f"  {month:<6}{base_total:>10d}{seasonal_total:>12d}{diff:>+10d}")
    lines.append(f"  {'итого':<6}{base_totals.sum():>10d}{seasonal_totals.sum():>12d}"
                 f"{int(seasonal_totals.sum() - base_totals.sum()):>+10d}")
    lines.append("")

    return "\n".join(lines)


def part2_report(is_low, low_stock_months, deficit_products):
    lines = []

    lines.append("Часть 2. Поиск дефицита")
    lines.append("=" * 60)
    lines.append("")

    lines.append("ЗАДАЧА 2*. Сколько месяцев товар был в дефиците")
    lines.append("-" * 60)
    lines.append("Дефицит - это остаток меньше 40 шт. Сравнил остатки с 40:")
    lines.append("is_low = stock_seasonal < 40")
    lines.append("Получился булев массив той же формы (50, 12), где True значит")
    lines.append("дефицит в конкретном месяце у конкретного товара.")
    lines.append("Потом сложил True по строкам: low_stock_months = is_low.sum(axis=1).")
    lines.append("True в NumPy считается за 1, поэтому сумма по строке - это число")
    lines.append("месяцев с дефицитом у товара.")
    lines.append("")
    lines.append(f"всего месяцев с дефицитом: {is_low.sum()} из {is_low.size}")
    lines.append("")
    lines.append("low_stock_months (индекс товара: месяцев в дефиците):")
    for product, months in enumerate(low_stock_months):
        lines.append(f"  товар {product:2d}: {months:2d}")
    lines.append("")

    lines.append("ЗАДАЧА 3*. Товары в дефиците 3 месяца и более")
    lines.append("-" * 60)
    lines.append("Сначала сделал маску low_stock_months >= 3, затем взял индексы")
    lines.append("True-элементов через np.where(...)[0].")
    lines.append("")
    if len(deficit_products) > 0:
        lines.append(f"подходящих товаров: {len(deficit_products)}")
        lines.append("индексы: " + ", ".join(str(i) for i in deficit_products))
        lines.append("")
        lines.append("индекс товара: месяцев в дефиците")
        for product in deficit_products:
            lines.append(f"  товар {product:2d}: {low_stock_months[product]:2d}")
    else:
        lines.append("подходящих товаров нет")
    lines.append("")

    return "\n".join(lines)


def part3_report(stock, updated_stock):
    lines = []

    lines.append("Часть 3. Векторизованное пополнение")
    lines.append("=" * 60)
    lines.append("")

    lines.append("ЗАДАЧА 2*. Правило автозаказа")
    lines.append("-" * 60)
    lines.append("Правило: если остаток меньше 40, добавляем 50, иначе не меняем.")
    lines.append("Записал это одной строкой:")
    lines.append("updated_stock = np.where(stock < 40, stock + 50, stock)")
    lines.append("np.where проверяет условие поэлементно и берёт число из ветки")
    lines.append("stock + 50 или из ветки stock. Обе ветки - массивы, поэтому")
    lines.append("цикл не нужен, всё считается сразу для всех 600 ячеек.")
    lines.append("")
    lines.append(f"ячеек, где сработало правило: {(stock < 40).sum()} из {stock.size}")
    lines.append(f"shape = {updated_stock.shape}, dtype = {updated_stock.dtype}")
    lines.append(f"минимум = {updated_stock.min()}, максимум = {updated_stock.max()}")
    lines.append(f"суммарный остаток после пополнения = {updated_stock.sum()} шт.")
    lines.append("")
    lines.append("Массив updated_stock (строки - товары, столбцы - месяцы):")
    for row in updated_stock:
        lines.append("  " + " ".join(f"{value:4d}" for value in row))
    lines.append("")

    return "\n".join(lines)


def part4_report(quarterly_avg, best_product, stds, stable, unstable):
    lines = []

    lines.append("Часть 4. Квартальная агрегация и стабильность")
    lines.append("=" * 60)
    lines.append("")

    lines.append("ЗАДАЧА 1*. Массив по кварталам")
    lines.append("-" * 60)
    lines.append("Сделал reshape(50, 4, 3): 12 месяцев идут по порядку, поэтому")
    lines.append("первые 3 столбца - это 1-й квартал, следующие 3 - 2-й и так далее.")
    lines.append("Вторая ось - квартал, третья - месяц внутри квартала.")
    lines.append("")

    lines.append("ЗАДАЧА 2*. Средний остаток по кварталам")
    lines.append("-" * 60)
    lines.append("mean(axis=2) считает среднее по трём месяцам внутри квартала,")
    lines.append("np.round(..., 2) округляет до двух знаков. Получился массив (50, 4):")
    lines.append("")
    lines.append(f"  {'товар':>6}{'Q1':>8}{'Q2':>8}{'Q3':>8}{'Q4':>8}")
    for product, row in enumerate(quarterly_avg):
        lines.append(f"  {product:>6}" + "".join(f"{value:>8.2f}" for value in row))
    lines.append("")

    lines.append("ЗАДАЧА 3*. Максимальный средний остаток в 4-м квартале")
    lines.append("-" * 60)
    lines.append("Взял последний столбец quarterly_avg[:, 3] и нашёл максимум")
    lines.append("через np.argmax - он возвращает индекс максимального элемента.")
    lines.append("")
    lines.append(f"товар с индексом {best_product}, средний остаток в Q4 = "
                 f"{quarterly_avg[best_product, 3]:.2f} шт.")
    lines.append("")

    lines.append("ЗАДАЧА 4*. Стабильность спроса")
    lines.append("-" * 60)
    lines.append("Стандартное отклонение показывает, насколько значения разбросаны")
    lines.append("вокруг среднего. Формула: sqrt(mean((x - mean(x)) ** 2)).")
    lines.append("np.std по умолчанию делит на n (ddof=0), то есть считает")
    lines.append("генеральное отклонение по всем 12 месяцам, а не выборочное.")
    lines.append("Посчитал по каждому товару: np.std(stock, axis=1) -")
    lines.append("ось 1 это месяцы, поэтому на выходе 50 значений.")
    lines.append("Дальше np.argsort сортирует индексы по возрастанию отклонения:")
    lines.append("первые три - самые стабильные, последние три - самые нестабильные.")
    lines.append("")
    lines.append("отклонение по каждому товару:")
    for product, value in enumerate(stds):
        lines.append(f"  товар {product:2d}: {value:6.2f}")
    lines.append("")
    lines.append("3 самых стабильных товара (минимальное отклонение):")
    for product in stable:
        lines.append(f"  товар {product:2d}: std = {stds[product]:.2f}")
    lines.append("")
    lines.append("3 самых нестабильных товара (максимальное отклонение):")
    for product in unstable:
        lines.append(f"  товар {product:2d}: std = {stds[product]:.2f}")
    lines.append("")

    return "\n".join(lines)


def main():
    # Часть 1.
    np.random.seed(42)
    stock = np.random.randint(30, 81, size=(50, 12))
    seasonality = np.array([1.5] * 3 + [0.8] * 3 + [1.2] * 3 + [1.0] * 3)
    stock_seasonal = np.round(stock * seasonality).astype(int)

    # Часть 2.
    is_low = stock_seasonal < 40
    low_stock_months = is_low.sum(axis=1)
    deficit_products = np.where(low_stock_months >= 3)[0]

    # Часть 3.
    updated_stock = np.where(stock < 40, stock + 50, stock)

    # Часть 4.
    quarterly_avg = np.round(updated_stock.reshape(50, 4, 3).mean(axis=2), 2)
    best_product = int(np.argmax(quarterly_avg[:, 3]))

    stds = np.std(stock, axis=1)
    order = np.argsort(stds)
    stable = order[:3]
    unstable = order[-3:][::-1]

    print("месяцев с дефицитом:", is_low.sum(), "из", is_low.size)
    print("товары с дефицитом 3+ месяца:", deficit_products.tolist())
    print("ячеек, где сработало пополнение:", (stock < 40).sum())
    print("quarterly_avg:", quarterly_avg.shape)
    print(f"максимум в Q4: товар {best_product}, "
          f"{quarterly_avg[best_product, 3]:.2f}")
    print("самые стабильные:", stable.tolist(),
          "std =", np.round(stds[stable], 2).tolist())
    print("самые нестабильные:", unstable.tolist(),
          "std =", np.round(stds[unstable], 2).tolist())

    report = "\n".join([
        part1_report(stock, seasonality, stock_seasonal),
        part2_report(is_low, low_stock_months, deficit_products),
        part3_report(stock, updated_stock),
        part4_report(quarterly_avg, best_product, stds, stable, unstable),
    ])
    REPORT_PATH.write_text(report, encoding="utf-8")
    print("Отчёт сохранён:", REPORT_PATH)


if __name__ == "__main__":
    main()
