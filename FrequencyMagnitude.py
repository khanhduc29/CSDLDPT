import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np

# 700 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử

# Mảng X_mag trả về một mảng bao gồm: 
# Giá trị của phần tử = giá trị magnitude, 
# vị trí của phần tử đó = hz tương ứng => Dùng 2 mảng để lưu lại 2 giá trị đó
# - FFT (Fast Fourier Transform): Một thuật toán nhanh để tính toán chuyển đổi Fourier, chuyển tín hiệu từ miền thời gian sang miền tần số.

#  FrequencyMagnitude (Độ lớn tần số)Đo lường cường độ tần số Tính toán các tần số xuất hiện nhiều nhất và mức độ (magnitude) của chúng từ tín hiệu âm thanh đầu vào.
# Mỗi loại âm thanh đều có cường độ khác nhau và những cái nhịp khác nhau
def funcFrequencyMagnitude(audio_dir):
    # Load file âm thanh vào librosa
    audio, sr = librosa.load(audio_dir, duration = 7)#Load file âm thanh vào librosa
    # Thực hiện FFT để chuyển đổi tín hiệu từ miền thời gian sang miền tần số
    X = np.fft.fft(audio) #Mảng X là mảng chứa dãy tần số và mật độ của nó (Mặc định thì độ lớn của mật độ là số ảo ) (Số thực = mật độ / Số ảo = giá trị pha (Ko cần))
    X_mag = np.absolute(X) #Lấy giá trị tuyệt đối thì sẽ có được phần số thực 

    f = np.linspace(0, sr, len(X_mag)) # Tạo mảng tần số tương ứng
    f_bins = int(len(X_mag))  

    #print(f)
    ################################################3 print(X_mag.size)
    #plt.plot(f[:f_bins], X_mag[:f_bins])
    f[:f_bins], X_mag[:f_bins]

    #print(f)
    #print(X_mag)
    #print(f.size)
    #print(f_bins)

    # Khởi tạo mảng lưu trữ tần số và magnitude lớn nhất cho 7 phần
    freq =[] #Freq là mảng ghi tần số có mức độ xuất hiện lớn nhất
    freq = [0 for i in range(7)]

    magnitude =[] #Magnitude là cụ thể mức độ xuất hiện là bao nhiêu
    magnitude = [0 for i in range(7)]
    # Biến trợ giúp để lưu trữ vị trí và giá trị lớn nhất
    position = 0
    max = 0
    pos = 0
    # Vòng lặp qua các giá trị magnitude
    for i in range(0, len(X_mag)):        
        if(X_mag[i] > max):
            max = X_mag[i]
            pos = i
        if(i> 0):
            if( (i % int(len(X_mag)/7)) == 0 and i != len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max
                #print('Position value at checkpoint: ' + str(position))
                position += 1
                max = 0
            if(i == len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max
                #print('Position value at checkpoint: ' + str(position))  

 # Tạo danh sách các cặp (frequency, magnitude)
    pairs = list(zip(freq, magnitude))
    # print(freq) 
    # print(magnitude)  
    return pairs


# test
# print(funcFrequencyMagnitude("E:/Learn/tool_instrument_voice_recognition/src/File âm thanh/1 máy sấy tóc/may_say_toc_1.wav"))