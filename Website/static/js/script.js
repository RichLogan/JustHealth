$(window).resize (
    function () {
        layout();
    }
);

//check form fields are not null
function validateForm() {
    var x = document.forms["register"]["username","firstName","surname","dob", "email", "confirmPassword", "password"].value;
    if (x==null || x=="") {
        alert("All fields be filled out");
    }
}

//check email is vaild and correct format
function validateEmail() {
    var x = document.forms["register"]["email"].value;
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        alert("Not a valid e-mail address");
        return false;
    }
}

//check dob is correct format
function validateDob() {
  var pattern =/^([0-9]{2})-([0-9]{2})-([0-9]{4})$/;
  if(pattern.test(dob) ==false {
     alert("Invalid date");
     return false;
   }
}
