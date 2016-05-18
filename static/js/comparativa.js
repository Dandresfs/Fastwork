$(document).ready(function(){

    $.ajax({
          type: "GET",
          url: "/rest/ofertas/"+$("#id_oferta").val(),
          success: function(data)
           {

               render_residencia(data.residencia);
               render_edad(data.edad);
               render_experiencia(data.experiencia);
               render_formacion(data.nivel);


           }
    });

});

function render_residencia(data){
    var residencia = [];
    var mensaje ="";

    for(i=0;i<data.residencia.length;i++){
        residencia.push(data.residencia[i].cantidad)
        if(data.residencia[i].user_request != ""){
            mensaje = data.residencia[i].user_request
        }
    }

    $("#residencia_div").html("<ul style='list-style:disc'>" +
        "<li>"+mensaje+"</li></ul>");



    var ctx = document.getElementById("residencia");
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Si", "No", "No registra"],
            datasets: [{
                label: '# de Aspirantes',
                data: residencia,
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47",
                    "#F18C02"
                ],
                hoverBackgroundColor: [
                    "#7db8fa",
                    "#3c5767",
                    "#F18C02"
                ]
            }]
        },

    });
}

function render_edad(data){
    var edad = [];
    var rango ="";

    for(i=0;i<data.edad.length;i++){
        edad.push(data.edad[i].cantidad)
        if(data.edad[i].user_request != ""){
            rango = data.edad[i].user_request
        }
    }

    $("#edad_div").html("<ul style='list-style:disc'>" +
        "<li>"+rango+"</li></ul>");


    var ctx = document.getElementById("edad");
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["18 y 24", "25 y 29", "30 y 34", "35 y 39", "40 y 44", "45 y 49", "Mas de 50", "No registra"],
            datasets: [{
                label: '# de Aspirantes',
                data: edad,
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47",
                    "#F18C02",
                    "#F4301B",
                    "#343F0F",
                    "#30FF9A",
                    "#885031",
                    "#842C9B",
                ]
            }]
        },

    });
}




function render_experiencia(data){
    var experiencia = [];
    var rango ="";

    for(i=0;i<data.experiencia.length;i++){
        experiencia.push(data.experiencia[i].cantidad)
        if(data.experiencia[i].user_request != ""){
            rango = data.experiencia[i].user_request
        }
    }

    $("#experiencia_div").html("<ul style='list-style:disc'>" +
        "<li>"+rango+"</li></ul>");


    var ctx = document.getElementById("experiencia");
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ["1 - 6", "7 - 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48", "48 o mas", "No registra"],
            datasets: [{
                label: '# de Aspirantes',
                data: experiencia,
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47",
                    "#F18C02",
                    "#F4301B",
                    "#343F0F",
                    "#30FF9A",
                    "#885031",
                    "#842C9B",
                ]
            }]
        },

    });
}




function render_formacion(data){
    var formacion = [];
    var rango ="";

    for(i=0;i<data.nivel.length;i++){
        formacion.push(data.nivel[i].cantidad)
        if(data.nivel[i].user_request != ""){
            rango = data.nivel[i].user_request
        }
    }

    $("#nivel_div").html("<ul style='list-style:disc'>" +
        "<li>"+rango+"</li></ul>");


    var ctx = document.getElementById("nivel");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Básico", "Medio", "Universitario", "Postgrado", "No registra"],
            datasets: [{
                label: '# de Aspirantes',
                data: formacion,
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47",
                    "#F18C02",
                    "#F4301B",
                    "#343F0F",
                ]
            }]
        },

    });
}