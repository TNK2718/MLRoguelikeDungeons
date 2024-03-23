from __future__ import annotations

import game.entity
from game.components.base_component import BaseComponent


class Fighter(BaseComponent):
    def __init__(self, hp: int, base_defense: int, base_power: int):
        super().__init__()
        self.max_hp = hp
        self.hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        actor = self.get_parent(game.entity.Actor)
        if actor.equipment:
            return actor.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        actor = self.get_parent(game.entity.Actor)
        if actor.equipment:
            return actor.equipment.power_bonus
        else:
            return 0
