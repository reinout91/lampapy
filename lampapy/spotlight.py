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
    Cylinder,
    Align,
    Hole,
    Locations,
    Location,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

with BuildPart() as spotlight:
    with BuildSketch() as base_sketch:
        with BuildLine() as bl:
            [
                Line(Vector(0, 0), Vector(0, 8)),
                Line(Vector(0, 8), Vector(2, 10)),
                Line(Vector(2, 10), Vector(22.4, 12)),
                Spline(
                    [Vector(22.4, 12), Vector(43.4, 46.55 / 2)],
                    tangents=[Vector(1, 1.5), Vector(5, 1)],
                ),
                Line(Vector(43.4, 46.55 / 2), Vector(43.4, 49.6 / 2)),
                Line(Vector(43.4, 49.6 / 2), Vector(45.6, 49.6 / 2)),
                Line(Vector(45.6, 49.6 / 2), Vector(45.6, 0)),
            ]
        make_face()
    revolve(axis=Axis.X)
    with Locations(
        Location((0, 10.2 / 2, 0), (-90, -90, 0)),
        Location((0, -10.2 / 2, 0), (-90, -90, 0)),
    ):
        Cylinder(4.85 / 2, 6.95, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(
            7, 3.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT
        )
        Cylinder(4.85 / 2, 0.9, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(2.85 / 2, 3.5, align=(Align.CENTER, Align.CENTER, Align.MIN))

show_all(reset_camera=Camera.KEEP)
