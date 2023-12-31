import cv2
from detect import detect_human

def collect_frames_w_suspects(frames):
    #ToDo: Explain the Algorithm!!
    
    frame_list = []
    detected_count = 0
    for idx in range(0,len(frames),30):
        results = detect_human(frames[idx])
        if "no detections" in results:
            detected_count = 0
            continue

        detected_count += 1
        if detected_count == 2:
            start_idx = idx - (4*30)
            frame_list.append(frames[start_idx:idx])
            detected_count = 0
    return frame_list


def generate_video(frame_list, session_id, frame_rate=10):
    output_name = f"{session_id}.mp4"
    if not frame_list:
        return
    print(len(frame_list))
    height, width, layers = frame_list[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (width, height)
    video = cv2.VideoWriter(output_name, fourcc, frame_rate, frame_size, isColor=True)

    for frame in frame_list:
        try:
            video.write(frame)
        except:
            pass
    video.release()
    return
