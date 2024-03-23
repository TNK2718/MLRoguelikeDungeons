import g
import game.color
import game.components.ai
from game.components.fighter import Fighter


def die(fighter: Fighter) -> None:
    actor = fighter.entity
    if actor.try_get(game.components.ai.BaseAI) is None:
        return

    if g.engine.player is actor:
        death_message = "You died!"
        death_message_color = game.color.player_die
    else:
        death_message = f"{actor.name} is dead!"
        death_message_color = game.color.enemy_die

    actor.char = "%"
    actor.color = (191, 0, 0)
    actor.blocks_movement = False
    actor[game.components.ai.BaseAI] = None
    actor.name = f"remains of {actor.name}"
    actor.render_order = game.render_order.RenderOrder.CORPSE

    g.engine.message_log.add_message(death_message, death_message_color)

    g.engine.player.level.add_xp(actor.level.xp_given)


def apply_damage(fighter: Fighter, damage: int) -> None:
    assert damage >= 0
    fighter.hp = max(0, fighter.hp - damage)
    if fighter.hp <= 0:
        die(fighter)


def heal(fighter: Fighter, amount: int) -> int:
    """Heal a fighter.  Return the total hp healed."""
    assert amount >= 0
    old_hp = fighter.hp
    fighter.hp = min(fighter.hp + amount, fighter.max_hp)
    return fighter.hp - old_hp
