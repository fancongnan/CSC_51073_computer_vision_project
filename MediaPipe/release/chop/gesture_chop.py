
def onCook(scriptOp):
    scriptOp.clear()


    ch_Squat    = scriptOp.appendChan('Body_Squat')
    ch_Leg_Up   = scriptOp.appendChan('Leg_Up')
    ch_Arm_Up   = scriptOp.appendChan('Arm_Up')
    

    if len(scriptOp.inputs) == 0: return    
    in_chop = scriptOp.inputs[0]
    

    if not in_chop['has_pose'] or in_chop['has_pose'][0] < 0.5:
        ch_Squat[0]=0; ch_Leg_Up[0]=0; ch_Arm_Up[0]=0
        return

    try:
        def get_y(part):
            return (in_chop[f'left_{part}_y'][0] + in_chop[f'right_{part}_y'][0]) / 2.0
            
        hip_y    = get_y('hip')
        nose_y   = in_chop['nose_y'][0]
        
        ly_ankle = in_chop['left_ankle_y'][0]; ry_ankle = in_chop['right_ankle_y'][0]
        ly_wrist = in_chop['left_wrist_y'][0]; ry_wrist = in_chop['right_wrist_y'][0]
        
    except:
        return 


    is_squat = hip_y < 0.38 

    leg_diff = abs(ly_ankle - ry_ankle)
    is_leg_up = leg_diff > 0.2


    l_up = ly_wrist > (hip_y + 0.05)
    r_up = ry_wrist > (hip_y + 0.05)
    is_arm_up = l_up or r_up

    ch_Squat[0]  = 1 if is_squat else 0
    ch_Leg_Up[0] = 1 if is_leg_up else 0
    ch_Arm_Up[0] = 1 if is_arm_up else 0
    
    return