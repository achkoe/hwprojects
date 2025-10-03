import pathlib
from pyx import canvas, path, style, color, text, unit


THIN = False
ZSAVE = 15


class NPath():
    def __init__(self):
        self.coordinates = []
        
    def moveto(self, x, y):
        self.coordinates.append((x, y))
        return path.moveto(x, y)
    
    def lineto(self, x, y):
        self.coordinates.append((x, y))
        return path.lineto(x, y)


def makegrid(contour, canvas):
    xmin = -60
    xmax = 60
    ymin = -45
    ymax = 45
    
    for x in range(xmin, xmax, 10):
        canvas.text(x, ymax + 1, f"{x}", [text.halign.boxcenter])
    for x in range(xmin, xmax, 1):
        contour.append(path.moveto(x, ymin))
        if divmod(x, 10)[1] == 0:
            contour.append(path.lineto(x, ymax + 1))
        else:
            contour.append(path.lineto(x, ymax))
            
            
    for y in range(ymin, ymax, 10):
        canvas.text(xmax + 1, y, f"{y}", [text.valign.middle])
        
    for y in range(ymin, ymax, 1):
        contour.append(path.moveto(xmin, y))
        if divmod(y, 10)[1] == 0:
            contour.append(path.lineto(xmax + 1, y))
        else:
            contour.append(path.lineto(xmax, y))


canvas = canvas.canvas()

# region 
unit.set(xscale=5)
basename = pathlib.Path(__file__)
contour = path.path()
makegrid(contour, canvas)    
canvas.stroke(contour, [style.linewidth.THIN, color.cmyk.Lavender])
# endregion

color_show = color.rgb.black
color_hidden = color.rgb.white
color_cut_1 = color.cmyk.SpringGreen
color_cut_2 = color.cmyk.ForestGreen

# region frame
W = 104.2  # width
H = 66.0   # height
D = 9      # height of material

contour = path.path(
    path.moveto(-W / 2, +H / 2),
    path.lineto(+W / 2, +H / 2),
    path.lineto(+W / 2, -H / 2),
    path.lineto(-W / 2, -H / 2),
    path.lineto(-W / 2, +H / 2)    
)
canvas.stroke(contour, [style.linewidth.THIN, color_show])
R = 3
npath_frame = NPath()
canvas.stroke(
    path.path(
        npath_frame.moveto(-W / 2 + R, +H / 2 - R),
        npath_frame.lineto(+W / 2 - R, +H / 2 - R),
        npath_frame.lineto(+W / 2 - R, -H / 2 + R),
        npath_frame.lineto(-W / 2 + R, -H / 2 + R),
        npath_frame.lineto(-W / 2 + R, +H / 2 - R)    
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color_cut_1])
# endregion


# region hole
M = 4      # margin
contour = path.path(
    path.moveto(-(W / 2) + M, +(H / 2) - M),
    path.lineto(+(W / 2) - M, +(H / 2) - M),
    path.lineto(+(W / 2) - M, -(H / 2) + M),
    path.lineto(-(W / 2) + M, -(H / 2) + M),
    path.lineto(-(W / 2) + M, +(H / 2) - M)    
)
canvas.stroke(contour, [style.linewidth.THIN, color_show])
R = 3
npath_hole = NPath()
canvas.stroke(
    path.path(
        npath_hole.moveto(-(W / 2) + M + R, +(H / 2) - M - R),
        npath_hole.lineto(+(W / 2) - M - R, +(H / 2) - M - R),
        npath_hole.lineto(+(W / 2) - M - R, -(H / 2) + M + R),
        npath_hole.lineto(-(W / 2) + M + R, -(H / 2) + M + R),
        npath_hole.lineto(-(W / 2) + M + R, +(H / 2) - M - R)    
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color_cut_2])
# endregion

# region hinge_left
R = 3
w = 17
h = 8
contour = path.path(
    path.moveto(-(W / 2) + w, +(H / 2) + 2),
    path.lineto(-(W / 2) + 0, +(H / 2) + 2),
    path.lineto(-(W / 2) + 0, +(H / 2) + 2 + h),
    path.lineto(-(W / 2) + w, +(H / 2) + 2 + h),
    path.lineto(-(W / 2) + w, +(H / 2) + 2),
)
if 0:
    canvas.stroke(contour, [style.linewidth.THIN, color_show])
