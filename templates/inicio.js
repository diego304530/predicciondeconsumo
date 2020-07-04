$(document).ready(function() {
	$("#envioDatos").hide();
	$("#modalenv").hide();
	$("#rechazo").hide();
	$("#iniciosesion").hide();


	enviar();
	
	cerrarmodal1();
	mostrarformsesion();
	cerrarmodalform();
	iniciosesion();

});

var enviar= function(){

	$("#formCl").submit(function(e) {
		e.preventDefault();



		if($("#colegio").val()==="0"){
			$("#rechazo").show();
			location.href="#seleccion";
			
		}else{
			$("#rechazo").hide();

			formulario= $(this);

			datos= new FormData(formulario[0]);
			$("#envioDatos").modal("show");
			$.ajax({
				url: '/_agregar/',
				type: 'POST',
				data: datos,
				cache: false,
				contentType: false,
				processData: false,
				success: function(res){
					console.log(res);

					if(res==="True"){
						$("#iconenvio").show();
						$("#textomodal").html("DATOS ENVIADOS")
						$("#envioDatos").modal("hide");
						$("#envioDatos").hide();
						$("#modalenv").modal("show");

					}else{
						$("#iconenvio").hide();

						$("#textomodal").html("PREDICCION EXISTENTE")
						$("#envioDatos").modal("hide");
						$("#envioDatos").hide();
						$("#modalenv").modal("show");
					}
					


				}
			});

		}
		

	});
}

var cerrarmodal1= function(){
	$("#cerrar").click(function(event) {
		/* Act on the event */

		event.preventDefault();
		location.href="/";
	});

}

var cerrarmodalform= function(){
	$("#cerrarmodalform").click(function(event) {
		/* Act on the event */

		event.preventDefault();
		location.href="/";
	});

}

var mostrarformsesion= function(){
	$("#btniniciosesion").click(function(event) {
		/* Act on the event */
		event.preventDefault();
		$("#iniciosesion").modal("show");
	});
}

var iniciosesion= function(){
	$("#initsesion").submit(function(event) {
		/* Act on the event */
		event.preventDefault();
		formulario= $(this);

		datos= new FormData(formulario[0]);
		$("#iniciosesion").modal("hide");
		$("#iniciosesion").hide();
		$("#envioDatos").modal("show");
		$.ajax({
			url: '/_iniciarsesion/',
			type: 'POST',
			data: datos,
			cache: false,
			contentType: false,
			processData: false,
			success: function(res){
				console.log(res);

				if(res==="True"){
					location.href="/_datos/"

				}else{
					$("#iconenvio").hide();
					
					$("#textomodal").html("CREDENCIALES INCORRECTAS")
					$("#envioDatos").modal("hide");
					$("#envioDatos").hide();
					$("#modalenv").modal("show");
				}



			}
		});




	});
	
}
