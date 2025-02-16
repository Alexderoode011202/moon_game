from typing import List
import re
paths: List[str] = [
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/half_left_moon.png",
        "media/main_game/moon_types/3_4_left_moon.png",
        "media/main_game/moon_types/full_moon.png",
        "media/main_game/moon_types/3_4_right_moon.png",
        "media/main_game/moon_types/half_right_moon.png",
        "media/main_game/moon_types/1_4_left_moon.png",
        "media/main_game/moon_types/empty_moon.png"
    ]

test = "media/main_game/moon_types/1_4_left_moon.png"
for name in paths:
    new = re.sub("[0-9]_[0-9]", "quarter", name)
    new = re.sub("_", " ", name)
    print(new)
#new: str = re.sub("[0-9]_[0-9]", "quarter", test)
#print(new)