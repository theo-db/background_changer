import pygame, random, math, time, numpy, ctypes
from scipy.spatial.distance import squareform, pdist, cdist

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
def mousePos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return [pt.x, pt.y]

class Boids:
    def __init__(self):
        self.width = 300
        self.height = 200
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("boids")

        self.speed = 1
        self.number = 50
        self.pos = numpy.random.rand(self.number*2).reshape(self.number, 2)
        self.pos *= [self.width, self.height]
        directions = numpy.random.rand(self.number)*2*math.pi
        vecx = numpy.cos(directions) * self.speed
        vecy = numpy.sin(directions) * self.speed
        self.vec = numpy.vstack((vecx,vecy)).T
        self.max_rule = 0.03

    def limit(self, vectors, max_val):
        #norm = sum((vectors**2).T)**0.5
        #too_big = norm > max_val
        #vectors[too_big] *= max_val/norm[too_big]
        #return vectors
        for vector in vectors:
            mag = numpy.linalg.norm(vector)
            if mag > max_val:
                vector[0], vector[1] = vector[0]*max_val/mag, vector[1]*max_val/mag
        return vectors

    def adjust(self):
        matrix = squareform(pdist(self.pos))

        #alignment
        m = matrix < 35
        vel1 = m.dot(self.vec)

        #separation
        m = matrix < 20
        vel2 = self.pos - m.dot(self.pos)/m.sum(axis=1).reshape(len(m),1)
        
        #group
        m = ((matrix < 150) & (matrix > 50)) | (matrix == 0)
        vel3 = m.dot(self.pos)/m.sum(axis=1).reshape(len(m),1) - self.pos

        #flee mouse
        pos = mousePos()
        screen = [ctypes.windll.user32.GetSystemMetrics(i) for i in range(2)]
        pos[0] *= self.width/screen[0]
        pos[1] *= self.height/screen[1]
        positions = numpy.concatenate((numpy.array(pos, numpy.float64).reshape(1,2),self.pos), axis=0)
        matrix_ = squareform(pdist(positions))
        m = matrix < 100
        M = matrix_ < 100
        v1 = self.pos - m.dot(self.pos)/m.sum(axis=1).reshape(len(m),1)
        v2 = positions - M.dot(positions)/M.sum(axis=1).reshape(len(M),1)
        v2 = numpy.delete(v2, 0, axis=0)
        vel4 = v2 - v1
        
        self.limit(vel1, self.max_rule)
        self.limit(vel2, self.max_rule)
        self.limit(vel3, self.max_rule)
        self.limit(vel4, self.max_rule * 2)
        vel = vel1 + vel2 + vel3 + vel4
        return vel

    def move(self):
        self.vec += self.adjust()
        self.limit(self.vec, self.speed)
        self.pos += self.vec
        OverX = (self.pos[numpy.arange(self.number),0] > self.width)
        self.pos[OverX,0] = 0
        OverY = (self.pos[numpy.arange(self.number),1] > self.height)
        self.pos[OverY,1] = 0
        UnderX = (self.pos[numpy.arange(self.number),0] < 0)
        self.pos[UnderX,0] = self.width
        UnderY = (self.pos[numpy.arange(self.number),1] < 0)
        self.pos[UnderY,1] = self.height

    def draw(self):
        self.screen.fill((255,255,255))
        for i in range(self.number):
            pos = self.pos[i]
            vec = self.vec[i]
            body = (int(pos[0]), int(pos[1]))
            head = (int(pos[0]+vec[0]*5), int(pos[1]+vec[1]*5))
            pygame.draw.circle(self.screen, (0,0,0), body, 5)
            pygame.draw.circle(self.screen, (0,0,0), head, 2)
        pygame.display.flip()

def main():
    pygame.init()
    boids = Boids()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        for i in range(5):
            boids.move()
        boids.draw()
        pygame.display.flip()
        pygame.time.wait(1)
        path = "C:/Users/theod/image.jpg"
        try:
            pygame.image.save(boids.screen, path)
            time.sleep(0.02)
        except Exception as e:
            print(e)
            continue
        try:
            ctypes.windll.user32.SystemParametersInfoW(20,0,path,0)
            time.sleep(0.02)
        except:
            pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
    finally:
        pygame.quit()
