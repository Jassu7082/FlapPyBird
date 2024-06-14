import pygame

from ..utils import GameConfig
from .entity import Entity


class Score(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.y = self.config.window.height * 0.1
        self.score = 0
        self.high_score = self.load_high_score()

    def reset(self) -> None:
        self.score = 0

    def add(self) -> None:
        self.score += 1
        self.config.sounds.point.play()

    def load_high_score(self) -> int:
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self) -> None:
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    @property
    def rect(self) -> pygame.Rect:
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        w = sum(image.get_width() for image in images)
        x = (self.config.window.width - w) / 2
        h = max(image.get_height() for image in images)
        return pygame.Rect(x, self.y, w, h)

    def draw(self) -> None:
        """displays score in center of screen"""
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        digits_width = sum(image.get_width() for image in images)
        x_offset = (self.config.window.width - digits_width) / 2

        for image in images:
            self.config.screen.blit(image, (x_offset, self.y))
            x_offset += image.get_width()

        # Display high score in the left corner
        high_score_digits = [int(x) for x in list(str(self.high_score))]
        high_score_images = [self.config.images.numbers[digit] for digit in high_score_digits]
        high_score_x = 10  # 10 pixels padding from the left

        for image in high_score_images:
            self.config.screen.blit(image, (high_score_x, self.y))
            high_score_x += image.get_width()
