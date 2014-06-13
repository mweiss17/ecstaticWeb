setTimeout(function(){
  if ((screen.width > 480) || (screen.height > 480)) {
		$(document).ready(function() {
		  $('.fancybox-media').trigger('click');
		});
  }
}, 100);
