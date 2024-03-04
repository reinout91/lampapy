from build123d import *
from ocp_vscode import *

with BuildPart() as p:
    with BuildSketch() as s:
        Rectangle(115, 50)
        with Locations((5 / 2, 0)):
            SlotOverall(90, 12, mode=Mode.SUBTRACT)
    extrude(amount=15)

    with BuildSketch(Plane.XZ.offset(50 / 2)) as s3:
        with Locations((-115 / 2 + 26, 15)):
            SlotOverall(42 + 2 * 26 + 12, 2 * 26, rotation=90)
    zz = extrude(amount=-12)
    split(bisect_by=Plane.XY)
    edgs = p.part.edges().filter_by(Axis.Y).group_by(Axis.X)[-2]
    fillet(edgs, 9)

    with Locations(zz.faces().sort_by(Axis.Y)[0]):
        with Locations((42 / 2 + 6, 0)):
            CounterBoreHole(24 / 2, 34 / 2, 4)
    mirror(about=Plane.XZ)

    with BuildSketch() as s4:
        RectangleRounded(115, 50, 6)
    extrude(amount=80, mode=Mode.INTERSECT)
    # fillet does not work right, mode intersect is safer

    with BuildSketch(Plane.YZ) as s2:
        Trapezoid(18, 8, 180 - 60, align=(Align.CENTER, Align.MIN))
    extrude(amount=80, both=True, mode=Mode.SUBTRACT)

show_object(p)