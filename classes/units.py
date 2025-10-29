from abc import ABC
from typing import Optional, Type
from .equipment import Weapon, Armor


class BaseUnit(ABC):
    """Абстрактный базовый класс для всех юнитов в игре"""

    def __init__(
            self,
            name: str,
            unit_class: Type['UnitClass'],
            weapon: Optional[Weapon] = None,
            armor: Optional[Armor] = None
    ):
        self.name: str = name
        self.unit_class: Type['UnitClass'] = unit_class
        self.health: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Optional[Weapon] = weapon
        self.armor: Optional[Armor] = armor
        self.skill_used: bool = False

    def equip_weapon(self, weapon: Weapon) -> None:
        """Снарядить персонажа оружием"""
        self.weapon = weapon

    def equip_armor(self, armor: Armor) -> None:
        """Снарядить персонажа броней"""
        self.armor = armor

    def _count_damage(self, enemy: 'BaseUnit') -> float:
        """метод вычисляющий итоговый урон"""

        base_damage: float = self.weapon.calculate_damage()
        damage: float = base_damage * self.unit_class.attack

        if enemy.armor:
            armor_defense: float = enemy.armor.defence
            damage -= armor_defense
            damage: float | int = max(damage, 0)

            enemy.stamina -= enemy.armor.stamina_per_turn
            enemy.stamina: float | int = max(enemy.stamina, 0)

        stamina_cost: float = self.weapon.stamina_per_hit
        self.stamina -= stamina_cost
        self.stamina: float | int = max(self.stamina, 0)

        return round(damage, 1)

    def use_skill(self, enemy: 'BaseUnit') -> str:
        """Использование умения"""

        if self.skill_used:
            return "Навык уже использован"

        if self.stamina < self.unit_class.skill.stamina_cost:
            return f"{self.name} попытался использовать {self.unit_class.skill.name}, но у него нехватает  выносливости"

        self.skill_used: bool = True
        self.stamina -= self.unit_class.skill.stamina_cost

        result: str = self.unit_class.skill.use(self, enemy)
        return result

    def hit(self, enemy: 'BaseUnit') -> str:
        """Нанесение удара по цели"""

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} не хватает выносливости на удар!"

        damage: float = self._count_damage(enemy)
        enemy.health -= damage
        enemy.health = max(enemy.health, 0)

        return (f"{self.name} использует {self.weapon.name} "
                f"и наносит {damage} урона")


class Player(BaseUnit):
    def __init__(self, name: str, unit_class: Type['UnitClass'], weapon: Weapon, armor: Armor):
        super().__init__(name=name, unit_class=unit_class, weapon=weapon, armor=armor)


class Enemy(BaseUnit):
    def __init__(self, name: str, unit_class: Type['UnitClass'], weapon: Weapon, armor: Armor):
        super().__init__(name=name, unit_class=unit_class, weapon=weapon, armor=armor)
