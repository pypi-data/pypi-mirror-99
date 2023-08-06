from PIL import  Image

def img_flag(fn):
    image_one = Image.open(fn)

    x, y = image_one.size

    x_list = list()
    y_list = list()

    for i in range(x):
        t = image_one.getpixel((i, int(y / 2)))
        x_list.append(t)

    for j in range(y):
        t = image_one.getpixel((int(x / 2), j))
        y_list.append(t)

    return x_list, y_list