R = 1
npath_hinge_left = NPath()
canvas.stroke(
    path.path(
        npath_hinge_left.moveto(-(W / 2) + w - R, +(H / 2) + 2 + R),
        npath_hinge_left.lineto(-(W / 2) + 0 + R, +(H / 2) + 2 + R),
        npath_hinge_left.lineto(-(W / 2) + 0 + R, +(H / 2) + 2 + h - R),
        npath_hinge_left.lineto(-(W / 2) + w - R, +(H / 2) + 2 + h - R),
        npath_hinge_left.lineto(-(W / 2) + w - R, +(H / 2) + 2 + R),
        npath_hinge_left.lineto(-(W / 2) + w - 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_left.lineto(-(W / 2) + 0 + 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_left.lineto(-(W / 2) + 0 + 2 * R, +(H / 2) + 2 + h - 2 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 2 * R, +(H / 2) + 2 + h - 2 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_left.lineto(-(W / 2) + 0 + 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_left.lineto(-(W / 2) + 0 + 3 * R, +(H / 2) + 2 + h - 3 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 3 * R, +(H / 2) + 2 + h - 3 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_left.lineto(-(W / 2) + w - 4 * R, +(H / 2) + 2 + 4 * R),
        npath_hinge_left.lineto(-(W / 2) + 0 + 4 * R, +(H / 2) + 2 + 4 * R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color_cut_2])
# endregion

# region hinge_right
R = 3
w = 17
h = 8
contour = path.path(
    path.moveto(+(W / 2) - w + w, +(H / 2) + 2),
    path.lineto(+(W / 2) - w + 0, +(H / 2) + 2),
    path.lineto(+(W / 2) - w + 0, +(H / 2) + 2 + h),
    path.lineto(+(W / 2) - w + w, +(H / 2) + 2 + h),
    path.lineto(+(W / 2) - w + w, +(H / 2) + 2),
)
if 0:
    canvas.stroke(contour, [style.linewidth.THIN, color_show])
R = 1
npath_hinge_right = NPath()
canvas.stroke(
    path.path(
        npath_hinge_right.moveto(+(W / 2) - w + w - R, +(H / 2) + 2 + R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + R, +(H / 2) + 2 + R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + R, +(H / 2) + 2 + h - R),
        npath_hinge_right.lineto(+(W / 2) - w + w - R, +(H / 2) + 2 + h - R),
        npath_hinge_right.lineto(+(W / 2) - w + w - R, +(H / 2) + 2 + R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + 2 * R, +(H / 2) + 2 + h - 2 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 2 * R, +(H / 2) + 2 + h - 2 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 2 * R, +(H / 2) + 2 + 2 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + 3 * R, +(H / 2) + 2 + h - 3 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 3 * R, +(H / 2) + 2 + h - 3 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 3 * R, +(H / 2) + 2 + 3 * R),
        npath_hinge_right.lineto(+(W / 2) - w + w - 4 * R, +(H / 2) + 2 + 4 * R),
        npath_hinge_right.lineto(+(W / 2) - w + 0 + 4 * R, +(H / 2) + 2 + 4 * R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color_cut_2])
# endregion


def make_cut(outlist, npath, zlist, flast=800):
    save = [*npath.coordinates[0], ZSAVE]
    outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(save[0], save[1], save[2], f))
    for z in zlist:
        for coordinate in npath.coordinates:
            outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(coordinate[0], coordinate[1], z, f))
    outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(save[0], save[1], save[2], flast))


filename = str(basename.with_suffix(".pdf"))
canvas.writePDFfile(filename)
print(f"{filename} written")


outlist = []
f = 800
zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -9.5]
outlist.append("; frame")
make_cut(outlist, npath_frame, zlist)
outlist.append("M1")

outlist.append("; holes")
outlist.append("G00 X-49.1 Y30.0 Z15 F800")
outlist.append("G00 X-49.1 Y30.0 Z-11.5 F800")
outlist.append("G00 X-49.1 Y30.0 Z15 F800")

outlist.append("G00 X49.1 Y30.0 Z15 F800")
outlist.append("G00 X49.1 Y30.0 Z-11.5 F800")
outlist.append("G00 X49.1 Y30.0 Z15 F800")

outlist.append("G00 X49.1 Y-30.0 Z15 F800")
outlist.append("G00 X49.1 Y-30.0 Z-11.5 F800")
outlist.append("G00 X49.1 Y-30.0 Z15 F800")

outlist.append("G00 X-49.1 Y-30.0 Z15 F800")
outlist.append("G00 X-49.1 Y-30.0 Z-11.5 F800")
outlist.append("G00 X-49.1 Y-30.0 Z15 F800")

zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19]
outlist.append("; greathole")
make_cut(outlist, npath_hole, zlist, 100)
outlist.append("M1")

if 0:
    zlist = [-1,]
    outlist.append("; hinge_left")
    make_cut(outlist, npath_hinge_left, zlist)
    outlist.append("M1")

    zlist = [-1,]
    outlist.append("; hinge_right")
    make_cut(outlist, npath_hinge_right, zlist)
    outlist.append("M1")

    
filename = str(basename.with_suffix(".nc"))
with open(filename, "w") as fh:
    print("\n".join(outlist), file=fh)