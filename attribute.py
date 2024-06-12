class toolInstrumentVoice:
    def __init__(self, a, b, c, d, e):
        # Tần số cơ bản của âm thanh 
        self.pitch = a
        # Sai số trung bình phương căn bậc hai
        self.RMSE = b
        # khoảng lặng
        self.percentSilence = c 
        # kích cỡ
        self.magnitude = d 
        # Lặp lại
        self.frequency = e