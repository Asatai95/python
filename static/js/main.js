// inputで受け取れる画像タイプの指定
$(function(){
  if ( $("input[name=company_image]").length ) {
    $("input[name=company_image]").attr("accept", ".png, .jpg, .jpeg");
  }
});

// 業者ページ, サイドバー表示の切り替え
$(function(){
  $(document).ready(function () {
    var sides = ["left", "top", "right", "bottom"];
    for (var i = 0; i < sides.length; ++i) {
        var cSide = sides[i];
        $(".sidebar." + cSide).sidebar({side: cSide});
    }

    $(".btn_sidebar[data-action]").on("click", function () {
      $(".sidebar.first").removeClass("first");
      if ($(".content_main_top").hasClass("action") ) {
        if ( $(".content_main_top").hasClass("side") ) {
          $(".content_main_top").removeClass("side");
          $(".content_main_top").removeClass("action");
        } else {
          $(".content_main_top").addClass("side");
        }
      } else if ( $(".content_main_top").hasClass("side") )  {
        if ($(".content_main_top").hasClass("action")){
          $(".content_main_top").removeClass("side");
          
        } else {
          $(".content_main_top").removeClass("side");
          $(".content_main_top").removeClass("action"); 
        }
      } else {
        $(".content_main_top").addClass("action");
      }

      var $this = $(this);
      var action = $this.attr("data-action");
      var side = $this.attr("data-side");
      $(".sidebar." + side).trigger("sidebar:" + action);
       
      return false;
    });
  });
});

// ボタンエフェクト
$(function() {
  $(document).on('click', function(e) {
    if ($(e.target).closest('.back_login_botton').length) {
      $(".login_menu").fadeOut();
      $(".content_main").css("filter", "brightness(100%)");
      $('.content_main').css("position", "");
    } 
  });
});

// トップページの要素を下からフェードイン
$(function(){
  $(document).ready(function(){
    $('body').each(function(){
      $(this).find(".item").fadeIn(800);
      $(this).find('.item').css("transition-duration", "1.0s");
      $(this).find(".item").css("margin-top", "20px");
    });
  });
});

$(function() {
  $('.item').css('opacity', '0');
  $('.item').on('inview', function(event, isInView, visiblePartX, visiblePartY) {
  	if (isInView) {
      $(this).stop().animate({opacity:1}, 300);
  	} else {
  		$(this).stop().animate({opacity: 0}, 300);
  	}
  });
});

// // ナビゲーションバー
// $(document).ready(function() {
//   var pagetop = $('.navbar-brand');
//   pagetop.click(function () {
//     $('body, html').animate({ scrollTop: 0 }, 500);
//     return false;
//   });
// });

$(function(){
  $(document).ready(function(){
    $('.login_after_title').fadeIn();
  });
});

$(function(){
  $('.main_topic_1').on("click", function(){
    $('.sample_selection.rent').fadeOut();
    $('.sample_selection.park').fadeIn();
    $('.form-1 a input').attr('value', '0');
  });
  $('.main_topic_2').on("click", function(){
    $('.sample_selection.rent').fadeOut();
    $('.sample_selection.park').fadeIn();
    $('.form-2 a input').attr('value', '1');
  });
  $('.main_topic_3').on("click", function(){
    $('.sample_selection.park').fadeOut();
    $('.sample_selection.address').fadeIn();
    $('.form-3 a input').attr('value', '0');
  });
  $('.main_topic_4').on("click", function(){
    $('.sample_selection.park').fadeOut();
    $('.sample_selection.address').fadeIn();
    $('.form-4 a input').attr('value', '1');
  });
  $(".form-5 input").focusin(function(){
    $(".form-5 input").css('box-shadow', '0 0 8px blue');
  });
  $(".form-5 input").focusout(function(){
    $(".form-5 input").css('box-shadow', '0 0 0');
  });
});

// 必要ないかも?
$(function() {
  $('.ribbon').on('click', function(e) {
    if (!$(e.target).closest(this).length ) {
      $(this).find('.ribbon12').fadeIn();
      $(this).find('.balloon1-top').fadeOut();
    } else if ($(e.target).closest(this).length) {
      if ($(this).find('.balloon1-top').css('display') == 'none') {
        $(this).find('.ribbon12').fadeOut();
        $(this).find('.balloon1-top').fadeIn();
      } else {
        $(this).find('.ribbon12').fadeIn();
        $(this).find('.balloon1-top').fadeOut();
      }
    }
  });
});


