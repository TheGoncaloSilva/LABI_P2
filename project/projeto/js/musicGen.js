function generateLines()
{
    const LINES = 10;
    const NUM_CELLS = 5;
    const CHECKBOXS_PER_CELL = 5;
    const EFFECTS = ["fadein","reverse","delay","fadeout"];

    var table = document.getElementById("table");

    var thead = document.createElement("thead");
    var tr1 = document.createElement("tr");
    tr1.id = "tablehead";
    var excerto = document.createElement("th");
    excerto.classList.add("text-center");
    excerto.scope = "col";
    excerto.innerHTML = "Excerto";

    tr1.appendChild(excerto);

    for(var i = 0;i < NUM_CELLS; i++)
    {
        var th = document.createElement("th");
        th.scope = "col";
        th.innerHTML = (i + 1);
        tr1.appendChild(th);
    }

    var efeito = document.createElement("th");
    efeito.classList.add("text-center");
    efeito.scope = "col";
    efeito.innerHTML = "Efeito";
    tr1.appendChild(efeito);
    thead.appendChild(tr1);
    table.appendChild(thead);
    var tbody = document.createElement("tbody");
    tbody.id = "tableBody";


    for(var i = 0; i < LINES; i++)
    {
        var tr = document.createElement("tr");
        var th = document.createElement("th");
        th.id = "select-left";
        th.scope = "row";

        var select = document.createElement("select");
        select.classList.add("form-select","form-select-sm","genSelect");
        var opSelecionar = document.createElement("option");
        opSelecionar.text = "Selecionar";
        opSelecionar.selected = true;
        opSelecionar.classList.add("genOption");
        select.appendChild(opSelecionar);

        for(var j = 0; j < window.samples.length;j++)
        {
            var op = document.createElement("option");
            op.text = window.samples[j][1];
            op.value = j;
            op.classList.add("genOption");
            select.appendChild(op);
        }

        th.appendChild(select);
        tr.appendChild(th);

        for(var j = 0; j < NUM_CELLS; j++)
        {
            var td = document.createElement("td");
            td.id = "tablecell";

            for(var z = 0; z < CHECKBOXS_PER_CELL; z++)
            {
                var input = document.createElement("input");
                input.classList.add("checkSong");
                input.type = "checkbox";
                input.style.margin = "2px";
                td.appendChild(input);
            }

            tr.appendChild(td);
        }

        var efeitos = document.createElement("td");
        efeitos.id = "select-right";

        var selectEfeitos = document.createElement("select");
        selectEfeitos.classList.add("form-select","form-select-sm","genSelect");
        
        var opSelecionar = document.createElement("option");
        opSelecionar.classList.add("genOption");
        opSelecionar.text = "Selecionar";
        opSelecionar.selected = true;
        
        selectEfeitos.appendChild(opSelecionar);

        for(var j = 0; j < EFFECTS.length; j++)
        {
            var op = document.createElement("option");
            op.classList.add("genOption");
            op.text = EFFECTS[j];
            op.value = EFFECTS[j];
            selectEfeitos.appendChild(op);
        }

        efeitos.appendChild(selectEfeitos);
        tr.appendChild(efeitos);
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
}

var samples = undefined;

async function getSampleList()
{
    const response = await fetch("/list?type=samples",{method: "GET"});
    const myJson = await response.json(); 

    window.samples = myJson;
    generateLines();
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

    const response = await fetch("/put?pauta=" + json + "&nome=" + nome + "&autor=" + autor,{method: "POST"});
    const myJson = await response.json();

    if(myJson["result"] == "success")
    {
        var ask = confirm("Musica gerada");

        if(ask)
        {
            window.location.href = "/index";
        }
    }
    else
    {
        confirm("Ocorreu um erro na geracao da musica");
    }
    
}

