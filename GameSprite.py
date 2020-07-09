import random

import pygame

from main import SCREEN_RECT


class GameSprite(pygame.sprite.Sprite):
    """
    精灵
    """

    def __init__(self, image_path, step_size=1):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.y_step_size = step_size

    def update(self):
        """
        飞机精灵向下移动
        :return:
        """
        self.rect.y += self.y_step_size


class BackGround(GameSprite):
    """
    背景
    """

    def __init__(self):
        super().__init__("./images/background.png")

    def update(self):
        """
        更新背景图片位置
        :return:
        """

        # 计算新位置
        super().update()

        # 如果当前图像已经移动出屏幕，则将图像移动到正上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """
    敌机精灵
    """

    def __init__(self):
        # 创建敌机精灵
        super().__init__("./images/enemy1.png")

        # 设置初始位置
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0

        # 设置敌机下降速度
        self.step_size = random.randint(1, 2)

    def update(self):
        # 更新敌机位置
        super().update()

        # 删除飞出屏幕的敌机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    def __del__(self):
        # print("敌机销毁")
        pass


class Hero(GameSprite):
    """
    英雄精灵
    """

    def __init__(self):
        super().__init__("./images/me1.png", 0)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 80

        self.x_speed = 0

        # 子弹精灵组
        self.bullets_group = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.x_speed

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        """
        发射子弹
        :return:
        """
        for i in range(3):
            bullet = Bullet()

            bullet.rect.bottom = self.rect.y - i * 15
            bullet.rect.centerx = self.rect.centerx

            self.bullets_group.add(bullet)


class Bullet(GameSprite):
    """
    子弹精灵
    """

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()
