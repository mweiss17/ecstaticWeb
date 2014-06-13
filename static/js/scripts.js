// JavaScript Document <script type="text/javascript">
      $(document).ready(function() {
        $.fn.fullpage({
          'scrollOverflow': false,
          'autoScrolling': false,
          'paddingTop' : '120px',
          'paddingBottom' : '120px',
        });
      });

       <script type="text/javascript">
      $(document).ready(function() {
        $.fn.fullpage({
          'scrollOverflow': false,
          'autoScrolling': false,
          'paddingTop' : '120px',
          'paddingBottom' : '120px',
        });
      });
    </script>

    <script>
      console.log({{etaList}});
      console.log({{upcomingEventsList}});
      var secondsLeftArray = {{etaList}};
      var upcomingEventsIDs = {{upcomingEventsList}};
      var eventTitle = "{{event.title}}";
      var future = "{{future}}";

      var timer;
      timer = setInterval(showRemaining, 1000);
    </script>


    <script type="text/javascript">
      $(document).ready(function() {

        $('.fancybox').fancybox();

        $('.fancybox-media')
        .attr('rel', 'media-gallery')
        .fancybox(
        {
          openEffect : 'fade',
          closeEffect : 'none',
          prevEffect : 'none',
          nextEffect : 'none',

          arrows : false,
          helpers : {
            media : {},
            buttons : {}
          }
        });
      });
    </script>

      console.log({{etaList}});
      console.log({{upcomingEventsList}});
      var secondsLeftArray = {{etaList}};
      var upcomingEventsIDs = {{upcomingEventsList}};
      var eventTitle = "{{event.title}}";
      var future = "{{future}}";

      var timer;
      timer = setInterval(showRemaining, 1000);
  
      $(document).ready(function() {

        $('.fancybox').fancybox();

        $('.fancybox-media')
        .attr('rel', 'media-gallery')
        .fancybox(
        {
          openEffect : 'fade',
          closeEffect : 'none',
          prevEffect : 'none',
          nextEffect : 'none',

          arrows : false,
          helpers : {
            media : {},
            buttons : {}
          }
        });
      });
