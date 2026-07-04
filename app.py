import pygame
import sys
import random
import time
import pandas as pd
import numpy as np

# Initialize Pygame engine modules
pygame.init()

# 1. --- SCREEN & WINDOW CONFIGURATION ---
WIDTH, HEIGHT = 950, 600
GRID_SIZE = 20
GRID_CELL = 20 # 20x20 blocks = 400x400 pixels for game arena
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚡ Modern AI-Powered Snake Game (Pro Edition)")

# Core Colors Setup
BLACK = (5, 5, 8)
WHITE = (255, 255, 255)
RED = (255, 51, 51)       # Target Food
BLUE = (51, 204, 255)     # Time Warp Power-up
ORANGE = (255, 165, 0)    # Hazard Triangle Obstacle
GRAY_BORDER = (68, 68, 68)
DARK_GRID = (26, 26, 36)

# Typography Engines
FONT_TITLE = pygame.font.SysFont("bahnschrift", 30, bold=True)
FONT_SUB = pygame.font.SysFont("bahnschrift", 20, bold=True)
FONT_HUD = pygame.font.SysFont("consolas", 16)
FONT_LOGS = pygame.font.SysFont("consolas", 14)

CLOCK = pygame.time.Clock()

class ModernSnakeGame:
    def __init__(self):
        # Configuration properties
        self.environment = "Futuristic Neon"
        self.snake_color = (0, 255, 0) # Glowing green skin
        self.base_speed = 0.15          # Lower is faster tick rate
        self.logs = []                 # Historical Deep Learning Logs array
        self.reset_game()

    def reset_game(self):
        # Initial positions inside grid bounds
        self.snake = [[10, 10], [10, 11], [10, 12]]
        self.direction = "UP"
        self.food = [random.randint(2, 17), random.randint(2, 17)]
        self.powerup = [random.randint(2, 17), random.randint(2, 17)]
        self.powerup_active = False
        self.powerup_timer = 0
        
        # Moving hazard coordinates setup
        self.obstacle = [random.randint(3, 16), random.randint(3, 16)]
        self.obstacle_dir = 1
        
        self.score = 0
        self.game_over = False
        self.game_started = False

    def process_input(self):
        # Keyboard inputs map perfectly to directional updates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_started:
                    if event.key == pygame.K_SPACE:
                        self.game_started = True
                elif self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_started = True
                else:
                    if event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    elif event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"

    def run_engine_logic(self):
        if not self.game_started or self.game_over:
            return

        # 1. Update active powerup timers
        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False

        # 2. Dynamic Obstacle Translation Loop (Moving Hazard)
        self.obstacle[1] += self.obstacle_dir
        if self.obstacle[1] >= GRID_SIZE - 2 or self.obstacle[1] <= 1:
            self.obstacle_dir *= -1

        # 3. Step forward Calculation
        head = self.snake[0].copy()
        if self.direction == "UP": head[0] -= 1
        elif self.direction == "DOWN": head[0] += 1
        elif self.direction == "LEFT": head[1] -= 1
        elif self.direction == "RIGHT": head[1] += 1

        # 4. Critical Boundaries & Body Intersection Collision Check
        if (head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE or 
            head in self.snake or head == self.obstacle):
            self.game_over = True
            return

        self.snake.insert(0, head)

        # Eating mechanisms validation
        if head == self.food:
            self.score += 10
            self.food = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        elif head == self.powerup and not self.powerup_active:
            self.powerup_active = True
            self.powerup_timer = 20 # Active cycle frames length
            self.powerup = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        else:
            self.snake.pop()

        # Append metrics directly to telemetry frame pipeline
        self.logs.append({
            "Head_X": head[0], "Head_Y": head[1],
            "Target_X": self.food[0], "Target_Y": self.food[1],
            "Obstacle_X": self.obstacle[0], "Obstacle_Y": self.obstacle[1],
            "Score": self.score,
            "PowerUp_Active": 1 if self.powerup_active else 0
        })

    def render_graphics(self):
        # Establish dynamic background based on configured Environment Zone
        if self.environment == "Futuristic Neon": bg_col = (5, 5, 8)
        elif self.environment == "Retro Dark": bg_col = (0, 0, 0)
        else: bg_col = (43, 29, 12) # Desert Hazard Theme color
        
        SCREEN.fill(bg_col)

        # --- LEFT SIDE: THE GAME BOARD CONTAINER AREA ---
        board_offset_x = 30
        board_offset_y = 30
        board_w = GRID_SIZE * GRID_CELL
        board_h = GRID_SIZE * GRID_CELL
        
        # Grid board canvas wrapper panel border mesh layout
        pygame.draw.rect(SCREEN, GRAY_BORDER, (board_offset_x - 3, board_offset_y - 3, board_w + 6, board_h + 6), 3, border_radius=6)

        # Draw structural internal grid blocks cells inside matrix bounds
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_rect = (board_offset_x + c * GRID_CELL, board_offset_y + r * GRID_CELL, GRID_CELL, GRID_CELL)
                pygame.draw.rect(SCREEN, DARK_GRID, cell_rect, 1)

        # Draw Serpent Elements (Snake Parts)
        for i, segment in enumerate(self.snake):
            seg_x = board_offset_x + segment[1] * GRID_CELL + 1
            seg_y = board_offset_y + segment[0] * GRID_CELL + 1
            color = WHITE if i == 0 else self.snake_color # Differentiate head node
            pygame.draw.rect(SCREEN, color, (seg_x, seg_y, 18, 18), border_radius=4)

        # Draw Food Object (Target Core Red Dot circle mesh representation)
        food_x = board_offset_x + self.food[1] * GRID_CELL + 10
        food_y = board_offset_y + self.food[0] * GRID_CELL + 10
        pygame.draw.circle(SCREEN, RED, (food_x, food_y), 8)

        # Draw Power-up Object Blue Square node if currently visible
        if not self.powerup_active:
            pw_x = board_offset_x + self.powerup[1] * GRID_CELL + 2
            pw_y = board_offset_y + self.powerup[0] * GRID_CELL + 2
            pygame.draw.rect(SCREEN, BLUE, (pw_x, pw_y, 16, 16), border_radius=2)

        # Draw Obstacle Hazard Item (Moving Triangle profile vertex array coordinates)
        obs_center_x = board_offset_x + self.obstacle[1] * GRID_CELL + 10
        obs_center_y = board_offset_y + self.obstacle[0] * GRID_CELL + 10
        points = [
            (obs_center_x, obs_center_y - 8),
            (obs_center_x - 8, obs_center_y + 8),
            (obs_center_x + 8, obs_center_y + 8)
        ]
        pygame.draw.polygon(SCREEN, ORANGE, points)

        # Bottom HUD Info Prompts Render block zone
        if not self.game_started:
            lbl = FONT_SUB.render("⚡ Engine Offline: Press SPACE to Launch Simulation", True, ORANGE)
            SCREEN.blit(lbl, (board_offset_x, board_offset_y + board_h + 20))
        elif self.game_over:
            lbl = FONT_SUB.render("🚨 CRITICAL COLLISION TERMINATED: Press R to Reset", True, RED)
            SCREEN.blit(lbl, (board_offset_x, board_offset_y + board_h + 20))
        elif self.powerup_active:
            lbl = FONT_SUB.render(f"🛡️ TIME WARP ACTIVE: Speed Stabilized. Timer: {self.powerup_timer}", True, BLUE)
            SCREEN.blit(lbl, (board_offset_x, board_offset_y + board_h + 20))

        # --- RIGHT SIDE: MODERN DASHBOARD PANEL VIEW ---
        panel_x = 470
        
        title_surf = FONT_TITLE.render("🐍 Snake Pro Dashboard", True, WHITE)
        SCREEN.blit(title_surf, (panel_x, 30))

        # Render Metrics HUD Block Indicators
        score_lbl = FONT_HUD.render(f"Score Potential: {self.score} PTS", True, WHITE)
        current_fps = round(1 / (self.base_speed + 0.15 if self.powerup_active else self.base_speed), 1)
        speed_lbl = FONT_HUD.render(f"Matrix Engine Speed: {current_fps} FPS", True, WHITE)
        SCREEN.blit(score_lbl, (panel_x, 80))
        SCREEN.blit(speed_lbl, (panel_x, 105))

        # Neural Analysis Area Box structure boundary
        ai_box_y = 140
        ai_box_w, ai_box_h = 450, 420
        pygame.draw.rect(SCREEN, GRAY_BORDER, (panel_x, ai_box_y, ai_box_w, ai_box_h), 2, border_radius=6)
        
        ai_head = FONT_SUB.render("🤖 Neural AI Coach Analytics", True, WHITE)
        SCREEN.blit(ai_head, (panel_x + 15, ai_box_y + 15))
        pygame.draw.line(SCREEN, GRAY_BORDER, (panel_x + 15, ai_box_y + 40), (panel_x + ai_box_w - 15, ai_box_y + 40), 1)

        # Compute Telemetry analytics parameters rules dynamically 
        if self.game_started and not self.game_over:
            head_now = self.snake[0]
            obs_now = self.obstacle
            distance_to_obstacle = abs(head_now[0] - obs_now[0]) + abs(head_now[1] - obs_now[1])

            tel_lbl = FONT_HUD.render("📡 Live Hazard Telemetry:", True, WHITE)
            SCREEN.blit(tel_lbl, (panel_x + 15, ai_box_y + 55))

            if distance_to_obstacle <= 3:
                ai_lines = [
                    "🚨 EVASIVE MANEUVER REQUIRED!",
                    f"Moving hazard (Orange) is only {distance_to_obstacle} blocks away!"
                ]
                ai_color = RED
            elif head_now[0] < 3 or head_now[0] > GRID_SIZE - 4 or head_now[1] < 3 or head_now[1] > GRID_SIZE - 4:
                ai_lines = [
                    "⚠️ WALL PROXIMITY ALERT:",
                    "Core grid boundaries close. Plan turns."
                ]
                ai_color = ORANGE
            else:
                ai_lines = [
                    "🎯 OPTIMAL SECTOR DETECTED:",
                    "Area safe. Move towards the Target Core Red dot."
                ]
                ai_color = (0, 255, 68)

            for line_idx, line_str in enumerate(ai_lines):
                ln_surf = FONT_HUD.render(line_str, True, ai_color)
                SCREEN.blit(ln_surf, (panel_x + 15, ai_box_y + 85 + line_idx * 22))

            # Simulate Modern DataFrame Log terminal view inside box workspace
            log_start_y = ai_box_y + 160
            db_title = FONT_HUD.render("📊 Historical Deep Learning Logs (Last 4 States):", True, WHITE)
            SCREEN.blit(db_title, (panel_x + 15, log_start_y))

            header_str = f"{'Head_X':<8}{'Head_Y':<8}{'Target_X':<10}{'Obs_X':<8}{'PwrActive':<10}"
            hdr_surf = FONT_LOGS.render(header_str, True, GRAY_BORDER)
            SCREEN.blit(hdr_surf, (panel_x + 15, log_start_y + 25))

            # Fetch DataFrame subset arrays slice tail from logged records matrix logs 
            if self.logs:
                recent_logs = self.logs[-4:]
                for log_idx, data_row
