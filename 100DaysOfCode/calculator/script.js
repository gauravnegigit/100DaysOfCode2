let string = "";
let buttons = document.querySelectorAll(".button");
Array.from(buttons).forEach(button => {
    button.addEventListener('click' , (e)=>{
        if(e.target.innerHTML == "="){
            try {
                string = eval(string);
                document.querySelector('input').value = string ;
            }
            catch(err){
                alert("You have enetered the wrong expression for evaluation")
            }
        }
        else if (e.target.innerHTML == "AC"){
            string  = "";
            document.querySelector('input').value = string ;
        }
        else{ 
            console.log(e.target);
            string = string + e.target.innerHTML;
            document.querySelector('input').value = string ;
        }

    })
});