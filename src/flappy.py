import asyncio
import sys
import cv2
import mediapipe as mp
import numpy as np
import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT
import time  # Importing time module for handling gesture detection delay

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window

# Initialize Pygame mixer
pygame.mixer.init()

# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    sys.exit()
else:
    print("Camera successfully opened.")

def is_thumb_index_touching(landmarks):
    thumb_tip = landmarks[mpHands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mpHands.HandLandmark.INDEX_FINGER_TIP]

    distance = np.sqrt(
        (thumb_tip.x - index_tip.x) ** 2 +
        (thumb_tip.y - index_tip.y) ** 2 +
        (thumb_tip.z - index_tip.z) ** 2
    )
    return distance < 0.05

class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        self.last_gesture_time = 0  # Initialize the last gesture detection time

    async def start(self):
        try:
            while True:
                self.background = Background(self.config)
                self.floor = Floor(self.config)
                self.player = Player(self.config)
                self.welcome_message = WelcomeMessage(self.config)
                self.game_over_message = GameOver(self.config)
                self.pipes = Pipes(self.config)
                self.score = Score(self.config)
                await self.splash()
                await self.play()
                await self.game_over()
                if self.score.score > self.score.high_score:
                    self.score.high_score = self.score.score
                    self.score.save_high_score()
        finally:
            cap.release()
            cv2.destroyAllWindows()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""
        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:
            if self.player.collided(self.pipes, self.floor):
                return

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    self.player.flap()
            if self.check_gesture_event():
                self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """Crashes the player down and shows game over image"""
        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return
            if self.check_gesture_event():
                if self.player.y + self.player.h >= self.floor.y - 1:
                    return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def check_gesture_event(self):
        current_time = time.time()
        if current_time - self.last_gesture_time < 0.25:  # 200ms delay
            return False

        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera")
            return False

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if is_thumb_index_touching(hand_landmarks.landmark):
                    print("Gesture detected!")
                    self.last_gesture_time = current_time  # Update the last gesture detection time
                    # sound.play()  # Uncomment if you have a sound to play
                    return True
        return False

