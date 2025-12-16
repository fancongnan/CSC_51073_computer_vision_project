import numpy as np
import cv2


def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Custom')

    par = page.appendInt('Threshold', label='Threshold')[0]
    par.normMin = 5
    par.normMax = 60
    par.default = 10
    par.min = 5
    par.max = 60
    par.clampMin = True
    par.clampMax = True


def onPulse(par):
    return


def _to_uint8_rgba01_to_255(img):
    img *= 255.0
    return img.astype(np.uint8, copy=False)


def onCook(scriptOp):
    t = int(scriptOp.par.Threshold.eval())


    src = scriptOp.inputs[0].numpyArray(delayed=True, writable=True)
    if src is None:
        return


    frame_u8 = _to_uint8_rgba01_to_255(src)


    g = cv2.cvtColor(frame_u8, cv2.COLOR_RGBA2GRAY)
    g = cv2.blur(g, (3, 3))


    lo = t
    hi = 3 * t
    edges = cv2.Canny(g, lo, hi, apertureSize=3)


    out = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGBA)


    scriptOp.copyNumpyArray(out)