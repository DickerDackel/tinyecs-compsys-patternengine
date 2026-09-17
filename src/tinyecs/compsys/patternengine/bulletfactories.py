"""Bullet image factories and preconfigured bullets.

patternengine comes with a set of preconfigured bullet factories to ease
experimenting with the library.

To create your own sizes and colors, see the documentation of
`bullet_image_factory` below.

The preconfigured factories can be found in the `BULLET_FACTORIES` dict under
their specific name in the following schema:

    SIZE[-ring]-COLOR

with the available sizes

    cores:
        tiny         radius=4
        small        radius=6
        medium       radius=12
        large        radius=16
        larger       radius=24

    rings:
        tiny         radius=4
        small        radius=6
        medium       radius=12
        large        radius=16
        larger       radius=24

Rings can be one of

    core, circle, square, diamond, triangle, oval, arrowhead

and colors

    pink, cyan, yellow, lightblue, green, red

So, if you need e.g. a pink medium sized sprite with a ring, you can get this
it like this:

    tinyecs.compsys.patternengine.bulletfactories.BULLETS['medium-ring-pink']


"""

import pygame

from rpeasings import in_quad  # noqa: F403

STROKE_SCALE = 1 / 8


def stroke_width(size):
    # min(int(size * STROKE_SCALE), 1)
    return max(int(size * STROKE_SCALE), 1)


# The ones that are a 1-to-1 mapping feel redundant, but they are common
# bullet colors.
BULLET_COLOR = {
    'white': 'white',
    'red': 'red',
    'green': 'green',
    'blue': 'blue',
    'cyan': 'cyan',
    'magenta': 'magenta',
    'yellow': 'yellow',
    'pink': 'hotpink',
    'orange': 'orange',
    'brown': 'brown',
    'lightblue': 'lightblue',
    'danmaku-magenta': '#660066',
    'danmaku-yellow': '#ffff66',
    'danmaku-blue': '#0066ff',
    'danmaku-green': '#226655',
}

CORE_SIZE = {
    'tiny': 8,
    'small': 12,
    'medium': 20,
    'large': 24,
    'larger': 40,
    'extralarge': 56,
}

RING_SIZE = {
    'tiny': 12,
    'small': 16,
    'medium': 24,
    'large': 32,
    'larger': 48,
    'extralarge': 64,
}


def core_factory(size, color, gradient=in_quad, *kwargs):  # noqa: F405
    r0 = int((3 / 4) * size) // 2

    image = pygame.Surface((size, size))
    image.set_colorkey('black')
    rect = image.get_rect()

    c0 = pygame.Color('white')
    c1 = pygame.Color(color)

    for r in range(r0, 1, -1):
        t = gradient(r / r0)  # noqa: F405
        color = c0.lerp(c1, t)
        pygame.draw.circle(image, color, rect.center, r)

    return image


def circle_factory(size, color):  # noqa: F405
    r = size // 2
    image = pygame.Surface((size, size))
    image.set_colorkey('black')
    rect = image.get_rect()

    stroke = stroke_width(size)

    pygame.draw.circle(image, color, rect.center, r, width=stroke)

    return image


def square_factory(size, color):
    image = pygame.Surface((size, size))
    image.set_colorkey('black')
    rect = image.get_rect()

    stroke = stroke_width(size)

    pygame.draw.rect(image, color, rect, width=stroke)

    return image


def diamond_factory(size, color):
    stroke = stroke_width(size)

    image = pygame.Surface((2 * size, size))
    image.set_colorkey('black')
    rect = image.get_rect()
    rect.width -= 1
    rect.height -= 1
    pygame.draw.rect(image, 'black', rect, 1)

    points = [rect.midtop, rect.midright, rect.midbottom, rect.midleft]
    pygame.draw.polygon(image, color, points, width=stroke)

    return image


def triangle_factory(size, color):
    size *= 1.75
    height = size * 0.75 ** 0.5
    shift = size / 2 - (height / 3 - 1)
    oversize = 2 * 2 * height / 3

    tri = pygame.Surface((size, size))
    tri.set_colorkey('black')
    r_tri = tri.get_rect()
    r_tri.width -= 1
    r_tri.height -= 1

    stroke = stroke_width(size)

    points = [(0, 0), (0, r_tri.width), (height, r_tri.centery), (0, 0)]
    pygame.draw.polygon(tri, color, points, width=stroke)

    image = pygame.Surface((oversize, oversize))
    image.set_colorkey('black')
    rect = image.get_rect()

    r_tri.centerx = rect.centerx + shift - 2
    r_tri.centery = rect.centery - 1

    image.blit(tri, r_tri)

    return image


def oval_factory(size, color):
    image = pygame.Surface((2 * size, size))
    image.set_colorkey('black')
    rect = image.get_rect()

    stroke = stroke_width(size)
    pygame.draw.ellipse(image, color, rect, width=stroke)

    return image


def arrowhead_factory(size, color):
    image = pygame.Surface((size, size))
    image.set_colorkey('black')
    rect = image.get_rect()

    e_rect = pygame.Rect(0, 0, size * 2, size)
    e_rect.centerx = 0

    stroke = stroke_width(size)
    pygame.draw.ellipse(image, color, e_rect, width=stroke)

    # Shift center point to make the core look better
    c_rect = rect.inflate(size // 3, 0)
    c_rect.topleft = (0, 0)
    canvas = pygame.Surface(c_rect.size)
    canvas.set_colorkey('black')
    rect.midright = c_rect.midright
    canvas.blit(image, rect)

    return canvas


# Must be declared down here because the functions need to be defined
RING_FACTORY = {
    'core': core_factory,
    'circle': circle_factory,
    'square': square_factory,
    'diamond': diamond_factory,
    'triangle': triangle_factory,
    'oval': oval_factory,
    'arrowhead': arrowhead_factory,
}


def merge(shape, core):
    """Merge two images into one.

    :param shape: An image containing the main shape of the bullet
    :param core: An image containing the core of the bullet
    :returns: Both images overlayed into a single image

    This is to combine rings and cores for bullet generation.
    """

    cs_rect = shape.get_rect()
    co_rect = core.get_rect(center=cs_rect.center)

    image = shape.copy()
    image.blit(core, co_rect)
    return image


def bullet_image_factory(size, color, kind):
    """Construct a new bullet image from the available sizes, colors and shapes.

    :param size: A symbolic name from ``CORE_SIZE`` or the size as a ``float``
    :param color: A symbolic name from ``BULLET_COLOR`` or a pygame-ce ``ColorLike``
    :param kind: A symbolic name from ``RING_FACTORY``
    :returns: A new bullet image

    """

    size_map = CORE_SIZE if kind == 'core' else RING_SIZE
    size_ = size_map.get(size, size)
    color_ = BULLET_COLOR.get(color, color)
    factory = RING_FACTORY[kind]

    return factory(size_, color_)
