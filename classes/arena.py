import random
from typing import Optional

from classes.units import BaseUnit


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=Singleton):
    """Класс арены, для управления боем между хероями"""

    def __init__(self):
        self.stamina_regen: float = 3.0
        self.player: Optional['BaseUnit'] = None
        self.enemy: Optional['BaseUnit'] = None
        self.game_is_running: bool = False

    def start_game(self, heroes: dict) -> None:
        self.player: BaseUnit = heroes.get("player")
        self.enemy: BaseUnit = heroes.get("enemy")
        self.game_is_running = True

    def end_game(self) -> str | None:
        self.game_is_running: bool = False

        if self.player.health <= 0:
            return f"Победил {self.enemy.name}!"
        elif self.enemy.health <= 0:
            return f"Победил {self.player.name}!"

    def _stamina_regen(self, unit: BaseUnit) -> str:
        """Восстановление выносливости юнита"""

        if unit.stamina + self.stamina_regen > unit.unit_class.max_stamina:
            unit.stamina = unit.unit_class.max_stamina
        else:
            unit.stamina += self.stamina_regen
        return f"{unit.name} восстановил {self.stamina_regen} выносливости"

    def next_turn(self) -> str | None:
        """Действия противника при передаче хода"""

        if not self.game_is_running:
            return "Бой не активен"

        battle_result: str | None = self.check_health()
        if battle_result:
            return battle_result

        use_skill_chance: bool = random.random() < 0.3
        can_use_skill: bool = (not self.enemy.skill_used and
                               self.enemy.stamina >= self.enemy.unit_class.skill.stamina_cost)
        can_attack: bool = (self.enemy.weapon and
                            self.enemy.stamina >= self.enemy.weapon.stamina_per_hit)

        match (use_skill_chance and can_use_skill, can_attack):
            case (True, _):
                enemy_action: str = self.enemy.use_skill(self.player)
                return f"Ход противника: {enemy_action}"

            case (False, True):
                enemy_action: str = self.enemy.hit(self.player)
                return f"Ход противника: {enemy_action}"

            case _:
                enemy_action: str = self._stamina_regen(self.enemy)
                return f"{self.enemy.name} выдохся и пропускает ход. {enemy_action}"

    def check_health(self) -> str | None:
        """Проверка здоровья"""
        if self.player.health <= 0 or self.enemy.health <= 0:
            return self.end_game()

    def hitting(self) -> str:
        """Обмен ударами"""

        if not self.game_is_running:
            return "Бой не активен"

        player_action: str = self.player.hit(self.enemy)
        if self.check_health():
            return f"{player_action}\n\n{self.check_health()}"

        enemy_action: str = self.next_turn()

        if self.check_health():
            return f"{player_action}\n\n{enemy_action}\n\n{self.check_health()}"

        return f"{player_action}\n\n{enemy_action}"

    def use_skill(self) -> str:
        """Использование скиллов"""

        if not self.game_is_running:
            return "Бой не активен"

        player_action: str = self.player.use_skill(self.enemy)

        if "Навык уже использован" in player_action:
            return player_action

        if self.check_health():
            return f"{player_action}\n\n{self.check_health()}"

        enemy_action = self.next_turn()

        if self.check_health():
            return f"{player_action}\n\n{enemy_action}\n\n{self.check_health()}"

        return f"{player_action}\n\n{enemy_action}"

    def skip_turn(self) -> str:
        """Пропуск хода для восстановления выносливости"""
        if not self.game_is_running:
            return "Бой не активен"

        recovery_msg: str = self._stamina_regen(self.player)

        enemy_action: str = self.next_turn()

        if self.check_health():
            return f"Игрок пропустил ход\n{recovery_msg}\n\n{enemy_action}\n\n{self.check_health()}"

        return f"Игрок пропустил ход\n{recovery_msg}\n\n{enemy_action}"
