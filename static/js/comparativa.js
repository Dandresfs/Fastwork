$(document).ready(function(){

    $.ajax({
          type: "GET",
          url: "/rest/ofertas/"+$("#id_oferta").val(),
          success: function(data)
           {

               render_residencia(data.residencia);
               render_edad(data.edad);

           }
    });

});

function render_residencia(data){

    $("#residencia_div").html("<ul style='list-style:disc'>" +
        "<li>El "+data['si_porcentaje']+"% de los aspirantes residen en "+data["ciudad"]+".</li>" +
        "<li>El "+data['no_porcentaje']+"% de los aspirantes no residen en "+data["ciudad"]+".</li></ul>");


    var ctx = document.getElementById("residencia");
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Si", "No"],
            datasets: [{
                label: '# de Aspirantes',
                data: [data['si'], data['no']],
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47"
                ],
                hoverBackgroundColor: [
                    "#7db8fa",
                    "#3c5767"
                ]
            }]
        },

    });
}

function render_edad(data){
    console.log(data);
/*
    $("#edad_div").html("<ul style='list-style:disc'>" +
        "<li>"+data['rango']+"</li></ul>");


    var ctx = document.getElementById("edad");
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ["18 y 24", "25 y 29", "30 y 34", "35 y 39", "40 y 44", "45 y 49", "Mas de 50"],
            datasets: [{
                label: '# de Aspirantes',
                data: data.edad,
                backgroundColor: [
                    "#6a9ad0",
                    "#273b47",
                    "#F18C02",
                    "#F4301B",
                    "#343F0F",
                    "#30FF9A",
                    "#885031"
                ]
            }]
        },

    });
    */
}