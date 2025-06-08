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
    Side,
    Vector,
    __version__,
    make_face,
    offset,
    revolve,
    sweep,
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


with BuildPart() as sweep_part:
    handle_center_curve = Bezier(
        *ctrl_points_handle,
    )

    sweep(sections=outer_faces, path=handle_center_curve, multisection=True)

with BuildPart() as sweep_part_inner:
    sweep(
        sections=inner_faces,
        path=handle_center_curve,
        multisection=True,
        mode=Mode.ADD,
    )

all_instances = []

# Make each sweep assembly at a rotated polar location
with Locations(Location((0, 0, 0), (90, 0, 0))):
    with PolarLocations(radius=0, count=20) as locs:  # adjust radius as needed
        with Locations(Location((0, 0, 0), (0, 0, 180))) as locs2:
            for loc in locs.locations:
                with BuildPart() as instance:
                    handle_center_curve = Bezier(*ctrl_points_handle)
                    # Outer sweep (add)
                    sweep(
                        sections=outer_faces,
                        path=handle_center_curve,
                        multisection=True,
                        mode=Mode.ADD,
                    )
                    # Inner sweep (subtract)
                    sweep(
                        sections=inner_faces,
                        path=handle_center_curve,
                        multisection=True,
                        mode=Mode.SUBTRACT,
                    )
                # Move the whole instance to its polar location
                instance.part.locate(loc * locs2.locations[0])
                all_instances.append(instance.part)

# Show all instances
show_all(reset_camera=Camera.KEEP)
# Add
