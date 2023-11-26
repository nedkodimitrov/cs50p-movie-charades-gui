import tkinter as tk
from helpers import get_random_movie_title, download_ai_img, mask_string
from PIL import ImageTk


class MovieCharadesGUI:
    """
    CS50P Movie Charades GUI

    An interactive game where the user is presented with an AI-generated image from the DALL·E 2 API.
    The image is based on a randomly selected movie title from the top 1000 rated movies on MoviesMiniDatabase retrieved through RapidAPI.
    The user's task is to guess the movie title associated with the image.

    Author: Nedko Dimitrov
    Version: 2.0
    """

    def __init__(self, lives=3, attempts=3):
        """
        Initialize the MovieCharadesGUI object.

        :param lives: Number of lives the player has, defaults to 3.
        :type lives: int, optional

        :param attempts: Number of attempts allowed for each movie title, defaults to 3.
        :type attempts: int, optional
        """
        self.root = tk.Tk()
        self.root.title("CS50P Movie Charades")

        self.score = 0
        self.lives = lives
        self.attempts = attempts
        self.current_movie_title = ""

        # Create the game's graphical elements
        self.create_labels()
        self.create_input_frame()
        self.create_image_label()
        self.create_footer_label()

    def create_labels(self):
        """
        Create and display the score, lives, header, and masked movie title labels.
        """
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack(side="left", padx=50, anchor="nw")

        self.lives_label = tk.Label(self.root, text=f"Lives: {self.lives}")
        self.lives_label.pack(side="right", padx=50, anchor="ne")

        self.remaining_attempts_label = tk.Label(self.root, text=f"Remaining attempts: {self.attempts}")
        self.remaining_attempts_label.pack()

        self.header_label = tk.Label(self.root, font=("Arial", 18), wraplength=600)
        self.header_label.pack(pady=10)

        self.masked_movie_title_label = tk.Label(self.root, font=("Arial", 16), wraplength=600)
        self.masked_movie_title_label.pack(pady=10)

    def create_input_frame(self):
        """
        Create and display the input entry and guess button in a frame.
        """
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)

        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 16))
        self.input_entry.pack(side="left")

        self.guess_button = tk.Button(self.input_frame, text="Guess", font=("Arial", 16), command=self.on_guess_button_click, state=tk.DISABLED)
        self.guess_button.pack(side="left")

    def create_image_label(self):
        """
        Create and display the label for the AI-generated image.
        """
        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=50, pady=10)

    def create_footer_label(self):
        """
        Create and display the footer label with attribution to the APIs used.
        """
        self.footer_label = tk.Label(self.root, text="Powered by OpenAI DALL-E 2 API and MoviesMiniDatabase RapidAPI")
        self.footer_label.pack()

    def on_guess_button_click(self):
        """
        Handler for the Guess button click event.
        """
        # Disable the Guess button to prevent multiple rapid clicks
        self.guess_button["state"] = tk.DISABLED

        # Check if the user's input matches the current movie title
        if self.input_entry.get().strip().lower() == self.current_movie_title.lower():
            # If the guess is correct, update the score label and load the next level
            self.update_score_label()
            self.load_level()
        else:
            # If the guess is incorrect, decrement the remaining attempts
            self.update_remaining_attempts_label(self.remaining_attempts - 1)
            if self.remaining_attempts:
                # If there are remaining attempts, re-enable the Guess button for the next try
                self.guess_button["state"] = tk.NORMAL
            else:
                # If there are no remaining attempts, update the lives label and show the correct movie title
                self.update_lives_label()
                self.masked_movie_title_label["text"] = f"The movie title was: {self.current_movie_title}"
                if self.lives:
                    # If there are lives left, load the next level
                    self.load_level()
                else:
                    # If there are no lives left, display "Game Over" in the header label
                    self.header_label["text"] = "Game Over"

    def update_remaining_attempts_label(self, remaining_attempts):
        """
        Update the label displaying the remaining attempts.

        :param remaining_attempts: The remaining attempts for the current movie title.
        :type remaining_attempts: int
        """
        self.remaining_attempts = remaining_attempts
        self.remaining_attempts_label["text"] = f"Remaining attempts: {self.remaining_attempts}"

    def update_score_label(self):
        """
        Update the score label when the player guesses correctly.
        """
        self.score += 1
        self.score_label["text"] = f"Score: {self.score}"

    def update_lives_label(self):
        """
        Update the lives label when the player loses a life.
        """
        self.lives -= 1
        self.lives_label["text"] = f"Lives: {self.lives}"

    def load_level(self):
        """
        Load a new level with a new movie title and AI-generated image.
        """

        IMAGE_FILE_NAME = "image.png"

        # Show "Loading image..." while fetching and generating the image
        self.header_label["text"] = "Loading image..."
        self.root.update()

        # Get a new random movie title and its corresponding AI-generated image
        self.current_movie_title = get_random_movie_title()
        download_ai_img(self.current_movie_title, IMAGE_FILE_NAME)
        self.photo = ImageTk.PhotoImage(file=IMAGE_FILE_NAME)
        self.image_label["image"] = self.photo

        # Update the header and masked movie title labels with the new movie title
        self.header_label["text"] = "Guess the movie title:"
        self.masked_movie_title_label["text"] = mask_string(self.current_movie_title)

        # Reset the remaining attempts label to the default value
        self.update_remaining_attempts_label(self.attempts)
        # Re-enable the Guess button for the player to make their guess
        self.guess_button["state"] = tk.NORMAL
        # Clear the input entry field for the player to enter a new guess
        self.input_entry.delete(0, tk.END)

    def play_game(self):
        """
        Start the game by loading the first level.
        """
        self.load_level()
        self.root.mainloop()