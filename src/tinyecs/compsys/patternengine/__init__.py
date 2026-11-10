from collections.abc import Callable
from dataclasses import dataclass

import glm
import tinyecs as ecs

from aenum import extend_enum
from patternengine import BulletSource
from tinyecs import EntityID
from tinyecs.compsys import Comp
from tinyecs.compsys.dynamics import PRSA


extend_enum(Comp, 'EMITTER')


@dataclass
class Emitter:
    """A component holding data for an emitter.

    :param bullet_source: See :class:`patternengine.engine.BulletSource`
    :param factory: The callback to launch bullets.

    The prototype for ``factory`` is::

        def factory(pos: glm.vec2, momentum: glm.vec2) -> None:
            ...

    """

    bullet_source: BulletSource
    factory: Callable[[glm.vec2, glm.vec2], None]


def sys_emitter(eid: EntityID, emitter: Emitter, prsa: PRSA):
    """Run an emit callback if the emitter fires.

    :param eid: The entity ID
    :param emitter: The :class:`Emitter` object
    :param prsa: The PRSA transform object of the entity

    The `patternengine` emits positions relative to ``(0, 0)``, and a
    normalized momentum vector, both dependent of the chosen ring type in the
    ``BulletSource``.

    The position will be rotated by the emitter's angle in degrees, after
    that, the emitter's position will be added to it.

    The momentum will also be rotated by the emitter's angle.

    Then both will be passed to the factory callback.

    Once the emitter is exhausted, the entity is marked as killed.
    """

    try:
        chunk = next(emitter.bullet_source)
    except StopIteration:
        ecs.add_component(eid, Comp.IS_KILLED, True)
        return

    rad = glm.radians(prsa.rotation)
    for pos, momentum in chunk:
        real_momentum = glm.rotate(momentum, rad)
        real_pos = glm.rotate(pos, rad)
        emitter.factory(real_pos + prsa.pos, real_momentum)