// いいね機能, ハートの表示の切り替え
$(function() {
  $('input[id=commit]').on("click", function(){
    $(this).attr('id', 'heart');
  });
});

$(function() {
  $('input[id=heart]').on("click", function(){
    $(this).attr('id', 'commit');
  });
});

$(function() {
  $('.item').each(function(e) {
    if (!$(e.target).closest(this).length ) {
      if ($(this).find('.heart').length){
        $(this).find('.dark').fadeOut();
      } else {
        $(this).find('.dark').fadeIn();
      }
    }
  });
});

// ログインページ、SNSログインのURLを押して、要素をドロップダウン
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.sns_text a').length && !$(e.target).closest('.container').length) {
      $('.container.facebook').fadeOut();
      $('.container.google').fadeOut();
    } else if ($(e.target).closest('.sns_text a').length) {

      if ($('.container.facebook').css('display') == 'none') {
        $('.container.facebook').fadeIn();
        $('.container.google').fadeIn();
      } else {
        $('.container.facebook').fadeOut();
        $('.container.google').fadeOut();
      }
      e.preventDefault();
    }
  });
});

$(function(){
  $('form[data-validate]').on('input', function () {
    $(this).find(':submit').attr('disabled', !this.checkValidity());
  });
});

// 画像をプレビューに表示
$(function(){
  $('form').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;
    if(file.type.indexOf("image") < 0){
      return false;
    }

    reader.onload = (function(file) {
      return function(e) {
        $preview.empty();
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
  $('#chat_img_preview').on('change', function(e) {

    $("#img_id").css("display", "block");
    $(".chat_room > input ").css("display", "none");
    $("#img_id > #chat-message-input").attr("readonly", true);
    $('#chat-message-submit').removeAttr('disabled');
    $(".img-view").fadeIn(800);

    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview_chat");
        t = this;
    if(file.type.indexOf("image") < 0){
      return false;
    }

    reader.onload = (function(file) {
      return function(e) {
        $preview.empty();
        $preview.append($('<img>').attr({
                  src: e.target.result,
                  class: "img_preview_chat",
                  title: file.name
              }));
      };
    })(file);

    reader.readAsDataURL(file);
  });
});

$(function(){
  $(".css-cancel").on("click", function(){
    $(".preview_chat img").remove();
    $(".img-view").css("display", "none");
    $("#img_id").css("display", "none");
    $(".chat_room > input ").css("display", "inline-block");
    $('#chat-message-submit').attr('disabled', 'disabled');
  });
});

// 画像をプレビューに表示
$(function(){
  $('#id_files').change(function(){
    if ( !this.files.length ) {
      return;
    }
    $('.preview_files').text('');

    var $files = $(this).prop('files');
    var len = $files.length;
    for ( var i = 0; i < len; i++ ) {
      var file = $files[i];
      var fr = new FileReader();

      fr.onload = function(e) {
        var src = e.target.result;
        var img = '<img src="'+ src +'">';
        $('.preview_files').append(img);
      }

      fr.readAsDataURL(file);
    }

    $('.preview_files').css('display','block');
  });
});

// 画像をプレビューに表示
$(function(){
  $('#id_article_image').change(function(){
    if ( !this.files.length ) {
      return;
    }
    $('.preview_files').text('');

    var $files = $(this).prop('files');
    var len = $files.length;
    for ( var i = 0; i < len; i++ ) {
      var file = $files[i];
      var fr = new FileReader();

      fr.onload = function(e) {
        var src = e.target.result;
        var img = '<img src="'+ src +'">';
        $('.preview_files').append(img);
      }

      fr.readAsDataURL(file);
    }

    $('.preview_files').css('display','block');

  });
  try { 
    var t = $(".img_preview_chat").offset().top;
    var p = t - $(".chat_room_contents").height();
    console.log(p)
    console.log(t)
   
    $("div.chat_room_contents").animate({
    scrollTop: $(".img_preview_chat").offset().top,}, { duration: 2000, easing: 'swing', });
    
  } catch {}
});

$(function(){
  if($('.img_preview').length){
    $(".sample_img").css("display", "none");
  }
});

$(function(){
  $('.img_item').mouseover(function() {
    $(this).find(".hide_text").css('display', 'block');
    $(this).find("img").css('filter', 'brightness(50%)');
  }).mouseout(function(){
    $(this).find(".hide_text").css('display', 'none');
    $(this).find("img").css('filter', 'brightness(100%)');
  });
});


// 検索ボックス表示、ドロップメニュー
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main_user').length && !$(e.target).closest('li.last ul a').length) {
      $('#fade-in li.last ul li').fadeOut();
    } else if ($(e.target).closest('li.last ul').length) {

      if ($('#fade-in li.last ul li').css('display') == 'none') {
        $('#fade-in li.last ul li').fadeIn();
      } else {
        $('#fade-in li.last ul li').fadeOut();
      }
    }
  });
});

