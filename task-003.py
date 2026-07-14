import timeit
import random
import os


# А ось бенчмарки я люблю, і інколи, коли маєш обмежені ресурси і
# працюєш з великою кількістю даних вже починаєш робити бенчмарки і оптимізації :)

# ==================== РЕАЛІЗАЦІЯ АЛГОРИТМІВ ====================

def insertion_sort(arr):
    """Сортування вставками. O(n²) у гіршому/середньому випадку, O(n) у найкращому."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """Сортування злиттям. O(n log n) у всіх випадках, O(n) додаткової пам'яті."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def timsort_builtin(arr):
    """Вбудоване сортування Python (Timsort)."""
    arr.sort()
    return arr


# ==================== ГЕНЕРАТОРИ ДАНИХ ====================

def gen_random(n):
    return [random.randint(0, n * 10) for _ in range(n)]


def gen_nearly_sorted(n):
    # Починаємо з відсортованого масиву та вносимо невеликий шум
    arr = list(range(n))
    noise = int(n * 0.05)
    for _ in range(noise):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def gen_sorted(n):
    return list(range(n))


def gen_reversed(n):
    return list(range(n))[::-1]


# ==================== ЕМПІРИЧНЕ ТЕСТУВАННЯ ====================

def benchmark(algo_func, datasets, trials=5):
    results = {}
    for name, data in datasets.items():
        times = []
        for _ in range(trials):
            # Копіюємо дані, щоб не змінювати оригінал між запусками
            arr_copy = data[:]
            t = timeit.timeit(lambda: algo_func(arr_copy), number=1)
            times.append(t)
        results[name] = sum(times) / len(times)
    return results


def verify_complexity_scaling(algo_func, base_size=500):
    """Перевіряє співвідношення часу виконання T(2n)/T(n) для підтвердження складності."""
    data = gen_random(base_size)
    t1 = timeit.timeit(lambda: algo_func(data[:]), number=3)

    data_2x = gen_random(base_size * 2)
    t2 = timeit.timeit(lambda: algo_func(data_2x[:]), number=3)

    ratio = t2 / t1 if t1 > 0 else float('inf')
    return ratio


def main():
    print("Початок емпіричного тестування алгоритмів сортування...")
    sizes = [500, 1000, 2000]
    dataset_types = {
        "random": gen_random,
        "nearly_sorted": gen_nearly_sorted,
        "sorted": gen_sorted,
        "reversed": gen_reversed
    }

    all_results = {}

    for size in sizes:
        print(f"\n Розмір масиву: {size}")
        datasets = {name: gen(size) for name, gen in dataset_types.items()}

        ins_res = benchmark(insertion_sort, datasets)
        merge_res = benchmark(merge_sort, datasets)
        timsort_res = benchmark(timsort_builtin, datasets)

        all_results[size] = {"insertion": ins_res, "merge": merge_res, "timsort": timsort_res}

        print(f"{'Набір даних':<15} | {'Insertion Sort':>12} | {'Merge Sort':>12} | {'Timsort':>12}")
        print("-" * 65)
        for ds in dataset_types.keys():
            print(f"{ds:<15} | {ins_res[ds]:>10.5f}s | {merge_res[ds]:>10.5f}s | {timsort_res[ds]:>10.5f}s")

    # Перевірка складності на великих масивах
    print("\nПеревірка теоретичної складності (співвідношення T(2n)/T(n) при n=1000):")
    for name, func in [("Insertion Sort", insertion_sort), ("Merge Sort", merge_sort), ("Timsort", timsort_builtin)]:
        ratio = verify_complexity_scaling(func, base_size=1000)
        print(f"{name:<15} | T(2n)/T(n) ≈ {ratio:.2f}")

    # Генерація README
    generate_readme(all_results)


