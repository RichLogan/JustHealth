//$(window).resize (
//    function () {
//        layout();
//    }
//);

//check form fields are not null
function validateForm() {
    $("form :input").each(function(){
      if ($(this).val() == null || $(this).val() == "") {
        return false;
      }
      return true;
    });
}

//check email is vaild and correct format
function validateEmail() {
    var x = document.forms["register"]["email"].value;
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        document.getElementById('errorEmail').innerHTML = "Not a valid e-mail address";
		alert("Not a valid e-mail address");
        return false;
    }
}


//check dob is correct format
function validateDob() {
  var pattern =/^([0-9]{2})-([0-9]{2})-([0-9]{4})$/;
  var dob = $('dob').val();
  if(pattern.test(dob) == false) {
     alert("Invalid date");
     return false;
	}
}

//password checking function
//(http://runnable.com/UfJrnXtk2tZXAAA1/how-to-check-password-strength-using-jquery)

function checkStrength(password)
{
	//default strength
	var strength = 0

	//if the password length is less than 6, return message
	if (password.length < 6) {
		$('#result').removeClass()
		$('#result').addClass('short')
		return 'Too short'
	}

	//length is okay, continue.

	//if length is 8 characters or more, increase strength value
	if (password.length > 7) strength += 1

	//if password contains both lower and uppercase characters, increase strength value
	if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))  strength += 1

	//if it has numbers and characters, increase strength value
	if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))  strength += 1

	//if it has one special character, increase strength value
	if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/))  strength += 1

	//if it has two special characters, increase strength value
	if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1

	//return messages on strength value

	//if value is less than 2
	if (strength < 2 )
	{
		$('#result').removeClass();
		$('#result').addClass('weak');
		return 'Weak'
	}
	else if (strength == 2 )
	{
		$('#result').removeClass();
		$('#result').addClass('good');
		return 'Good'
	}
	else
	{
		$('#result').removeClass();
		$('#result').addClass('strong');
		return 'Strong'
	}
}

//terms and conditions check
//http://www.the-art-of-web.com/html/html5-checkbox-required/
function terms()
  {
    if(!register.terms.checked) {
      alert("Please indicate that you accept the Terms and Conditions");
      form.terms.focus();
      return false;
    }
    return true;
  }

  //check the registration passwords match
  //http://keithscode.com/tutorials/javascript/3-a-simple-javascript-password-validator.html
 function passwordCheck() {

    //Store the password field objects into variables
    var password = document.getElementById('password');
    var password2 = document.getElementById('password2');
    //Store the Confimation Message
    var message = document.getElementById('confirmationMessage');
    //Set field background colours
    var yesColour = "#30D917";
    var noColour = "#DF111C";

    //Compare the values in the password field and the confirmation field
    if(password.value == password2.value) {
        //The passwords match.
        //Set the colour to yesColour and show message
        password2.style.backgroundColor = yesColour;
        message.style.color = yesColour;
        message.innerHTML = "<i class='fa fa-check'></i>"
    }
	else {
        //The passwords do not match.
        //Set the colour to noColour and show message
        password2.style.backgroundColor = noColour;
        message.style.color = noColour;
        message.innerHTML = "<i class='fa fa-times'></i>"
    }
}
