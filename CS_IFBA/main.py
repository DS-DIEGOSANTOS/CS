import pygame
from data.scripts import scene
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()

        self.fps = 120
        self.running = True

        self.colors = {
            'background': (125, 112, 113),
            'text': (223, 246, 245),
            'shadows': (48, 44, 46)
        }

        self.screen_width, self.screen_height = 1024, 576
        self.screen_dimensions = (self.screen_width, self.screen_height)

        self.render_width, self.render_height = 1024, 576
        self.render_dimensions = (self.render_width, self.render_height)

        self.font = pygame.font.Font('data/font/font.ttf', 15)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.clock = pygame.time.Clock()
        self.render_surface = pygame.Surface(self.render_dimensions)

        self.input = []
        self.music_player = MusicPlayer(self.screen)
        self.background = Background(self.screen_dimensions)
        self.active_scene = scene.MainMenuScene()


    def run(self):

        while self.running:
            self.clock.tick(self.fps)

            self.handle_input()

            self.active_scene.update(self.render_surface, self.input,self.background.background_surface)
            self.render_surface.blit(
                self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5))

            self.screen.blit(pygame.transform.scale(self.render_surface, self.screen_dimensions), (0, 0))

            self.music_player.handle_events()
            self.music_player.update(self.screen)
           # self.background.update(self.screen)


            if self.active_scene.next_scene:
                self.active_scene = self.active_scene.next_scene
                if isinstance(self.active_scene, scene.MainMenuScene):
                    pygame.display.set_caption('CsLow: MainMenu')
                elif isinstance(self.active_scene, scene.ClientScene):
                    pygame.display.set_caption('CsLow: Client')
                elif isinstance(self.active_scene, scene.HostScene):
                    pygame.display.set_caption('CsLow: Host')

            pygame.display.update()

    def handle_input(self):
        self.input = pygame.event.get()
        for event in self.input:
            if event.type == pygame.QUIT:
                self.active_scene.stop()
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active_scene.stop()
                    self.running = False

class MusicPlayer:
    def __init__(self, screen):
        self.music_list = []
        self.current_track = 0

        # Recuperar a lista de caminhos das músicas do arquivo de texto
        with open('./data/music/listaMusic.txt', 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                caminho = linha.strip()
                self.music_list.append(caminho)

        pygame.mixer.music.load(self.music_list[self.current_track])

        # Iniciar a reprodução da música
        pygame.mixer.music.play(-1)

        self.screen = screen  # Armazena a referência da tela

        self.button_width, self.button_height = 40, 40

        self.pause_button_image = pygame.image.load('data/icons/botao-pausa.png')
        self.play_button_image = pygame.image.load('data/icons/botao-play.png')
        self.forward_button_image = pygame.image.load('data/icons/botao-proximo.png')
        self.backward_button_image = pygame.image.load('data/icons/botao-volta.png')

        self.pause_button_image = pygame.transform.scale(self.pause_button_image,
                                                         (self.button_width, self.button_height))
        self.play_button_image = pygame.transform.scale(self.play_button_image, (self.button_width, self.button_height))
        self.forward_button_image = pygame.transform.scale(self.forward_button_image,
                                                           (self.button_width, self.button_height))
        self.backward_button_image = pygame.transform.scale(self.backward_button_image,
                                                            (self.button_width, self.button_height))

        button_x = 60
        button_y = self.screen.get_height() - self.button_height - 10

        self.pause_button_rect = self.pause_button_image.get_rect(topleft=(button_x, button_y))
        self.play_button_rect = self.play_button_image.get_rect(topleft=(button_x + 70, button_y))
        self.forward_button_rect = self.forward_button_image.get_rect(topleft=(button_x + 140, button_y))
        self.backward_button_rect = self.backward_button_image.get_rect(topleft=(button_x + 210, button_y))

        # Variável para controlar a reprodução da música
        self.is_paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                # Verificar se o botão de pausa foi clicado
                if self.pause_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.pause()
                    self.is_paused = True
                # Verificar se o botão de reprodução foi clicado
                elif self.play_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                # Verificar se o botão de avanço foi clicado
                elif self.forward_button_rect.collidepoint(event.pos):
                    if len(self.music_list)-1 > self.current_track:
                        pygame.mixer.music.stop()
                        self.current_track = self.current_track + 1
                        pygame.mixer.music.load(self.music_list[self.current_track])
                        pygame.mixer.music.play(-1)
                # Verificar se o botão de retorno foi clicado
                elif self.backward_button_rect.collidepoint(event.pos):
                    if self.current_track>0 :
                        pygame.mixer.music.stop()
                        self.current_track = self.current_track - 1
                        pygame.mixer.music.load(self.music_list[self.current_track])
                        pygame.mixer.music.play(-1)

    def update(self, screen):

        # Desenhar os botões na tela
        screen.blit(self.pause_button_image, self.pause_button_rect)
        screen.blit(self.play_button_image, self.play_button_rect)
        screen.blit(self.forward_button_image, self.forward_button_rect)
        screen.blit(self.backward_button_image, self.backward_button_rect)

        pygame.display.flip()  # Atualiza a tela

class Background:
    def __init__(self, screen_dimensions):
        # Carregar a imagem de fundo
        background_image = pygame.image.load('data/img/menu.jpg')

        # Redimensionar a imagem para as dimensões desejadas
        background_image = pygame.transform.scale(background_image, screen_dimensions)

        # Atribuir a imagem como superfície de fundo
        self.background_surface = background_image


if __name__ == '__main__':
    app = Game()
    app.run()
