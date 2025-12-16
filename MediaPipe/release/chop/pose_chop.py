import numpy as np
import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
mpIndex = mp_pose.PoseLandmark

# Initialize
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

JOINTS = [
    "NOSE",
    "LEFT_WRIST", "RIGHT_WRIST",
    "LEFT_ELBOW", "RIGHT_ELBOW",
    "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "LEFT_HIP", "RIGHT_HIP",
    "LEFT_KNEE", "RIGHT_KNEE",     
    "LEFT_ANKLE", "RIGHT_ANKLE"     
]

def onSetupParameters(scriptOp):

    scriptOp.clear() 
    return

def onPulse(par):
    return


def _get_frame(scriptOp):
    top = None
    if len(scriptOp.inputs) > 0:
        top = scriptOp.inputs[0]
    else:
        top = scriptOp.parent().op('video')
    
    if top is None:
        return None, -1

    img = top.numpyArray(delayed=True, writable=False)
    
    if img is None:
        return None, -2
        
    return img, 0

def onCook(scriptOp):
    scriptOp.clear()
    
    ch_error   = scriptOp.appendChan("error")
    ch_haspose = scriptOp.appendChan("has_pose")
    
    chan_buffers = {}
    for j in JOINTS:
        jn = j.lower()
        chan_buffers[f"{jn}_x"] = scriptOp.appendChan(f"{jn}_x")
        chan_buffers[f"{jn}_y"] = scriptOp.appendChan(f"{jn}_y")
        chan_buffers[f"{jn}_z"] = scriptOp.appendChan(f"{jn}_z")
        chan_buffers[f"{jn}_vis"] = scriptOp.appendChan(f"{jn}_vis")

    ch_error[0] = 0
    ch_haspose[0] = 0
    
    img, err = _get_frame(scriptOp)
    if err != 0:
        ch_error[0] = err
        return

    rgb = (img[:, :, :3] * 255.0).astype(np.uint8)
    
    rgb = np.flipud(rgb)
    
    results = pose.process(rgb)
    
    if not results.pose_landmarks:
        return 

    ch_haspose[0] = 1
    lm = results.pose_landmarks.landmark


    for j in JOINTS:
        idx = getattr(mpIndex, j).value 
        p = lm[idx]
        jn = j.lower()
        
        # X: 0 (left) to 1 (right)
        chan_buffers[f"{jn}_x"][0] = float(p.x)
        
        # Y: Invert Y so 0 is bottom and 1 is top (Standard TD)
        chan_buffers[f"{jn}_y"][0] = 1.0 - float(p.y)
        
        # Z: Relative depth
        chan_buffers[f"{jn}_z"][0] = float(p.z)
        
        # Visibility Score (0.0 to 1.0)
        chan_buffers[f"{jn}_vis"][0] = float(p.visibility)

    return