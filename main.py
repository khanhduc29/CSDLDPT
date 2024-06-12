from flask import Flask, request, render_template, jsonify,send_from_directory
from process import process_search, get_all_paths_from_csv
import os
import tempfile
import traceback
  
app = Flask(__name__)


@app.route('/')
# def home():
#     return render_template('index.html')
def home():
    try:
        # Lấy danh sách tất cả các đường dẫn từ file CSV
        csv_file_path = 'E:\\CHTPT_code_me\\CSDLDPT.csv'
        all_paths = get_all_paths_from_csv(csv_file_path)
        return render_template('index.html', all_paths=all_paths)
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return "Internal Server Error", 500

@app.route('/static/<folder>/<path:path>')
def static_folder(folder, path):
    return send_from_directory(os.path.join('static', folder), path)

@app.route('/process', methods=['POST'])
def process():
    try:
        audio_file = request.files['audioFile']
        
        if audio_file:
            # Tạo tệp tạm thời
            temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            try:
                audio_file.save(temp_audio_file.name)
                
                # Ghi log đường dẫn tệp tạm thời
                print(f"Temporary audio file path: {temp_audio_file.name}")
                
                # Đóng tệp tạm thời để cho phép truy cập khác
                temp_audio_file.close()
                
                # Xử lý tệp âm thanh đã lưu
                results = process_search(temp_audio_file.name)
                
                # Log kết quả
                # print(f"Results: {results}")
                
            finally:
                # Xóa tệp tạm thời
                os.remove(temp_audio_file.name)
            
            return jsonify(results)
        else:
            return jsonify({"error": "No file uploaded"})
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)



