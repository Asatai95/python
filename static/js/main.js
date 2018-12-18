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
    }
  });
});


$(function(){
  $('form[data-validate]').on('input', function () {
    $(this).find(':submit').attr('disabled', !this.checkValidity());
  });
});

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
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.middle ul a').length) {
      $('#fade-in li.middle ul li').fadeOut();
    } else if ($(e.target).closest('li.middle ul').length) {

      if ($('#fade-in li.middle ul li').css('display') == 'none') {
        $('#fade-in li.middle ul li').fadeIn();

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

$(function() {
  $('#fade-in li ul li a').click(function(){

    if ($(this).find('input[name="room"]').prop('checked')) {
      $(this).find('input[name="room"]').prop('checked', false);
    } else {
      $(this).find('input[name="room"]').prop('checked', true);
    }

    if ($(this).find('input[name="live"]').prop('checked')) {
      $(this).find('input[name="live"]').prop('checked', false);
    } else {
      $(this).find('input[name="live"]').prop('checked', true);
    }

    if ($(this).find('input[name="floor"]').prop('checked')) {
      $(this).find('input[name="floor"]').prop('checked', false);
    } else {
      $(this).find('input[name="floor"]').prop('checked', true);
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
      $('.calendar input').removeAttr("required");
    } else if (val === "0")  {
      $('.vacant').fadeIn();
      $('.vacant_live').fadeOut();
      $('.calendar').fadeIn();
      $('.calendar input').attr("required", true);
      $('.vacant_live input').removeAttr("required");
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
