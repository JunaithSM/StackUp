#include <iostream>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include "game.cpp"  // Your game logic
#include <string>
#include <ctime>
#include "text.cpp"
#include <fstream>
using namespace std;

int WIDTH = 1000, HEIGHT = 500;
bool RUNNING = true;
SDL_Renderer* render = NULL;
SDL_Window* window = NULL;

void StartWindow() {
    SDL_DisplayMode DM;
    SDL_GetCurrentDisplayMode(0, &DM);
    WIDTH = DM.w;
    HEIGHT = DM.h;
    SetGameScreen(DM.w, DM.h);
}

void SetBackground(SDL_Renderer* renderer) {
    SDL_Color topColor = {135, 206, 235, 255};  // Blue
    SDL_Color bottomColor = {173, 216, 230, 255};
    for (int y = 0; y < HEIGHT; ++y) {
        float t = static_cast<float>(y) / HEIGHT;
        Uint8 r = static_cast<Uint8>((1 - t) * topColor.r + t * bottomColor.r);
        Uint8 g = static_cast<Uint8>((1 - t) * topColor.g + t * bottomColor.g);
        Uint8 b = static_cast<Uint8>((1 - t) * topColor.b + t * bottomColor.b);
        SDL_SetRenderDrawColor(renderer, r, g, b, SDL_ALPHA_OPAQUE);
        SDL_RenderDrawLine(renderer, 0, y, WIDTH, y);
    }
}

void CloseWindow() {
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(render);
    TTF_CloseFont(font);
    TTF_Quit();
    SDL_Quit();
}

void HandleText(SDL_Renderer* renderer){
    SDL_Color color = {51,51,51,255};
    string score_num = to_string(Block.score);
    NewText(renderer,score_num,WIDTH/2,20,color,80,"center");
    NewText(renderer,"Score",WIDTH/2,90,color,15,"center");
    if(RunGame){SetTimer();}
    NewText(renderer,Block.timer,WIDTH/2,120,color,15,"center");
    
    int speed = ((floor((Block.speed/0.2)*10)/10 )*100);
    NewText(renderer,"Speed: "+to_string(speed/100),WIDTH-10,10,color,15,"last");
    if(Block.highscore < Block.score){
        Block.show_msg = false;
        Block.highscore = Block.score;
        
        if(Block.show_msg){
       // create_text("New Score")
        }
     }
    NewText(renderer,"HighScore: "+to_string(Block.highscore),10,10,color,15);
}
void Animation(SDL_Renderer* renderer) {
    SDL_RenderClear(renderer);
    SetBackground(renderer);
    HandelBlocks(renderer);
    HandleText(renderer);
    SDL_RenderPresent(renderer);
}
void OnClick(SDL_Renderer* renderer){
    BlockStop(renderer);
    CreateBlocks();
    if(Block.start){
    Block.time.start = time(NULL);
    Block.start = false;}
    Block.speed+=0.0005;
}
void HandleEvents(SDL_Renderer* renderer) {
    SDL_Event event;
    if (SDL_PollEvent(&event)) {
        if (event.type == SDL_QUIT) {
            RUNNING = false;
        } else if (event.type == SDL_KEYDOWN) {
            if (event.key.keysym.sym == SDLK_ESCAPE) {
                RUNNING = false;
            } else if (event.key.keysym.sym == SDLK_SPACE) {
                OnClick(renderer);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    SDL_Init(SDL_INIT_EVERYTHING);
    if (!InitTTF("../Grandstander/static/Grandstander-Medium.ttf", 24)) {
        return -1;
    }
    StartWindow();
    fstream file("game.txt");
    string word;
    if(file){
        file.open("game.txt");
        while (getline (file,word)) {
            Block.highscore = stoi(word);
        }
    }
        file.close();
    window = SDL_CreateWindow("Stack Up", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WIDTH, HEIGHT, SDL_WINDOW_ALLOW_HIGHDPI);
    render = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (window == NULL) {
        cout << "Could not create window " << SDL_GetError() << endl;
        return 1;
    }
    CreateBlocks();
    BlockStop(render);
    CreateBlocks();
    while (RUNNING) {
        HandleEvents(render);
        Animation(render);
    }
    CloseWindow();
    file.open("game.txt");
    file << to_string(Block.highscore);
    file.close();
    
    for (Blocks* block : blocks) {
        delete block;
    }
    return EXIT_SUCCESS;
}
