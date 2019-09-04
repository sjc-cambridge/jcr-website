$(function () {
  $(document).scroll(function () {
    var $nav = $(".fixed-top");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});

$(function () {
  var lastScrollTop = 0;
  var $navbar = $('.navbar');
  var $heading = $('#navbarheading');

  $(window).scroll(function (event) {
    var st = $(this).scrollTop();

    if (st > lastScrollTop && st > $heading.height()) { // scroll down
      $navbar.slideUp();

    } else { // scroll up
      $navbar.slideDown();
    }
    lastScrollTop = st;
  });
});