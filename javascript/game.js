/**@type {HTMLCanvasElement} */
const score_num= document.getElementById("score_num")
const timer= document.getElementById("timer")
const highscore= document.getElementById("highscore")
const speed= document.getElementById("speed")
const messages= document.getElementById("msg")
const FPS = document.getElementById("fps")
///////////////////
let frame = 0;
let start_time = new Date().getTime();
const c = document.getElementById("game");
const ctx = c.getContext("2d");
c.width = 500;c.height = window.innerHeight;
let first_block = true
const abs =x=>x>=0?x:-x
const Block = {
    x:c.width/2,
    y:c.height-250,
    width:200,
    height:200,speed:0.2,
    score:0,start:false,
    time:{
        start:0,
        end:0
    },
    highscore:localStorage.getItem("highscore")||0,
    show_msg:true
}

let RunGame = true;
class Float_Text{
    constructor(text){
        this.x = c.width/2;
        this.y = c.height/2
        this.opacity = 1
        this.text = text
    }
    draw(){
        ctx.beginPath();
        ctx.fillStyle =`rgba(0,0,0,${this.opacity})`
        ctx.textAlign = "center";
        ctx.font = '80px "Grandstander"'
        ctx.fillText(this.text,this.x,this.y,)
        ctx.fill()
        ctx.closePath();
    }
    update(){
        this.y--
        this.opacity-=0.005;

    }
}
let float_texts = []
const create_text= (text)=>{
    float_texts.push(new Float_Text(text))
}
const handle_text = ()=>{
    for (let i = 0; i < float_texts.length; i++) {
        const txt = float_texts[i];
        txt.draw();
        txt.update()
        if(txt.opacity <= 0){
            float_texts.splice(i,1);
            i--;
        }
    }
}
class Blocks{
    constructor(x,y,color){
        this.hsl = color;
        this.x = Block.x
        this.y = Block.y 
        const portrait = c.width/c.height,lanscape = c.height/c.width;
        this.coner = {
            top:{
                x:0,y:0,s:10
            },
            bottom:{
                x:0,y:0,s:10
            },
            left:{
                x:0,y:0,s:10
            },
            right:{
                x:0,y:0,s:10
            }
        }
        
        this.run = true  
        this.dirX = x,this.dirY =y
        // 
        this.width = Block.width;
        this.height = Block.height;
        this.color = color
        this.length = 50;
      
        this.speed = Math.floor(Block.speed*10)/10;
        if(!first_block){
            this.update(-c.width*portrait)
            first_block = false
            
        }else{
            Block.y-=this.length*2
            first_block = false
        } 
    }
    draw(){
        let x = this.x, y = this.y,getXY,angle = 30

        ///
        ctx.beginPath();
        ctx.fillStyle=`hsl(${this.hsl},100%,50%)`
        this.coner.top.x = x-5;
        this.coner.top.y = y-5
        ctx.moveTo(x,y);
        getXY = this.rotateLine(x,y,angle,this.width);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        angle+=120
        getXY = this.rotateLine(x,y,angle,this.height);x=getXY[0],y=getXY[1]
        
        ctx.lineTo(x,y);
        angle+=60
        getXY = this.rotateLine(x,y,angle,this.width);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        angle+=120
        getXY = this.rotateLine(x,y,angle,this.height);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        ctx.fill()
        ctx.closePath();
        /////
         
        ////////////
        ctx.beginPath();
        
        angle-=180
        getXY = this.rotateLine(x,y,angle,this.height);x=getXY[0],y=getXY[1]
        ctx.fillStyle = `hsl(${this.hsl},100%,40%)`
        ctx.moveTo(x,y);
        angle-=120
        getXY = this.rotateLine(x,y,angle,this.width);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        angle+=60
        getXY = this.rotateLine(x,y,angle,this.length);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        angle+=120
        getXY = this.rotateLine(x,y,angle,this.width);x=getXY[0],y=getXY[1]
        this.coner.left.x = x-5;
        this.coner.left.y = y-5
        ctx.lineTo(x,y);
        angle+=60
        getXY = this.rotateLine(x,y,angle,this.length);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        ctx.fill()
        ctx.closePath();
        /////////////////
        ctx.beginPath();
        ctx.fillStyle =`hsl(${this.hsl},100%,70%)`
        angle-=240
        getXY = this.rotateLine(x,y,angle,this.width);x=getXY[0],y=getXY[1]
        ctx.moveTo(x,y)
        angle-=60
        getXY = this.rotateLine(x,y,angle,this.height);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        angle+=120
        getXY = this.rotateLine(x,y,angle,this.length);x=getXY[0],y=getXY[1]
        
        this.coner.right.x = x-5;
        this.coner.right.y = y-5
        ctx.lineTo(x,y);
        angle+=60
        getXY = this.rotateLine(x,y,angle,this.height);x=getXY[0],y=getXY[1]
        this.coner.bottom.x = x-5;
        this.coner.bottom.y = y-5
        ctx.lineTo(x,y);
        angle+=120
        getXY = this.rotateLine(x,y,angle,this.length);x=getXY[0],y=getXY[1]
        ctx.lineTo(x,y);
        ctx.fill()
        ctx.closePath();
    }

