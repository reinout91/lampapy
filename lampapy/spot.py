from build123d import (
    Axis,
    BuildLine,
    BuildPart,
    BuildSketch,
    Line,
    Spline,
    Vector,
    make_face,
    Side,
    Kind,
    revolve,
    offset,
    Mode,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

# fitiing: 27.4 diameter
# h = 15.15
# scroefgaten op 17.7 uit elkaar
# diameter schroefgat: 4.0
# offset 6.3
# 22.9 inner maat.

with BuildPart() as spot:
    with BuildSketch() as base_sketch:
        with BuildLine() as bl:
            [
                Line(Vector(0, 0), Vector(29, 0)),
                Spline(
                    [Vector(29, 0), Vector(10, 150)],
                    tangents=[Vector(2, 1), Vector(-1, 5)],
                ),
                Line(Vector(10, 150), Vector(0, 150)),
            ]
        make_face()
    revolve(axis=Axis.Y)
    offset(
        spot.solids()[0],
        amount=-1,
        openings=[spot.faces().sort_by(Axis.Y)[0], spot.faces().sort_by(Axis.Y)[-1]],
    )


show_all(reset_camera=Camera.KEEP)
