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
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

# fitiing: 27.4 diameter
# h = 15.15
# scroefgaten op 17.7 uit elkaar
# diameter schroefgat: 4.0
# offset 6.3
# 22.9 inner maat.

with BuildPart() as fitting:
    Cylinder(27.4 / 2, 15.15, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(
        22.9 / 2, 6.3, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT
    )
    with Locations([(17.7 / 2, 0, 0), (-17.7 / 2, 0, 0)]):
        Hole(4 / 2)


show_all(reset_camera=Camera.KEEP)
