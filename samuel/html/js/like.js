const like = document.querySelector(".give-like");
let icn = document.querySelector(".btn-solid-md");

let clicked = false;

like.addEventListener("click", () =>{
	if(!clicked) {
		clicked = true;
		icn.innerHTML = `<i class="fas fa-thumbs-up fa-2x" style="color: #FF1493;"></i>`;
	} 
	else {
		clicked = false;
		icn.innerHTML = `<i class="far fa-thumbs-up fa-2x" style="color: #FF1493;"></i>`;
	}
});

