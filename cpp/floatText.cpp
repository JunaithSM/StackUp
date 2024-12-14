#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <string>
#include <vector>
#include "text.cpp"
class FloatText{
    public:
    double x,y;
    int width,height;
    string txt = " ";
        FloatText(string text,double X ,double Y, int w, int h){
            x=X,y=Y,width = w,height=h;
            txt = text;
        }
        void Draw(SDL_Renderer*render){
            NewText(render,txt,x,y,)
        }
};
