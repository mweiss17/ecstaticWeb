function arrangeEvents(){
  var doneTheStuff = false;
  if (!doneTheStuff) {
    doneTheStuff = true;
    var events = document.getElementsByName('eventBox');

    

      if(events.length==1){
        events[0].style.height = "100%";
        events[0].style.width="100%";
        events[0].style.background = "cover";

      }
      if(events.length==2){
        events[0].style.width="50%";
        events[0].style.height = "100%";
        events[1].style.width="50%";
        events[1].style.height = "100%";
        events[1].style.left = "50%";
      }
      if(events.length==3){
        events[0].style.width="33.3%";
        events[0].style.height = "100%";
        events[1].style.width="33.3%";
        events[1].style.height = "100%";
        events[1].style.left = "33.3%";
        events[2].style.width="33.3%";
        events[2].style.height = "100%";
        events[2].style.left = "66%";
    }
      if(events.length==4){
        events[0].style.width="50%";
        events[0].style.height = "50%";

        events[1].style.width="50%";
        events[1].style.height = "50%";
        events[1].style.left = "50%";

        events[2].style.width="50%";
        events[2].style.height = "50%";
        events[2].style.left = "50%";
        events[2].style.top = "50%";

        events[3].style.width="50%";
        events[3].style.height = "50%";
        events[3].style.left = "50%";
        events[3].style.top = "50%";
    }

      if(events.length==5){
        events[0].style.width="33.3%";
        events[0].style.height = "50%";
        events[1].style.width="33.3%";
        events[1].style.height = "50%";
        events[1].style.left = "33.3%";
        events[2].style.width="33.3%";
        events[2].style.height = "50%";
        events[2].style.left = "66%";
    }

      if(events.length==6){
        events[0].style.width="33.3%";
        events[0].style.height = "50%";
        events[1].style.width="33.3%";
        events[1].style.height = "50%";
        events[1].style.left = "33.3%";
        events[2].style.width="33.3%";
        events[2].style.height = "50%";
        events[2].style.left = "66.4%";
    }
  }
}  