// 検索ボックス表示、ドロップメニュー
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.middle ul a').length) {
      $('#fade-in li.middle ul li').fadeOut();
    } else if ($(e.target).closest('li.middle ul').length) {

      if ($('#fade-in li.middle ul li').css('display') == 'none') {
        $('#fade-in li.middle ul li').fadeIn();
      } else {
        $('#fade-in li.middle ul li').fadeOut();
      }
    }
  });
});

// 検索ボックス表示、ドロップメニュー
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.first ul a').length) {
      $('#fade-in li.first ul li').fadeOut();
    } else if ($(e.target).closest('li.first ul').length) {

      if ($('#fade-in li.first ul li').css('display') == 'none') {
        $('#fade-in li.first ul li').fadeIn();
      } else {
        $('#fade-in li.first ul li').fadeOut();
      }
    }
  });
});

// 検索ボックス表示、ドロップメニュー
$(function() {
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.first ul a').length) {
      $('#fade-in li.price ul li').fadeOut();
    } else if ($(e.target).closest('li.price ul').length) {

      if ($('#fade-in li.price ul li').css('display') == 'none') {
        $('#fade-in li.price ul li').fadeIn();
      } else {
        $('#fade-in li.price ul li').fadeOut();
      }
    }
  });
});

// 検索中の項目表示
$(function(){

  $(".view_checkbox").each(function(){
    if ($(this).find("li").hasClass("check")){
      $(this).fadeIn();
      if ($(".room_word").text() != "間取り: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".room_word").fadeIn();
        });
      } 
      if ($(".live_word").text() != "空室状況: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".live_word").fadeIn();
        });
      } 
      if ($(".rent_word").text() != "家賃: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".rent_word").fadeIn();
        });
      } 
      if ($(".name_word").text() != "物件名称: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".name_word").fadeIn();
        });
      } 
      if ($(".floor_word").text() != "階数: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".floor_word").fadeIn();
        });
      } 
      if ($(".address_word").text() != "物件所在地: ") {
        $(".view_checkbox").each(function(){
          $(this).find(".address_word").fadeIn();
        });
      } 
    }
  });
});

