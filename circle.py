import pygame, ctypes, random, time

def main():
    pygame.init()
    info = pygame.display.Info()
    size = (int(info.current_w/10), int(info.current_h/10))
    screen = pygame.display.set_mode(size)
    #screen = pygame.Surface(size)
    file = "image.jpg" #or what ever path you want
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill((0,0,0))
        pygame.draw.circle(screen, [random.randint(0,255) for i in range(3)], (10,10), 10)
        pygame.display.flip()
        try:
            pygame.image.save(screen, file)
            time.sleep(0.02)
        except:
            continue
        try:
            ctypes.windll.user32.SystemParametersInfoW(20,0,file,0)
            time.sleep(0.02)
        except:
            pass
    

if __name__ == "__main__":
    main()
    pygame.quit()
