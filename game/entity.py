from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar

import game.components.ai
import game.components.consumable
import game.components.equipment
import game.components.equippable
import game.components.fighter
import game.components.inventory
import game.components.level
import game.game_map
import game.render_order
from game.node import Node

T = TypeVar("T", bound="Entity")


class Entity(Node):
    """A generic object to represent players, enemies, items, etc."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: game.render_order.RenderOrder = game.render_order.RenderOrder.CORPSE,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

    @property
    def gamemap(self) -> game.game_map.GameMap:
        return self.get_parent(game.game_map.GameMap)

    def spawn(self: T, gamemap: Node, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        return clone

    def place(self, x: int, y: int, gamemap: Optional[Node] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        self.parent = gamemap

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        *,
        ai_cls: Type[game.components.ai.BaseAI],
        equipment: game.components.equipment.Equipment,
        fighter: game.components.fighter.Fighter,
        inventory: Optional[game.components.inventory.Inventory] = None,
        level: game.components.level.Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=game.render_order.RenderOrder.ACTOR,
        )

        ai_cls(self).parent = self
        equipment.parent = self
        fighter.parent = self
        if inventory is None:
            inventory = game.components.inventory.Inventory(0)
        inventory.parent = self
        level.parent = self

    @property
    def equipment(self) -> game.components.equipment.Equipment:
        return self[game.components.equipment.Equipment]

    @property
    def fighter(self) -> game.components.fighter.Fighter:
        return self[game.components.fighter.Fighter]

    @property
    def inventory(self) -> game.components.inventory.Inventory:
        return self[game.components.inventory.Inventory]

    @property
    def level(self) -> game.components.level.Level:
        return self[game.components.level.Level]

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return self.try_get(game.components.ai.BaseAI) is not None


class Item(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        *,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[game.components.consumable.Consumable] = None,
        equippable: Optional[game.components.equippable.Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=game.render_order.RenderOrder.ITEM,
        )
        if consumable:
            consumable.parent = self
        if equippable:
            equippable.parent = self

    @property
    def consumable(self) -> Optional[game.components.consumable.Consumable]:
        return self.try_get(game.components.consumable.Consumable)

    @property
    def equippable(self) -> Optional[game.components.equippable.Equippable]:
        return self.try_get(game.components.equippable.Equippable)
