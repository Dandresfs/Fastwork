$(document).ready(function(){

    $('#closeFormacionModal').click(function(){
        $('#formacionForm')[0].reset();
    });

    render_formacion();

    $('#guardarFormacionConfirmacionModal').click(function(e){
        var pk = $('#formacion_delete').val();
        $.ajax({
          type: "DELETE",
          url: "/rest/formacion/delete/"+pk,
          success: function(data)
           {
               render_formacion();
               $('#ConfirmacionFormacionModal').modal('hide');
               $( ".confirmacionFormacion").empty();
           }
        });
    });

    $('#cerrarFormacionConfirmacionModal').click(function(e){
        $( ".confirmacionFormacion").empty();
    });

    $('#closeFormacionConfirmacionModal').click(function(e){
        $( ".confirmacionFormacion").empty();
    });

    $('#FormacionModal').submit(function(e){
        $.ajax({
          type: "POST",
          url: "/rest/formacion/",
          data: $('#formacionForm').serialize(),
          success: function(data)
           {
               $('#FormacionModal').modal('hide');
               render_formacion();
               $('#formacionForm')[0].reset();
           }
        });
        e.preventDefault();
    });


    $('#updateFormacionModal').submit(function(e){
        $.ajax({
          type: "PUT",
          url: "/rest/formacion/update/"+$('#update_id_formacion').val()+"/",
          data: $('#formacionUpdateForm').serialize(),
          success: function(data)
           {
               $('#updateFormacionModal').modal('hide');
               render_formacion();
               $('#formacionUpdateForm')[0].reset();
           }
        });
        e.preventDefault();
    });

});


function delete_formacion(pk){
    $.ajax({
          type: "GET",
          url: "/rest/formacion/detail/"+pk,
          success: function(data)
           {
               $( ".confirmacionFormacion" ).append( "<div>" +
                            "<p id='advertencia'>Vas a eliminar el siguiente registro de tu hoja de vida:</p>"+
                            "<p id='empresa' style='font-size:20px;font-weight:bold;'>"+data.institucion+"</p>"+
                            "<p id='sector'>"+data.nivel+"</p>"+
                            "<p id='departamento'>"+data.area+"</p>"+
                            "<p id='area'>"+data.estado+"</p>"+
                            "<p id='funciones_logros'>"+data.periodo+"</p>"+
                            "<input type='hidden' id='formacion_delete' value='"+pk+"'></input>"+
                           "</div>" );
           }
    });
    $('#ConfirmacionFormacionModal').modal('show');
}


function update_formacion(pk){
    $.ajax({
          type: "GET",
          url: "/rest/formacion/detail/"+pk,
          success: function(data)
           {
               $('#update_id_formacion').val(pk);
               $('#u_institucion_formacion').val(data.institucion);
               $('#u_nivel_formacion').val(data.nivel);
               $('#u_area_formacion').val(data.area);
               $('#u_estado_formacion').val(data.estado);
               $('#u_periodo_formacion').val(data.periodo);
               $('#updateFormacionModal').modal('show');
           }
    });
}

function render_formacion(){
    $( ".formaciones").empty();
    $( ".formaciones").removeClass("formaciones-none");
    $.ajax({
          type: "GET",
          url: "/rest/formacion/",
          success: function(data)
           {
               if(data.count == 0){
                   $( ".formaciones" ).addClass("formaciones-none");
                   $( ".formaciones" ).append( "<p>No tienes registro de formacion.</p>" );
               }
               else{
                   for(i=0;i<data.count;i++){
                       $( ".formaciones" ).append( "<div class='formacion col-md-6'><div class='registro'>" +
                           "<a class='delete-experience' onclick='delete_formacion("+data['results'][i].id+");'><span class='fa fa-times'></span></a>"+
                           "<a class='update-experience' onclick='update_formacion("+data['results'][i].id+");'><span class='fa fa-pencil'></span></a>"+
                           "<p class='title-empresa'>"+data['results'][i].nivel+"</p>"+
                           "<p>"+data['results'][i].institucion+" - "+data['results'][i].area+"</p>"+
                           "</div></div>" );
                   }
               }
           }
    });
}