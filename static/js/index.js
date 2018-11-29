$(function(){
  //一応エラーメッセージ部分を非表示にしておく
  $("#username_error").hide();
  $("#usermail_error").hide();
  $("#userpassword_error").hide();
  $("#userpasswordsub_error").hide();

   $("#name").focusin(function(){
     $("#dump_usermail_error").hide();
     $("#name").css('background-color', '#ffc');
   });
   //名前フォームからフォーカスが外れたとき
   $("#name").focusout(function(){
     $("#name").css('background-color', '');
      check_username();
   });

   //ユーザーネームフォームのチェック処理
   function check_username(){
       //文字数を取得する
       var form_length = $("#name").val().length;

       if (form_length == 0){
         $("#username_error").html("ユーザー名を入力してください");
         $("#username_error").show();

       } else if (form_length < 0 || form_length > 15){

         $("#username_error").html("15文字以内である必要があります");
         $("#username_error").show();

       } else {
         $("#username_error").hide();
       }

   }

   $("#email").focusin(function(){
     $("#dump_usermail_error").hide();
     $("#email").css('background-color', '#ffc');
   });

   $("#email").focusout(function(){
     $("#email").css('background-color', '');
      check_usermail();
   });

   function check_usermail(){

     $("input[name='email']").keyup(function(){
       if(!$('#email').val().match(/^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i)) {
         $("#usermail_error").html("適切なメールアドレスを入力してください");
         $("#usermail_error").show();
       } else {
         $("#usermail_error").hide();

       }
     });
   }

   $("input[name='password']").focusin(function(){
     $("#dump_usermail_error").hide();
     $("input[name='password']").css('background-color', '#ffc');
   });

   //パスワードのチェック
   $("input[name='password']").focusout(function(){
     $("input[name='password']").css('background-color', '')
      check_password();
   });

   $("input[name='retrypassword']").focusin(function(){
     $("#dump_usermail_error").hide();
     $("input[name='retrypassword']").css('background-color', '#ffc');
   });


   $("input[name='retrypassword']").focusout(function(){
     $("input[name='retrypassword']").css('background-color', '');
     check_retrypassword();
   });

   // パスワード確認（入力数）

   function check_password(){
     var form_password = $("input[name='password']").val().length;

     if(form_password == 0){
       $("#userpassword_error").html("パスワードを入力してください");
       $("#userpassword_error").show();

     } else if(form_password != 0) {
       $("#userpassword_error").hide();
     }

     if(form_password > 0 && form_password < 6){
       $("#userpassword_error").html("パスワードは６文字以上入力してください");
       $("#userpassword_error").show();
     } else {
       $("#userpassword_error").hide();

     }
   }

   //再度パスワードのチェック
   function check_retrypassword(){
     var form_password_check = $("input[name='password']").val();
     var form_retrypassword_check = $("input[name='retrypassword']").val();

     if (form_retrypassword_check != form_password_check) {
       $("#userpasswordsub_error").html("同一の内容を記述してください");
       $("#userpasswordsub_error").show();
     } else if(form_retrypassword_check == form_password_check) {
       $("#userpasswordsub_error").hide();

       $('form[data-validate]').on('input', function () {
         $(this).find(':submit').attr('disabled', !this.checkValidity());
       });

     }
   }

});

$(function(){
  $('#name').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('.input__label-content--hoshi.name').addClass('input--filled');
    } else {
      $('.input__label-content--hoshi.name').removeClass('input--filled');
    }
  });
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
  $('input[name="retrypassword"]').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('.input__label-content--hoshi.password_sub').addClass('input--filled');
    } else {
      $('.input__label-content--hoshi.password_sub').removeClass('input--filled');
    }
  });
});
