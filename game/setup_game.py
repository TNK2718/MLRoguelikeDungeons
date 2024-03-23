"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import random
import traceback
from pathlib import Path
from typing import Optional

import tcod
from PIL import Image  # type: ignore

import g
import game.color
import game.engine
import game.entity_factories
import game.game_map
import game.input_handlers
import game.procgen
from game.input_handlers import BaseEventHandler

# Load the background image.  Pillow returns an object convertable into a NumPy array.
background_image = Image.open(Path("data/menu_background.png"))


def new_game() -> game.engine.Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    engine = game.engine.Engine()
    engine.game_world = game.game_map.GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )
    engine.rng = random.Random()
    engine.game_world.generate_floor()
    engine.player = game.entity_factories.player.spawn(engine.game_map, *engine.game_map.enter_xy)
    engine.update_fov()

    engine.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", game.color.welcome_text)

    dagger = copy.deepcopy(game.entity_factories.dagger)
    leather_armor = copy.deepcopy(game.entity_factories.leather_armor)

    dagger.parent = engine.player.inventory
    leather_armor.parent = engine.player.inventory

    engine.player.inventory.items.append(dagger)
    engine.player.equipment.toggle_equip(dagger, add_message=False)

    engine.player.inventory.items.append(leather_armor)
    engine.player.equipment.toggle_equip(leather_armor, add_message=False)

    g.engine = engine
    return engine


def save_game(path: Path) -> None:
    """If an engine is active then save it."""
    if not hasattr(g, "engine"):
        return  # If called before a new game is started then g.engine is not assigned.
    path.write_bytes(lzma.compress(pickle.dumps(g.engine)))
    print("Game saved.")


def load_game(path: Path) -> game.engine.Engine:
    """Load an Engine instance from a file."""
    engine = pickle.loads(lzma.decompress(path.read_bytes()))
    assert isinstance(engine, game.engine.Engine)
    g.engine = engine
    return engine


class MainMenu(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE ANCIENT KINGS",
            fg=game.color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By (Your name here)",
            fg=game.color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=game.color.menu_text,
                bg=game.color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[game.input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                load_game(Path("savegame.sav"))
                return game.input_handlers.MainGameEventHandler()
            except FileNotFoundError:
                return game.input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return game.input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            new_game()
            return game.input_handlers.MainGameEventHandler()

        return None
