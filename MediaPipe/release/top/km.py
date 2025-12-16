import numpy as np
import cv2

def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('CV Settings')
    p = page.appendInt('K', label='K Clusters')
    p.min = 2
    p.max = 10
    p.default = 4
    return

def onCook(scriptOp):
    img_input = scriptOp.inputs[0].numpyArray()
    if img_input is None: return


    img_uint8 = (img_input[:, :, :3] * 255).astype(np.uint8)
    pixel_values = img_uint8.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)


    try:
        k = int(scriptOp.par.K.eval())
    except AttributeError:
        k = 4 
    
    if k < 2: k = 2 


    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)


    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_uint8.shape)

    final_img = segmented_image.astype(np.float32) / 255.0
    alpha = np.ones((final_img.shape[0], final_img.shape[1], 1), dtype=np.float32)
    final_img = np.dstack((final_img, alpha))

    scriptOp.copyNumpyArray(final_img)