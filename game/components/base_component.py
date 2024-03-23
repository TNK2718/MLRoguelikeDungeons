from __future__ import annotations

import game.engine
import game.entity
import game.game_map
from game.node import Node


class BaseComponent(Node):
    @property
    def entity(self) -> game.entity.Actor:
        """Owning entity instance."""
        return self.get_parent(game.entity.Actor)

    @property
    def owner(self) -> game.entity.Actor:
        """Owning entity instance."""
        return self.get_parent(game.entity.Actor)

    @property
    def gamemap(self) -> game.game_map.GameMap:
        return self.get_parent(game.game_map.GameMap)
