$(function () {
	$(document).scroll(function () {
		var $nav = $(".fixed-top");
		$nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
	});
});

$(function () {
	var lastScrollTop = 0;
	var inProgress = false;
	var $navbar = $('.navbar');
	var $heading = $('#navbarheading');
	var topHeight = $heading.height() + $navbar.height();

	function animationComplete() {
		inProgress = false;
	};

	$(window).scroll(function (event) {
		var st = $(this).scrollTop();

		if (inProgress === false) {
			inProgress = true
			if (st > lastScrollTop && st > topHeight) { // scroll down
				$navbar.slideUp(undefined, animationComplete);

			} else { // scroll up
				$navbar.slideDown(undefined, animationComplete);
			}
			lastScrollTop = st;
		}
	});

});