    rotateLine(x,y,angle,len){
        let rotate= angle *Math.PI/180
        x+=len*Math.cos(rotate);
        y+=len*Math.sin(rotate);
        return [x,y]
    }
    update(pos = 1){
        if (this.run) {
            if(this.coner.right.x >c.width ){
                this.dirX=(this.dirX==this.dirY)?-1:1,this.dirY=-1
            }
            if(this.coner.left.x <0){
                this.dirX=(this.dirX==this.dirY)?1:-1,this.dirY=1
            }
            let rotate = (this.dirY == 1)?30:150
            let angle =this.dirX*rotate*Math.PI/180
            this.x+=Math.cos(angle)*pos*this.speed
            this.y+=Math.sin(angle)*pos*this.speed    
          
        }    
    }
    stop(){
        this.speed = 0
        if(this.run){ Block.y+=this.length}
        this.run = false
        if(Block.y <= 200){
            this.y+=this.length
        }
       
    }
    changeSize(b){
        Block.score += ((Math.floor(this.x) == Math.floor(b.x) || Math.floor(this.y) ==Math.floor(b.y))?5:1)
        //console.log(Math.floor(this.x) ,Math.floor(b.x) ,Math.floor(this.y) ,Math.floor(b.y));
        if(Math.floor(this.x) == Math.floor(b.x) || Math.floor(this.y) ==Math.floor(b.y)){create_text("PERFECT")}
        if(b.coner.top.x < this.coner.top.x &&b.coner.right.x < this.coner.right.x &&this.dirX!=this.dirY){
            this.height -= abs(Math.floor(this.x)-b.x)
            this.x =b.x;
            this.y = b.y-this.length
            Block.height = this.height
        }
        if(b.coner.top.x > this.coner.top.x &&b.coner.right.x > this.coner.right.x &&this.dirX!=this.dirY){
            this.height -= abs(Math.floor(this.x)-b.x)
            this.draw();
            b.draw();
            let dx = abs(this.x - this.coner.left.x)
            let dx1 = abs(b.x - b.coner.left.x)
            this.x = b.x-(dx1-dx)
            this.draw()
            b.draw()
            let dx2 = abs(b.coner.left.y - this.coner.left.y)
           // console.log(abs(dx2-this.length),b.coner.left.y, this.coner.left.y);
            this.y+=dx2-this.length
            Block.height = this.height
        } 
        if(b.coner.top.x > this.coner.top.x &&b.coner.right.x > this.coner.right.x &&this.dirX==this.dirY){
            this.width -= abs(Math.floor(this.x)-b.x)
            this.x =b.x;
            this.y = b.y-this.length
            Block.width = this.width
        }
        if(b.coner.top.x < this.coner.top.x &&b.coner.right.x < this.coner.right.x &&this.dirX==this.dirY){
            this.width -= abs(Math.floor(this.x)-b.x)
            this.draw();
            b.draw();
            let dx = abs(this.x - this.coner.right.x)
            let dx1 = abs(b.x - b.coner.right.x)
            this.x = b.x+abs(dx1-dx)
            Block.width = this.width
            this.draw()
            b.draw()
            console.log(b.coner.right.x - this.coner.right.x);
            let dx2 = abs(b.coner.right.y - this.coner.right.y)
           // console.log(abs(dx2-this.length),b.coner.left.y, this.coner.left.y);
            this.y+=dx2-this.length
          /*   
           
            */
        } 
        Block.x = this.x;
        Block.y = this.y-this.length
        if(this.height <= 0 || this.width <= 0){
            Block.speed = 0;
            messages.style.display = "block";
            messages.innerText = "Click to Restart";
            create_text("Game Over");
            RunGame = false
        }
       
    }
}
let blocks = []
//let block = new Blocks(1,1,"green");
let hsl = 60
const create_blocks = ()=>{    
    if (Block.height > 0 && Block.speed&&Block.width>0) {
    hsl++
     let dirX = Math.floor(Math.random()*2) == 0?-1:1;
    let dirY = Math.floor(Math.random()*2) == 0?-1:1; 
    /* let dirX =  -1;
    let dirY = -1 */
    blocks.push(new Blocks(dirX,dirY,hsl))
}
}
const blocks_stop = ()=>{
    for (let i = 0; i < blocks.length; i++) {
        blocks[i].stop()
    }
       
     if(blocks[blocks.length-2]&&blocks[blocks.length-1]){
        blocks[blocks.length-1].changeSize(blocks[blocks.length-2])} 
 
} 
create_blocks()
blocks_stop()
create_blocks()
const onClick=()=>{
    messages.style.display = "none"
    Block.speed+=0.0005
    if(!RunGame){
        RunGame=true;
        blocks = [];
        first_block = true;
        Block.speed = 0.2;
        Block.score = 1;
        Block.start = false;
        Block.width = 200;
        Block.height = 200;
        Block.x=c.width/2;
        Block.y=c.height-250;
        hsl = 60
        create_blocks()
    }
    blocks_stop()
    create_blocks()
    if(!Block.start){
        Block.time.start = new Date().getTime();
        Block.start=true;
    }
    
     if(parseInt(Block.highscore) < Block.score){
        Block.show_msg = false
        localStorage.setItem("highscore",Block.score)
        
        if(Block.show_msg){
        create_text("New Score")}
        
     }
     
    Block.highscore=localStorage.getItem("highscore")
    if(Block.speed){
    speed.innerText = `Speed: ${Math.floor((Block.speed/0.2)*10)/10}x`   }  
    highscore.innerText = `HighScore:${Block.highscore}`
}
highscore.innerText = `HighScore:  ${Block.highscore}`
window.addEventListener("keypress",(e)=>{

    if(e.key == " "){
       onClick()
    }
    
})

