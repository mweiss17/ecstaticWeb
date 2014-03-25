function showRemaining() {
  for(i=0; i < secondsLeftArray.length; i++)
  {
    /*if(future=='True' && secondsLeftArray[i] <= 300){
      window.location.assign('/stream.html/?title='+eventTitle);
    }*/
    if(future!='True' && secondsLeftArray[i] <= 0 && secondsLeftArray[i] >= -7200)
    {
      document.getElementById("eventID"+upcomingEventsIDs[i]).innerHTML = "IN PROGRESS!";
      continue;
    }
      secondsLeftArray[i] = secondsLeftArray[i] - 1;
      var days = Math.floor( secondsLeftArray[i] / 86400);
      var hours = Math.floor( (secondsLeftArray[i] / 3600) % 24);
      var minutes = Math.floor(( secondsLeftArray[i] / 60) % 60);
      var seconds = Math.floor( secondsLeftArray[i] % 60);
      document.getElementById("eventID"+upcomingEventsIDs[i]).innerHTML = days + 'days ';
      document.getElementById("eventID"+upcomingEventsIDs[i]).innerHTML += hours + 'hrs ';
      document.getElementById("eventID"+upcomingEventsIDs[i]).innerHTML += minutes + 'mins ';
      document.getElementById("eventID"+upcomingEventsIDs[i]).innerHTML += seconds + 'secs';
  }
}