//cria rows para a tabela de excertos de exporter.html
const userAction = async () => { 
	const response = await fetch('/list?type=samples');
	const myJson = await response.json();
	
	const sampArr = myJson;
	console.log(sampArr)
	const tbl = document.getElementById('pr');//tabl

	for(var i = 0; i<sampArr.length; i++){
		const name = sampArr[i]["nome"];	
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		td.style.color = "white";
		td.innerHTML = name;
		tr.appendChild(td);
		//tr.insertCell(0).innerHTML = name;
		tr.children[0].classList.add("table-beauty-plus");

		var td2 = document.createElement("td");
		var audio = document.createElement("audio");

		audio.src = "samples/" + sampArr[i][0] + ".wav";
		audio.controls = true;
		audio.id = "smp";
		audio.style = "display: block;margin-left: auto;margin-right: auto;";

		td2.appendChild(audio);
		tr.appendChild(td2);
		//tr.insertCell(1).innerHTML = "<audio id=\"smp\" style=\"display: block;margin-left: auto;margin-right: auto;\" src=\"/samples/" + sampArr[i]["id"] + ".wav\" controls></audio>";
		tbl.appendChild(tr);
		/*tbl = document.getElementById('pr');//table 
		elmnt = tbl.getElementsByTagName("TR")[1];
		cln = elmnt.cloneNode(true);
		tbl.tBodies[0].appendChild(cln);*/			
	}
}

async function criarExcerto(){

	const name = document.getElementById("nameFile").value;
    const file = document.getElementById("uploadFile").files[0];
	console.log(file)
	let formData = new FormData();
		 
	formData.append("photo", file);

    const response = await fetch("../uploadSample?nome=" + name + "&file=" + file, {method: "POST", body: formData});
    const myJson = await response.json();

    if(myJson["result"] == "success")
    {
        alert("Excerto carregado com sucesso");
        window.location.href = "";
    }
    else
    {
        alert("Ocorreu um erro na geracao da musica");
    }

}





