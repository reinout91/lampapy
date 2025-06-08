from build123d import (
    Axis,
    Bezier,
    BuildLine,
    BuildPart,
    BuildSketch,
    Circle,
    Line,
    Mode,
    Side,
    __version__,
    export_stl,
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

    with BuildSketch():
        with BuildLine() as handle_center_line:
            h = Bezier(
                (0, -140),
                (0, 0),
                (510, 440),
                (0, 440),
                (0, 240),
            )

    for i in range(segment_count + 1):
        with BuildSketch(handle_center_line.line ^ (i / segment_count)) as section:
            if i == 0:
                Circle(20)
            if i == segment_count:
                Circle(30)
            else:
                Circle(20)
    sections = klein_bottle_outside.pending_faces

    sweep(sections=sections, path=handle_center_line, multisection=True)


with BuildPart(mode=Mode.SUBTRACT) as klein_bottle_inside:
    with BuildSketch():
        with BuildLine() as handle_center_line:
            h = Bezier(
                (0, -140),
                (0, 0),
                (510, 440),
                (0, 440),
                (0, 240),
            )

    for i in range(segment_count + 1):
        with BuildSketch(handle_center_line.line ^ (i / segment_count)) as section:
            if i == 0:
                Circle(5)
            if i == segment_count:
                Circle(20)
            else:
                Circle(10)
    sections = klein_bottle_inside.pending_faces

    sweep(sections=sections, path=handle_center_line, multisection=True)

klein_bottle = klein_bottle_outside.part - klein_bottle_inside.part

export_stl(klein_bottle, "klein_bottle.stl")
show_all(reset_camera=Camera.KEEP)
