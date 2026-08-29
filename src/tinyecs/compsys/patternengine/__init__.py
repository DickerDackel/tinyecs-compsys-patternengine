from collections.abc import Callable
from dataclasses import dataclass

import glm
import tinyecs as ecs

from aenum import extend_enum
from patternengine import BulletSource
from tinyecs import EntityID
from tinyecs.compsys import Comp
from tinyecs.compsys.sdl2 import PRSA


extend_enum(Comp, 'EMITTER')


@dataclass
class Emitter:
    """A component holding data for an emitter.
    :param bullet_source: See :class:`patternengine.engine.BulletSource`
    :param factory: The callback to launch bullets.

    The prototype for ``factory`` is

        def factory(pos: Vector, momentum: Vector)
    """

    bullet_source: BulletSource
    factory: Callable


def sys_emitter(dt: float, eid: EntityID, emitter: Emitter, prsa: PRSA):
    """Run an emit callback if the emitter fires.

    :param dt: Delta time
    :param eid: The entity ID
    :param emitter: The :class:`Emitter` object
    :param prsa: The PRSA transform object of the entity

    The `patternengine` emits position relative to ``(0, 0)``.  ``prsa.pos``
    of the emitter will be added to that before sending position and momentum
    to the factory callback.
    """

    try:
        chunk = next(emitter.bullet_source)
    except StopIteration:
        ecs.add_component(eid, Comp.IS_KILLED, True)
        return

    rad = glm.radians(prsa.rotation)
    for pos, momentum in chunk:
        real_momentum = glm.rotate(momentum, rad)
        emitter.factory(pos + prsa.pos, real_momentum)
