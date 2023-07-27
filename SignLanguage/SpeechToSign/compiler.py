#  Copyright (c) 2023 Harikeshav R
#  All rights reserved.

import os

import cv2


class VideoDisplayer:
    def __init__(self, window_name: str = 'Sign') -> None:
        """
        Initialize the VideoDisplayer.

        Parameters:
        - window_name (str): The name of the window to display the videos.

        """
        self.window_name = window_name
        self.delay_between_signs = 1000 // 30
        self.frame_rate = 60

        self.data = os.listdir("data/videos/")

        self.rescale = 2
        self.create_window()

    def create_window(self) -> None:
        """
        Create the window for video display.

        """
        cap = cv2.VideoCapture('data/videos/0.mp4')
        height, width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, width // self.rescale, height // self.rescale)
        cap.release()

    def display_word(self, path: str) -> None:
        """
        Display the video corresponding to a word.

        Parameters:
        - path (str): The path to the video file.

        """
        cap = cv2.VideoCapture(path)

        if not cap.isOpened():
            print("Does not exist:", path[8:-4])
        while cap.isOpened():

            ret, frame = cap.read()

            if ret:
                if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                    self.create_window()

                cv2.imshow(self.window_name, frame)

                if cv2.waitKey(1000 // self.frame_rate) & 0xFF == ord('q'):
                    break

            else:
                break

        cap.release()

    def show(self, words: list[str]) -> None:
        """
        Show the videos corresponding to a list of words.

        Parameters:
        - words (str): The space-separated words to display.

        """
        for word in words:
            if os.path.exists(f"data/videos/{word}.mp4"):
                self.display_word(f"data/videos/{word}.mp4")

            else:
                for char in word:
                    self.display_word(f'data/videos/{char}.mp4')

            cv2.waitKey(500)

    def destroy(self) -> None:
        """
        Destroy the video display window.

        """
        cv2.destroyWindow(self.window_name)

    def destroy_delayed(self) -> None:
        """
        Destroy the video display window after a delay.

        """
        try:
            cv2.waitKey(1000)
            self.destroy()
        except Exception as e:
            print(e)


def read_and_display_videos() -> None:
    """
    Read input from the user and display corresponding videos.

    """
    text = input("> ")
    displayer = VideoDisplayer()
    displayer.show(text.split())
    displayer.destroy_delayed()


if __name__ == "__main__":
    read_and_display_videos()
