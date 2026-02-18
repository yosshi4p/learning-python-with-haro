
###Visual Studio Codeで動く、上から落ちてくる物体を下部にあるバーでキャッチするゲームのコード例です。Pygameのライブラリを使用します。###
import pygame
import random
# Pygameの初期化
pygame.init()
# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# バーのクラス
class Bar:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 5
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
# 落ちてくる物体のクラス
class FallingObject:
    def __init__(self):
        self.size = 20
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = 0
        self.speed = random.randint(2, 5)
    def fall(self):
        self.y += self.speed
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
# ゲームのメインループ
def main():
    clock = pygame.time.Clock()
    bar = Bar()
    falling_objects = []
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bar.move("left")
        if keys[pygame.K_RIGHT]:
            bar.move("right")
        # 新しい物体を追加
        if random.randint(1, 20) == 1:
            falling_objects.append(FallingObject())
        # 物体を落とす
        for obj in falling_objects:
            obj.fall()
            # キャッチの判定
            if (bar.x < obj.x < bar.x + bar.width) and (bar.y < obj.y + obj.size < bar.y + bar.height):
                score += 1
                falling_objects.remove(obj)
            # 画面外に出た物体を削除
            elif obj.y > SCREEN_HEIGHT:
                falling_objects.remove(obj)
        # 画面の描画
        screen.fill(WHITE)
        bar.draw(screen)
        for obj in falling_objects:
            obj.draw(screen)
        # スコアの表示
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()
    