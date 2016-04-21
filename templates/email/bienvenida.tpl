{% extends "mail_templated/base.tpl" %}

{% block subject %}
Bienvenido!!
{% endblock %}

{% block html %}
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Really Simple HTML Email Template</title>
<style>
/* -------------------------------------
    GLOBAL
------------------------------------- */
* {
  font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
  font-size: 100%;
  line-height: 1.6em;
  margin: 0;
  padding: 0;
}
img {
  max-width: 600px;
  width: auto;
}
body {
  -webkit-font-smoothing: antialiased;
  height: 100%;
  -webkit-text-size-adjust: none;
  width: 100% !important;
  color: #ffffff;
}
/* -------------------------------------
    ELEMENTS
------------------------------------- */
a {
  color: #348eda;
}
.btn-primary {
  Margin-bottom: 10px;
  width: auto !important;
}
.btn-primary td {
  background-color: #348eda;
  border-radius: 25px;
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
  font-size: 14px;
  text-align: center;
  vertical-align: top;
}
.btn-primary td a {
  background-color: #348eda;
  border: solid 1px #348eda;
  border-radius: 25px;
  border-width: 10px 20px;
  display: inline-block;
  color: #ffffff;
  cursor: pointer;
  font-weight: bold;
  line-height: 2;
  text-decoration: none;
}
.last {
  margin-bottom: 0;
}
.first {
  margin-top: 0;
}
.padding {
  padding: 10px 0;
}
/* -------------------------------------
    BODY
------------------------------------- */
table.body-wrap {
  padding: 20px;
  width: 100%;
}
table.body-wrap .container {
  border: 1px solid #f0f0f0;
}
/* -------------------------------------
    FOOTER
------------------------------------- */
table.footer-wrap {
  clear: both !important;
  width: 100%;
}
.footer-wrap .container p {
  color: #666666;
  font-size: 12px;

}
table.footer-wrap a {
  color: #999999;
}
/* -------------------------------------
    TYPOGRAPHY
------------------------------------- */
h1,
h2,
h3 {
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
  font-weight: 200;
  line-height: 1.2em;
  margin: 20px 0 10px;
  color: #ffffff;
}
h1 {
  font-size: 32px;
  color: #ffffff;
}
h2 {
  font-size: 24px;
}
h3 {
  font-size: 18px;
}
p,
ul,
ol {
  font-size: 14px;
  font-weight: normal;
  margin-bottom: 10px;
}
ul li,
ol li {
  margin-left: 5px;
  list-style-position: inside;
}
/* ---------------------------------------------------
    RESPONSIVENESS
------------------------------------------------------ */
/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
.container {
  clear: both !important;
  display: block !important;
  Margin: 0 auto !important;
  max-width: 600px !important;
}
/* Set the padding on the td rather than the div for Outlook compatibility */
.body-wrap .container {
  padding: 20px;
}
/* This should also be a block element, so that it will fill 100% of the .container */
.content {
  display: block;
  margin: 0 auto;
  max-width: 600px;
}
/* Let's make sure tables in the content area are 100% wide */
.content table {
  width: 100%;
}
</style>
</head>

<body bgcolor="#f6f6f6">

<!-- body -->
<table class="body-wrap" bgcolor="#f6f6f6">
  <tr>
    <td></td>
    <td class="container" bgcolor="#273b47">

      <!-- content -->
      <div class="content">
      <table>
        <tr>
          <td>
            <img src="http://www.fastworkcolombia.com/static/imagenes/logo.png">
            <h1>¡Hola!</h1>
            <h3>¡Gracias por unirte! Aquí tienes la información de tu cuenta:</h3>

            <p>Username: {{ username }}</p>
            <p>Email: {{ email }}</p>


            <p>Recuerda:</p>
            <p>1. Personaliza tu perfil: Personaliza tu cuenta de usuario y registra tus datos personales, contacto y residencia, mantenlos actualizados para que los empleadores se puedan comunicar contigo rapidamente.</p>
            <p>2. Registra tu experiencia y formación: Dale a conocer toda tu experiencia laboral y tu formación academica a los empleadores, tambien ayudanos a sugerirte las ofertas mas acordes a tu perfil laboral.</p>
            <p>3. Aplica a ofertas de empleo: Filtra las ofertas de empleo con palabras clave, categorias, ubicación, salario, tipo de contratación y mucho mas, aplica a las ofertas y observa tu comparativa con los demas aspirantes.</p>

            <!-- button -->
            <table class="btn-primary" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td>
                  <a href="http://www.fastworkcolombia.com/">Iniciar sesión en Fast Work Colombia</a>
                </td>
              </tr>
            </table>
            <!-- /button -->

            <table>
          <tr>
            <td align="center">
              <p>&copy 2016</p>
            </td>
          </tr>
        </table>

          </td>
        </tr>
      </table>
      </div>
      <!-- /content -->

    </td>
    <td></td>
  </tr>
</table>
<!-- /body -->



</body>
</html>
{% endblock %}