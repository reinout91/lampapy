from build123d import (
    BuildLine,
    BuildPart,
    Spline,
    sweep,
    revolve,
    Line,
    BuildSketch,
    make_face,
    Axis,
    Bezier,
    offset,
    Mode,
    Side,
    extrude,
    __version__,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

print(__version__)


with BuildPart() as klein_bottle:
    with BuildSketch() as f:
        with BuildLine():
            Line([(20, 240), (20, 220)])
            Bezier(
                (20, 220),
                (20, 160),
                (310, -100),
                (20, -240),
                (20, -140),
            )
            offset(side=Side.LEFT, amount=10)
        make_face()
    revolve(axis=Axis.Y, clean=False)

show_all(reset_camera=Camera.KEEP)
