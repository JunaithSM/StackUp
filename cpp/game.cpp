#include <random>
#include <iostream>
#include <SDL2/SDL.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include "hsltorgb.cpp"
#include <ctime>
#include <string>
using namespace std;
bool RunGame = true;
int random(int min = 0,int max = 2){
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(min, max);
    return dist(gen);
}
bool first_block = true;

struct Block{
    double x = 0,y =0, height= 200,width = 200;
    int hsl = 60;
    long double speed = 0.2;
    int dirX = -1,dirY = -1;
    int score = 0,highscore = 0;
    bool show_msg = true;
    struct time{
        int start = 0,end = 0;
    }time;
    string timer="00:00";
    bool start = true;
}Block;
void SetTimer (){
    if(Block.time.start){
    Block.time.end = time(NULL);
    int timer = (Block.time.end - Block.time.start);
    int sec = floor(Block.time.end - Block.time.start);
    
    int min = floor(sec/60);
    string txtsec= to_string(sec%60),txtmin = to_string(min);
    if(sec%60 < 10){
        txtsec= "0"+to_string(sec%60);
    }
    if(min<10){
        txtmin= "0"+to_string(min);
    }
    Block.timer = txtmin+":"+txtsec;
    }
}
struct Game{
    int width = 500,height;double x,y = 0;
}Game;

void SetGameScreen(int width, int height){
    Game.height = height,Game.x = width /2 - Game.width*0.5,Block.y = height-250;
}

class Blocks{
    private:
        double hsl = Block.hsl;
        struct Point{double x ,y;};
        vector<Point> vertices = {};
        void createPolygon(SDL_Renderer * render,double l = 0.5){
            int numVertices = vertices.size();
            SDL_Vertex sdlVertices[numVertices];
            int r,g,b;
            HSL data = HSL(hsl, 1.0f, l);
            RGB value = HSLToRGB(data);
            SDL_Color color = {static_cast<Uint8>(value.R),static_cast<Uint8>(value.G),static_cast<Uint8>(value.B), 255}; // Red color
            for (int i = 0; i < numVertices; ++i) {
                sdlVertices[i].position.x = vertices[i].x;
                sdlVertices[i].position.y = vertices[i].y;
                sdlVertices[i].color = color;
                sdlVertices[i].tex_coord.x = 0.0f;
                sdlVertices[i].tex_coord.y = 0.0f;
            }
            // Indices to form the triangles
            int numIndices = (numVertices - 2) * 3;
            int indices[numIndices];
            for (int i = 0, j = 1; i < numIndices; i += 3, ++j) {
                indices[i] = 0;
                indices[i + 1] = j;
                indices[i + 2] = j + 1;
            }
            SDL_RenderGeometry(render, nullptr, sdlVertices, numVertices, indices, numIndices);

        }
        void rotate(double& x,double& y,int angle, double len){
            double rotate= angle *M_PI/180;
            x+=len*cos(rotate);
            y+=len*sin(rotate);
            vertices.push_back({x,y});
        }
    public:
        long double x = Game.x+Game.width/2,y;
        int 
        dirX = Block.dirX,dirY = Block.dirY,length = 50;
        double width ,height;
        long double speed = Block.speed;
        struct coner{
            struct pos{
                double x =0,y=0;
            }top,left,right,bottom;
        }coner;
        bool run = true;
        //Draw Image
        void Draw(SDL_Renderer * render){
            if((height <= 0 || width <= 0)){
                width = 0;
                height = 0;
                Block.width =0;
                Block.height = 0;
            }
            double X= x,Y =y;
            coner.top.x = X;
            coner.top.y = Y;
            vertices.push_back({X,Y});
            int angle = 30;
            rotate(X,Y,angle,width);
            angle+=120;
            rotate(X,Y,angle,height);
            angle+=60;
            rotate(X,Y,angle,width);
            angle+=120;
            rotate(X,Y,angle,height);
            createPolygon(render);
            vertices.clear();
            angle-=180;
            rotate(X,Y,angle,height);
            angle-=120;
            rotate(X,Y,angle,width);
            angle+=60;
            rotate(X,Y,angle,length);
            angle+=120;
            rotate(X,Y,angle,width);
            coner.left.x = X;
            coner.left.y = Y;
            angle+=60;
            rotate(X,Y,angle,length);
            createPolygon(render,0.4); 
            vertices.clear();
            angle-=240;
            rotate(X,Y,angle,width);
            angle-=60;
            rotate(X,Y,angle,height);
            angle+=120;
            rotate(X,Y,angle,length);
            coner.right.x = X;
            coner.right.y = Y;
            angle+=60;
            rotate(X,Y,angle,height);
            coner.bottom.x = x-5;
            coner.bottom.y = y-5;
            angle+=120;
            rotate(X,Y,angle,length);
            createPolygon(render,0.7); 
            vertices.clear();
        }

