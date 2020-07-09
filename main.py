from GameSprite import *

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新的帧率
FRAME_PER_SEC = 60

# 创建敌机事件常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 英雄发射子弹时间ID
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class PlaneGame(object):
    """
    游戏主控制类
    """

    def __init__(self):
        # 初始化pygame
        pygame.init()

        # 主窗口
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)

        # 背景图片
        self.bg_img = pygame.image.load("./images/background.png")

        #  游戏时钟
        self.clock = pygame.time.Clock()

        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        """
        创建精灵和精灵组
        :return:
        """

        # 创建背景精灵
        bg1 = BackGround()
        bg2 = BackGround()
        bg2.rect.y = -bg2.rect.height
        self.back_img_group = pygame.sprite.Group(bg1, bg2)

        # 敌机精灵
        self.enemy_group = pygame.sprite.Group()

        # 英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        """
        游戏循环
        :return:
        """
        while True:
            # 设置循环频率
            self.clock.tick(FRAME_PER_SEC)

            # 事件监听
            self.__event_handler()

            # 检测碰撞
            self.__check_crash()

            # 重新绘制精灵
            self.__update_sprites()

            # 刷新画面
            pygame.display.update()

    def __event_handler(self):
        """
        处理事件
        :return:
        """
        # 捕获并处理事件
        for e in pygame.event.get():
            # 关闭
            if e.type == pygame.QUIT:
                self.__game_over()
            elif e.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif e.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 处理键盘事件
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            self.hero.x_speed = 2
        elif pressed_keys[pygame.K_LEFT]:
            self.hero.x_speed = -2
        else:
            self.hero.x_speed = 0

    @staticmethod
    def __game_over():
        print("游戏关闭")
        pygame.quit()
        exit()

    def __check_crash(self):
        """
        碰撞检测
        :return: 
        """

        # 检测子弹和敌机的碰撞
        pygame.sprite.groupcollide(self.hero.bullets_group, self.enemy_group, True, True)

        # 检测敌机和英雄的碰撞
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        """
        更新精灵
        :return:
        """
        # 更新背景
        self.back_img_group.update()
        self.back_img_group.draw(self.main_window)

        # 更新敌机
        self.enemy_group.update()
        self.enemy_group.draw(self.main_window)

        # 更新英雄位置
        self.hero_group.update()
        self.hero_group.draw(self.main_window)

        # 更新子弹位置
        self.hero.bullets_group.update()
        self.hero.bullets_group.draw(self.main_window)


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
