function streamEmailPopup(){
  var csrf = String(document.getElementsByName("csrfmiddlewaretoken")[0].value);
  var eventID = String(document.getElementsByName("eventID")[0].value);
  var str = '<input type="hidden" name="csrfmiddlewaretoken" value=';
  var str2 = '>';
  var some_html = '<form id="formToFind" method="post" action="/mixMailSignup/" class="wide">';
  some_html += str;
  some_html += csrf;
  some_html += str2;
  some_html += '<input type="text" class="user-mailchimp" placeholder="email" name="email">';
  some_html += '<input type="text" name=id value=';
  some_html += eventID;
  some_html += ' style="display: none">';
  some_html += '<input type="text" name="mixAccess" value="stream" style="display: none">';
  some_html += '<br><br><br>';
  some_html += '<input type="checkbox" name="newsletter" value="newsletter" checked>I want to receive SDS event updates (only Disco Goodness, we don\'t spam)<br><br>';
  some_html += '<input type="checkbox" name="survey" value="survey" checked>i want to participate in the SDS survey to help create a better SDS experience<br>';
  some_html += '</form>';

  bootbox.dialog({
    message: some_html,
    title: "Enter your email to Join the Disco",
    buttons: {
      success: {
        label: "Submit!",
        className: "btn-success",
        callback: function() {
         document.getElementById("formToFind").submit();        
       }
      },
      login: {
        label: "Login",
        className: "btn-success",
        callback: function() {
            var s = "/future.html/?id=";
            s += eventID;
            s += "#login";
            window.location.href = s;
        }
      }
    }
  });
}
function downloadEmailPopup(){
  var csrf = String(document.getElementsByName("csrfmiddlewaretoken")[0].value);
  var eventID = String(document.getElementsByName("eventID")[0].value);
  var str = '<input type="hidden" name="csrfmiddlewaretoken" value=';
  var str2 = '>';
  var eventMixURL = String(document.getElementsByName("eventMix")[0].value);

  var some_html = '<form id="formToFind" method="post" action="/mixMailSignup/" class="wide">';
  some_html += str;
  some_html += csrf;
  some_html += str2;
  some_html += '<input type="text" class="user-mailchimp" placeholder="email" name="email">';
  some_html += '<input type="text" name=id value=';
  some_html += eventID;
  some_html += ' style="display: none">';
  some_html += '<input type="text" name=download value="';
  some_html += eventMixURL;
  some_html += '" style="display: none">';
  some_html += '<br><br><br>';
  some_html += '<input type="checkbox" name="newsletter" value="newsletter" checked>I want to receive SDS event updates (only Disco Goodness, we don\'t spam)<br><br>';
  some_html += '<input type="checkbox" name="survey" value="survey" checked>i want to participate in the SDS survey to help create a better SDS experience<br>';
  some_html += '</form>';

  bootbox.dialog({
    message: some_html,
    title: "Enter your email to Join the Disco",
    buttons: {
      success: {
        label: "Submit!",
        className: "btn-success",
        callback: function() {
         document.getElementById("formToFind").submit();        
        }
      },
      login: {
        label: "Login",
        className: "btn-success",
        callback: function() {
            var s = "/future.html/?id=";
            s += eventID;
            s += "#login";
            window.location.href = s;
        }
      }
    }
  });
}

function streamLoggedin(){
  var eventID = String(document.getElementsByName("eventID")[0].value);
  var s = "/stream.html/?id=";
  s += eventID;
  window.location.href = s;
}



