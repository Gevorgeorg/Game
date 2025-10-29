from dataclasses import dataclass
import random
import marshmallow_dataclass
import json


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def calculate_damage(self) -> float:
        """Рассчитывает случайный урон оружия"""

        return random.uniform(self.min_damage, self.max_damage)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: list[Weapon]
    armors: list[Armor]


EquipDataSchema = marshmallow_dataclass.class_schema(EquipmentData)


class Equipment:
    def __init__(self, data: str) -> None:
        self.data: EquipmentData = self.__reader(data)

    def get_weapon(self, name: str) -> Weapon:
        for weapon in self.data.weapons:
            if weapon.name == name:
                return weapon

    def get_armor(self, name: str) -> Armor:
        for armor in self.data.armors:
            if armor.name == name:
                return armor

    def get_weapon_names(self) -> list[str]:
        return [weapon.name for weapon in self.data.weapons]

    def get_armor_names(self) -> list[str]:
        return [armor.name for armor in self.data.armors]

    def __reader(self, data: str) -> EquipmentData:
        with open(data, 'r', encoding="utf-8") as file:
            json_data = json.load(file)
            return EquipDataSchema().load(json_data)
