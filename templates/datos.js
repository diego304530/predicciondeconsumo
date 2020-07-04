$(document).ready(function() {
	verificacion();
	cerrarsesion();
	
});


var verificacion= function(){
	$.ajax({
		url: '/_verificar/',
		type: 'POST',
		success: function(res){
			
			if (res == "False") {
				// statement
				location.href="/";
			}else {
				$("#usonline").html(res);
				cargar();
			}
		}
	});

}

var cargar= function(){
	$.ajax({
		url: '/_tomardatos/',
		type: 'POST',
		success: function(res){
			var aux="";
			
			for (c in res) {
				// statement
				aux+="<tr>";
				for (x in res[c]) {
					// statement


					if (x==5){
						var aux2="";
						if(res[c][x]==0){
							aux2="Negativo";
						}else {
							aux2="Positivo";
						}
						aux+= "<td>" + aux2 + "</td>";
					}else if (x==6) {
						aux+= "<td>" + res[c][x]+ "%</td>";
					}else {
						aux+= "<td>" + res[c][x] + " </td>";
					}


				}
				aux+="</tr>";

			}
			$("#cuerpo").html(aux);
		}
	});

}


var cerrarsesion= function(){
	$("#btncerrarsesion").click(function(event) {
		/* Act on the event */
		event.preventDefault();
		$.ajax({
			url: '/_cerrarsesion/',
			type: 'POST',
			success: function(res){
				location.href="/";
			}
		});
	});
}