def generate_readme(results, complexity_ratios):
    header = "| Розмір | Тип даних      | Insertion Sort (с) | Merge Sort (с) | Timsort (с) |\n|--------|----------------|--------------------|----------------|-------------|"
    rows = []
    for size in sorted(results.keys()):
        for ds in ["random", "nearly_sorted", "sorted", "reversed"]:
            ins = results[size]["insertion"][ds]
            merge = results[size]["merge"][ds]
            timsort = results[size]["timsort"][ds]
            rows.append(f"| {size} | {ds:<14} | {ins:>16.5f} | {merge:>16.5f} | {timsort:>13.5f} |")

    empirical_table = header + "\n" + "\n".join(rows)

    comp_header = "| Алгоритм         | T(2n)/T(n) (при n=500) |\n|------------------|------------------------|"
    comp_rows = []
    for name, ratio in complexity_ratios.items():
        comp_rows.append(f"| {name:<16} | {ratio:>24.2f} |")
    complexity_table = comp_header + "\n" + "\n".join(comp_rows)

    readme_content = f"""# Порівняння алгоритмів сортування: Insertion Sort, Merge Sort та Timsort (автоматична регенерація при запуску бенчмарка)

## Мета дослідження
Емпірична перевірка теоретичної складності трьох алгоритмів сортування на різних типах даних. Демонстрація переваг гібридного підходу Timsort у реальних умовах.

## Методологія
- Алгоритми: Insertion Sort, Merge Sort, Timsort (вбудований list.sort()).
- Набори даних: випадкові, майже відсортовані, повністю відсортовані, зворотні.
- Розміри масивів: 500, 1000, 2000 елементів.
- Замір часу: модуль timeit, середнє значення з 5 запусків на кожен набір.
- Перевірка складності: аналіз співвідношення T(2n)/T(n) для підтвердження асимптотики.

## Емпіричні результати
{empirical_table}

## Перевірка теоретичної складності
{complexity_table}

## Аналіз результатів
1. Insertion Sort демонструє квадратичне зростання часу виконання (T(2n)/T(n) ~ 4.0), що підтверджує O(n^2). На майже відсортованих даних працює швидше через мінімальну кількість порівнянь.
2. Merge Sort показує лінійно-логарифмічне зростання (T(2n)/T(n) ~ 1.8-2.0), що відповідає O(n log n). Час виконання стабільний незалежно від початкового порядку, але має вищі накладні витрати через копіювання та рекурсію.
3. Timsort демонструє найменший час виконання на всіх типах даних. Його гібридна архітектура (поєднання сортування вставками для малих блоків і злиттям для великих) забезпечує адаптивність до реальних даних та мінімізацію накладних витрат.

## Висновки
1. Insertion Sort ефективний лише для малих або частково впорядкованих масивів. На великих випадкових даних його продуктивність різко падає через O(n^2).
2. Merge Sort гарантує стабільну асимптотику O(n log n), але поступається Timsort у практичних умовах через додаткові витрати пам'яті та рекурсію.
3. Timsort є оптимальним вибором для більшості задач завдяки:
   - Адаптивності до наявної впорядкованості в даних.
   - Використанню Insertion Sort для малих підмасивів, що зменшує накладні витрати.
   - Стабільній складності O(n log n) у гіршому випадку з меншою константою порівняно з класичним Merge Sort.
4. Програмістам рекомендується використовувати вбудовані функції sorted() та list.sort(), оскільки вони реалізують оптимізований Timsort, який забезпечує найкраще співвідношення продуктивності, стабільності та споживання пам'яті. Власна реалізація алгоритмів сортування рідко виправдана з точки зору підтримки коду та ефективності.

## Додатково
- Тестування виконано на Python 3.x.
- Для точних вимірювань завжди використовуйте timeit з достатньою кількістю ітерацій.
- Реальні дані часто містять локальну впорядкованість, що робить Timsort ще більш переважним у промисловому середовищі.
- Теоретична складність O(n²) або O(n log n) описує поведінку алгоритму лише у границі, коли розмір вхідних даних прямує до нескінченності. На малому об'ємі даних алгоритм не завжди має перевагу, через особливості роботи пайтона та операційної системи, а також навіть тактування енергоефективних ядер процесора.
"""

    with open("readme.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("\nЕмпіричні дані та висновки збережено у файлі readme.md")


def main():
    print("Початок емпіричного тестування алгоритмів сортування...")
    sizes = [500, 1000, 2000, 5000]
    dataset_types = {
        "random": gen_random,
        "nearly_sorted": gen_nearly_sorted,
        "sorted": gen_sorted,
        "reversed": gen_reversed
    }

    all_results = {}

    for size in sizes:
        print(f"\nРозмір масиву: {size}")
        datasets = {name: gen(size) for name, gen in dataset_types.items()}

        ins_res = benchmark(insertion_sort, datasets)
        merge_res = benchmark(merge_sort, datasets)
        timsort_res = benchmark(timsort_builtin, datasets)

        all_results[size] = {"insertion": ins_res, "merge": merge_res, "timsort": timsort_res}

        print(f"{'Набір даних':<15} | {'Insertion Sort':>12} | {'Merge Sort':>12} | {'Timsort':>12}")
        print("-" * 65)
        for ds in dataset_types.keys():
            print(f"{ds:<15} | {ins_res[ds]:>13.5f}s | {merge_res[ds]:>11.5f}s | {timsort_res[ds]:>11.5f}s")

    print("\nПеревірка теоретичної складності (співвідношення T(2n)/T(n) при n=500):")
    complexity_ratios = {}
    for name, func in [("Insertion Sort", insertion_sort), ("Merge Sort", merge_sort), ("Timsort", timsort_builtin)]:
        ratio = verify_complexity_scaling(func, base_size=500)
        complexity_ratios[name] = ratio
        print(f"{name:<15} | T(2n)/T(n) ~ {ratio:.2f}")

    generate_readme(all_results, complexity_ratios)


if __name__ == "__main__":
    main()
