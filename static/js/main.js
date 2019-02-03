$(function(){
  if ( $("input[name=company_image]").length ) {
    $("input[name=company_image]").attr("accept", ".png, .jpg, .jpeg");
  }
});

$(document).ready(function () {
  var sides = ["left", "top", "right", "bottom"];
  for (var i = 0; i < sides.length; ++i) {
      var cSide = sides[i];
      $(".sidebar." + cSide).sidebar({side: cSide});
  }

  $(".btn_sidebar[data-action]").on("click", function () {
      var $this = $(this);
      var action = $this.attr("data-action");
      var side = $this.attr("data-side");
      $(".sidebar." + side).trigger("sidebar:" + action);
      return false;
  });
});

$(function() {
  $(document).on('click', function(e) {
    if ($(e.target).closest('.back_login_botton').length) {
      $(".login_menu").fadeOut();
      $(".content_main").css("filter", "brightness(100%)");
      $('.content_main').css("position", "");
    } 
  });
});

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

$(document).ready(function() {
  var pagetop = $('.navbar-brand');
  pagetop.click(function () {
    $('body, html').animate({ scrollTop: 0 }, 500);
    return false;
  });
});

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
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.container').length && !$(e.target).closest('.content_main').length && !$(e.target).closest('li.first ul a').length) {
      $('#fade-in li.price ul li').fadeOut();
    } else if ($(e.target).closest('li.price ul').length) {

      if ($('#fade-in li.price ul li').css('display') == 'none') {
        $('#fade-in li.price ul li').fadeIn();
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

    if ($(this).find('input[name="price"]').prop('checked')) {
      $(this).find('input[name="price"]').prop('checked', false);
    } else {
      $(this).find('input[name="price"]').prop('checked', true);
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
    } else {
      $('.vacant_live input').removeAttr("required");
      $('.vacant_live').fadeOut();
      $('.calendar input').removeAttr("required");
      $('.calendar').fadeOut();
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

$(window).on('scroll', function () {
  var doch = $(document).innerHeight(); 
  var winh = $(window).innerHeight(); 
  var bottom = doch - winh; 
  if (bottom <= $(window).scrollTop()) {
    $('.row.mx-auto').fadeIn();
  } else {
    $('.row.mx-auto').fadeOut();
  }

});

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

$(function(){
  if ( $(".msg-right").length ) {
    $(".msg-right-sub").css("display", "none")
  } else {
    $(".msg-right-sub").css("display", "block");
  }
});

$(function() {
  if ( $('#chat-message-input').val().length == 0 ) {
    $('#chat-message-submit').attr('disabled', 'disabled');
  }
  $('#chat-message-input').bind('keydown keyup keypress change', function() {
    if ( $(this).val().length > 0 ) {
      $('#chat-message-submit').removeAttr('disabled');
    } else {
      $('#chat-message-submit').attr('disabled', 'disabled');
    }
  });
});

$(function(){
  $(".customer_list ul li a").on("click", function(e){
    e.preventDefault();
    $(".customer_list").fadeIn();
  });
});

$(function(){
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.profile_img a img').length && !$(e.target).closest('.main_content').length) {
      $('.customer_list').fadeOut();
    } else if ($(e.target).closest('.profile_img a img').length) {

      if ($('.customer_list').css('display') == 'none') {
        $('.customer_list').fadeIn();
      } else {
        $('.customer_list').fadeOut();
      }
    }
    
  });
});
