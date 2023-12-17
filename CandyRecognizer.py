from ctypes import util

import cv2
import numpy as np
from matplotlib import pyplot as plt
from Colors import Colors as CLR
import util

class CandyRecognizer:
    video_capture = None
    color_ranges = None

    def __init__(self):
        self.video_path = 'videos/video1.mp4'
        self.video_capture = cv2.VideoCapture(self.video_path)
        if not self.video_capture.isOpened():
            raise Exception("Failed to open file")
        self.color_ranges = {
            "czerwony": (util.get_limits(CLR.RED.value, CLR.RED.name)),
            "różowy": (util.get_limits(CLR.PINK.value, CLR.PINK.name)),
            "pomarańczowy": (util.get_limits(CLR.ORANGE.value, CLR.ORANGE.name)),
            "zielony": (util.get_limits(CLR.GREEN.value, CLR.GREEN.name))
        }

    def run_program(self):
        while True:
            try:
                frame = self.read_frame()
                self.detect_candy(frame)
            except Exception as e:
                print(e)
                break
        self.close_program()

    def read_frame(self):
        is_frame_loaded, frame = self.video_capture.read()
        if not is_frame_loaded:
            raise Exception("No frame loaded")
        if cv2.waitKey(20) & 0xFF == ord('q'):
            raise Exception("User quit program")
        return frame

    def detect_candy(self, image):
        masks = {}
        for color, (lower, upper) in self.color_ranges.items():
            masks[color] = self.create_color_mask(image, lower, upper)

        result_image = image.copy()

        candy_counts = {}
        for color, mask in masks.items():
            count = self.detect_and_draw_contours(image, mask, color, result_image)
            cv2.imshow(color, mask)
            candy_counts[color] = count

        cv2.imshow('Frame', result_image)
        print("Ilosc cukierkow: " + str(candy_counts))

    def close_program(self):
        self.video_capture.release()
        cv2.destroyAllWindows()


    def detect_and_draw_contours(self, image, mask, color_name, output_image):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 4000:  # Filtruj małe kontury, które mogą być szumem
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(output_image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                count += 1
        return count

    def create_color_mask(self, image, lower_color, upper_color):
        # Tworzenie maski dla podanego zakresu kolorów
        mask = cv2.inRange(image, lower_color, upper_color)
        return mask
