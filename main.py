from CandyRecognizer import CandyRecognizer

video_path = 'videos/video1.mp4'
candy_recognizer = CandyRecognizer(video_path)

try:
    candy_recognizer.run_program()
except Exception as e:
    print(e)
finally:
    candy_recognizer.close_program()

