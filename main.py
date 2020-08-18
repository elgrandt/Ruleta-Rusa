__author__ = 'Dylan'
import pygame,pygame.gfxdraw
import math,random,Tkinter,copy,time

PI = math.pi
CENTER = -1

class Roulette:
    def __init__(self,radius,cfg):
        self.angle = 0
        self.r = radius
        self.d = 2*self.r
        self.divs = cfg["Options count"]
        self.font = pygame.font.Font("Chiller.ttf",90)
        self.rotating = False
        self.desrotating = False
        self.enabled_border = cfg["Enabled border"]
        self.colors = cfg["Colours"]
        self.initial_rotation_speed = cfg["Speed"]
        self.rotation_speed = self.initial_rotation_speed
        self.download_speed = cfg["Download speed"]
        self.points = []
        self.texts = [self.font.render(cfg["Textos"][0],1,(255,255,0)),self.font.render(cfg["Textos"][1],1,(0,0,255)),self.font.render(cfg["Textos"][2],1,(0,0,255))]
        self.img = pygame.transform.scale(pygame.image.load("OBLEA.png"),(int(self.d/4),int(self.d/4)))
        self.image_corners = pygame.transform.scale(pygame.image.load("oblea de pablo burgos.png"),(pygame.display.get_surface().get_size()[0]/6,pygame.display.get_surface().get_size()[1]/6))
        self.winner_texts = cfg["Textos-Ganador"]
        self.text_to_put = ""
        self.conclution_text_time = time.time()
        self.GenerateSurface()
    def GenerateSurface(self):
        self.surface = pygame.Surface((2*self.r+8, 2*self.r+8), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        scale = 0
        points = []
        cant = 0
        count = 20*self.divs
        pts = []
        x = 0
        angles = []
        while True:
            n = (2*PI)/count*x # regula n desde 0 a 2PI, en 100 partes iguales
            sc = ((2*PI)/self.divs)*scale
            if scale < self.divs/2:
                X = math.sin(n+sc)
                Y = math.cos(n+sc)
            else:
                X = math.sin(n+sc)
                Y = math.cos(n+sc)
            points.append([self.r + 4 + X * self.r, self.r + 4 + Y * self.r])
            if x > count/self.divs:
                angles.append(n+sc)
                pts.append(points[len(points)-1])
                points.append([self.r,self.r])
                pygame.gfxdraw.filled_polygon(self.surface,points,self.colors[cant])
                x = 0
                points = []
                scale += 1
                cant += 1
                if cant == self.divs:
                    break
            x += 1
        self.points = pts
        if self.enabled_border:
            for x in range(len(pts)):
                pygame.gfxdraw.line(self.surface,int(self.r),int(self.r),int(pts[x][0]), int(pts[x][1]), (0,0,0))
                pygame.gfxdraw.filled_circle(self.surface,int(pts[x][0]),int(pts[x][1]),4,(0,0,0))
            pygame.draw.circle(self.surface,(0,0,0),[int(self.r+4),int(self.r+4)],int(self.r),1)
        self.surface.blit(self.img,(self.surface.get_size()[0]/2 - self.img.get_size()[0]/2, self.surface.get_size()[1]/2 - self.img.get_size()[1]/2))
        self.original_size = self.surface.get_size()
    def Rotate(self,speed):
        self.angle += speed
        if self.angle >= 360:
            self.angle -= 360
    def PressedEnter(self):
        self.text_to_put = ""
        if self.rotating:
            self.desrotating = True
        else:
            self.rotating = True
    def BlitCornersImages(self,screen):
        X,Y = screen.get_size()
        SX,SY = self.image_corners.get_size()
        positions = [
            [0,0],
            [0,Y-SY],
            [X-SX,0],
            [X-SX,Y-SY]
        ]
        for x in range(4):
            screen.blit(self.image_corners,positions[x])
    def Update(self,surf,position):
        self.BlitCornersImages(surf)
        if self.rotating:
            self.Rotate(self.rotation_speed)
            if self.desrotating:
                self.rotation_speed -= self.download_speed
                if self.rotation_speed <= 0:
                    self.rotation_speed = self.initial_rotation_speed
                    self.rotating = False
                    self.desrotating = False
                    color_pos = 10 + int(self.angle/(360/self.divs))
                    colors2 = copy.copy(self.colors)
                    colors2.reverse()
                    if color_pos < len(colors2):
                        indice = color_pos
                    else:
                        indice = color_pos-len(colors2)
                    self.text_to_put = self.winner_texts[indice % len(self.winner_texts)]
                    self.conclution_text_time = time.time()

        rotated = pygame.transform.rotate(self.surface,self.angle)
        if position == CENTER:
            position = surf.get_size()[0]/2-rotated.get_size()[0]/2,surf.get_size()[1]/2-rotated.get_size()[1]/2
        surf.blit(rotated,position)
        if not self.rotating:
            if self.text_to_put == "":
                text = self.texts[0]
            else:
                text = self.font.render(self.text_to_put,1,(255,255,0))
                if time.time() - self.conclution_text_time >= 10:
                    self.text_to_put = ""
        elif self.desrotating:
            text = self.texts[1]
        else:
            text = self.texts[2]
        surf.blit(text,(surf.get_size()[0]/2-text.get_size()[0]/2,10))
        midx = surf.get_size()[0]/2
        pos = surf.get_size()[0]/2-self.original_size[0]/2,surf.get_size()[1]/2-self.original_size[1]/2
        final_pos = [midx,pos[1]+25]
        pygame.gfxdraw.filled_trigon(surf,midx-5,pos[1]-8,midx+5,pos[1]-8,final_pos[0],final_pos[1],(255,0,255))

def main():
    prueba = False
    pygame.init()
    root = Tkinter.Tk()
    pygame.display.set_caption("Ruleta rusa")
    if not prueba:
        res = (root.winfo_screenwidth(),root.winfo_screenheight())
        surface = pygame.display.set_mode(res,pygame.FULLSCREEN)
    else:
        res = (1024,720)
        surface = pygame.display.set_mode(res)
    config = eval(open("data.cfg").read())
    roulette = Roulette(surface.get_size()[1]/config["Radius scale"],config)
    finished = False
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load("Background.jpg"),res)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    roulette.PressedEnter()
                elif event.key == pygame.K_ESCAPE:
                    finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pygame.mouse.get_pressed()[0]):
                    roulette.PressedEnter()
        surface.blit(background,(0,0))
        roulette.Update(surface,CENTER)
        pygame.display.update()
        clock.tick(30)

main()
