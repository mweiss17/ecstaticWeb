$(function() {
  var controller = new ScrollMagic.Controller();

  var blockTween = new TweenMax.to('#cover', 1.0, {
    backgroundColor: 'red'
  });

  var containerScene = new ScrollMagic.Scene({
      offset: 340, // start scene after scrolling for 100px
      triggerElement: '#container'
    })
    .setTween(blockTween)
    .addIndicators()
    .addTo(controller);

});

