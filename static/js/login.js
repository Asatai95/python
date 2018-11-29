$(function(){

  $("#email").focusin(function(){
    $("#email").css('background-color', '#ffc');
  });

  $("#email").focusout(function(){
    $("#email").css('background-color', '');
  });

  $("input[name='password']").focusin(function(){
    $("input[name='password']").css('background-color', '#ffc');
  });

  $("input[name='password']").focusout(function(){
    $("input[name='password']").css('background-color', '');
  });

  $('form[data-validate]').on('input', function () {
    $(this).find(':submit').attr('disabled', !this.checkValidity());
  });

});

$(function(){
  $('#email').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('.input__label-content--hoshi.email').addClass('input--filled');
    } else {
      $('.input__label-content--hoshi.email').removeClass('input--filled');
    }
  });
  $('input[name="password"]').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('.input__label-content--hoshi.password').addClass('input--filled');
    } else {
      $('.input__label-content--hoshi.password').removeClass('input--filled');
    }
  });
});
