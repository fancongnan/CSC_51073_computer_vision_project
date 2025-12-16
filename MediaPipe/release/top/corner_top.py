
import numpy as np
import cv2

def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Corners')


    p = page.appendInt('Maxcorners', label='Max Corners')
    p[0].default = 80
    p[0].min = 1
    p[0].max = 500
    p[0].clampMin = True; p[0].clampMax = True

    p = page.appendFloat('Quality', label='Quality Level')
    p[0].default = 0.05 
    p[0].min = 0.001
    p[0].max = 0.5
    p[0].clampMin = True; p[0].clampMax = True

    p = page.appendFloat('Mindist', label='Min Distance')
    p[0].default = 15.0
    p[0].min = 1.0
    p[0].max = 200.0
    p[0].clampMin = True; p[0].clampMax = True
    

    p = page.appendInt('Blur', label='Pre-Blur Amount')
    p[0].default = 3   
    p[0].min = 0
    p[0].max = 20
    p[0].clampMin = True; p[0].clampMax = True
    
    p = page.appendInt('Blocksize', label='Block Size')
    p[0].default = 3
    p[0].min = 3
    p[0].max = 21   
    p[0].clampMin = True; p[0].clampMax = True
    return

def onCook(scriptOp):
    try:
        input_op = scriptOp.inputs[0]
        if input_op is None: return
        img = input_op.numpyArray(delayed=True)
        if img is None: return

        if img.dtype == np.float32:
            frame = (img * 255.0).astype(np.uint8)
        else:
            frame = img.astype(np.uint8)

        frame = cv2.flip(frame, 0)


        if frame.ndim == 2:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            gray = frame
        elif frame.shape[2] == 4:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        else:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        blur_amount = scriptOp.par.Blur.eval()
        if blur_amount > 0:
            k_size = (blur_amount * 2) + 1
            gray_for_detection = cv2.GaussianBlur(gray, (k_size, k_size), 0)
        else:
            gray_for_detection = gray


        max_corners = scriptOp.par.Maxcorners.eval()
        quality = scriptOp.par.Quality.eval()
        min_dist = scriptOp.par.Mindist.eval()
        block_size = scriptOp.par.Blocksize.eval()
        

        if block_size < 3: block_size = 3


        corners = cv2.goodFeaturesToTrack(
            gray_for_detection, 
            maxCorners=max_corners,
            qualityLevel=quality,
            minDistance=min_dist,
            blockSize=block_size,
            useHarrisDetector=False,
            k=0.04
        )


        out = frame_bgr.copy() 

        n_corners = 0 if corners is None else len(corners)
        cv2.putText(out, f"Corners: {n_corners}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        if corners is not None:
            pts = corners.reshape(-1, 2)
            for (x_f, y_f) in pts:
                x, y = int(x_f), int(y_f)
                cv2.circle(out, (x, y), 4, (0, 255, 255), -1, cv2.LINE_AA)
                

                tx, ty = x + 6, y - 6
                if ty < 12: ty = y + 14
                cv2.putText(out, f"{x},{y}", (tx, ty),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)


        out_rgba = cv2.cvtColor(out, cv2.COLOR_BGR2RGBA)
        out_rgba = cv2.flip(out_rgba, 0) # Flip back
        
        final_out = out_rgba.astype(np.float32) / 255.0
        final_out[:, :, 3] = 1.0 

        scriptOp.copyNumpyArray(final_out)

    except Exception as e:
        print(f"Script TOP Error: {e}")