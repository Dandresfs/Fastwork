$(document).ready(function(){
    if($('#error-login').text() != ""){
        $('#login-social').modal('show');
    }

    if($('#error-register').text() != ""){
        $('#register_modal').modal('show');
    }


    if($('#emailConfirmation').text() != ""){
        $('#confirmation_modal').modal('show');
    }

    $('#show_password').click(function(){
        if($('#show_password').attr('aria-pressed') == "false"){
            $('#eye').removeClass('glyphicon-eye-close');
            $('#eye').addClass('glyphicon-eye-open');
            $('#id_password').attr('type','text')
        }
        else{
            $('#eye').removeClass('glyphicon-eye-open');
            $('#eye').addClass('glyphicon-eye-close');
            $('#id_password').attr('type','password')
        }
    });

    $('#registerButton').click(function(){
        $('#login-social').modal('hide');
        $('#id_email').val($('#email_login').val());
        $('#id_password').val($('#password_login').val());
        $('#register_modal').modal('show');
    });
});