import pygame
import sys
import random
import os
from pygame import mixer

# Inicialização segura do Pygame
pygame.init()
try:
    mixer.init()
    sound_enabled = True
except:
    print("Aviso: Sistema de som não inicializado")
    sound_enabled = False

# Configurações do "celular" simulado
PHONE_WIDTH = 360
PHONE_HEIGHT = 760
PHONE_BORDER = 20
SCREEN_WIDTH = PHONE_WIDTH + (PHONE_BORDER * 2)
SCREEN_HEIGHT = PHONE_HEIGHT + (PHONE_BORDER * 2)

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_surface = pygame.Surface((PHONE_WIDTH, PHONE_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Gerenciador de recursos
class ResourceManager:
    @staticmethod
    def load_image(path, size):
        try:
            return pygame.transform.scale(pygame.image.load(path), size)
        except:
            # Criar uma superfície colorida se a imagem não for encontrada
            surf = pygame.Surface(size)
            surf.fill((255, 0, 255))  # Roxo para indicar erro
            return surf

    @staticmethod
    def load_sound(path):
        if not sound_enabled:
            return None
        try:
            return mixer.Sound(path)
        except:
            print(f"Não foi possível carregar o som: {path}")
            return None

# Carregar recursos
class GameResources:
    def __init__(self):
        # Imagens
        self.player_image = ResourceManager.load_image("imgs/player.png", (60, 60))
        self.enemy_image = ResourceManager.load_image("imgs/enemy.png", (50, 50))
        self.background_image = ResourceManager.load_image("imgs/fondo.png", (PHONE_WIDTH, PHONE_HEIGHT))
        self.bullet_image = ResourceManager.load_image("imgs/bullet.png", (20, 20))

        # Sons
        self.shoot_sound = ResourceManager.load_sound("sounds/shoot.mp3")
        self.explosion_sound = ResourceManager.load_sound("sounds/explosion.mp3")
        self.death_sound = ResourceManager.load_sound("sounds/death.mp3")

        # Tentar carregar e iniciar música de fundo
        try:
            if sound_enabled:
                mixer.music.load("sounds/bk.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(-1)
        except:
            print("Música de fundo não carregada")

# Classe principal do jogo
class Game:
    def __init__(self):
        self.resources = GameResources()
        self.reset_game()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def control_background_music(self, play=True):
        if sound_enabled:
            try:
                if play:
                    mixer.music.play(-1)
                else:
                    mixer.music.stop()
            except:
                pass

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 30

        # Configurar jogador
        self.player_rect = self.resources.player_image.get_rect()
        self.player_rect.centerx = PHONE_WIDTH // 2
        self.player_rect.bottom = PHONE_HEIGHT - 20
        self.player_speed = 8

        # Reiniciar música
        self.control_background_music(True)

    def play_sound(self, sound):
        if sound is not None and sound_enabled:
            try:
                sound.play()
            except:
                pass

    def spawn_enemy(self):
        enemy = pygame.Rect(random.randint(0, PHONE_WIDTH - 50), -50, 50, 50)
        self.enemies.append(enemy)

    def show_game_over(self):
        text = self.font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to Restart", True, WHITE)

        game_surface.blit(text, (PHONE_WIDTH//2 - text.get_width()//2, PHONE_HEIGHT//2 - 60))
        game_surface.blit(score_text, (PHONE_WIDTH//2 - score_text.get_width()//2, PHONE_HEIGHT//2))
        game_surface.blit(restart_text, (PHONE_WIDTH//2 - restart_text.get_width()//2, PHONE_HEIGHT//2 + 60))

    def update(self):
        if not self.game_over:
            # Movimento do jogador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_rect.left > 0:
                self.player_rect.x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_rect.right < PHONE_WIDTH:
                self.player_rect.x += self.player_speed

            # Spawn de inimigos
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_enemy()
                self.spawn_timer = 0

            # Atualizar balas
            for bullet in self.bullets[:]:
                bullet.y -= 10
                if bullet.bottom < 0:
                    self.bullets.remove(bullet)

            # Atualizar inimigos
            for enemy in self.enemies[:]:
                enemy.y += 5
                if enemy.top > PHONE_HEIGHT:
                    self.enemies.remove(enemy)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                        self.play_sound(self.resources.death_sound)
                        self.control_background_music(False)  # Para a música quando morre

            # Colisões
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.colliderect(enemy):
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 1
                        self.play_sound(self.resources.explosion_sound)
                        break

    def draw(self):
        # Desenhar fundo
        game_surface.blit(self.resources.background_image, (0, 0))

        if not self.game_over:
            # Desenhar jogador
            game_surface.blit(self.resources.player_image, self.player_rect)

            # Desenhar balas
            for bullet in self.bullets:
                game_surface.blit(self.resources.bullet_image, bullet)

            # Desenhar inimigos
            for enemy in self.enemies:
                game_surface.blit(self.resources.enemy_image, enemy)

            # HUD
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            game_surface.blit(score_text, (10, 10))
            game_surface.blit(lives_text, (10, 50))
        else:
            self.show_game_over()

    def run(self):
        while True:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_SPACE and not self.game_over:
                        # Atirar
                        bullet = pygame.Rect(
                            self.player_rect.centerx - 10,
                            self.player_rect.top,
                            20, 20
                        )
                        self.bullets.append(bullet)
                        self.play_sound(self.resources.shoot_sound)

            # Atualizar
            self.update()

            # Desenhar
            screen.fill(BLACK)
            self.draw()

            # Desenhar borda do celular
            pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), border_radius=20)
            screen.blit(game_surface, (PHONE_BORDER, PHONE_BORDER))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()