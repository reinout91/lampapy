from build123d import (
    Axis,
    BuildPart,
    Compound,
    Face,
    GeomType,
    Location,
    Part,
    RevoluteJoint,
    RigidJoint,
    add,
    Vector,
)
from spot import spot
from fitting import fitting
from spotlight import spotlight
from ocp_vscode import Camera, set_port, show

assy_spot = Compound(
    label="assy_leaf", children=[spot.part, fitting.part, spotlight.part]
)
spot.part.color = "red"
fitting.part.color = "green"
# spotlight.part


vec1 = Vector(0, 0, 15.15)
j1 = RigidJoint(
    label="j1", to_part=fitting.part, joint_location=Location((0, 0, 6.3), (0, 90, 0))
)
j2 = RigidJoint(label="j2", to_part=spotlight.part, joint_location=Location((0, 0, 0)))

j3 = RigidJoint(
    label="j3", to_part=fitting.part, joint_location=Location((0, 0, 15.15))
)

j4 = RigidJoint(
    label="j4",
    to_part=spot.part,
    joint_location=Location((0, 45.6 + 15.15 - 6.3, 0), (-90, 0, 0)),
)

j2.connect_to(j1)
j3.connect_to(j4)

if __name__ == "__main__":
    set_port(3939)
    show([assy_spot, vec1], reset_camera=Camera.KEEP)
