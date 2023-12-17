import cv2
import numpy as np
from matplotlib import pyplot as plt

class CandyRecognizer:
    video_capture = None

    def __init__(self):
        self.video_path = 'videos/video1.mp4'
        self.video_capture = cv2.VideoCapture(self.video_path)
        if not self.video_capture.isOpened():
            raise Exception("Failed to open file")

    def run_program(self):
        while True:
            try:
                frame = self.read_frame()
                cv2.imshow('Frame', frame)
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


    def close_program(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def try_gpt_mask(self):
        # Ponowne wczytanie wideo i próba wczytania klatek ze środka nagrania
        cap = cv2.VideoCapture(self.video_path)

        # Znalezienie długości wideo w klatkach
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Próba wczytania klatek z około środkowej części wideo
        middle_frame = total_frames // 2
        frames = []

        # Ustawienie czytnika wideo na środkową klatkę i wczytanie kilku klatek od tego punktu
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame - 3)
        for _ in range(6):
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            else:
                break

        # Zwolnienie uchwytu wideo
        cap.release()

        # Wyświetlenie wczytanych klatek
        plt.figure(figsize=(18, 12))
        for i, frame in enumerate(frames):
            plt.subplot(2, 3, i + 1)
            plt.imshow(frame)
            plt.title(f"Klatka {middle_frame - 3 + i}")
            plt.axis('off')
        plt.show()

    # Funkcja do wykrywania konturów i rysowania ramki wokół cukierków
    def detect_and_draw_contours(self, image, mask, color_name, output_image):
        # Znalezienie konturów na masce
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Rysowanie ramki wokół każdego konturu i zliczanie cukierków
        count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filtruj małe kontury, które mogą być szumem
                # Obliczenie prostokąta otaczającego kontur
                x, y, w, h = cv2.boundingRect(contour)

                # Rysowanie prostokąta na obrazie wyjściowym
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(output_image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                count += 1
        return count

    # Funkcja do konwersji obrazu do HSV i stworzenia maski koloru
    def create_color_mask(self, image, lower_color, upper_color):
        # Konwersja obrazu do przestrzeni kolorów HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        # Tworzenie maski dla podanego zakresu kolorów
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        return mask

    def final_gpt_res(self):
        # Ponowne wczytanie wideo i próba wczytania klatek ze środka nagrania
        cap = cv2.VideoCapture(self.video_path)

        # Znalezienie długości wideo w klatkach
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Próba wczytania klatek z około środkowej części wideo
        middle_frame = total_frames // 2
        frames = []

        # Ustawienie czytnika wideo na środkową klatkę i wczytanie kilku klatek od tego punktu
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame - 3)
        for _ in range(6):
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            else:
                break

        # Zwolnienie uchwytu wideo
        cap.release()

        # Wyświetlenie wczytanych klatek
        plt.figure(figsize=(18, 12))
        for i, frame in enumerate(frames):
            plt.subplot(2, 3, i + 1)
            plt.imshow(frame)
            plt.title(f"Klatka {middle_frame - 3 + i}")
            plt.axis('off')
        plt.show()

        # Zakresy kolorów HSV dla wybranych kolorów cukierków
        # Zakresy mogą wymagać dostosowania w zależności od oświetlenia i odcieni kolorów w wideo
        color_ranges = {
            "czerwony": (np.array([0, 100, 100]), np.array([10, 255, 255])),
            "różowy": (np.array([160, 50, 50]), np.array([180, 255, 255])),
            "pomarańczowy": (np.array([11, 100, 100]), np.array([25, 255, 255])),
            "zielony": (np.array([50, 100, 100]), np.array([70, 255, 255]))
        }

        # Tworzenie masek dla każdego koloru na pierwszej z wybranych klatek
        masks = {}
        for color, (lower, upper) in color_ranges.items():
            masks[color] = self.create_color_mask(frames[0], lower, upper)

        # Wyświetlenie masek dla każdego koloru
        plt.figure(figsize=(15, 10))
        for i, (color, mask) in enumerate(masks.items()):
            plt.subplot(2, 2, i + 1)
            plt.imshow(mask, cmap='gray')
            plt.title(f"Maska dla koloru {color}")
            plt.axis('off')
        plt.show()

        # Stworzenie kopii obrazu do rysowania na nim wyników
        result_image = frames[0].copy()

        # Detekcja cukierków dla każdego koloru i rysowanie ramki
        candy_counts = {}
        for color, mask in masks.items():
            count = self.detect_and_draw_contours(frames[0], mask, color, result_image)
            candy_counts[color] = count

        # Wyświetlenie obrazu z wynikami
        plt.figure(figsize=(8, 6))
        plt.imshow(result_image)
        plt.title("Detekcja Cukierków")
        plt.axis('off')
        plt.show()

        # Wyświetlenie liczby cukierków każdego koloru
        print(candy_counts)
