from point_mass import point_mass, all_masses
from vector_class import vector
import pygame

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    
    ram = point_mass(0.1,10,vector(330,20),screen,"ram",vector(4,0))
    SUN = point_mass(10000,20,vector(500,300),screen,"SUN",vector(0,0))
    hari = point_mass(0.1,10,vector(770,580),screen,"hari",vector(-4,0))
    keshab = point_mass(0.1,10,vector(300,510),screen,"keshab",vector(0,-4))
    
    list_of_masses = [ram,SUN,hari,keshab]
    masses = all_masses(list_of_masses)
    run = True
    while (run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        screen.fill((255,255,255))
        masses.execute()
        pygame.display.flip()
    pygame.quit()

main()
