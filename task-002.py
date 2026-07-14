import turtle
import math
import sys


def koch(t, length, depth):
    """
    Рекурсивна функція для малювання кривої Коха.
    :param t: екземпляр Turtle
    :param length: довжина поточного відрізка
    :param depth: рівень рекурсії (глибина)
    """
    if depth == 0:
        # Базовий випадок рекурсії: малюємо прямий відрізок
        t.forward(length)
    else:
        # Рекурсивний крок: замінюємо відрізок на 4 менші відрізки,
        # що утворюють рівносторонній трикутник без основи
        koch(t, length / 3, depth - 1)
        t.left(60)
        koch(t, length / 3, depth - 1)
        t.right(120)
        koch(t, length / 3, depth - 1)
        t.left(60)
        koch(t, length / 3, depth - 1)


def draw_koch_snowflake(size, depth):
    """Ініціалізує середовище turtle та малює сніжинку Коха."""
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха (рівень рекурсії: {depth})")

    t = turtle.Turtle()
    t.speed(0)      # Максимальна швидкість малювання
    t.hideturtle()  # Приховуємо курсор для чистого вигляду
    t.pensize(1)

    # Розрахунок початкової позиції для центрування трикутника на екрані
    height = size * math.sqrt(3) / 2
    start_x = -size / 2
    start_y = -height / 3

    t.penup()
    t.goto(start_x, start_y)
    t.pendown()

    # Малюємо три сторони сніжинки (кожна сторона є кривою Коха)
    for _ in range(3):
        koch(t, size, depth)
        t.right(120)

    screen.mainloop()


def main():
    try:
        user_input = input("Введіть рівень рекурсії (ціле число >= 0): ")
        level = int(user_input)

        if level < 0:
            print("Помилка: рівень рекурсії має бути невід'ємним числом.")
            sys.exit(1)

        # Попередження про можливу повільну роботу при високих рівнях
        if level > 6:
            print("Увага: високі рівні рекурсії (>6) можуть значно уповільнити малювання та споживати багато пам'яті.")

        draw_koch_snowflake(300, level)

    except ValueError:
        print("Помилка: введено некоректне значення. Будь ласка, введіть ціле число.")
        sys.exit(1)


if __name__ == "__main__":
    main()
