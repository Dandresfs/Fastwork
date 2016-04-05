$(document).ready(function(){
    $('.closeExperienciaModal').click(function(){
        $('#experienciaForm')[0].reset();
    });


    render_experiencia();


    $('#guardarConfirmacionModal').click(function(e){
        var pk = $('#experiencia_delete').val();
        $.ajax({
          type: "DELETE",
          url: "/rest/experiencia/delete/"+pk,
          success: function(data)
           {
               render_experiencia();
               $('#ConfirmacionModal').modal('hide');
               $( ".confirmacion").empty();
           }
        });
    });

    $('#cerrarConfirmacionModal').click(function(e){
        $( ".confirmacion").empty();
    });

    $('#closeConfirmacionModal').click(function(e){
        $( ".confirmacion").empty();
    });

    $('#ExperienciaModal').submit(function(e){
        var rango = $('#periodo').val();
        rango = rango.split(" - ");
        var start = new Date(rango[0]);
        var end = new Date(rango[1]);
        var timeDiff = Math.abs(end.getTime() - start.getTime());
        var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
        var months = Math.round(diffDays/30);

        $.ajax({
          type: "POST",
          url: "/rest/experiencia/",
          data: $('#experienciaForm').serialize()+"&meses="+months,
          success: function(data)
           {
               $('#ExperienciaModal').modal('hide');
               render_experiencia();
               $('#experienciaForm')[0].reset();
           }
        });
        e.preventDefault();
    });

    $('#updateExperienciaModal').submit(function(e){
        var rango = $('#u_periodo').val();
        rango = rango.split(" - ");
        var start = new Date(rango[0]);
        var end = new Date(rango[1]);
        var timeDiff = Math.abs(end.getTime() - start.getTime());
        var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
        var months = Math.round(diffDays/30);

        $.ajax({
          type: "PUT",
          url: "/rest/experiencia/update/"+$('#update_id').val()+"/",
          data: $('#experienciaUpdateForm').serialize()+"&meses="+months,
          success: function(data)
           {
               $('#updateExperienciaModal').modal('hide');
               render_experiencia();
               $('#experienciaUpdateForm')[0].reset();
           }
        });
        e.preventDefault();
    });
});

function delete_experience(pk){
    $.ajax({
          type: "GET",
          url: "/rest/experiencia/detail/"+pk,
          success: function(data)
           {
               var mes = "";
               (data.meses < 2) ? mes = "Mes" : mes = "Meses";

               $( ".confirmacion" ).append( "<div>" +
                            "<p id='advertencia'>Vas a eliminar el siguiente registro de tu hoja de vida:</p>"+
                            "<p id='empresa' style='font-size:20px;font-weight:bold;'>"+data.empresa+"</p>"+
                            "<p id='cargo'><b>Cargo:</b> "+data.cargo+" - "+data.meses+" "+mes+"</p>"+
                            "<p id='sector'><b>Sector:</b> "+data.sector+"</p>"+
                            "<p id='departamento'><b>Departamento:</b> "+data.departamento+"</p>"+

                            "<p id='periodo'><b>Periodo:</b> "+data.periodo+"</p>"+
                            "<p id='area'><b>Area:</b> "+data.area+"</p>"+
                            "<p id='funciones_logros'><b>Logros:</b> "+data.funciones_logros+"</p>"+
                            "<input type='hidden' id='experiencia_delete' value='"+pk+"'></input>"+
                           "</div>" );
           }
    });
    $('#ConfirmacionModal').modal('show');
}


function update_experience(pk){
    $.ajax({
          type: "GET",
          url: "/rest/experiencia/detail/"+pk,
          success: function(data)
           {
               console.log(data.area);
               $('#update_id').val(pk);
               $('#u_empresa').val(data.empresa);
               $('#u_sector').val(data.sector);
               $('#u_departamento').val(data.departamento);
               $('#u_cargo').val(data.cargo);
               $('#u_periodo').val(data.periodo);
               $('#u_area').val(data.area);
               $('#u_funciones_logros').val(data.funciones_logros);
               $('#updateExperienciaModal').modal('show');
           }
    });
}



function render_experiencia(){
    $( ".experiencias").empty();
    $( ".experiencias").removeClass("experiencias-none");
    $.ajax({
          type: "GET",
          url: "/rest/experiencia/",
          success: function(data)
           {
               if(data.length == 0){
                   $( ".experiencias" ).addClass("experiencias-none");
                   $( ".experiencias" ).append( "<p>No tienes experiencias registradas.</p>" );
               }
               else{
                   for(i=0;i<data.length;i++){
                       var mes = "";
                       (data[i].meses < 2) ? mes = "Mes" : mes = "Meses";
                       $( ".experiencias" ).append( "<div class='experiencia col-md-6'><div class='registro'>" +
                           "<a class='delete-experience' onclick='delete_experience("+data[i].id+");'><span class='fa fa-times'></span></a>"+
                           "<a class='update-experience' onclick='update_experience("+data[i].id+");'><span class='fa fa-pencil'></span></a>"+
                           "<p class='title-empresa'>"+data[i].empresa+"</p>"+
                           "<p>"+data[i].cargo+" - "+data[i].meses+" "+mes+"</p>"+
                           "</div></div>" );
                   }
               }
           }
    });
}