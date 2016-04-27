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


    $('#registerButton').click(function(){
        $('#login-social').modal('hide');
        $('#id_email').val($('#email_login').val());
        $('#id_password').val($('#password_login').val());
        $('#register_modal').modal('show');
    });
});