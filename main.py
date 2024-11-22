import time

import pygame
import random
from EntityList import EntityList
from MapKey import MapKey


class MapApp:
    def __init__(self, screen_width=900, screen_height=710):
        # 初始化Pygame
        pygame.init()
        self.entityList = EntityList()

        # 设置窗口大小
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # 设置窗口标题
        pygame.display.set_caption('地图应用')

        # 加载背景图片
        self.background_images = {
            'mi_city': pygame.image.load('img/micity.png'),
            'another_city': pygame.image.load('img/yiji.png')
        }

        # 调整图片大小
        for key in self.background_images:
            self.background_images[key] = pygame.transform.scale(self.background_images[key], (700, 700))

        # 初始背景设置为mi_city
        self.current_background = 'mi_city'

        # 按钮的矩形区域
        self.button_rect = pygame.Rect(725, 50, 150, 50)
        self.spawn_button_rect = pygame.Rect(725, 150, 150, 50)  # 新增按钮

        # 图标类型
        self.icon_images = {
            2: pygame.image.load('img/T.png'),  # 假设CT.png是30x30的小图片
            3: pygame.image.load('img/CT.png')  # 假设T.png是30x30的小图片
        }

        # 调整图标大小
        for teamFlag in self.icon_images:
            self.icon_images[teamFlag] = pygame.transform.scale(self.icon_images[teamFlag], (30, 30))

        # 存储小图片的位置、类型、角度和要显示的数字
        self.icons = []  # 每个元素是一个字典，包含位置、类型、角度和数字

        # 字体设置
        self.font = pygame.font.Font(None, 15)

    def draw_button(self, text, rect):
        pygame.draw.rect(self.screen, (0, 255, 0), rect)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def spawn_icons(self):
        # 清除之前的图标
        self.icons.clear()

        self.entityList.registerEntity()

        # 随机生成十个图标
        for entity in self.entityList.list:
            teamFlag = entity.getTeamFlag()
            angle = entity.getViewAngles()
            number = entity.getHealth()
            x, y = self.GameToMap(entity.posX, entity.posY)
            self.icons.append({'pos': (x, y), 'teamFlag': teamFlag, 'angle': angle, 'number': number})
        self.entityList.updateList()

    def move_icons(self):
        self.entityList.updateList()
        # 移动图标到新的随机位置，并随机更新角度和数字
        for i, icon in enumerate(self.icons):
            entity = self.entityList.list[i]
            angle = entity.getViewAngles()
            number = entity.getHealth()
            x, y = self.GameToMap(entity.posX, entity.posY)
            icon.update({
                'pos': (x, y),
                'angle': angle,
                'number': number
            })

    def GameToMap(self, x, y):

        if self.current_background == 'mi_city':
            x, y = MapKey.micity(x, y)
        elif self.current_background == 'another_city':
            x, y = MapKey.yiji(x, y)

        return x, y

    def rotate_and_add_number(self, image, angle, number):
        rotated_image = pygame.transform.rotate(image, angle)
        text_surface = self.font.render(str(number), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rotated_image.get_rect().center)
        rotated_image.blit(text_surface, text_rect)
        return rotated_image

    def run(self):
        running = True
        clock = pygame.time.Clock()  # 添加计时器来控制帧率
        while running:
            clock.tick(60)  # 控制每秒刷新60次

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        # 切换背景
                        self.current_background = 'another_city' if self.current_background == 'mi_city' else 'mi_city'
                    elif self.spawn_button_rect.collidepoint(event.pos):
                        # 生成图标
                        self.spawn_icons()

            # 移动图标
            self.move_icons()

            # 清除屏幕
            self.screen.fill((0, 0, 0))

            # 绘制背景图
            self.screen.blit(self.background_images[self.current_background], (0, 0))

            # 绘制按钮
            self.draw_button('Change Map', self.button_rect)
            self.draw_button('Spawn Icons', self.spawn_button_rect)

            # 绘制图标
            for icon in self.icons:
                rotated_icon = self.rotate_and_add_number(self.icon_images[icon['teamFlag']], icon['angle'],
                                                          icon['number'])
                self.screen.blit(rotated_icon, icon['pos'])

            # 更新屏幕
            pygame.display.flip()

        # 游戏退出时，退出pygame
        pygame.quit()


# 使用类创建实例并运行程序
if __name__ == "__main__":
    app = MapApp()
    app.run()
