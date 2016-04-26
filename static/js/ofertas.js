$(document).ready(function(){
    localStorage.setItem("categoria","todo");
    localStorage.setItem("departamento","todo");
    localStorage.setItem("ciudad","todo");
    localStorage.setItem("palabra_clave","");
    localStorage.setItem("page","1");
    localStorage.setItem("page_prev","");
    localStorage.setItem("page_next","");
    render_ofertas();


   jQuery.timeago.settings.strings = {
   prefixAgo: "Hace",
   prefixFromNow: "Dentro de",
   suffixAgo: "",
   suffixFromNow: "",
   seconds: "menos de un minuto",
   minute: "un minuto",
   minutes: "%d minutos",
   hour: "una hora",
   hours: "%d horas",
   day: "un día",
   days: "%d días",
   month: "un mes",
   months: "%d meses",
   year: "un año",
   years: "%d años"
};


});

function clickAndDisableCategoria(link) {
     // disable subsequent clicks
    var categorias = $('.categoria_link');
    for(i=0;i < categorias.length;i++){
        if(categorias[i].classList.contains("disable_link")){
            categorias[i].classList.remove("disable_link")
        }
    }
    link.classList.add("disable_link");
    localStorage.setItem("categoria",link.id);
    localStorage.setItem("page","1");
    render_ofertas();
}


function clickAndDisableDepartamento(link) {
     // disable subsequent clicks
    var departamentos = $('.departamento_link');
    for(i=0;i < departamentos.length;i++){
        if(departamentos[i].classList.contains("disable_link")){
            departamentos[i].classList.remove("disable_link")
        }
    }
    link.classList.add("disable_link");
    localStorage.setItem("departamento",link.id);
    localStorage.setItem("page","1");
    render_ofertas();
}




function clickAndDisableCiudad(link) {
     // disable subsequent clicks
    var ciudades = $('.ciudad_link');
    for(i=0;i < ciudades.length;i++){
        if(ciudades[i].classList.contains("disable_link")){
            ciudades[i].classList.remove("disable_link")
        }
    }
    link.classList.add("disable_link");
    localStorage.setItem("ciudad",link.id);
    localStorage.setItem("page","1");
    render_ofertas();
}



function update_prev(){
    if(localStorage.getItem("page_prev") != '') {
        localStorage.setItem("page", localStorage.getItem("page_prev"));
        render_ofertas();
    }
}


function update_next(){
    if(localStorage.getItem("page_next") != '') {
        localStorage.setItem("page", localStorage.getItem("page_next"));
        render_ofertas();
    }
}


function palabra_clave(){
    $( "#palabra").empty();
    $( "#palabra").append("<a href='#' class='close-link' onclick='closePalabra();'><span class='glyphicon glyphicon-remove'></span></a><p class='inline'>"+$('#clave').val()+"</p>")
    localStorage.setItem("palabra_clave",$('#clave').val());
    $('#clave').val('');
    localStorage.setItem("page","1");
    render_ofertas();
}

function closePalabra(){
    $( "#palabra").empty();
    localStorage.setItem("palabra_clave","");
    render_ofertas();
}


function render_ofertas(){
    $( ".ofertas_render").empty();
    $.ajax({
          type: "GET",
          url: "/rest/ofertas/?categoria="+localStorage.getItem("categoria")+"&departamento="+localStorage.getItem("departamento")+
        "&municipio="+localStorage.getItem("ciudad")+"&palabra="+localStorage.getItem("palabra_clave")+"&page="+localStorage.getItem("page"),
          success: function(data)
           {
               var previous = "";
               var next = "";


               if(data.previous == undefined){
                   $(".previous").addClass('disabled');
               }
               else{
                   $(".previous").removeClass('disabled');
                   localStorage.setItem("page_prev",data.previous);
               }


               if(data.next == undefined){
                   $(".next").addClass('disabled');
               }
               else{
                   $(".next").removeClass('disabled');
                   localStorage.setItem("page_next",data.next);
               }


               var data = data['results'];
               if(data.length == 0){
                   $( ".ofertas_render" ).append( "<h4>No se ha encontrado ofertas de empleo con los filtros actuales.</h4><h4>Pruebe a buscar con otras palabras o reduzca los filtros aplicados</h4>" );
               }
               else{
                   for(i=0;i<data.length;i++){
                       var descripcion = data[i].descripcion;
                       var publicacion = jQuery.timeago(data[i].publicacion);
                       var verificada = '';

                       if(data[i].empresa.verificada == true){
                           verificada = "<span class='fa fa-check-circle verificada'></span>"
                       }

                       if(descripcion.length > 200){
                           descripcion = descripcion.substr(0,199) + "...";
                       }

                       $( ".ofertas_render" ).append( "<div class='row card'><div class='col-sm-8'>" +
                           "<p class='title-oferta'><a href='#'>"+data[i].titulo+"</a></p>"+
                           verificada+"<p class='oferta-empresa inline'>"+data[i].empresa.nombre_comercial+"</p>"+
                           "<p class='oferta-descripcion'>"+descripcion+"</p>"+
                           "</a></div><div class='col-sm-4'>"+
                           "<div class='row'><div class='propiedad'><span class='glyphicon glyphicon-time time-icon'></span><p class='inline'>"+publicacion+"</p></div></div>"+
                           "<div class='row'><div class='propiedad'><span class='glyphicon glyphicon-map-marker gps-icon'></span><p class='inline'>"+data[i].municipio+", "+data[i].departamento+"</p></div></div>"+
                           "<div class='row'><div class='propiedad'><span class='glyphicon glyphicon-th-large categoria-icon'></span><p class='inline'>"+data[i].categoria.nombre+"</p></div></div>"+
                           "</div></div>" );
                   }
               }
           }
    });
}