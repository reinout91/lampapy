import math

from build123d import (
    Axis,
    Bezier,
    BuildLine,
    BuildPart,
    BuildSketch,
    Face,
    GeomType,
    Location,
    Locations,
    Mode,
    PolarLocations,
    RegularPolygon,
    Side,
    Vector,
    __version__,
    make_face,
    offset,
    revolve,
    sweep,
    Spline,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)


def cassini_oval(
    a: float,
    c: float,
    n: int = 13,
    scale: float = 1.0,
    z: float = 0.0,
) -> Spline:
    """
    Cassini oval with foci at (±c, 0, z) and parameter a (product of distances = a²).

    - a > c  → single-loop “peanut / fat oval”
    - a = c  → lemniscate of Bernoulli (figure eight)
    - a < c  → two separate loops (this simple sampler is intended for a >= c)

    Parameters
    ----------
    a      : shape parameter (same units as c, dimensionless before `scale`)
    c      : half distance between the two foci
    n      : number of sample points around the oval
    scale  : overall size multiplier (applied to radius)
    z      : z-coordinate of the curve (0 = XY plane)

    Returns
    -------
    Spline : periodic spline approximating the Cassini oval
    """
    pts: list[Vector] = []

    for i in range(n):
        theta = 2.0 * math.pi * i / n

        # r^4 - 2c^2 r^2 cos(2θ) + (c^4 - a^4) = 0  →  quadratic in r²
        # r² = c² cos(2θ) + √(a⁴ - c⁴ sin²(2θ))  (single-loop branch, a >= c)
        s2 = math.sin(2.0 * theta)
        disc = a**4 - (c**4) * (s2 * s2)
        if disc < 0:
            disc = 0.0  # numerical safety

        r2 = c**2 * math.cos(2.0 * theta) + math.sqrt(disc)
        if r2 < 0:
            r2 = 0.0  # numerical safety

        r = math.sqrt(r2) * scale
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        pts.append(Vector(x, y, z))

    return Spline(pts, periodic=True)


print(f"build123d version: {__version__}")

ctrl_points_jar = [
    Vector(i) for i in [(15, 110), (15, 0), (700, -50), (45, -150), (45, -40)]
]
ctrl_points_handle = [
    Vector(i)
    for i in [
        (0, (ctrl_points_jar[-1]).Y),
        (0, 100),
        (200, 100, 200),
        (600, -40, 200),
        (600, 280, -200),
        (400, 350, 700),
        (0, 280),
        (0, (ctrl_points_jar[0]).Y),
    ]
]


with BuildPart() as klein_bottle:
    with BuildSketch():
        with BuildLine():
            base_curve = Bezier(*ctrl_points_jar)
            offset(side=Side.LEFT, amount=10)
        make_face()

    revolve(axis=Axis.Y, clean=False)

    planar_faces = klein_bottle.part.faces().filter_by(GeomType.PLANE)

    outer_faces = [Face(outer_wire=face.outer_wire()) for face in planar_faces]
    inner_faces = [Face(outer_wire=face.inner_wires()[-1]) for face in planar_faces]

handle_center_curve = Bezier(*ctrl_points_handle)
mid_loc = handle_center_curve ^ 0.7
loc2 = handle_center_curve ^ 0.2
loc3 = handle_center_curve ^ 0.8

outer_intermediate = make_face(cassini_oval(a=1, c=0.8, scale=30))
inner_intermediate = make_face(cassini_oval(a=1, c=0.8, scale=25))

all_instances = []

# Make each sweep assembly at a rotated polar location
with Locations(Location((0, 0, 0), (90, 0, 0))):
    with PolarLocations(radius=0, count=9) as locs:  # adjust radius as needed
        with Locations(Location((0, 0, 0), (0, 0, 180))) as locs2:
            for i, loc in enumerate(locs.locations):
                with BuildPart() as instance:
                    # Outer sweep (add)
                    sweep(
                        sections=[
                            outer_faces[0],
                            outer_intermediate.located(mid_loc),
                            outer_faces[1],
                        ],
                        path=handle_center_curve,
                        multisection=True,
                        mode=Mode.ADD,
                    )
                    # Inner sweep (subtract)
                    sweep(
                        sections=[
                            inner_faces[0],
                            inner_intermediate.located(mid_loc),
                            inner_faces[1],
                        ],
                        path=handle_center_curve,
                        multisection=True,
                        mode=Mode.SUBTRACT,
                    )
                # Move the whole instance to its polar location
                instance.part.locate(loc * locs2.locations[0])
                all_instances.append(instance.part)
del instance
# Show all instances
show_all(reset_camera=Camera.KEEP)
# Add
