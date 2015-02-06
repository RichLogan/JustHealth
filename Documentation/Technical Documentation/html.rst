========================
HTML Listing
========================

Listed below is the complete list of all HTML pages in JustHealth.

Each HTML page is broken down by its general functionality describing the features of each page.
All of the pages have the standard header and footer from the template page and the content is within a <fieldset> tag. 

------------------------
login.html
------------------------
This page consists of 2 input boxes: Username and Password, which a user is required to fill in in order to be able to gain access to the site.

Below these there is a link called forgot password which on click will show a modal where the user will be required to enter their email address in order to continue with resetting their password.

Above the input boxes there is another think which takes a new user to the registration screen.

------------------------
register.html
------------------------
This page has one form with 10 input fields: Username, Firstname, Surname, Date of Birth, Gender, Account Type, Email Address, Password, Confirm password and a check box to agree to the terms and conditions.

Linked to the terms and conditions is a modal which shows the terms and conditions a user is agreeing to when they click on the link.

------------------------
dashboard.html
------------------------
*This page is only for patients.*

Our website has two home pages, one for patients and one for carers. They are both follow the same style where notifications and reminders appear at the top of the page, their profile picture, username and option to edit their profile in the top left. Also down the side is the connections model, a search option to search other users, a search box to search the NHS website and a settings link to the settings page. 

The connections model, shows in tables all the incoming, outgoing and completed connection. You have the ability to delete current connections or cancel incoming and outgoing ones. To complete an incoming connection a user is required to enter in a 4 digit code provided by the connector in the model.

Underneath the notifications on the this page is all the active patients prescriptions and upcoming appointments. 

All icons are from `font awesome <http://fortawesome.github.io/Font-Awesome/>`_,
which a user can click to take them to the respective page.


------------------------
dashboardCarer.html
------------------------
*This page is only for carers.*

As mentioned above, it follows exactly the same format and the only difference is instead of showing the active prescriptions it shows all the carers current patients. 

------------------------
profile.html
------------------------
On the profile page it displays the current users firstname, surname, dob, gender, account type and their email. Underneath this, there is a link which will allow a user to edit their profile. 


------------------------
deactivate.html
------------------------

This page requires users to select a reason they would like to deactivate their account from a drop down list populated from the database. There is also an option for any other comments and a tick box asking the user if they would like JustHealth to keep their data.

Underneath the tick box there is a link which will open a modal to list reasons on why JustHealth should keep a users data.

------------------------
search.html
------------------------
This page allows user to search for either a carer or patient depending on the account logged in. By typing text into the search bar and clicking search, it will use the information provided to search for a username, firstname or surname matching the information.

Below this is a table to display the search results.

------------------------
resetpassword.html
------------------------
Reset password can only be accessed via the email sent to the user to change their password. This page automatically fills in the username and asks for the user to enter in other details in order to change their password.

Once this is completed the user clicks submit to complete the password change

------------------------
myPatients.html
------------------------
*This page is only for carers.*

My Patients is a page that only carers can view. It shows every patient they are connect to in a list.

If you click on each patient a model drops down to list two options: Prescription and Appointments.
Click on the Prescriptions link and it will open up another model showing two tabs: 'Active' prescriptions for the respective patient and 'Upcoming & Expired' prescriptions for the patient.
Active prescriptions will show green, upcoming blue and expired red.

If you click on either of tab boxes showing the appointment details, it will open up another model giving you the option to edit the details.

If you click on the 'Appointments' tab this will open up another model listing all that patients non private appointments.
There are options here to update and delete current appointments.
On the top left had side there is also the option to add new appointments for that patient.

------------------------
carerAppointments.html
------------------------
*This page is only for carers.*

This page can be found from a carers home page by click on the calendar. This page list all the carers personal appointments.
It is broken into two tabs: Upcoming and Create Appointment.
Clicking on an appointment within the Upcoming tab will allow you to see all the details, delete or edit them if needed.
Clicking on Create Appointment will open a new tab listing a form with the respective fields to fill in to create a new appointment.


------------------------
patientAppointments.html
------------------------
*This page is only for patients.*

This page consists of 3 tabs: Upcoming, Create and Past.

Upcoming shows all the appointment which are in the future. They are listed in order of the closest appointment. By clicking on an appointment it will open up showing more details and a google maps image of where the appointment is.
There are also two buttons update, which allows you to edit the appointment details and delete which deletes the appointment.

Create tab allows a patient to add a new appointment. This tab displays a form with all the respective fields to create a new appointment.
If the patient clicks to mark the appointment private then their carer would not be able to view it.

Past tab displays all appointments that have already happened. They are here to allow the user to recap on past appointments if needed.
They are in a list format and like upcoming if you click on an appointment you will be able to see more details.


------------------------------
patientUpdateAppointment.html
------------------------------
*This page is only for patients.*

This page is accessed through a patient clicking update on an appointment.
It will allow a patient to edit and update an appointment.
The page has place holders in all the fields of the current data from the appointment.
To edit it, a user needs to click in a field and change the text and click update at the confirm the update.


------------------------
prescriptions.html
------------------------
*This page is only for patients.*

It can be access by clicking on the flask on the home page.
This page displays the patients current prescriptions in a list format.
Clicking on the name of the prescription will show the full details of the patients prescriptions.

------------------------
contactUs.html
------------------------
This page can be accessed by clicking on the 'contact us' in the footer. It has a link the JustHealth twitter and a form which had the current users firstname, surname and email automatically filled in. A user can fill in the message field and click submit for an email to be send to JustHealth. 

------------------------
faq.html
------------------------
This page holds a list of questions with on click toggles displaying the answers to the questions.

------------------------
template.html
------------------------
Template.html is the design behind every other page, this page creates the header, footer and container and links jQuery, Font Awesome, DataTables plugin and Our resources.

------------------------
searchNHSDirect.html
------------------------
This page has a form with a search box which sends a POST request to the NHS webiste and searches their website. The result is displayed in a new window.

------------------------
settings.html
------------------------
This page holds basic details on the users and has links in a table for the user to change their password, deativate their account and to connect JustHealth. These are all links which will take the user to a seperate pages. 

------------------------
legal.html
------------------------
This page hold 4 tiles each a link onto the respective legal page

------------------------
privacypolicy.html
------------------------
JustHealth's Privacy Policy

------------------------
references.html
------------------------
This page references all the external sources we have used

------------------------
sitemap.html
------------------------
Guide to JustHealths site

------------------------
termandconditions.html
------------------------
The terms and conditions a user agrees to when they register

------------------------
error pages
------------------------
All the error pages below have the same style just different text indicating what the error is.

400- Request Malformed page

401- Unauthorised Access page

404- Not found error page

internal error page

-------------------------
Admin Pages
-------------------------
(Add admin pages to html)
