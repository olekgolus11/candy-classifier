from CandyRecognizer import CandyRecognizer

candy_recognizer = CandyRecognizer()

try:
    candy_recognizer.run_program()
except Exception as e:
    print(e)
finally:
    candy_recognizer.close_program()

