$(function(){

  $("#name").focusin(function(){
    $("#name").css('background-color', '#ffc');
  });

  $("#name").focusout(function(){
    $("#name").css('background-color', '');
  });

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
    if(!$('#email').val().match(/^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i)) {
      $(".error_text").html("適切なメールアドレスを入力してください");
      $(".error_text").show();
    } else {
      $(".error_text").hide();
    }
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

$(function(){
  //画像ファイルプレビュー表示のイベント追加 fileを選択時に発火するイベントを登録
  $('form').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;

    // 画像ファイル以外の場合は何もしない
    if(file.type.indexOf("image") < 0){
      return false;
    }

    // ファイル読み込みが完了した際のイベント登録
    reader.onload = (function(file) {
      return function(e) {
        //既存のプレビューを削除
        $preview.empty();
        // .prevewの領域の中にロードした画像を表示するimageタグを追加
        $preview.append($('<img>').attr({
                  src: e.target.result,
                  class: "img_preview",
                  title: file.name
              }));
      };
    })(file);

    reader.readAsDataURL(file);
  });
});

$(function(){
  if($('.img_preview').length){
    $(".sample_img").css("display", "none");
  }
});