// 検索ボックス, チェックボックス入力内容表示
$(function() {
  $('#fade-in li ul li a').click(function(){
    $(".view_checkbox").fadeIn();
    if ($(this).find('input[name="room"]').prop('checked')) {
      $(this).find('input[name="room"]').prop('checked', false);
      var word = $(this).find('input[name="room"]').val(); 
      $(".room_word").each(function(){
        var txt = $(this).text();
        $(this).text(
          txt.replace(word , "")
        )
        
      });
    } else {
      $(this).find('input[name="room"]').prop('checked', true);
      var word = $(this).find('input[name="room"]').val(); 
      // console.log(word)
      if (word == undefined) {
        console.log(word)
      } else {
        if ($(".room_word").css("display") == "none") {
          $(".room_word").fadeIn();
        } 
        
        if ( $(".room_word").text().indexOf(word) != -1 ) {
          return false
        } else {
          $(".room_word").append(word+" ");
        }
      }
    }

    if ($(this).find('input[name="live"]').prop('checked')) {
      $(this).find('input[name="live"]').prop('checked', false);
      var word = $(this).find('input[name="live"]').val(); 
      if (word == "0"){
        word = "空室あり"
      } else if (word=="1") {
        word = "空室なし"
      }
      $(".live_word").each(function(){
        var txt = $(this).text();
        $(this).text(
          txt.replace(word , "")
        )
      });

    } else {
      $(this).find('input[name="live"]').prop('checked', true);
      var word = $(this).find('input[name="live"]').val(); 

      if (word == "0") {
        word = "空室あり"
      } else if (word == "1") {
        word = "空室なし"
      } 
      if (word == undefined) {
        console.log(word)
      } else {
        if ($(".live_word").css("display") == "none") {
          $(".live_word").fadeIn();
        }
        if ( $(".live_word").text().indexOf(word) != -1 ) {
          return false
        } else {
          $(".live_word").append(word+" ");
        }
      }
    }

    if ($(this).find('input[name="floor"]').prop('checked')) {
      $(this).find('input[name="floor"]').prop('checked', false);
      var word = $(this).find('input[name="floor"]').val(); 
      $(".floor_word").each(function(){
        var txt = $(this).text();
        $(this).text(
          txt.replace(word , "")
        )
      });
    } else {
      $(this).find('input[name="floor"]').prop('checked', true);
      var word = $(this).find('input[name="floor"]').val(); 
      
      if (word == undefined) {
        console.log(word)
      } else {
        if ($(".floor_word").css("display") == "none" ) {
          $(".floor_word").fadeIn();
        }
        if ( $(".floor_word").text().indexOf(word) != -1 ) {
          return false
        } else {
          $(".floor_word").append(word+" ");
        }
      }
    }

    if ($(this).find('input[name="price"]').prop('checked')) {
      $(this).find('input[name="price"]').prop('checked', false);
      var word = $(this).find('input[name="price"]').val(); 
    
      if (word == "1") {
        word = "3万円以上"
      } else if (word == "2") {
        word = "4万円~6万円"
      } else if (word == "3") {
        word = "7万円以上"
      }
      $(".rent_word").each(function(){
        var txt = $(this).text();
        $(this).text(
          txt.replace(word , "")
        )
      });
    } else {
      $(this).find('input[name="price"]').prop('checked', true);
      var word = $(this).find('input[name="price"]').val(); 
      
      if (word == "1") {
        word = "3万円以下"
      } else if (word == "2") {
        word = "4万円~6万円"
      } else if (word == "3") {
        word = "7万円以上"
      }
      if (word == undefined) {
        console.log(word)
      } else {
        if ($(".rent_word").css("display") == "none") {
          $(".rent_word").fadeIn();
        }
        if ( $(".rent_word").text().indexOf(word) != -1 ) {
          return false
        }
        $(".rent_word").append(word+" ");
      }
    }
  });
});


// 物件の名称, 検索ワード表示
$(function(){
  var $input = $('#sbox');
  var $output = $('.name_word');
  $input.on('input', function(event) {
    if ($(".view_checkbox").css("display") == "none") {
      $(".view_checkbox").fadeIn();
    }
    $(".name_word").fadeIn();
    var value = $input.val();
    $output.text("物件名称: " + value);
  });
});

// 物件所在地, 検索ワード表示
$(function(){
  var $input = $('#search');
  var $output = $('.address_word');
  $input.on('input', function(event) {
    if ($(".view_checkbox").css("display") == "none") {
      $(".view_checkbox").fadeIn();
    }
    $(".address_word").fadeIn();
    var value = $input.val();
    $output.text("物件所在地: " + value);
  });
});


// 物件情報入力、カレンダー関連
$(function(){
  $("#id_live_flag").change(function(){
    var val = $(this).val();
    if (val === '1') {
      $('.vacant').fadeIn();
      $('.vacant_live').fadeIn();
      $('.vacant_live input').attr("required", true);
      $('.calendar').fadeOut();
      $('.calendar input').removeAttr("required");
    } else if (val === "0")  {
      $('.vacant').fadeIn();
      $('.vacant_live').fadeOut();
      $('.calendar').fadeIn();
      $('.calendar input').attr("required", true);
      $('.vacant_live input').removeAttr("required");
    } else {
      $('.vacant_live input').removeAttr("required");
      $('.vacant_live').fadeOut();
      $('.calendar input').removeAttr("required");
      $('.calendar').fadeOut();
    }
  });
});

// 物件情報入力フォーム、空室情報
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

// 物件詳細、画像スライドショー
$(function(){
  $(document).ready(function(){
    $('div.image_contents').slick({
     accessibility: true,
     autoplay: true,
     arrows: true,
     slidesToShow: 1,
     slidesToScroll: 1,
     arrows: false,
     fade: true,
     asNavFor: 'div.image_sub_contents'
    });
  });
});

$(function(){
  $(document).ready(function(){
    $('div.image_sub_contents').slick({
     accessibility: true,
     autoplay: true,
     arrows: true,
     slidesToShow: 3,
     slidesToScroll: 1,
     asNavFor: 'div.image_contents',
     dots: true,
     centerMode: true,
     focusOnSelect: true
    });
  });
});

// エラー表示
$(function(){
  $('span.error').each(function(){
    if ( $(this).text() != "" ) {
      $(this).css("display", "block");
    }
  });
});


