const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 3000;                  //Save the port number where your server will be listening
const prompt = require('prompt-sync')();
const ip   = require("ip")

console.log(ip.address())

let randcode = []

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

const choice = prompt('Voulez-vous jouer solo(1) ou en duo(2) ? Tapez 1 ou 2 dans le terminal pour choisir votre mode : ');

if (choice === '1') {
    for(i=0; i<4; i++){
        getRandomInt(9)
        randcode.push(getRandomInt(9))
    }
    console.log("Votre code secret a été généré. Essayez de le trouver via le keypad !")
    // console.log(randcode)
} else if (choice === '2'){
    console.log("Entrer votre code secret à 4 chiffres. Ne le montrer pas au joueur 2 ! ")
    while (randcode.length !== 4){
        const joueur = prompt('Votre chiffre : ');
        if (joueur >= 0 && joueur <= 9){
            let chiffre = parseInt(joueur);
            randcode.push(chiffre)
        }else{
            console.log("Mauvais chiffre veuillez réessayer")
        }

    }
    console.log("Votre code secret a été généré. Joueur 2 à vous de le trouver via le keypad !")
    // console.log(randcode)
} else{
    console.log("Erreur de typo. Veuillez relancer")
}


//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => {
    console.log("get /")
    res.send({"randcode": randcode })

});

app.listen(port, () => {            //server starts listening for any attempts from a client to connect at port: {port}
    // console.log(`Now listening on port ${port}`);
});