import cv2
import numpy as np

class CandyRecognizer:
    video_capture = None
    color_ranges = None

    def __init__(self, video_path):
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(self.video_path)
        if not self.video_capture.isOpened():
            raise Exception("Failed to open file")
        self.color_ranges = {
            "Red": (np.array([0, 50, 100]), np.array([10, 200, 255])),
            "Pink": (np.array([160, 50, 50]), np.array([180, 255, 255])),
            "Orange": (np.array([11, 100, 100]), np.array([25, 255, 255])),
            "Green":  (np.array([30, 80, 50]), np.array([60, 255, 255]))
        }

    def run_program(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break  # Exit if no frame is loaded
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            result_frame = self.detect_candy(frame, hsv_frame)
            cv2.imshow('Detected Candies', result_frame)  # Display the result frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Exit if 'q' is pressed
        self.close_program()

    def detect_candy(self, original_frame, hsv_image):
        masks = {}
        candy_counts = {}
        result_frame = original_frame.copy()  # Copy the original frame to draw on
        for color, (lower, upper) in self.color_ranges.items():
            masks[color] = self.create_color_mask(hsv_image, lower, upper)
            count = self.detect_and_draw_contours(result_frame, masks[color], color)
            if color == "Pink":
                cv2.imshow(color, masks[color])
            candy_counts[color] = count

        print("Ilość cukierków: " + str(candy_counts))
        return result_frame  # Return the frame with drawn contours

    def detect_and_draw_contours(self, output_image, mask, color_name):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 30000:  # Adjust the area threshold as needed
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(output_image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 2)
                count += 1
        return count

    def create_color_mask(self, hsv_image, lower_color, upper_color):
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        return mask

    def close_program(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

# Path to the video file
video_path = 'videos/video1.mp4'
gptRes = CandyRecognizer(video_path)

# Run the candy detection program
gptRes.run_program()
