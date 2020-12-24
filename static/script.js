var lastCardClicked = "singleCard";

function cardClicked(cardId) {
    lastCardClicked = cardId;
}

function sendData(cardId) {
    let cardInputs = document.getElementById(cardId).getElementsByTagName('input');
    let data = "";
    let isColor = false;
    for (let cInput of cardInputs) {
        if (cInput.type == "checkbox"){
            data += "/" + cInput.checked;
        } else if (cInput.type == "color"){
            isColor = true;
            data += cInput.value.slice(1);
        } else  {
            data += "/" + cInput.value;
        }
    }
    if (isColor) {
        data = "/color/" + data;
    } else {
        data = "/grad" + data;
    }

    window.location.href = data;
}

function enablerClicked(enablerId) {
    let l = enablerId.search("ChkBox");
    let idStart = enablerId.slice(0, l);
    let n = enablerId.slice(l+6)
    document.getElementById(idStart + "SpeedRange" + n).disabled = !document.getElementById(enablerId).checked;
}

