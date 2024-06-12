import sys
import numpy as np
from aubio import source, pitch

# 700 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử
# Nhằm xác định và tính toán độ cao của âm thanh (pitch) trong các đoạn âm thanh. 
# Đo lường tần số cơ bản của âm thanh
# Độ cao của âm thanh là một trong những đặc trưng quan trọng để nhận diện các loại âm thanh khác nhau
def funcPitch(path, pitch):
    win_s = 4096
    hop_s = 512

    # samplerate = 44100
    samplerate = 28000

    # Đọc file
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    result = []

    # print(len(pitches))
    step = int(len(pitches)/7)

    for i in range(0, 7, 1):
        max = step*(i+1)
        if(i == 6):
            max = len(pitches) - 1
        pitchLocal = []
        for j in range(step*i, max, 1):
            pitchLocal.append(pitches[j])
        result.append(np.array(pitchLocal).mean())  # tính trung bình 

    # print("Average frequency = " + str(np.array(pitches).mean()) + " hz")
    # print(len(result))
    # print(result)
    return result