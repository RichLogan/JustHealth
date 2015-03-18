//$(window).resize (
//    function () {
//        layout();
//    }
//);

function checkDate(element, type) {
    // Set Original Message
    message = type + " Date<sup style='color:red'>*</sup>"
    
    // Attempt to convert to date
    var date = new Date($(element).val());
    var now = new Date()
    
    // Show response
    if (date == "Invalid Date") {
      $(element).siblings("label").html(message + ' is not a valid date');
      $(element).parent().removeClass('has-warning');
      $(element).parent().removeClass('has-success');
      $(element).parent().addClass('has-error');
      return false;
    }
    else if (date < now) {
      $(element).siblings("label").html(message + ' is in the past');
      $(element).parent().removeClass('has-error');
      $(element).parent().removeClass('has-success');
      $(element).parent().addClass('has-warning');
    }
    else {
      $(element).siblings("label").html(message);
      $(element).parent().removeClass('has-error');
      $(element).parent().removeClass('has-warning');
      $(element).parent().addClass('has-success');
    }
  }

  function checkTime(element, type) {
    // Set Original Message
    message = type + " Time<sup style='color:red'>*</sup>"
    
    // Check validity of 
    timeStr = $(element).val();

    var time = timeStr.match(/([01]?[0-9]|2[0-3]):[0-5][0-9]/);
      
    // Show Response
    if (!time) {
      // Not a real Time
      $(element).siblings("label").html(message + ' is not a valid date');
      $(element).parent().removeClass('has-warning');
      $(element).parent().removeClass('has-success');
      $(element).parent().addClass('has-error');
      return false;
    }
    else {
      $(element).siblings("label").html(message);
      $(element).parent().removeClass('has-error');
      $(element).parent().removeClass('has-warning');
      $(element).parent().addClass('has-success');
    }
}


// Inspired By http://stackoverflow.com/questions/9776015/jquery-animate-a-rotating-div
function flip(id, degrees) {
  $(id).animate({
        borderSpacing: degrees
    },
    {
        step: function(now,fx) {
            $(this).css('-webkit-transform','rotate('+now+'deg)'); 
            $(this).css('-moz-transform','rotate('+now+'deg)');
            $(this).css('transform','rotate('+now+'deg)');
        }
    });
}

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

function goBack() {
    window.history.back()
}

//Date validation: Courtesy of SmartWebby.com (http://www.smartwebby.com/dhtml/datevalidation.asp)
// Declaring valid date character, minimum year and maximum year
var dtCh= "/";
var minYear=1900;
var maxYear=2100;

function isInteger(s){
    var i;
    for (i = 0; i < s.length; i++){   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function stripCharsInBag(s, bag){
    var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++){   
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function daysInFebruary (year){
    // February has 29 days in any year evenly divisible by four,
    // EXCEPT for centurial years which are not also divisible by 400.
    return (((year % 4 == 0) && ( (!(year % 100 == 0)) || (year % 400 == 0))) ? 29 : 28 );
}
function DaysArray(n) {
    for (var i = 1; i <= n; i++) {
        this[i] = 31
        if (i==4 || i==6 || i==9 || i==11) {this[i] = 30}
        if (i==2) {this[i] = 29}
   } 
   return this
}

function isDate(dtStr){
    var daysInMonth = DaysArray(12)
    var pos1=dtStr.indexOf(dtCh)
    var pos2=dtStr.indexOf(dtCh,pos1+1)
    var strDay=dtStr.substring(0,pos1)
    var strMonth=dtStr.substring(pos1+1,pos2)
    var strYear=dtStr.substring(pos2+1)
    strYr=strYear
    if (strDay.charAt(0)=="0" && strDay.length>1) strDay=strDay.substring(1)
    if (strMonth.charAt(0)=="0" && strMonth.length>1) strMonth=strMonth.substring(1)
    for (var i = 1; i <= 3; i++) {
        if (strYr.charAt(0)=="0" && strYr.length>1) strYr=strYr.substring(1)
    }
    month=parseInt(strMonth)
    day=parseInt(strDay)
    year=parseInt(strYr)
    if (pos1==-1 || pos2==-1){
        $('#dobValidate').html('<i class="fa fa-times"></i> Invalid date, please enter it in the format shown').addClass('wrongInputs');
        return false
    }
    if (strMonth.length<1 || month<1 || month>12){
        $('#dobValidate').html('<i class="fa fa-times"></i> Invalid date, please enter it in the format shown').addClass('wrongInputs');
        return false
    }
    if (strDay.length<1 || day<1 || day>31 || (month==2 && day>daysInFebruary(year)) || day > daysInMonth[month]){
        $('#dobValidate').html('<i class="fa fa-times"></i> Invalid date, please enter it in the format shown').addClass('wrongInputs');
        return false
    }
    if (strYear.length != 4 || year==0 || year<minYear || year>maxYear){
        $('#dobValidate').html('<i class="fa fa-times"></i> Invalid date, please enter it in the format shown').addClass('wrongInputs');
        return false
    }
    if (dtStr.indexOf(dtCh,pos2+1)!=-1 || isInteger(stripCharsInBag(dtStr, dtCh))==false){
        $('#dobValidate').html('<i class="fa fa-times"></i> Invalid date, please enter it in the format shown').addClass('wrongInputs');
        return false
    }
return true
}

function ValidateFormRegister(){
    var dt=document.register.dob
    if (isDate(dt.value)==false){
        dt.focus()
        return false
    }
    return true
}

function ValidateFormProfile(){
    var dt=document.editDetails.dob
    if (isDate(dt.value)==false){
        dt.focus()
        return false
    }
    return true
}

function formcheck1() {
    var fields = $(".appt-item-required").find("select, textarea, input").serializeArray();
    var success = true;
    $.each(fields, function(i, field) {
        if (!field.value && success==true) {
            alert('Please check the you have filled in the required fields');
            success = false;
            return;
        }
    });
    return success;
}

function formcheck2() {
    var fields = $(".code-required").find("input").serializeArray();
    var success = true;
    $.each(fields, function(i, field) {
        if (!field.value && success==true) {
            alert('Please check the code is correct and try again');
            success = false;
            return;
        }
    });
    return success;
}