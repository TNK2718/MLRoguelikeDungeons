"""Frequently accessed globals are delcared here."""
from __future__ import annotations

from typing import TYPE_CHECKING

import tcod

if TYPE_CHECKING:
    import game.engine

context: tcod.context.Context
engine: game.engine.Engine
