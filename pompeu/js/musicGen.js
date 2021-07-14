function addTableLines(){
    var lines = ''
    for(i = 0; i < 3; i++){
        lines += "<tr> <th scope='row' id='select-left'><select class='form-select form-select-sm genSelect'><option class='genOption' selected>Selecionar</option><option class='genOption' value='1'>Batatas</option><option class='genOption' value='2'>Tomates</option><option class='genOption' value='3'>Cebolas</option></select></th>";
        for(l = 0; l < 3; l++){
            lines += "<td id = 'tablecell'><input style='margin: 0px;' type='checkbox' class='checkSong'><input style='margin: 0px;' type='checkbox' class='checkSong'><input style='margin: 0px;' type='checkbox' class='checkSong'><input style='margin: 0px;' type='checkbox' class='checkSong'><input style='margin: 0px;' type='checkbox' class='checkSong'></td>";
        }
        lines += "<td id='select-right'><select class='form-select form-select-sm genSelect'><option class='genOption' selected>Selecionar</option><option class='genOption' value='1'>Vinho</option><option class='genOption' value='2'>Vinagre</option><option class='genOption' value='3'>Azeite</option></select></td></tr>";
    }
    document.getElementById('table-body').insertAdjacentHTML('afterbegin', lines);
}

var samples = undefined;

async function getSampleList()
{
    const response = await fetch("/list?type=samples",{method: "GET"});
    const myJson = await response.json(); 

    window.samples = myJson;
    setSamples();
}

function setSamples()
{
    var trs = document.getElementById("tableBody").children;

    for(i = 0; i < trs.length; i++)
    {
        var select = trs[i].children[0].children[0];

        for(j = 0; j < window.samples.length; j++)
        {
            var op = document.createElement("option");
            op.text = window.samples[j][1];
            op.value = j;
            op.classList.add("genOption");
            select.appendChild(op)
        }
    }

}

function gerarArray(){
    var col = []

    const trs = document.getElementById("tableBody").children;
    for(j = 0; j < trs.length;j++)
    {
        const trChildren = trs[j].children;
        const sample = trChildren[0].children[0].value;

        if(sample == "Selecionar")
            continue;

        for(z = 1; z < trChildren.length - 1;z++)
        {
            const tdChildren = trChildren[z].children;

            for(w = 0; w < tdChildren.length; w++)
            {
                if(col[(z-1) * 5 + w] == undefined)
                    col[(z-1) * 5 + w] = [];
                
                if(tdChildren[w].checked)
                {
                    col[(z-1) * 5 + w].push(sample);
                }
            }
        }
    }
    return col;
}

function getEffects()
{
    var effects = {};
    const trs = document.getElementById("tableBody").children;
    for(i = 0; i < trs.length; i++)
    {
        const trChildren = trs[i].children;
        const effect = trChildren[trChildren.length - 1].children[0].value;

        if(effect == "Selecionar")
            continue;

        effects[i] = effect;
    }

    return effects
}

function getSamplesWithPath()
{
    var samples = []

    for(i = 0;i < window.samples.length; i++)
    {
        samples.push("samples/" + window.samples[i][0] + ".wav");
    }

    return samples;
}

async function gerar()
{
    const col = gerarArray();
    const volume = document.getElementById("volume").value;
    const bpm = document.getElementById("tempo").value;
    const mascara = document.getElementById("mascara").value;
    const autor = document.getElementById("autor").value;
    const nome = document.getElementById("nome").value; //nome da musica
    const effects = getEffects();
    const samples = getSamplesWithPath()

    const pauta = {"bpm":bpm,"volume":volume,"mask":mascara,"samples": samples,"effects": effects,"music": col}
    console.log(pauta)
    const json = JSON.stringify(pauta);
    console.log(json)
    const response = await fetch("/put?pauta=" + json + "&nome=" + nome + "&autor=" + autor,{method: "POST"});
    const myJson = await response.json();
    console.log(myJson)
    
}

