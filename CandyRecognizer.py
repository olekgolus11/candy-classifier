import cv2
import constants as C


class CandyRecognizer:
    video_capture = None
    color_ranges = None
    width = None
    height = None
    middle_x = None

    def __init__(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        self.counter = {C.RED_KEY: 0, C.PINK_KEY: 0, C.ORANGE_KEY: 0, C.GREEN_KEY: 0}
        self.tracked_candies_y = {C.RED_KEY: [], C.PINK_KEY: [], C.ORANGE_KEY: [], C.GREEN_KEY: []}
        if not self.video_capture.isOpened():
            raise Exception("Failed to open file")
        self.color_ranges = {
            C.RED_KEY: C.RED_VALUE,
            C.PINK_KEY: C.PINK_VALUE,
            C.ORANGE_KEY: C.ORANGE_VALUE,
            C.GREEN_KEY: C.GREEN_VALUE
        }

    def run_program(self):
        while True:
            is_frame_loaded, frame = self.video_capture.read()
            if not is_frame_loaded:
                break
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            result_frame = self.detect_candy(frame, hsv_frame)
            frame_with_middle_line = self.append_middle_line(result_frame)
            self.draw_counter(frame_with_middle_line)
            cv2.imshow('Detected Candies', frame_with_middle_line)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.close_program()

    def draw_counter(self, frame):
        cv2.putText(frame, f"{C.RED_KEY}: " + str(self.counter[C.RED_KEY]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, C.INFO_COLOR, C.TEXT_THICKNESS)
        cv2.putText(frame, f"{C.PINK_KEY}: " + str(self.counter[C.PINK_KEY]), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, C.INFO_COLOR, C.TEXT_THICKNESS)
        cv2.putText(frame, f"{C.ORANGE_KEY}: " + str(self.counter[C.ORANGE_KEY]), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, C.INFO_COLOR, C.TEXT_THICKNESS)
        cv2.putText(frame, f"{C.GREEN_KEY}: " + str(self.counter[C.GREEN_KEY]), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, C.INFO_COLOR, C.TEXT_THICKNESS)

    def detect_candy(self, original_frame, hsv_image):
        masks = {}
        result_frame = original_frame.copy()
        for color, (lower, upper) in self.color_ranges.items():
            masks[color] = self.create_color_mask(hsv_image, lower, upper)
            self.detect_and_draw_contours(result_frame, masks[color], color)

        return result_frame

    def detect_and_draw_contours(self, output_image, mask, color_name):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > C.MIN_CONTOUR_AREA:
                x, y, width, height = cv2.boundingRect(contour)
                tracked_candies_y_for_this_color = self.tracked_candies_y[color_name]
                tracked_candies_y_for_this_color_ranges = self.convert_to_ranges(tracked_candies_y_for_this_color, C.Y_THRESHOLD)

                if self.is_candy_tracked(color_name, y):
                    self.untrack_candy(color_name, tracked_candies_y_for_this_color, tracked_candies_y_for_this_color_ranges)
                elif self.is_candy_in_check_area(x):
                    self.tracked_candies_y[color_name].append(y)
                    self.counter[color_name] += 1
                elif self.is_candy_after_check_area(x):
                    self.untrack_candy(color_name, tracked_candies_y_for_this_color,
                                       tracked_candies_y_for_this_color_ranges)

                self.draw_detected_candy_border(output_image, color_name, x, y, width, height)

    def convert_to_ranges(self, values, threshold):
        return [range(value - threshold, value + threshold) for value in values]

    def untrack_candy(self, color_name, tracked_candies_y_for_this_color, tracked_candies_y_for_this_color_ranges):
        self.tracked_candies_y[color_name] = [y for y in tracked_candies_y_for_this_color if y in tracked_candies_y_for_this_color_ranges]

    def is_candy_tracked(self, candy_color, candy_y):
        tracked_candies_y_for_this_color = self.tracked_candies_y[candy_color]
        return any(y in tracked_candies_y_for_this_color for y in range(candy_y - C.Y_THRESHOLD, candy_y + C.Y_THRESHOLD))

    def is_candy_in_check_area(self, current_x):
        return self.middle_x - C.X_THRESHOLD <= current_x <= self.middle_x + C.X_THRESHOLD

    def is_candy_after_check_area(self, current_x):
        return current_x > self.middle_x + C.X_THRESHOLD

    def create_color_mask(self, hsv_image, lower_color, upper_color):
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        return mask

    def draw_detected_candy_border(self, output_image, color_name, x, y, width, height):
        cv2.rectangle(output_image, (x, y), (x + width, y + height), C.INFO_COLOR, thickness=C.LINE_THICKNESS)
        cv2.putText(output_image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5, C.INFO_COLOR,
                    C.TEXT_THICKNESS)

    def close_program(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def find_middle_of_frame(self, frame):
        self.height, self.width = frame.shape[:2]
        self.middle_x = self.width // 2

    def append_middle_line(self, frame):
        self.find_middle_of_frame(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame, (self.middle_x, 0), (self.middle_x, self.height), C.INFO_COLOR, C.LINE_THICKNESS)

        return frame
