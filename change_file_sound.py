import os
from pydub import AudioSegment

def process_audio(file_path, target_length=7000, target_sample_rate=28000):
    audio = AudioSegment.from_wav(file_path)
    
    # Change the sample rate to 28000 Hz
    if audio.frame_rate != target_sample_rate:
        audio = audio.set_frame_rate(target_sample_rate)
        print(f"Sample rate of {file_path} changed to {target_sample_rate} Hz")
    
    current_length = len(audio)
    print(f"Original length of {file_path}: {current_length} ms")
    
    if current_length < target_length:
        silence = AudioSegment.silent(duration=target_length - current_length)
        audio = audio + silence  # Add silence to the end
    elif current_length > target_length:
        audio = audio[:target_length]  # Truncate audio
    
    final_length = len(audio)
    print(f"Processed length of {file_path}: {final_length} ms")
    
    return audio

def process_folder(folder_path, target_length=7000, target_sample_rate=28000):
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(subdir, file)
                processed_audio = process_audio(file_path, target_length, target_sample_rate)
                processed_audio.export(file_path, format="wav")
                
                # Recheck the length and sample rate of the saved file
                reloaded_audio = AudioSegment.from_wav(file_path)
                reloaded_length = len(reloaded_audio)
                reloaded_sample_rate = reloaded_audio.frame_rate
                print(f"Rechecked length of {file_path} after saving: {reloaded_length} ms")
                print(f"Rechecked sample rate of {file_path} after saving: {reloaded_sample_rate} Hz")
                if reloaded_length != target_length:
                    print(f"Error: {file_path} length mismatch after saving. Expected {target_length} ms, got {reloaded_length} ms")
                if reloaded_sample_rate != target_sample_rate:
                    print(f"Error: {file_path} sample rate mismatch after saving. Expected {target_sample_rate} Hz, got {reloaded_sample_rate} Hz")
                    # Force resample and save again
                    reloaded_audio = reloaded_audio.set_frame_rate(target_sample_rate)
                    reloaded_audio.export(file_path, format="wav")
                    reloaded_audio = AudioSegment.from_wav(file_path)
                    if reloaded_audio.frame_rate != target_sample_rate:
                        print(f"Critical Error: Unable to set sample rate of {file_path} to {target_sample_rate} Hz")

# Thư mục chính chứa các thư mục con
main_folder = 'E:\\CHTPT_code_me\\static'

# Thực hiện xử lý
process_folder(main_folder)
