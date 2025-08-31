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
    xmax = 50
    ymin = -30
    ymax = 30
    
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

# region display frame
contour = path.path(
    path.moveto(-71.0 / 2, +24.0 / 2),
    path.lineto(+71.0 / 2, +24.0 / 2),
    path.lineto(+71.0 / 2, -24.0 / 2),
    path.lineto(-71.0 / 2, -24.0 / 2),
    path.lineto(-71.0 / 2, +24.0 / 2)    
)
R = 1
npath_frame = NPath()
canvas.stroke(
    path.path(
        npath_frame.moveto(-71.0 / 2 + R, +24.0 / 2 - R),
        npath_frame.lineto(+71.0 / 2 - R, +24.0 / 2 - R),
        npath_frame.lineto(+71.0 / 2 - R, -24.0 / 2 + R),
        npath_frame.lineto(-71.0 / 2 + R, -24.0 / 2 + R),
        npath_frame.lineto(-71.0 / 2 + R, +24.0 / 2 - R)    
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color.cmyk.OliveGreen])
canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
# endregion

# region display nose
contour = path.path(
    path.moveto(-71.0 / 2 - 0, +18.0 / 2),
    path.lineto(-71.0 / 2 - 5, +18.0 / 2),
    path.lineto(-71.0 / 2 - 5, -18.0 / 2),
    path.lineto(-71.0 / 2 - 0, -18.0 / 2),
    path.lineto(-71.0 / 2 - 0, +18.0 / 2)
)
R = 1
npath_nose = NPath()
canvas.stroke(
    path.path(
        npath_nose.moveto(-71.0 / 2 - 1 + R, +18.0 / 2 - R),
        npath_nose.lineto(-71.0 / 2 - 5 + R, +18.0 / 2 - R),
        npath_nose.lineto(-71.0 / 2 - 5 + R, -18.0 / 2 + R),
        npath_nose.lineto(-71.0 / 2 - 1 + R, -18.0 / 2 + R),
        npath_nose.lineto(-71.0 / 2 - 1 + R, +18.0 / 2 - R),
        npath_nose.lineto(-71.0 / 2 - 2 + R, +18.0 / 2 - 1 - R),
        npath_nose.lineto(-71.0 / 2 - 4 + R, +18.0 / 2 - 1 - R),
        npath_nose.lineto(-71.0 / 2 - 4 + R, -18.0 / 2 + 3 - R),
        npath_nose.lineto(-71.0 / 2 - 2 + R, -18.0 / 2 + 3 - R),
        npath_nose.lineto(-71.0 / 2 - 2 + R, +18.0 / 2 - 1 - R),
        npath_nose.lineto(-71.0 / 2 - 3 + R, +18.0 / 2 - 2 - R),
        npath_nose.lineto(-71.0 / 2 - 3 + R, -18.0 / 2 + 4 - R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color.cmyk.NavyBlue])
canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
# endregion

# region display pcb
contour = path.path(
    path.moveto(-71.0 / 2 - 5, 24.0 / 2 + 7),
    path.lineto(+71.0 / 2 + 5, 24.0 / 2 + 7),
    path.lineto(+71.0 / 2 + 5, -24.0 / 2 - 7),
    path.lineto(-71.0 / 2 - 5, -24.0 / 2 - 7),
    path.lineto(-71.0 / 2 - 5, 24.0 / 2 + 7),
)
R = 3
npath_pcb = NPath()
canvas.stroke(
    path.path(
        npath_pcb.moveto(-71.0 / 2 - 5 + 0.5 * R, +24.0 / 2 + 7 - R),
        npath_pcb.lineto(+71.0 / 2 + 5 - 0.5 * R, +24.0 / 2 + 7 - R),
        npath_pcb.lineto(+71.0 / 2 + 5 - 0.5 * R, -24.0 / 2 - 7 + R),
        npath_pcb.lineto(-71.0 / 2 - 5 + 0.5 * R, -24.0 / 2 - 7 + R),
        npath_pcb.lineto(-71.0 / 2 - 5 + 0.5 * R, +24.0 / 2 + 7 - R),
        npath_pcb.lineto(-71.0 / 2 - 5 + 2 + 0.5 * R, +24.0 / 2 + 5 - R),
        npath_pcb.lineto(+71.0 / 2 - 2 + 2 + 0.5 * R, +24.0 / 2 + 5 - R),
        npath_pcb.lineto(+71.0 / 2 - 2 + 2 + 0.5 * R, -24.0 / 2 + 1 - R),
        npath_pcb.lineto(-71.0 / 2 - 5 + 2 + 0.5 * R, -24.0 / 2 + 1 - R),
        npath_pcb.lineto(-71.0 / 2 - 5 + 2 + 0.5 * R, +24.0 / 2 + 5 - R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color.cmyk.NavyBlue])

canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
# endregion

# region holes
contour = path.path(
    path.arc(+71 / 2 + 14, 0, 5, 0, 360),
    path.arc(0, -24 / 2 - 14, 5, 0, 360),
    path.arc(-71 / 2 + 10, -24 / 2 - 14, 5, 0, 360),
    path.arc(+71 / 2 - 10, -24 / 2 - 14, 5, 0, 360),
)
canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
# endregion

# region usb
R = 1
npath_usb = NPath()
contour = path.path(
    path.moveto(+71 / 2 + 14 - 1.6, -16 + 4.7),
    path.lineto(+71 / 2 + 14 - 1.6, -16 - 4.7),
    path.lineto(+71 / 2 + 14 + 1.6, -16 - 4.7),
    path.lineto(+71 / 2 + 14 + 1.6, -16 + 4.7),
    path.lineto(+71 / 2 + 14 - 1.6, -16 + 4.7),
)
canvas.stroke(
    path.path(
        npath_usb.moveto(+71 / 2 + 14 - 1.6 + R, -16 + 4.7- R),
        npath_usb.lineto(+71 / 2 + 14 - 1.6 + R, -16 - 4.7 + R),
        npath_usb.lineto(+71 / 2 + 14 + 1.6 - R, -16 - 4.7 + R),
        npath_usb.lineto(+71 / 2 + 14 + 1.6 - R, -16 + 4.7 - R),
        npath_usb.lineto(+71 / 2 + 14 - 1.6 + R, -16 + 4.7 - R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color.cmyk.NavyBlue])
canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
# endregion

# regin usbpcb
R = 1
npath_usbpcb = NPath()
contour = path.path(
    path.moveto(+71 / 2 + 14 - 1.6, -16 + 9),
    path.lineto(+71 / 2 + 14 - 1.6, -16 - 9),
    path.lineto(+71 / 2 + 14 - 3.6, -16 - 9),
    path.lineto(+71 / 2 + 14 - 3.6, -16 + 9),
    path.lineto(+71 / 2 + 14 - 1.6, -16 + 9),
)
canvas.stroke(
    path.path(
        npath_usbpcb.moveto(+71 / 2 + 14 - 1.6 - R, -16 + 9 - R ),
        npath_usbpcb.lineto(+71 / 2 + 14 - 1.6 - R, -16 - 9 + R),
        npath_usbpcb.lineto(+71 / 2 + 14 - 3.6 + R, -16 - 9 + R),
        npath_usbpcb.lineto(+71 / 2 + 14 - 3.6 + R, -16 + 9 - R),
        npath_usbpcb.lineto(+71 / 2 + 14 - 1.6 - R, -16 + 9 - R),
    ),
    [style.linewidth(0.1 if THIN else 2 * R), style.linecap.round, color.cmyk.NavyBlue])
canvas.stroke(contour, [style.linewidth.THIN, color.rgb.black])
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
zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
outlist.append("; frame")
make_cut(outlist, npath_frame, zlist)
outlist.append("M1")

zlist = [-1, -2, -3, -4, -5, -5.5]
outlist.append("; nose")
make_cut(outlist, npath_nose, zlist)
outlist.append("M1")


zlist = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
outlist.append("; usb")
make_cut(outlist, npath_usb, zlist)
outlist.append("M1")

zlist = [-1, -2, -3, -4, -5, -6, -7]
outlist.append("; usbpcb")
make_cut(outlist, npath_usbpcb, zlist)
outlist.append("M1")

# region holes
outlist.append("; holes")
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 + 14, 0, ZSAVE, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 + 14, 0, -2, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 + 14, 0, ZSAVE, f))

outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(0, -24 / 2 - 14, ZSAVE, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(0, -24 / 2 - 14, -2, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(0, -24 / 2 - 14, ZSAVE, f))
               
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(-71 / 2 + 10, -24 / 2 - 14, ZSAVE, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(-71 / 2 + 10, -24 / 2 - 14, -2, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(-71 / 2 + 10, -24 / 2 - 14, ZSAVE, f))
               
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 - 10, -24 / 2 - 14, ZSAVE, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 - 10, -24 / 2 - 14, -2, f))
outlist.append("G00 X{0} Y{1} Z{2} F{3}".format(+71 / 2 - 10, -24 / 2 - 14, ZSAVE, f))

zlist = [-0.5, -1, -1.5, -2]
outlist.append("; pcb")
make_cut(outlist, npath_pcb, zlist)


    
filename = str(basename.with_suffix(".nc"))
with open(filename, "w") as fh:
    print("\n".join(outlist), file=fh)