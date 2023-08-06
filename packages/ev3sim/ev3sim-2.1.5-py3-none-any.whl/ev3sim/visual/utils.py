from typing import Tuple
import numpy as np

GLOBAL_COLOURS = {}


def rgb_to_hex(r, g, b):
    return "#" + "".join(
        (
            str(hex(r)).split("x")[-1].rjust(2, "0"),
            str(hex(g)).split("x")[-1].rjust(2, "0"),
            str(hex(b)).split("x")[-1].rjust(2, "0"),
        )
    )


def hex_to_pycolor(hex_str: str) -> Tuple[int]:
    assert len(hex_str) == 6, f"Invalid hex string, #{hex_str}"
    return (int(hex_str[:2], 16), int(hex_str[2:4], 16), int(hex_str[4:], 16))


def hsl_to_rgb(h, s, l):
    # Here, h is measured in degrees (0-360), s, l are between 0 and 1.
    c = (1 - abs(2 * l - 1)) * s
    r = ((h / 60) % 2) - 1
    x = c * (1 - abs(r))
    m = l - c / 2
    if 0 <= h < 60:
        return c + m, x + m, m
    if h < 120:
        return x + m, c + m, m
    if h < 180:
        return m, c + m, x + m
    if h < 240:
        return m, x + m, c + m
    if h < 300:
        return x + m, m, c + m
    return c + m, m, x + m


def worldspace_to_screenspace(point, customScreen=None):
    from ev3sim.visual.manager import ScreenObjectManager

    if customScreen is None:
        return (
            int(
                point[0] * ScreenObjectManager.instance.SCREEN_WIDTH / ScreenObjectManager.instance.MAP_WIDTH
                + ScreenObjectManager.instance._SCREEN_WIDTH_ACTUAL / 2
            ),
            int(
                -point[1] * ScreenObjectManager.instance.SCREEN_HEIGHT / ScreenObjectManager.instance.MAP_HEIGHT
                + ScreenObjectManager.instance._SCREEN_HEIGHT_ACTUAL / 2
            ),
        )
    return (
        int(point[0] * customScreen["SCREEN_WIDTH"] / customScreen["MAP_WIDTH"] + customScreen["SCREEN_WIDTH"] / 2),
        int(-point[1] * customScreen["SCREEN_HEIGHT"] / customScreen["MAP_HEIGHT"] + customScreen["SCREEN_HEIGHT"] / 2),
    )


def screenspace_to_worldspace(point, customScreen=None):
    from ev3sim.visual.manager import ScreenObjectManager

    if customScreen is None:
        return np.array(
            [
                float(
                    (point[0] - ScreenObjectManager.instance._SCREEN_WIDTH_ACTUAL / 2)
                    / ScreenObjectManager.instance.SCREEN_WIDTH
                    * ScreenObjectManager.instance.MAP_WIDTH
                ),
                float(
                    -(point[1] - ScreenObjectManager.instance._SCREEN_HEIGHT_ACTUAL / 2)
                    / ScreenObjectManager.instance.SCREEN_HEIGHT
                    * ScreenObjectManager.instance.MAP_HEIGHT
                ),
            ]
        )
    return np.array(
        [
            float(
                (point[0] - customScreen["SCREEN_WIDTH"] / 2) / customScreen["SCREEN_WIDTH"] * customScreen["MAP_WIDTH"]
            ),
            float(
                -(point[1] - customScreen["SCREEN_HEIGHT"] / 2)
                / customScreen["SCREEN_HEIGHT"]
                * customScreen["MAP_HEIGHT"]
            ),
        ]
    )
