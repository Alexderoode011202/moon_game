import re
from typing import List
paths: List[str] = [
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/half_left_moon.png",
        "media/main_game/moon_types/3_4_left_moon.png",
        "media/main_game/moon_types/full_moon.png",
        "media/main_game/moon_types/3_4_right_moon.png",                            # in total 8 unique cards
        "media/main_game/moon_types/half_right_moon.png",
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/empty_moon.png"
    ]

for path in paths:
    name = re.sub("[0-9]_[0-9]", "quarter", path)
    name = re.sub("_", " ", name)
    name = name[:-4]
    print(name)