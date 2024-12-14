import pygame,math,random,time
storageFile = "stackBox.csv"
pygame.init()
RunGame = True
device = pygame.display.Info()
screen = pygame.display.set_mode((device.current_w,device.current_h))
clock = pygame.time.Clock()
fontFamily = '../Grandstander/static/Grandstander-Medium.ttf'
running  = True
dt = 0
first_block = True
#gradiant code
def gradientRect( window, left_colour, right_colour, target_rect ):
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )  
#blocks
class Game:
    width = 500
    height = device.current_h
    x= device.current_w*0.5-width*0.5
    y = 0
class coords:
    x =0
    y =0
    width =10
    height = 10
    
class Coners:
    def __init__(self):
        self.top =coords()
        self.bottom =coords()
        self.left =coords()
        self.right =coords()
class Float_Text:
    def __init__(self,text):
        self.y = device.current_h/2
        self.opacity = 1
        self.text = text
    
    def draw(self):
        color = pygame.Color(1)
        color.hsla = 2,100,50,100
        font = pygame.font.Font(fontFamily,80)
        text = font.render(self.text,True,(0,0,0))
        textRect = text.get_rect()
        textRect.centerx =device.current_w//2
        textRect.top = self.y
        text = text.convert_alpha()
        text.fill((255, 255, 255, int(self.opacity*255)), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(text,textRect)
    
    def update(self):
        self.y-=1
        self.opacity-=0.005
float_texts = []
def create_text (text):
    float_texts.append(Float_Text(text))
def handle_text ():
    for txt in float_texts:
        txt.draw()
        txt.update()
        if(txt.opacity <= 0):
            float_texts.remove(txt)
class times:
    start = 0
    end = 0
class Blocks:
    start_msg = True;msg = 'Click to start\nor\nPress "Space Bar"\n';start= True;x = device.current_w/2;y = device.current_h-250;dirX = -1 if math.floor(random.random()*2) else 1;dirY =  -1 if math.floor(random.random()*2) else 1;hsl = 60;width = 200;height = 200;speed = 0.2;score = 0;timer = "00:00";highscore = 0;time = times()
    def __init__(self):
        self.hsl = Blocks.hsl
        self.x = Blocks.x
        self.y = Blocks.y
        self.dirX = Blocks.dirX
        self.dirY = Blocks.dirY
        self.run = True
        self.width = Blocks.width
        self.height = Blocks.height
        self.length = 50
        self.speed = Blocks.speed
        self.coner= Coners()
        global first_block
        if(not first_block):
            self.update(-(Game.width)*Game.width/Game.height)
        else:
            first_block = False
            Blocks.y-=self.length*2
        
    def draw(self):
        x = self.x; y = self.y;angle = 30
        color = pygame.Color(0)
        color.hsla=(self.hsl,100,50,100)
        polygon = []
        self.coner.top.x = x-5
        self.coner.top.y = y-5
        polygon.append([x,y])
        (x,y) = self.rotateLine(x,y,angle,self.width)
        polygon.append([x,y])
        angle+=120
        (x,y) = self.rotateLine(x,y,angle,self.height)
        polygon.append([x,y])
        angle+=60
        (x,y) = self.rotateLine(x,y,angle,self.width)
        polygon.append([x,y])
        angle+=120
        (x,y) = self.rotateLine(x,y,angle,self.height)
        polygon.append([x,y])
        pygame.draw.polygon(screen,color ,polygon)
        polygon = []
        color.hsla = (self.hsl,100,40,100)
        angle -=180
        (x,y) = self.rotateLine(x,y,angle,self.height)
        polygon.append([x,y])
        angle-=120
        (x,y) = self.rotateLine(x,y,angle,self.width)
        polygon.append([x,y])
        angle+=60
        (x,y) = self.rotateLine(x,y,angle,self.length)
        polygon.append([x,y])
        angle+=120
        (x,y) = self.rotateLine(x,y,angle,self.width)
        self.coner.left.x = x-5
        self.coner.left.y = y-5
        polygon.append([x,y])
        angle+=60
        (x,y) = self.rotateLine(x,y,angle,self.length)
        polygon.append([x,y])
        pygame.draw.polygon(screen,color ,polygon)
        color.hsla = (self.hsl,100,70,100)
        polygon = []
        angle -=240
        (x,y) = self.rotateLine(x,y,angle,self.width)
        polygon.append([x,y])
        angle-=60
        (x,y) = self.rotateLine(x,y,angle,self.height)
        polygon.append([x,y])
        angle+=120
        (x,y) = self.rotateLine(x,y,angle,self.length)
        self.coner.right.x = x-5
        self.coner.right.y = y-5
        polygon.append([x,y])
        angle+=60
        (x,y) = self.rotateLine(x,y,angle,self.height)
        self.coner.bottom.x = x-5
        self.coner.bottom.y = y-5
        polygon.append([x,y])
        angle+=120
        (x,y) = self.rotateLine(x,y,angle,self.length)
        polygon.append([x,y])
        pygame.draw.polygon(screen,color ,polygon)
        
    def rotateLine( self,x,y,angle,len):
        rotate= angle *math.pi/180
        x+=len*math.cos(rotate)
        y+=len*math.sin(rotate)
        return (x,y)
    
    def update(self,pos = 1):
        if (self.run) :
            if(self.coner.right.x > Game.x+Game.width and pos == 1):
                self.dirX=-1 if (self.dirX==self.dirY) else 1;self.dirY=-1
            if(self.coner.left.x <Game.x and pos==1):
                self.dirX=1 if (self.dirX==self.dirY) else -1;self.dirY=1
            rotate =30 if (self.dirY == 1) else 150
            angle =self.dirX*rotate
            self.x+=math.cos(math.radians(angle))*pos*self.speed
            self.y+=math.sin(math.radians(angle))*pos*self.speed    
    def stop(self):
        self.speed = 0
        if self.run: 
            Blocks.y+=self.length
        self.run = False
        if(Blocks.y <= 200):
            self.y+=self.length
    def changeSize(self,b):
        if(math.floor(self.x) == math.floor(b.x) or math.floor(self.y) ==math.floor(b.y)):
            if(Blocks.score):
                create_text("PERFECT")
        Blocks.score += (5 if (math.floor(self.x) == math.floor(b.x) or math.floor(self.y) == math.floor(b.y)) else 1)
        if(b.coner.top.x < self.coner.top.x and b.coner.right.x < self.coner.right.x and self.dirX!=self.dirY):
            self.height -= abs(math.floor(self.x)-b.x)
            self.x =b.x
            self.y = b.y-self.length
            Blocks.height = self.height
        
        if(b.coner.top.x > self.coner.top.x and b.coner.right.x > self.coner.right.x and self.dirX!=self.dirY):
            self.height -= abs(math.floor(self.x)-b.x)
            self.draw()
            b.draw()
            dx = abs(self.x - self.coner.left.x)
            dx1 = abs(b.x - b.coner.left.x)
            self.x = b.x-(dx1-dx)
            self.draw()
            b.draw()
            dx2 = abs(b.coner.left.y - self.coner.left.y)
            self.y+=dx2-self.length
            Blocks.height = self.height
         
        if(b.coner.top.x > self.coner.top.x and b.coner.right.x > self.coner.right.x and self.dirX==self.dirY):
            self.width -= abs(math.floor(self.x)-b.x)
            self.x =b.x
            self.y = b.y-self.length
            Blocks.width = self.width
        
        if(b.coner.top.x < self.coner.top.x and b.coner.right.x < self.coner.right.x and self.dirX==self.dirY):
            self.width -= abs(math.floor(self.x)-b.x)
            self.draw()
            b.draw()
            dx = abs(self.x - self.coner.right.x)
            dx1 = abs(b.x - b.coner.right.x)
            self.x = b.x+abs(dx1-dx)
            Blocks.width = self.width
            self.draw()
            b.draw()
            dx2 = abs(b.coner.right.y - self.coner.right.y)
            self.y+=dx2-self.length  
        Blocks.x = self.x
        Blocks.y = self.y-self.length
        global RunGame
        if(self.height <= 0 or self.width <= 0 and RunGame):
            Blocks.speed = 0
            Blocks.msg= "Click to Restart\n"
            create_text("Game Over")
            RunGame = False
        
with open(storageFile,"r") as file:
    reader = file.read()
    Blocks.highscore = int(reader)
    
            
blocks = []
def create_blocks():
    Blocks.dirX = -1 if math.floor(random.random()*2) else 1
    Blocks.dirY = -1 if math.floor(random.random()*2) else 1
    blocks.append(Blocks())

def handle_blocks():
    for block in blocks:
        block.draw()
        block.update()
        if(block.height <= 0 or block.width <=0):
            blocks.remove(block)
        
#click
def blocks_stop ():
    for block in blocks :
        block.stop()
    if(blocks[len(blocks)-2] and blocks[len(blocks)-1]):
        blocks[len(blocks)-1].changeSize(blocks[len(blocks)-2]) 
create_blocks()
blocks_stop()
Blocks.score = 0
create_blocks()
def onClick():
    global blocks,first_block,RunGame
    if(not RunGame):
        RunGame=True
        blocks = []
        first_block = False
        Blocks.speed = 0.2
        Blocks.score = 0
        Blocks.start = True
        Blocks.start_msg = True
        Blocks.width = 200
        Blocks.height = 200
        Blocks.x=device.current_w/2
        Blocks.y=Game.height-250
        Blocks.hsl = 60
        create_blocks()
        blocks_stop()
        Blocks.score = 0
        create_blocks()
        return

    Blocks.hsl+=1
    Blocks.speed+=0.0005
    blocks_stop()
    if(Blocks.height > 0 or Blocks.width > 0):
        if(RunGame):
            create_blocks()
    msg = ["Nice","Cool","Good","Wow","Super"]
    if(Blocks.start):
        Blocks.time.start = int(time.time())
        Blocks.start=False
    if(Blocks.score%25 == 0):
        create_text(msg[math.floor(random.random()*len(msg))])
    if(int(Blocks.highscore) < Blocks.score):
        Blocks.show_msg = False
        Blocks.highscore = Blocks.score
        if(Blocks.show_msg):
            create_text("New Score")
        
     
     
#animation

def log(msg):
    word = ""
    h = 0
    for i in msg:
        if i == "\n" or i == msg[len(msg)-1]:
            font = pygame.font.Font(fontFamily,30)
            text = font.render(str(word), True,(51,51,51))
            textRect = text.get_rect()
            textRect.center=device.current_w//2,device.current_h//2
            textRect.top += h
            h+=30
            word = ""
            screen.blit(text, textRect)
            continue
        word+=i
def score_num():
    font = pygame.font.Font(fontFamily,80)
    text = font.render(str(Blocks.score), True,(51,51,51))
    textRect = text.get_rect()
    textRect.centerx =device.current_w//2
    textRect.top = 20
    screen.blit(text, textRect)
def highscore():
    font = pygame.font.Font(fontFamily,15)
    text = font.render("HighScore: "+str(Blocks.highscore), True,(51,51,51))
    textRect = text.get_rect()
    textRect.top = 10
    textRect.left = 10
    screen.blit(text, textRect)
def speed():
    font = pygame.font.Font(fontFamily,15)
    text = font.render("Speed: "+str(math.floor((Blocks.speed/0.2)*10)/10)+"x", True,"black")
    textRect = text.get_rect()
    textRect.top = 10
    textRect.right = 10
    textRect.left = device.current_w-120
    screen.blit(text, textRect)
def scoretext():
    font = pygame.font.Font(fontFamily,15)
    text = font.render("Score", True,(51,51,51))
    textRect = text.get_rect()
    textRect.top = 90
    textRect.centerx =device.current_w//2
    screen.blit(text, textRect)
def timer():
    font = pygame.font.Font(fontFamily,15)
    text = font.render(str(Blocks.timer), True,(51,51,51))
    textRect = text.get_rect()
    textRect.top = 120
    textRect.centerx =device.current_w//2
    screen.blit(text, textRect)
def showFPS(fps):
    font = pygame.font.Font(fontFamily,15)
    text = font.render("FPS: "+str(fps), True,(51,51,51))
    textRect = text.get_rect()
    textRect.top = 50
    textRect.left = 10
    screen.blit(text, textRect)
def setTimer ():
    if(Blocks.time.start and RunGame):
        Blocks.time.end = int(time.time())
        sec = math.floor((Blocks.time.end - Blocks.time.start))
        min = math.floor(sec/60)
        txtsec = str(sec % 60);txtmin = str(min)
        if(sec%60 < 10):
            txtsec= "0"+str(sec%60)
        if(min<10):
            txtmin= "0"+str(min)
        Blocks.timer = txtmin+":"+txtsec
frame = 0
start_time = int(time.time())
frame_txt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                Blocks.msg = ""
                onClick() 
                break
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                Blocks.msg = ""
                onClick() 
                break
        elif event.type == pygame.FINGERDOWN:
            Blocks.msg = ""
            onClick() 
            break
    screen.fill("black")
    gradientRect( screen, "skyblue", "lightblue", pygame.Rect( 0,0, device.current_w,device.current_h ) )
    handle_blocks()
    handle_text()
    score_num()
    highscore()
    scoretext()
    if(Blocks.speed):
        speed()
    setTimer()
    timer()
    log(Blocks.msg)
    if int(time.time()) - start_time >= 1.0:
        start_time = int(time.time())
        frame_txt = frame
        frame = 0
    frame+=1
    showFPS(frame_txt)
    pygame.display.flip()
   
pygame.QUIT
with open(storageFile,"w") as file:
    write = file.write(str(Blocks.highscore))