$(function(){
  $('label').each(function(){
    var divText = $(this).html();
    if (divText.match(':')){
      $(this).html($(this).text().slice(0,-1));
    }
  });
});


// ロゴを押したら、トップにスクロール
$(window).on('scroll', function () {
  var doch = $(document).innerHeight(); 
  var winh = $(window).innerHeight(); 
  var bottom = doch - winh; 
  if (bottom <= $(window).scrollTop() + 30) {
    $('.row.mx-auto').fadeIn();
  } else {
    $('.row.mx-auto').fadeOut();
  }

});

// チャット機能、
// 内容送信 → コメントボックス表示
// 内容送信後、ページ最下層にスクロール
$(function(){
  try{
    $("html,div.chat_room_contents").animate({scrollTop:$('#chat-log').offset().top, },{ duration: 2000, easing: 'swing', });
  }catch {

  }
  try { 
    var t = $("#chat-log").offset().top;
    var p = t - $(".chat_room_contents").height();
    if ( t > p ){  
      $("div.chat_room_contents").animate({
      scrollTop: $("#chat-log").offset().top,}, { duration: 2000, easing: 'swing', });
    }
  } catch {}
});

// チャット入力確認後に送信ボタン表示
$(function() {
  if ( $('.chat_room > #chat-message-input').val() == "" ) {
    $('.chat_room > #chat-message-submit').attr('disabled', 'disabled');
  }
  $('.chat_room > #chat-message-input').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('.chat_room > #chat-message-submit').removeAttr('disabled');
    } else {
      $('.chat_room > #chat-message-submit').attr('disabled', 'disabled');
    }
  });
});

// $(function(){

//   $("#chat-message-submit").on("click", function(){
//     $(".img-view.first").css("display", "none")
//   });
// });

// ユーザーページ(業者)、チャット可能ユーザーの表示
$(function(){
  $(".customer_list ul li a").on("click", function(e){
    e.preventDefault();
    $(".customer_list").fadeIn();
  });
});

$(function() {
  $(".content").on('click', function(e) {
    if (!$(e.target).closest('div.inline .stream-content .profile_img').length) {
      $(e.target).next("div.customer_list").fadeOut();
    } else if ($(e.target).closest('div.inline .stream-content .profile_img').length) {
      if ( $(this).next("div.customer_list").css('display') == 'none') {
        $(this).next("div.customer_list").fadeIn();
      } else {
        $(this).next("div.customer_list").fadeOut();
      }
    }
  });
});


$(function(){
  if ($('button.stripe-button-el>span').length) {
    $('button.stripe-button-el>span').text("プランの変更");
  }
});

$(function(){
  $(".article_remake").on("click", function(){
    $(this).next('div').children(".remake_article").animate({
      width : 'toggle'
    }, 'normal')
  });
  
  $(".article_name.nak").on("click", function(){
    $(".remake_article").css("width", "50%");
    $('.remake_article_sub.nak').animate({
      width : 'toggle'
    }, 'normal')
  });
  $(".article_name.gi").on("click", function(){
    $(".remake_article").css("width", "50%");
    $('.remake_article_sub.gi').animate({
      width : 'toggle'
    }, 'normal')
  });
  $(".article_name.naha").on("click", function(){
    $(".remake_article").css("width", "50%");
    $('.remake_article_sub.naha').animate({
      width : 'toggle'
    }, 'normal')
  });
  $(".article_name.oki").on("click", function(){
    $(".remake_article").css("width", "50%");
    $('.remake_article_sub.oki').animate({
      width : 'toggle'
    }, 'normal')
  });

});

$('.sel').each(function() {
  $(this).children('select').css('display', 'none');
  
  var $current = $(this);
  
  $(this).find('option').each(function(i) {
    if (i == 0) {
      $current.prepend($('<div>', {
        class: $current.attr('class').replace(/sel/g, 'sel__box')
      }));
      
      var placeholder = $(this).text();
      $current.prepend($('<span>', {
        class: $current.attr('class').replace(/sel/g, 'sel__placeholder'),
        text: placeholder,
        'data-placeholder': placeholder
      }));
      
      return;
    }
    
    $current.children('div').append($('<span>', {
      class: $current.attr('class').replace(/sel/g, 'sel__box__options'),
      text: $(this).text()
    }));
  });
});

$('.sel').click(function() {
  $(this).toggleClass('active');
});

