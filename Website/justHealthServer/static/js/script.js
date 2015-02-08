//$(window).resize (
//    function () {
//        layout();
//    }
//);

function validateFormResetPassword() {
    var x = document.forms["resetpassword"]["username","confirmdob", "confirmemail", "confirmnewpassword", "newpassword"].value;
    if (x==null || x=="") {
        alert("All fields be filled out");
    }
}

//validate email address format
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(email);
}

//password checking function
//(http://runnable.com/UfJrnXtk2tZXAAA1/how-to-check-password-strength-using-jquery)
function checkStrength(password) {
	//default strength
	var strength = 0

	//if the password length is less than 6, return message
	if (password.length < 6) {
		$('#result').removeClass()
		$('#result').addClass('passwordWeak')
		return 'Weak'
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
		$('#result').addClass('passwordWeak');
		return 'Weak'
	}
	else if (strength == 2 )
	{
		$('#result').removeClass();
		$('#result').addClass('passwordGood');
		return 'Good'
	}
	else
	{
		$('#result').removeClass();
		$('#result').addClass('passwordStrong');
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
    var confirmPassword = document.getElementById('confirmPassword');
    //Store the Confimation Message
    var message = document.getElementById('confirmationMessage');
    //Set field background colours
    var yesColour = "#30D917";
    var noColour = "#DF111C";

    //Compare the values in the password field and the confirmation field
    if(password.value == confirmPassword.value) {
        //The passwords match.
        //Set the colour to yesColour and show message
        confirmPassword.style.backgroundColor = yesColour;
        message.style.color = yesColour;
        message.innerHTML = "<i class='fa fa-check'></i>"
    }
	else {
        //The passwords do not match.
        //Set the colour to noColour and show message
        confirmPassword.style.backgroundColor = noColour;
        message.style.color = noColour;
        message.innerHTML = "<i class='fa fa-times'></i>"
    }
}

function validateFormAddAppointment() {
    var x = document.forms["createappointment"]["name","apptype", "postcode", "startdate", "starttime", "enddate", "endtime"].value;
    if (x==null || x=="") {
        alert("All fields be filled out");
    }
}

function checkPastDate() {
    var selectedDate = $('#startdate').startdate('getDate');
    var now = new Date();
    if (selectedDate < now) {
        // selected date is in the past
        $('#validDate').html('<i class="fa fa-times"></i> Date is in the past').addClass('wrongInputs');
    }
}

// Thanks to: http://www.jquerybyexample.net/2012/06/get-url-parameters-using-jquery.html
function getUrlParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}     