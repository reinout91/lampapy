from build123d import (
    Axis,
    Bezier,
    BuildLine,
    BuildPart,
    BuildSketch,
    Face,
    GeomType,
    Line,
    Mode,
    Side,
    __version__,
    make_face,
    offset,
    revolve,
    sweep,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

print(__version__)
segment_count = 6


with BuildPart() as klein_bottle_outside:
    with BuildSketch():
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

    ft = klein_bottle_outside.part.faces().filter_by(GeomType.PLANE).sort_by(Axis.Y)
    outer_wires = [Face(outer_wire=face.outer_wire()) for face in ft]
    inner_wires = [Face(outer_wire=face.inner_wires()[-1]) for face in ft]

    handle_center_line = Bezier(
        (0, -140),
        (0, 0),
        (510, 440),
        (0, 440),
        (0, 240),
    )

    sweep(sections=outer_wires, path=handle_center_line, multisection=True)
    sweep(
        sections=inner_wires,
        path=handle_center_line,
        multisection=True,
        mode=Mode.SUBTRACT,
    )

show_all(reset_camera=Camera.KEEP)
