from abc import ABC, abstractmethod
from .units import BaseUnit


class Skill(ABC):

    def __init__(self, name: str, damage: float, stamina_cost: float):
        self.name: str = name
        self.damage: float = damage
        self.stamina_cost: float = stamina_cost

    @abstractmethod
    def skill_effect(self, user: 'BaseUnit', enemy: 'BaseUnit') -> str:
        """Абстрактный метод эффекта умения. Должен быть переопределен в сабклассах."""
        pass

    def use(self, user: 'BaseUnit', enemy: 'BaseUnit') -> str:
        """Применение скилла"""

        return self.skill_effect(user, enemy)


class SuckerPunch(Skill):
    def __init__(self):
        super().__init__(name="Крысиный удар", damage=6.5, stamina_cost=10.0)

    def skill_effect(self, user: 'BaseUnit', enemy: 'BaseUnit') -> str:
        """Наносит подлый удар исподтишка, не требуя оружия и игнорирую вражескую броню"""

        total_damage: float = self.damage * user.unit_class.attack
        enemy.health -= total_damage
        return f"{user.name} использует {self.name} на {enemy.name}! Нанесено {total_damage} урона"


class IronButt(Skill):
    def __init__(self):
        super().__init__(name="Железный тыл", damage=0.0, stamina_cost=10.0)

    def skill_effect(self, user: 'BaseUnit', enemy: 'BaseUnit') -> str:
        """Сжатие стальных булок увеличивает броню"""

        armor_bonus: float = 1.8
        user.armor.defence += armor_bonus
        return f"{user.name} использует {self.name}! Броня увеличена на {armor_bonus}"
