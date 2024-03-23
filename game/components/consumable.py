from __future__ import annotations

from typing import Optional

import g
import game.action
import game.color
import game.combat
import game.components.ai
import game.components.inventory
import game.engine
import game.entity
import game.exceptions
import game.input_handlers
from game.node import Node
from game.typing import ActionOrHandler


class Consumable(Node):
    @property
    def item(self) -> game.entity.Item:
        assert isinstance(self.parent, game.entity.Item)
        return self.parent

    def get_action(self, consumer: game.entity.Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return game.action.ItemAction(consumer, self.item)

    def activate(self, action: game.action.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        item = self.item
        inventory = item.parent
        assert isinstance(inventory, game.components.inventory.Inventory)
        inventory.items.remove(item)
        item.parent = None


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        super().__init__()
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: game.entity.Actor) -> Optional[ActionOrHandler]:
        g.engine.message_log.add_message("Select a target location.", game.color.needs_target)
        return game.input_handlers.SingleRangedAttackHandler(
            callback=lambda xy: game.action.ItemAction(consumer, self.item, xy),
        )

    def activate(self, action: game.action.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not g.engine.game_map.visible[action.target_xy]:
            raise game.exceptions.Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise game.exceptions.Impossible("You must select an enemy to target.")
        if target is consumer:
            raise game.exceptions.Impossible("You cannot confuse yourself!")

        g.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            game.color.status_effect_applied,
        )
        target[game.components.ai.BaseAI] = game.components.ai.ConfusedEnemy(
            entity=target,
            previous_ai=target[game.components.ai.BaseAI],
            turns_remaining=self.number_of_turns,
        )

        self.consume()


class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        super().__init__()
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: game.entity.Actor) -> Optional[ActionOrHandler]:
        g.engine.message_log.add_message("Select a target location.", game.color.needs_target)
        return game.input_handlers.AreaRangedAttackHandler(
            radius=self.radius,
            callback=lambda xy: game.action.ItemAction(consumer, self.item, xy),
        )

    def activate(self, action: game.action.ItemAction) -> None:
        target_xy = action.target_xy

        if not g.engine.game_map.visible[target_xy]:
            raise game.exceptions.Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in g.engine.game_map.entities:
            if not isinstance(actor, game.entity.Actor):
                continue
            if actor.distance(*target_xy) <= self.radius:
                g.engine.message_log.add_message(
                    f"The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!"
                )
                game.combat.apply_damage(actor.fighter, self.damage)
                targets_hit = True

        if not targets_hit:
            raise game.exceptions.Impossible("There are no targets in the radius.")
        self.consume()


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        super().__init__()
        self.amount = amount

    def activate(self, action: game.action.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = game.combat.heal(consumer.fighter, self.amount)

        if amount_recovered > 0:
            g.engine.message_log.add_message(
                f"You consume the {self.item.name}, and recover {amount_recovered} HP!",
                game.color.health_recovered,
            )
            self.consume()
        else:
            raise game.exceptions.Impossible("Your health is already full.")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        super().__init__()
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: game.action.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in g.engine.game_map.entities:
            if not isinstance(actor, game.entity.Actor):
                continue
            if actor is not consumer and self.item.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            g.engine.message_log.add_message(
                f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            game.combat.apply_damage(target.fighter, self.damage)
            self.consume()
        else:
            raise game.exceptions.Impossible("No enemy is close enough to strike.")