         void ChangeSize(Blocks* block,SDL_Renderer* render){
            if(!block || !RunGame)return;
            Block.score += (floor(x) == floor(block->x) || floor(y) ==floor(block->y))?5:1;
           
           // if(floor(x) == floor(block->x) || floor(y) ==floor(block->y)){//create_text("PERFECT");}
            if(block->coner.top.x < coner.top.x &&block->coner.right.x < coner.right.x && dirX!=dirY){
            
                height -= abs(floor(x)-block->x);
                x =block->x;
                y = block->y-length;
                Block.height = height;
            }
            if(block->coner.top.x > coner.top.x &&block->coner.right.x > coner.right.x &&dirX!=dirY){
                height -= abs(floor(x)-block->x);
                
                Block.height = height;
                Draw(render);
                block->Draw(render);
                double dx = abs(x - coner.left.x);
                double dx1 = abs(block->x - block->coner.left.x);
                x = block->x-(dx1-dx);
                Draw(render);
                block->Draw(render);
                double dx2 = abs(block->coner.left.y - coner.left.y);
                y+=dx2-length;
            } 
            if(block->coner.top.x > coner.top.x &&block->coner.right.x > coner.right.x &&dirX==dirY){
                width -= abs(floor(x)-block->x);
                x =block->x;
                y = block->y-length;
                Block.width = width;
            }
            if(block->coner.top.x < coner.top.x &&block->coner.right.x < coner.right.x &&dirX==dirY){
                width -= abs(floor(x)-block->x);
                
                Block.width = width;
                Draw(render);
                block->Draw(render);
                double dx = abs(x - coner.right.x);
                double dx1 = abs(block->x - block->coner.right.x);
                x = block->x+abs(dx1-dx);
                Draw(render);
                block->Draw(render);
                double dx2 = abs(block->coner.right.y - coner.right.y);
                y+=dx2-length;
            } 
            Block.x = x;
            Block.y = y-length;
             if(height <= 0 || width <= 0){
                Block.speed = 0;
               // messages.style.display = "block";
                //messages.innerText = "Click to Restart";
               // create_text("Game Over");
                RunGame = false;
            } 
            
        }
        void Update(double pos = 1){
            if(run){
                if(pos ==1){
                    if(coner.right.x >= Game.x + Game.width){
                        dirX=(dirX==dirY)?-1:1,dirY=-1;
                    }
                    if(coner.left.x <=Game.x){
                        dirX=(dirX==dirY)?1:-1,dirY=1;
                    }
                }
                int rotate = (dirY == 1)?30:150;
                double angle =dirX*rotate*M_PI/180;
                x+=cos(angle)*pos*speed;
                y+=sin(angle)*pos*speed;  
            }
        }
        Blocks(){
            width = Block.width,height = Block.height;
            y = Block.y;
            if(!first_block){
                x = Game.x+Game.width/2;
                Update(-200);
                first_block = false;
            }else{
                first_block = false;
            } 
            
        }
        void stop(){
            speed = 0;
            if(run && Block.y>=200){ Block.y-=length;
            }else if(Block.y <= 200){
                y+=length;
            }
            run = false;

        }
};
vector<Blocks*> blocks;

void CreateBlocks(){
    Block.dirX = random()==0?-1:1,Block.dirY = random()==0?-1:1;
    Blocks* block = new Blocks();
    blocks.push_back(block);
    Block.hsl++;
}
void BlockStop (SDL_Renderer* render){
    for (Blocks* block : blocks) {
        block->stop();
    }
    
    if (blocks.size() >= 2) {
        blocks.back()->ChangeSize(blocks[blocks.size() - 2], render);
    }

}
void HandelBlocks(SDL_Renderer * render){
     for (Blocks* block : blocks) {
       // system("clear");
       //cout<<"starts\n\n\n";
        block->Draw(render);
        block->Update();
        
    }
}