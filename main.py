import numpy as np
import matplotlib.pyplot as plt
import re

# N = 4096
# N = 2048
N = 1024

CANVAS = np.zeros((N, N), dtype=int)

# Чайник скейлится вместе с размерами N, но при этом теряется качество картинки
def split_lines_V(lines):
    img_npX = np.array([])
    img_npY = np.array([])

    for line in lines.split("\n"):
        try:
            v, x, y, z = re.split(" ", line)
            if v == "v":
                x = int(float(x) * (N / 7) - N / 2)
                y = int(float(y) * (N / 7))
                np_x = np.array([x])
                np_y = np.array([y])
                img_npX = np.append(img_npX, [np_x])
                img_npY = np.append(img_npY, [np_y])
        except:
            continue

    return img_npX, img_npY


def split_lines_F(lines):
    img_npF = np.array([], )

    for line in lines.split("\n"):
        try:
            f, x, y, z = re.split(" ", line)
            if f == "f":
                x, y, z = int(x), int(y), int(z)
                img_npF = np.append(img_npF, [x, y, z])

        except:
            continue

    img_npF = np.reshape(img_npF, (-1, 3))
    return img_npF


def bresenham(img_npX, img_npY, img_npF):
    # Здесь алгоритм построения из линий -> треугольники -> фигура
    canvasNew = np.zeros((N, N), dtype=int)

    img_npXY = img_npX
    img_npXY = np.append(img_npXY, img_npY)
    img_npXY = np.reshape(img_npXY, (2, -1))

    for f in img_npF:
        for edge in range(0, 3, 1):
            if edge == 0 or edge == 1:
                cur_f = int(f[edge])
                next_f = int(f[edge + 1])
                points = bresenham_1_line(int(img_npXY[1, cur_f - 1]), int(img_npXY[0, cur_f - 1]),
                                          int(img_npXY[1, next_f - 1]), int(img_npXY[0, next_f - 1]))

            else:
                cur_f = int(f[-1])
                next_f = int(f[0])
                points = bresenham_1_line(int(img_npXY[1, cur_f - 1]), int(img_npXY[0, cur_f - 1]),
                                          int(img_npXY[1, next_f - 1]), int(img_npXY[0, next_f - 1]))
            # Здесь надо в канвасе делать прорисовку
            for point in points:
                canvasNew[int(point[0]), int(point[1])] = 255


    # print(img_npXY[0].__len__(), img_npXY[1].__len__()) # 2 * 3644
    return canvasNew


def bresenham_1_line(x1, y1, x2, y2):
    # Здесь алгоритм построения одной линии
    # Начальные значения
    dx = x2 - x1
    dy = y2 - y1

    # Определяем крутизну линии
    is_steep = abs(dy) > abs(dx)

    # "Перевернем" линию
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Если нужно поменяем значения начала и конца линии
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Пересчитаем разницу
    dx = x2 - x1
    dy = y2 - y1

    # Ошибка по у
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Создание точек между началом и концом линии
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Перевернем список, если координаты были свапнуты
    if swapped:
        points.reverse()
    return points



def draw_teapot(lines):
    global CANVAS

    img_npX, img_npY = split_lines_V(lines)
    img_npF = split_lines_F(lines)

    # Производим все расчеты и изменяем canvas
    CANVAS = bresenham(img_npX, img_npY, img_npF)

    plt.figure()
    plt.title("Алгоритм Брезенхема")
    # plt.axis("off")
    plt.xlabel('Ширина чайника')
    plt.ylabel('Высота чайника')
    plt.imshow(CANVAS, origin='lower')
    plt.grid(False)
    plt.show()


if __name__ == "__main__":
    # Чтобы файл не закрывать самому когда он станет не нужен
    with open("teapot.obj", "r") as img_file:
        lines = img_file.read()

        draw_teapot(lines)
        # print("Points:", bresenham_1_line(0, 0, 10, 15))
