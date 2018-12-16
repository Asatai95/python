$(document).ready(function() {
  var pagetop = $('.navbar-brand');
  pagetop.click(function () {
    $('body, html').animate({ scrollTop: 0 }, 500);
    return false;
  });
});

$(function(){
  $('label').each(function(){
    var divText = $(this).html();
    $(this).html(divText.replace("ユーザー名:", "ユーザー名")
                           .replace("メールアドレス:", "メールアドレス")
                           .replace("パスワード:", "パスワード")
                           .replace("パスワードの確認:", "パスワードの確認")
                           .replace("Email:", "Email")
                           .replace("新しいパスワード:", "新しいパスワード")
                           .replace("新しいパスワード(確認用):", "新しいパスワード(確認用)")

    );
  });
});

$(function(){
  $(".sns_text").on("click", function(){
    $('.container.facebook').fadeIn(800);
    $('.container.google').fadeIn(800);
  });
});

$(function(){
  $('form[data-validate]').on('input', function () {
    $(this).find(':submit').attr('disabled', !this.checkValidity());
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

$(function(){
  $('.image_item').mouseover(function() {
    $(this).css('filter', 'brightness(50%)');
  }).mouseout(function(){
    $(this).css('filter', 'brightness(100%)');
  });
});

$(function(){
  $('.hide_text').mouseover(function() {
    $(this).find("p.text").css('display', 'block');
    $(this).find("p.text").css('color', 'white');
  }).mouseout(function(){
    $(this).find("p.text").css('display', 'none');
  });
});

$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.last ul a').length) {
      $('#fade-in li.last ul li').fadeOut();
    } else if ($(e.target).closest('li.last ul').length) {

      if ($('#fade-in li.last ul li').css('display') == 'none') {
        $('#fade-in li.last ul li').fadeIn();

      }
    }
  });
});
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.first ul a').length) {
      $('#fade-in li.first ul li').fadeOut();
    } else if ($(e.target).closest('li.first ul').length) {

      if ($('#fade-in li.first ul li').css('display') == 'none') {
        $('#fade-in li.first ul li').fadeIn();
      }
    }
  });
});

$(function(){
  $("#id_live_flag").change(function(){
    var val = $(this).val();
    if (val === '1') {
      $('.vacant').fadeIn();
      $('.vacant_live').fadeIn();
      $('.vacant_live input').attr("required", true);
      $('.calendar').fadeOut();
    } else if (val === "0")  {
      $('.vacant').fadeIn();
      $('.vacant_live').fadeOut();
      $('.calendar').fadeIn();
      $('.calendar input').attr("required", true);
    }
  });
});

$(function(){
  $(document).on('click', function(e) {
    if (!$(e.target).closest('#id_live_flag option[value=1]').length && !$(e.target).closest('.article').length) {
      $('.vacant').fadeOut();
    } else if ($(e.target).closest('#id_live_flag option[value=2]').length) {

      if ($('.vacant').css('display') == 'none') {
        $('#fade-in li.first ul li').fadeIn();
      } else {
        $('#fade-in li.first ul li').fadeOut();
      }
    }
  });
});

$(function(){
  $('form').find('.cancel_date input').removeAttr('required');
  $('form').find('.update_date input').removeAttr('required');
  $('form').find('.start_date input').removeAttr('required');
  $('form').find('.vacant_live input').removeAttr('required');
});
