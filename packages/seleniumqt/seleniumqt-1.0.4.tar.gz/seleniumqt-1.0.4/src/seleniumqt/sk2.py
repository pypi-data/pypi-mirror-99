# coding: utf-8
# scroll to view
import logging


logger = logging.getLogger(__name__)


def gte(d, p):
    try:
        wind = d.get_window_size()
        obj = p.rect

        print(wind, obj)

        x_ = 0
        y_ = 0
        if obj['y'] < 1 and obj['x'] < 1:
            x_ = obj['width'] * 2
            y_ = obj['height'] * 3

        if obj['y'] < 1 or obj['x'] < 1:
            return True
        else:
            d.execute_script("arguments[0].scrollIntoView(false);", p)
            if obj['y'] > wind['height'] * 2 / 3:
                y_ = obj['height'] * 3

            elif obj['y'] < wind['height'] / 3:
                y_ = 0 - obj['height'] * 3

            if obj['x'] > wind['width'] * 4 / 5:
                x_ = obj['width'] * 2
            elif obj['x'] < wind['width'] / 5:
                x_ = 0 - obj['width'] * 2

        d.execute_script("window.scrollBy(%s,%s)" % (x_, y_))

    except:
        logger.info('控件无法显示')

    return True
