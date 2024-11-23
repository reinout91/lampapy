import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *
from build123d_ease import align, back_face_of, bottom_face_of, front_face_of, left_face_of, right_face_of, top_face_of

set_port(3939)

print(build123d.__version__)

# specify parameters on base of the hinges
ideal_layer_height = 0.2 * MM
ideal_vert_gap = 2 * ideal_layer_height

W1 = 6 * MM
H = 6 * MM
H3 = 3 * MM #height of T joint.
H2 = H3 - ideal_vert_gap
pin_radius = 1.8 * MM
hole_radius = 2 * MM
length_thinge = 50 * MM
length_snapfinger = 7 * MM

hole_x = 10 * MM
axle_to_axle = 20 * MM

#shackle parameters
dist1 = axle_to_axle-length_snapfinger
dist2 = (H+H3)/4

with BuildPart() as t_hinge:
    Cylinder(pin_radius, H, align=align.CENTER)
    with Locations((0,W1/2,0)):
        ref1 = Box(W1, length_snapfinger, H2, align=align.BACK)
    with Locations((0, -axle_to_axle, 0)):
        Box(hole_x+3, W1, H2, align = align.LEFT)
        with Locations((hole_x, 0, 0)):
            hole = Hole(hole_radius)
    with Locations(front_face_of(ref1)):
        ref2 = Box(H,  W1, length_thinge, align = align.BOTTOM)

    max_fillet = t_hinge.part.max_fillet(
        t_hinge.edges().filter_by(Axis.Z),
        tolerance=0.2, max_iterations=20
    )
    fillet(objects=t_hinge.edges().filter_by(Axis.Z), radius=max_fillet)

    #add dovetail.
    with BuildSketch(Plane(front_face_of(ref2))):
        with Locations((H/3,0,0)):
            Triangle(a=H/3,b=H/3,C=90,align=align.FRONT)
        with Locations((-H/3,0,0)):
            Triangle(a=H/3,B=90,c=H/3,align=align.FRONT)
    extrude(amount=-length_thinge*2/3, mode=Mode.SUBTRACT)


with BuildPart() as shackle:
    with BuildSketch():
        SlotCenterToCenter(dist1,W1)
    arms_shackle = extrude(amount=(H-H3)/4, both=True, mode = Mode.PRIVATE)
    with Locations((dist1/2,0,0)):
        with Locations((0,0,-dist2), (0,0,dist2)):
            add(arms_shackle)
    cyl = Cylinder(pin_radius, H3, align = align.CENTER, mode=Mode.ADD)

    Plane_Snapfinger_shackle = Plane(origin=((axle_to_axle+length_snapfinger)/2,0,0))
    with BuildSketch(Plane_Snapfinger_shackle):
        SlotCenterToCenter(dist1, W1)
    extrude(amount=H3/2, both=True, mode = Mode.ADD)

    with Locations((axle_to_axle,0,0)):
        Cylinder(pin_radius, H, align = align.CENTER, mode=Mode.ADD)


#joints
j1 = RevoluteJoint(label="t_hinge_hole", to_part=t_hinge.part, axis= Axis(hole.center(),(0,0,1)))
j2 = RigidJoint(label="shackle_pin", to_part=shackle.part, joint_location=Location(cyl.center()))

j1.connect_to(j2, angle = 90)

del cyl, j1, j2, hole, ref1, ref2, arms_shackle, Plane_Snapfinger_shackle

shackle.part.color = "red"

show_all(reset_camera=Camera.KEEP)

comp_hinge_arms = Compound((t_hinge.part, shackle.part))
export_step(comp_hinge_arms, "hinge_lever.step")
