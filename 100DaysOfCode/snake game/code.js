
// # game constants and variables 
let direction = {x:0 , y:0};
const fruitsound = new Audio('food.mp3');
const gameOverSound = new Audio('gameover.mp3');
const moveSound = new Audio('move.mp3');
const musicSound = new Audio('music.wav');
let speed  = 10;
let lastTime = 0 ;
let snakeArr = [
    {x: 13 , y:15}
]

let food = {x: 10 , y:9};
let vel = {x: 0, y: 0}; 
let score = 0 ;
let highscore = 0 ;

// game functions 
const main = (ctime)=>{
    musicSound.play()
    window.requestAnimationFrame(main);
    // console.log(ctime)
    console.log(snakeArr)
    if((ctime - lastTime)/1000 < 1/speed){
        return ;
    }
    lastTime = ctime ;
    game()
}

const isCollide = (snake)=> {
    // If you bump into yourself 
    for (let i = 1; i < snakeArr.length; i++) {
        if(snake[i].x === snake[0].x && snake[i].y === snake[0].y){
            return true;
        }
    }
    // If you bump into the wall
    if(snake[0].x >= 18 || snake[0].x <=0 || snake[0].y >= 18 || snake[0].y <=0){
        return true;
    }
        
    return false;
}

const game = ()=>{
    // part 1 is about updating teh snake array 
    if(isCollide(snakeArr)){
        gameOverSound.play();
        musicSound.pause();
        vel = {x:0 , y:0};
        alert("GameOver . Preess any key to continue ...")
        snakeArr = [{x:13 , y:15}]
        musicSound.play()
        score = 0 ;
        scoreBox.innerHTML = "Score : " + 0 ;
    }

    // if the snake has eaten the food , increment the score regenerate the food .
    if (snakeArr[0].y === food.y && snakeArr[0].x === food.x){
        fruitsound.play()
        snakeArr.unshift({x: snakeArr[0].x + vel.x , y: snakeArr[0].y + vel.y })
        let a = 1 ;
        let b = 17 ; 
        // generating the food to be random between a and b 
        score += 1;
        if (highscore < score){
            highscore = score ; 
        }
        scoreBox.innerHTML = "Score : " + score ;
        highscoreBox.innerHTML = "High score : " + highscore ;
        food = {x: Math.round(a + (b-a) * Math.random()) , y: Math.round(a + (b-a)* Math.random())} 
    }

    // moving the snake 
    for(let i = snakeArr.length - 2 ; i>=0 ; i--){
        snakeArr[i + 1] = {...snakeArr[i]};
    }

    snakeArr[0].x += vel.x ;
    snakeArr[0].y += vel.y ;


    // part 2 is about rendering teh snake and food 
    board.innerHTML = "";
    snakeArr.forEach((element , index) => {
        snakeElement = document.createElement('div');
        snakeElement.style.gridRowStart = element.y ;
        snakeElement.style.gridColumnStart = element.x ;
        snakeElement.classList.add('head')
        board.appendChild(snakeElement);
    });

    // display the food 
    foodElement = document.createElement('div');
    foodElement.style.gridRowStart = food.y ;
    foodElement.style.gridColumnStart = food.x ; 
    foodElement.classList.add('food')
    board.appendChild(foodElement )
}

// main logic starts here 
window.requestAnimationFrame(main);
window.addEventListener('keydown' , e=>{
    vel = {x:0 , y:1}  // start the game 
    moveSound.play()
    switch(e.key){
        case "ArrowUp":
            console.log("ArrowUp")
            vel.x = 0;
            vel.y = -1;
            break ;
        case "ArrowDown":
            console.log("ArrowDown")
            vel.x = 0;
            vel.y = 1;
            break ;
        case "ArrowLeft":
            console.log("ArrowLeft")
            vel.x = -1;
            vel.y = 0;
            break ;
        case "ArrowRight":
            console.log("ArrowRight")
            vel.x = 1;
            vel.y = 0;
            break ;

        default:
            break
    }
})