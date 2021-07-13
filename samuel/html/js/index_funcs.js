var songs;
var dic = {};

async function getMusic(){

    const result = await fetch("/list?type=songs",{method: "GET"});
    const data = await result.json();
    /*if(data["result"] != "sucess")
    {
        windows.songs =  undefined;
        return;
    }*/
    console.log(data);
    //console.log(data.length + " " + data)
    window.songs = data;
    setMusic();
    loadPref();
}

/*function setMusic(){
    
    var trs = document.getElementById("MusicaIndiv").children;
    for(i = 0; i < songs.length; i++)
    {
        //var select = songs[i].children[0].children[0];
        //var código = """ """

    }

}*/

function setMusic(){
    var container = document.getElementById("MusicaIndiv");
     
    for(var i = 0; i<window.songs.length; i++){
        console.log(i);
        var div1 = document.createElement("div");
        div1.classList.add("row", "music-box1");
        div1.style.borderRadius = "0px";

        var div2 = document.createElement("div");
        div2.classList.add("col-md-3", "music-img1");
        div2.style.padding = "0px";
        var img = document.createElement("img");
        img.src = "./../images/about.jpg"
        div2.appendChild(img);

        var div3 = document.createElement("div");
        div3.classList.add("col-md-6");

        var div4 = document.createElement("div");
        div4.classList.add("music-box-box");

        var h2 = document.createElement("h2");
        h2.style.color = "white";
        h2.innerHTML = window.songs[i][1];

        var div5 = document.createElement("div");
        div5.classList.add("author");
        var span1 = document.createElement("span");
        span1.style.color = "#000000";
        span1.innerHTML = window.songs[i][2] + " | ";
        var span2 = document.createElement("span");
        span2.style.color = "#000000";
        span2.innerHTML = window.songs[i][4];
        div5.appendChild(span1);
        div5.appendChild(span2);

        var div6 = document.createElement("div");
        var audio = document.createElement("audio");
        audio.classList.add("audio");
        audio.src = "songs/" + window.songs[i][0] + ".wav";
        audio.controls = true;
        div6.appendChild(audio);

        //APENDAR
        div4.appendChild(h2);
        div4.appendChild(div5);
        div4.appendChild(div6);

        div3.appendChild(div4);

        var div7 = document.createElement("div");
        div7.classList.add("col-md-3");

        var div8 = document.createElement("div");
        div8.id = "right-child1";

        var a1 = document.createElement("a");
        a1.classList.add("btn-solid-md");
        a1.id = "like-" + window.songs[i][0];
        console.log(i);
        a1.onclick = function(){ console.log(i-1 + window.songs); likeUp(window.songs[i-1][0]); };
        var i1 = document.createElement("i");
        i1.classList.add("far", "fa-thumbs-up", "fa-3x");
        i1.style.color = "#FF1493";
        a1.appendChild(i1);

        div8.appendChild(a1);

        var div9 = document.createElement("div");
        div9.id = "right-child2";

        var a2 = document.createElement("a");
        a2.classList.add("btn-solid-md");
        a2.id = "dislike-" + window.songs[i][0];
        a2.onclick = function(){ dislike(window.songs[i-1][0]); };
        var i2 = document.createElement("i");
        i2.classList.add("far", "fa-thumbs-down", "fa-3x");
        i2.style.color = "#FF1493";
        a2.appendChild(i2);

        div9.appendChild(a2);
        div7.appendChild(div8);
        div7.appendChild(div9);
        div1.appendChild(div2);
        div1.appendChild(div3);
        div1.appendChild(div7);

        container.appendChild(div1);
        window.dic[window.songs[i][0]] = [false, false];
    }
    
}

var clickLike = false;
var clickDisLike = false;

function likeUp(id, change){
	var like = document.getElementById("like-" + id);
	console.log("like");
	if(!window.dic[id][0]){
		window.dic[id][0]= true;
		like.innerHTML = `<i class="fas fa-thumbs-up fa-3x" style="color: #FF1493;"></i>`;
        var j = JSON.stringify(window.dic);
        sessionStorage.pref = j;
        if(window.dic[id][1]){
            dislike(id, true); 
        }
	}else{
		window.dic[id][0] = false;
		like.innerHTML = `<i class="far fa-thumbs-up fa-3x" style="color: #FF1493;"></i>`;
        if(!change){
            sessionStorage.pref = "none";
        }
	}
}

function dislike(id, change){
	var like = document.getElementById("dislike-" + id);
	console.log("dislike");
	if(!window.dic[id][1]){
		window.dic[id][1] = true;
		like.innerHTML = `<i class="fas fa-thumbs-down fa-3x" style="color: #FF1493;"></i>`;
        var j = JSON.stringify(window.dic);
        sessionStorage.pref = j;
        if(window.dic[id][0]){
            likeUp(id, true);
        }
	}else{
		window.dic[id][1] = false;
		like.innerHTML = `<i class="far fa-thumbs-down fa-3x" style="color: #FF1493;"></i>`;
        if(!change){
            sessionStorage.pref = "none";
        }
    }
}

function loadPref(){
    var sess = sessionStorage.pref;
    if(sess == "none") return;
    var j = JSON.parse(sessionStorage.pref);
    var keys = Object.keys(j);
    for(i in keys){
        console.log(keys[i]);
        if(j[keys[i]][0])
            likeUp(keys[i]);
        else if(j[keys[i]][1])
            dislike(keys[i]);
    }
}