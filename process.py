


import os
import csv
import json
import traceback

# Định nghĩa lớp pathAndResult
class pathAndResult:
    def __init__(self, path, name, distance):
        self.path = path
        self.name = name
        self.distance = distance

from Pitch import funcPitch
from aubio import pitch
from RMSE import funcRMSE
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude
from attribute import toolInstrumentVoice

configPercentSilence = 0.1
configRMSE = 0.3
configPitch = 0.3
configFrequencyMagnitude = 0.3
# Hàm compareFile sẽ tính toán mức độ tương đồng giữa các thông số đặc trưng của hai file âm thanh bằng cách tính tổng trọng số của độ khác biệt 
# giữa các thông số này. Mức độ tương đồng được đo bằng cách tính giá trị nhỏ nhất của tổng trọng số này.
def compareFile(att1, att2):
    maxRes = 1
    for i in range(7):
        for j in range(7):
            same = float(abs(att1[i].percentSilence - att2[j].percentSilence) / max(att1[i].percentSilence, att2[j].percentSilence) * configPercentSilence)
            same += float(abs(att1[i].RMSE - att2[j].RMSE) / max(att1[i].RMSE, att2[j].RMSE) * configRMSE)
            same += float(abs(att1[i].pitch - att2[j].pitch) / max(att1[i].pitch, att2[j].pitch) * configPitch)
            same += float(abs(att1[i].magnitude - att2[j].magnitude) / max(att1[i].magnitude, att2[j].magnitude) * configFrequencyMagnitude / 2)
            same += float(abs(att1[i].frequency - att2[j].frequency) / max(att1[i].frequency, att2[j].frequency) * configFrequencyMagnitude / 2)
            if maxRes > same:
                maxRes = same
    
    return maxRes



def process_search(audio_file_path):
    try:
        att1 = []

        pitchAtt = funcPitch(audio_file_path, pitch)
        RMSEAtt = funcRMSE(audio_file_path)
        percentSilenceAtt = funcPercentSilence(audio_file_path)
        frequencyMagnitudeAtt = funcFrequencyMagnitude(audio_file_path)

        magnitudeAtt = []
        frequencyAtt = []

        for a, b in frequencyMagnitudeAtt:
            magnitudeAtt.append(a)
            frequencyAtt.append(b)

        for i in range(7):
            att1.append(
                toolInstrumentVoice(
                    pitchAtt[i],
                    RMSEAtt[i],
                    percentSilenceAtt[i],
                    magnitudeAtt[i],
                    frequencyAtt[i]
                )
            )

        with open('E:\CHTPT_code_me\CSDLDPT.csv', 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            metadata = [row for row in reader][1:]  # Bỏ qua hàng tiêu đề

        lastResult = []

        for row in metadata:
            if len(row) < 5:
                continue

            try:
                file_path = row[0].split(",")[0].strip()  # Lấy đường dẫn từ cụm từ ổ đĩa E
                pitch_values = json.loads(row[1])
                # print("audio_file_path: ", audio_file_path)
                # print("file_path: ", file_path)

                # if(audio_file_path == file_path):
                #     continue
                rmse_values = json.loads(row[2])
                percent_silence_values = json.loads(row[3])
                frequency_magnitude_values = [tuple(map(float, fm.strip("()").split(','))) for fm in row[4].strip("[]").split('), (')]

                magnitudeAtt = []
                frequencyAtt = []
                for mag, freq in frequency_magnitude_values:
                    magnitudeAtt.append(mag)
                    frequencyAtt.append(freq)

                att2 = []
                for i in range(7):
                    att2.append(
                        toolInstrumentVoice(
                            pitch_values[i],
                            rmse_values[i],
                            percent_silence_values[i],
                            magnitudeAtt[i],
                            frequencyAtt[i]
                        )
                    )

                filename = os.path.basename(file_path)
                
                # Lấy trước dấu phẩy để tạo trường path
                path = file_path.split(",")[0].strip()
                
                lastResult.append(
                    {"name": filename, "distance": compareFile(att1, att2), "path": path}
                )
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for row: {row}. Error: {e}")
                traceback.print_exc()
            except Exception as e:
                print(f"Unexpected error for row: {row}. Error: {e}")
                traceback.print_exc()

        lastResult.sort(key=lambda x: x["distance"])
        results = lastResult[1:4]
        return results
    
    except Exception as e:
        print(f"Error in process_search: {e}")
        traceback.print_exc()
        return []



def get_all_paths_from_csv(csv_file_path):
    try:
        paths = []
        with open(csv_file_path, 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            next(reader)  # Bỏ qua hàng tiêu đề
            for row in reader:
                if len(row) > 0:
                    paths.append(row[0].split(",")[0].strip().replace("E:/CHTPT_code_me", ""))

        return paths
    except Exception as e:
        print(f"Error in get_all_paths_from_csv: {e}")
        traceback.print_exc()
        return []



if __name__ == "__main__":
    # audio_file_path = "E:\\CHTPT_code_me\\Sound\\Car\\bmw-320-vg91.wav"
    audio_file_path = "E:\\CHTPT_code_me\\Boat_test.wav"

    print(process_search(audio_file_path))


    csv_file_path = 'E:\CHTPT_code_me\CSDLDPT.csv'
    all_paths = get_all_paths_from_csv(csv_file_path)
    print(all_paths)