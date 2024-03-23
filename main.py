#!/usr/bin/env python3
import logging
import sys
import traceback
import warnings
from pathlib import Path

import tcod

import g
import game.color
import game.engine
import game.entity
import game.exceptions
import game.input_handlers
import game.procgen
import game.setup_game
from game.typing import EventHandlerLike


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(Path("data/dejavu16x16_gs_tc.png"), 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler: EventHandlerLike = game.setup_game.MainMenu()

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as g.context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                event_handler.on_render(console=root_console)
                g.context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        g.context.convert_event(event)
                        event_handler = event_handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(event_handler, game.input_handlers.EventHandler):
                        g.engine.message_log.add_message(traceback.format_exc(), game.color.error)
        except game.exceptions.QuitWithoutSaving:
            raise SystemExit()
        except SystemExit:  # Save and quit.
            game.setup_game.save_game(Path("savegame.sav"))
            raise
        except BaseException:  # Save on any other error.
            game.setup_game.save_game(Path("savegame.sav"))
            raise


if __name__ == "__main__":
    if __debug__:
        if not sys.warnoptions:
            warnings.simplefilter("default")
        logging.basicConfig(level=logging.DEBUG)
    main()
