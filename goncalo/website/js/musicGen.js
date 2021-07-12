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
