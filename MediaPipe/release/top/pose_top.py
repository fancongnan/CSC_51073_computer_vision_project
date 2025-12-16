import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

def onSetupParameters(scriptOp):
    return

def onPulse(par):
    return

def onCook(scriptOp):
    if not scriptOp.inputs or scriptOp.inputs[0] is None:
        return

    in_top = scriptOp.inputs[0]

    # Get the image as numpy array
    img = in_top.numpyArray(delayed=False, writable=False)
    if img is None:
        return

    # img is float32 in [0,1], shape (H, W, 4) or (H, W, 3)
    if img.shape[2] < 3:
        return

    rgb = img[:, :, :3]
    frame_rgb = (rgb * 255.0).astype(np.uint8)

    # Run MediaPipe pose
    results = pose.process(frame_rgb)

    # Draw landmarks on a copy
    output = frame_rgb.copy()
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(thickness=2)
        )

    # Convert back to float32 [0,1] and write to Script TOP
    output_float = output.astype(np.float32) / 255.0
    scriptOp.copyNumpyArray(output_float)
    return