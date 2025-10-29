from dataclasses import dataclass
from .skills import Skill, SuckerPunch, IronButt


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


Warrior: UnitClass = UnitClass(
    name="Воин",
    max_health=100.0,
    max_stamina=100.0,
    attack=1.2,
    stamina=1.0,
    armor=1.0,
    skill=SuckerPunch()
)

Tank: UnitClass = UnitClass(
    name="Танк",
    max_health=110.0,
    max_stamina=95.0,
    attack=1.0,
    stamina=1.0,
    armor=1.2,
    skill=IronButt()
)
