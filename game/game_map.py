from __future__ import annotations

from typing import Iterator, Optional

import numpy as np
from numpy.typing import NDArray

import game.engine
import game.entity
from game.node import Node


class GameMap(Node):
    def __init__(self, engine: game.engine.Engine, width: int, height: int):
        super().__init__()
        self.engine = engine
        self.width, self.height = width, height
        self.tiles: NDArray[np.uint8] = np.zeros((width, height), dtype=np.uint8, order="F")
        self.enter_xy = (width // 2, height // 2)  # Entrance coordinates.

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

        self.downstairs_location = (0, 0)

    @property
    def entities(self) -> Iterator[game.entity.Entity]:
        yield from self.get_children(game.entity.Entity)

    @property
    def gamemap(self) -> GameMap:
        return self

    def get_blocking_entity_at(self, x: int, y: int) -> Optional[game.entity.Entity]:
        """Returns an entity that blocks the position at x,y if one exists, otherwise returns None."""
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[game.entity.Actor]:
        for actor in self.entities:
            if actor.blocks_movement and actor.x == x and actor.y == y and isinstance(actor, game.entity.Actor):
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: game.engine.Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        current_floor: int = 0,
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.current_floor = current_floor

    def generate_floor(self) -> None:
        import game.procgen

        self.current_floor += 1

        self.engine.game_map = game.procgen.generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
        )
