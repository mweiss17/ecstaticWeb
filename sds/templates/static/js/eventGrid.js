  var events = document.getElementsByName("eventBox");

  count = 0;
  for (var i=0, n=events.length; i<n; ++i) {
    if (events[i].id == "eventBox") {
      ++count;
    }
  }
  console.log(events)

  if(count==1){
    document.getElementById('eventBox').style.width="100%";
    document.getElementById('eventBox').style.height = "100%";
  }
  if(count==2){
    events[0].style.width="50%";
    events[0].style.height = "100%";
    events[1].style.width="50%";
    events[1].style.height = "100%";
    events[1].style.left = "50%";
  }
  if(count==3){
    events[0].style.width="33%";
    events[0].style.height = "100%";
    events[1].style.width="33%";
    events[1].style.height = "100%";
    events[1].style.left = "33%";
    events[2].style.width="33%";
    events[2].style.height = "100%";
    events[2].style.left = "66%";
}
  if(count==4){
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

  if(count==5){
    events[0].style.width="33%";
    events[0].style.height = "100%";
    events[1].style.width="33%";
    events[1].style.height = "100%";
    events[1].style.left = "33%";
    events[2].style.width="33%";
    events[2].style.height = "100%";
    events[2].style.left = "66%";
}

  if(count==6){
    events[0].style.width="33%";
    events[0].style.height = "100%";
    events[1].style.width="33%";
    events[1].style.height = "100%";
    events[1].style.left = "33%";
    events[2].style.width="33%";
    events[2].style.height = "100%";
    events[2].style.left = "66%";
}
