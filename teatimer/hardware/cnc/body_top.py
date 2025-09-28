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
    ymin = -40
    ymax = 40
    
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
H = 66.5   # height
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


def make_cut(outlist, npath, zlist):
    save = [*npath.coordinates[0], ZSAVE]
    outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(save[0], save[1], save[2], f))
    for z in zlist:
        for coordinate in npath.coordinates:
            outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(coordinate[0], coordinate[1], z, f))
    outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(save[0], save[1], save[2], f))


filename = str(basename.with_suffix(".pdf"))
canvas.writePDFfile(filename)
print(f"{filename} written")


outlist = []
f = 800
zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -9.5]
outlist.append("; frame")
make_cut(outlist, npath_frame, zlist)
outlist.append("M1")

zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17]
outlist.append("; hole")
make_cut(outlist, npath_hole, zlist)
outlist.append("M1")

    
filename = str(basename.with_suffix(".nc"))
with open(filename, "w") as fh:
    print("\n".join(outlist), file=fh)