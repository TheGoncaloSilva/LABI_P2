const userAction = async () => {
	const response = await fecth('C:/Users/samut/Desktop/LABI/Projeto%20Final/labi2021-p2-g14/samuel/html/index.html');
	const myJson = await response.json();
	console.log(myJson);
	console.log(response);
}