$('.sel__box__options').click(function() {
  var txt = $(this).text();
  var index = $(this).index();
  
  $(this).siblings('.sel__box__options').removeClass('selected');
  $(this).addClass('selected');
  
  var $currentSel = $(this).closest('.sel');
  $currentSel.children('.sel__placeholder').text(txt);
  $currentSel.children('select').prop('selectedIndex', index + 1);
});

$(function(){
  $('.add-image').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0];
    if(file["name"] != "") {
      $(".icon-hi").fadeIn();
    } else {
      $(".icon-hi").fadeOut();
    }
  });
});

$(function(){
  $(".switch__input").on("click", function(){
    if ($(".get_not_info").text() == "空室情報を受け取る") {
      $(".get_not_info").text("空室情報を受け取らない");
    } else {
      $(".get_not_info").text("空室情報を受け取る");
    }
  });
});

$(function(){
  $(".switch__input").on("click", function(){
    if ( $("#checkbutton").val() == "0" )  {
      $("#checkbutton").val("1");
    } else {
      $("#checkbutton").val("0");
    }
  });
});

// $(function(){
//   $(".info_live_li").each(function(){
//     $(this).find(".send_info_mail").children(".info_live_mail").mouseover(function(){
//       $(this).find("live_info_comment").fadeIn();
//     }).mouseout(function() {
//       $(this).find("live_info_comment").fadeOut();
//   });
// });


// メール一括送信
// ユーザーの表示数制限
// もっと見るリンク
// 元に戻すリンク

$(function() {
  // 表示させる要素の総数をlengthメソッドで取得
  var $numberListLen = $("#number_list ul").length;
  // デフォルトの表示数
  var defaultNum = 5;
  // ボタンクリックで追加表示させる数
  var addNum = 5;
  // 現在の表示数
  var currentNum = 0;

  $("#number_list").each(function() {
    // moreボタンを表示し、closeボタンを隠す
    $(this).next(".more_button").find("#more_btn").show();
    $(this).next(".more_button").find("#close_btn").hide();

    // defaultNumの数だけ要素を表示
    // defaultNumよりインデックスが大きい要素は隠す
    $(this).find("ul:not(:lt("+defaultNum+"))").hide();

    // 初期表示ではデフォルト値が現在の表示数となる
    currentNum = defaultNum;

    // moreボタンがクリックされた時の処理
    $(this).next(".more_button").find("#more_btn").click(function() {
     
      // 現在の表示数に追加表示数を加えていく
      currentNum += addNum;

      // 現在の表示数に追加表示数を加えた数の要素を表示する
      $("#number_list").find("ul:lt("+currentNum+")").slideDown();

      // 表示数の総数よりcurrentNumが多い=全て表示された時の処理
      if($numberListLen <= currentNum) {
        // 現在の表示数をデフォルト表示数へ戻す
        currentNum = defaultNum;
        
        // インデックス用の値をセット
        indexNum = currentNum - 1;
       
        // moreボタンを隠し、closeボタンを表示する
        $("#number_list").next(".more_button").find("#more_btn").hide();
        $("#number_list").next(".more_button").find("#close_btn").show();

        // closeボタンがクリックされた時の処理
        $("#number_list").next(".more_button").find("#close_btn").click(function() {
          // デフォルト数以降=インデックスがindexNumより多い要素は非表示にする
          $("#number_list").find("ul:gt("+indexNum+")").slideUp();

          // closeボタンを隠し、moreボタンを表示する
          $("#number_list").next(".more_button").find("#close_btn").hide();
          $("#number_list").next(".more_button").find("#more_btn").show();
        });
      }
    });
  });
});

// マイページ
// 画面幅に合わせて、要素のwidthのサイズを変更
$(function(){
  if ($("body").width() < 435 ){
    if( $(".main_mypage div.main_content .stream").length ) {
      $(".sec2_info_img.pc").css("display", "none");
      $(".sec2_info_img.sp").css("display", "block");
    }
  } else {
    $(".sec2_info_img.pc").css("display", "block");
    $(".sec2_info_img.sp").css("display", "none");
  }
});

$(function(){
  if ($("body").width() > 435 ){
    $('.sec5_content').slick({
      infinite: true,
      slidesToShow: 3,
      slidesToScroll: 3,
      dots: true
    });
  }
});


$('#chat-message-input').bind('keydown keyup keypress change', function() {
  if ( $(this).val().length > 0 ) {
    $("#img_id").css("display", "none")
    $(".chat_room > input ").css("display", "inline-block")
  } 
});