const handle_blocks = ()=>{
    for (let i = 0; i < blocks.length; i++) {
        const block = blocks[i];
        block.draw()
        block.update()
        if(block.height <=0 || block.width <= 0){
            blocks.splice(i,1)
            i--;
        }
    }
}
const setTimer = ()=>{
    if(Block.time.start){
    Block.time.end = new Date().getTime();
    let time = (Block.time.end - Block.time.start)/1000;
    let sec = Math.floor((Block.time.end - Block.time.start)/1000);
    
    let min = Math.floor(sec/60)
    let txtsec= sec%60,txtmin = min
    if(sec%60 < 10){
        txtsec= "0"+sec%60;
    }
    if(min<10){
        txtmin= "0"+min;
    }
    timer.innerText = `${txtmin}:${txtsec}`}
    
}
const handleScore = ()=>{
    score_num.innerText = Block.score
   
}
let frame_txt = "FPS: 0"
const animate= ()=>{
    ctx.clearRect(0,0,c.width,c.height);
    handle_blocks()
    handle_text()
    if(RunGame){
    setTimer()}
    handleScore()
    if ((new Date().getTime())/1000 - start_time/1000 >= 1.0){
        start_time = new Date().getTime()
        frame_txt = "FPS: "+frame
        frame = 0}
    frame+=1
    FPS.innerText = frame_txt;
    requestAnimationFrame(animate);
}
window.addEventListener("click",onClick)
animate()