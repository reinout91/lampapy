from build123d import (
    Axis,
    Bezier,
    BuildLine,
    BuildPart,
    BuildSketch,
    Face,
    GeomType,
    Mode,
    Side,
    __version__,
    make_face,
    offset,
    revolve,
    sweep,
    Vector,
)
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

print(f"build123d version: {__version__}")

ctrl_points_jar = [
    Vector(i) for i in [(15, 110), (15, 0), (700, -50), (45, -150), (45, -40)]
]
ctrl_points_handle = [
    Vector(i)
    for i in [
        (0, (ctrl_points_jar[-1]).Y),
        (0, 100),
        (200, 100),
        (600, -40),
        (600, 280),
        (400, 350),
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

    handle_center_curve = Bezier(
        *ctrl_points_handle,
    )

    sweep(sections=outer_faces, path=handle_center_curve, multisection=True)
    sweep(
        sections=inner_faces,
        path=handle_center_curve,
        multisection=True,
        mode=Mode.SUBTRACT,
    )

show_all(reset_camera=Camera.KEEP)
