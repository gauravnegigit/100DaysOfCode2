console.log("Welcome to tic tac toe")
let music = new Audio("music.wav")
let turnaudio = new Audio("ting.mp3")
let gameover = new Audio("gameover.mp3")
let turn = "X"
let gameOver = false

// function to change the turn 
const changeTurn = ()=>{
    return turn === "X"?"0":"X"
}

// function to check for wn
const checkWin = ()=>{
    let boxtext = document.getElementsByClassName("boxtext")
    let wins = [
        [0 , 1, 2],
        [3 , 4 , 5],
        [6 , 7, 8],
        [0 ,  3, 6],
        [1 , 4 , 7],
        [2 , 5 , 8],
        [0 , 4 , 8],
        [2 , 4 , 6]
    ]
    wins.forEach(e => {
        if ((boxtext[e[0]].innerText === boxtext[e[1]].innerText) && (boxtext[e[1]].innerText === boxtext[e[2]].innerText) && (boxtext[e[0]].innerText !== "")){
            document.querySelector('.info').innerText = boxtext[e[0]].innerText + " Won"
            gameOver = true 
            document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "200px"
            gameover.play()
            turn , gameOver = resetGame()
        }
    });
}

// function to reset the game 
const resetGame = ()=>{
    let boxtexts = document.querySelectorAll('.boxtext');
    Array.from(boxtexts).forEach(element => {
        element.innerText = ""
    });
    turn = "X"; 
    gameOver = false
    document.querySelector(".line").style.width = "0vw";
    document.getElementsByClassName("info")[0].innerText  = "Turn for " + turn;
    document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "0px"

    return turn , gameOver
}

gameover.play()
// game logic
let boxes = document.getElementsByClassName("box")
Array.from(boxes).forEach(element => {
    let boxtext = element.querySelector('.boxtext')
    element.addEventListener('click' , ()=>{
        if (boxtext.innerText === ''){
            boxtext.innerText = turn ;
            turn = changeTurn();
            turnaudio.play()
            checkWin();
            if(!gameOver){
                document.getElementsByClassName("info")[0].innerText = `Turn for ${turn}`
            }
        }
    })
});

// Add onclick listener to reset button
reset.addEventListener('click', ()=>{
    turn , gameOver = resetGame()
})