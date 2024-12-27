"""
Clase principal para el manejo del juego
"""
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.running = False
        self.screen = None
        self.clock = pygame.time.Clock()
        
    def setup(self):
        """Inicializa los componentes del juego"""
        pass
        
    def run(self):
        """Loop principal del juego"""
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
            
    def handle_events(self):
        """Maneja los eventos de input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        """Actualiza el estado del juego"""
        pass
        
    def render(self):
        """Renderiza el frame actual"""
        pass
