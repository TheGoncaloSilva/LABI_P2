var songs;

async function getMusic(){

    const result = await fetch("/list?type=songs",{method: "GET"});
    const data = await result.json();
    /*if(data["result"] != "sucess")
    {
        windows.songs =  undefined;
        return;
    }*/
    console.log(data.length + " " + data)
    window.songs = data;
    loadPref();
}

function setMusic(){
    
    var trs = document.getElementById("tableBody").children;
    for(i = 0; i < trs.length; i++)
    {
        var select = trs[i].children[0].children[0];
        for(j = 0; j < window.samples.length; j++)
        {
            var op = document.createElement("option");
            op.text = window.samples[j]["nome"];
            op.value = window.samples[j]["nome"];
            op.classList.add("genOption");
            select.appendChild(op)
        }
    }
}


var clickLike = false;
var clickDisLike = false;

function likeUp(){
	var like = document.getElementById("like");
	console.log("like");
	if(!clickLike){
		clickLike = true;
		like.innerHTML = `<i class="fas fa-thumbs-up fa-3x" style="color: #FF1493;"></i>`;
        sessionStorage.pref = "like";
        if(clickDisLike){
            dislike();
        }
	}else{
		clickLike = false;
		like.innerHTML = `<i class="far fa-thumbs-up fa-3x" style="color: #FF1493;"></i>`;
        sessionStorage.pref = "none";
	}
}

function dislike(){
	var like = document.getElementById("dislike");
	console.log("dislike");
	if(!clickDisLike){
		clickDisLike = true;
		like.innerHTML = `<i class="fas fa-thumbs-down fa-3x" style="color: #FF1493;"></i>`;
        sessionStorage.pref = "dislike";
        if(clickLike){
            likeUp();
        }
	}else{
		clickDisLike = false;
		like.innerHTML = `<i class="far fa-thumbs-down fa-3x" style="color: #FF1493;"></i>`;
        sessionStorage.pref = "none";
    }
}

function loadPref(){
    if(sessionStorage.pref == "like"){
        likeUp();
    }else if(sessionStorage.pref == "dislike"){
        dislike();
    }
}