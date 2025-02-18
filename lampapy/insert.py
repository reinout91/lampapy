from build123d import (
    Face,
    Line,
    Polyline,
    Shell,
    Solid,
    Spline,
    Vector,
    Wire,
)
from ocp_vscode import Camera, set_port, show_all

b0 = Vector(0, 0, 0)
b1 = Vector(0, 32.8, 0)
b2 = Vector(17.4, 40, 0)
b3 = Vector(36.2, 43.8, 0)
b5 = Vector(28.6, 0, 0)
b6 = Vector(14.3, 0, 0)


base = [b0, b1, b2, b3, b5, b6, b0]

m0 = Vector(0, 0, -13)
m1 = Vector(0, 26.4, -13)
m2 = Vector(15, 35, -13)
m3 = Vector(29.3, 33.5, -13)
m5 = Vector(20.5, 0, -13)
m6 = Vector(10.2, 0, -13)


d3 = Vector(31.4, 40, -3.5)
d5 = Vector(23.5, 0, -3.5)

mid = [m0, m1, m2, m3, m5, m6, m0]
o = [(0, 0, -2) + pt for pt in mid[3:5]]
o[0] += (-0.1, -1, 0)

top = [
    Vector(0, 0, -43),
    Vector(7, 0, -46.5),
    Vector(14, 0, -50),
]

wire1 = Wire(Polyline(b0, m0, m1, b1, b0))

wire3 = Wire(
    [
        Spline([b3, d3, m3, o[0]]),
        Line(o[0], o[1]),
        Spline([o[1], m5, d5, b5]),
        Line(b5, b3),
    ]
)

wire4 = Wire(
    [Line([m0, top[0]]), Spline([top[0], Vector(0, 19.25, -23.7), m1]), Line(m1, m0)]
)


wire6 = Wire(
    [
        Line([o[1], top[2]]),
        Spline([top[2], Vector(24.8, 18.8, -34.6), o[0]]),
        Line(o[0], o[1]),
    ]
)

wire8 = Wire(Polyline([o[1], top[2]], top[1], m6, o[1]))
wire9 = Wire(Polyline([m6, top[1], top[0], m0, m6]))
wire10 = Wire([Spline([o[1], m5, d5, b5]), Line(b5, b6), Line(b6, m6), Line(m6, o[1])])
wire11 = Wire(Polyline(b0, m0, m6, b6, b0))
wire12 = Wire(Polyline(b1, m1, m2, b2, b1))
wire13 = Wire(Polyline(b0, b1, b2, b6, b0))
wire14 = Wire(Polyline(b6, b2, b3, b5, b6))
wire15 = Wire([Line(b2, m2), Line(m2, o[0]), Spline([b3, d3, m3, o[0]]), Line(b3, b2)])
wire16 = Wire(
    [
        Line(top[0], top[1]),
        Spline([top[1], Vector(12, 25, -27.6), m2]),
        Line(m2, m1),
        Spline([top[0], Vector(0, 19.25, -23.7), m1]),
    ]
)
wire17 = Wire(
    [
        Line(top[2], top[1]),
        Spline([top[1], Vector(12, 25, -27.6), m2]),
        Line(m2, o[0]),
        Spline([top[2], Vector(24.8, 18.8, -34.6), o[0]]),
    ]
)

solid = Solid(
    Shell(
        [
            Face.make_surface(wire)
            for wire in [
                wire1,
                wire3,
                wire4,
                wire6,
                wire8,
                wire9,
                wire10,
                wire11,
                wire12,
                wire13,
                wire14,
                wire15,
                wire16,
                wire17,
            ]
        ]
    )
)


if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
