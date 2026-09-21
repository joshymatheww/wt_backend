from enum import Enum


class Category(str, Enum):
    push = "push"
    pull = "pull"
    legs = "legs"
    core = "core"


class MuscleGroup(str, Enum):
    chest = "chest"
    front_detlts = "front_delts"
    side_delts = "side_delts"
    triceps = "triceps"
    lats = "lats"
    upper_back = "upper_back"
    lower_back = "lower_back"
    rear_delts = "rear_delts"
    biceps = "biceps"
    forearms = "forearms"
    quads = "quads"
    hamstrings = "hamstrings"
    glutes = "glutes"
    calves = "calves"
    abs = "abs"

CATALOGUE: dict[MuscleGroup, tuple[str, Category, int]] = {
    MuscleGroup.chest: ("Chest", Category.push, 2),
    MuscleGroup.front_detlts: ("Front delts", Category.push, 2),
    MuscleGroup.side_delts: ("Side delts", Category.push, 2)
}
