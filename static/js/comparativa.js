$(document).ready(function(){

    $.ajax({
          type: "GET",
          url: "/rest/ofertas/"+$("#id_oferta").val(),
          success: function(data)
           {
               console.log(data);

               var p = "participantes han";
               if(data.residencia['total'] == 1){
                   var p = "participante ha";
               }


               var p_si = data.residencia['si'];

               if(p_si == 0){
                   var p_si = "Ningun aspirante reside";
               }
               else if(p_si == 1){
                    var p_si = "Un aspirante reside";
                }
               else{
                   var p_si = p_si+" aspirantes residen";
               }



               var p_no = data.residencia['no'];

               if(p_no == 0){
                   var p_no = "Todos los aspirantes residen";
               }
               else if(p_no == 1){
                    var p_no = "Un aspirante no reside";
                }
               else{
                   var p_no = p_no+" aspirantes no residen";
               }


               $("#residentes_total").text(data.residencia['total']+" "+p+" aplicado a esta oferta.");

               $("#residentes_si").text(p_si+" en la ciudad de la oferta.");

               $("#residentes_no").text(p_no+" en la ciudad de la oferta.");

               var ctx = document.getElementById("residencia");
                var myChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ["Si", "No"],
                        datasets: [{
                            label: '# de Aspirantes',
                            data: [data.residencia['si'], data.residencia['no']],
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
    });





    var ctx2 = document.getElementById("experiencia");
    var myChart2 = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ["0", "1 - 12", "13 - 24", "25 - 48", "49 o más"],
            datasets: [{
                label: '# Aspirantes',
                data: [12, 19, 3, 5, 2],
                backgroundColor: [
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });


    var ctx3 = document.getElementById("edad");
    var myChart3 = new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: ["18 - 23", "24 - 30", "31 - 35", "36 - 40", "41 - 50", "50 o más"],
            datasets: [{
                label: '# Aspirantes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });



    var ctx4 = document.getElementById("estudios");
    var myChart4 = new Chart(ctx4, {
        type: 'bar',
        data: {
            labels: ["Educación Básica", "Educación Media", "Carrera Técnica","Universidad", "Postgrado"],
            datasets: [{
                label: '# Aspirantes',
                data: [12, 19, 3, 5, 2],
                backgroundColor: [
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                "#6a9ad0",
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });


});