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
