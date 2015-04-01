========================
HTML Listing
========================

Listed below is the complete list of all HTML pages in JustHealth.

Each HTML page is broken down by its general functionality describing the features of each page.
All of the pages have the standard header and footer from the template page and the content is within a <fieldset> tag.

------------------------
frontpage.html
------------------------
This is the front page of the web application and is available at: **http://raptor.kent.ac.uk:5000**. The page has two input boxes for a user to login with their username and password. There is also a button for a new user to click to register a new account.
The page also has a video demonstration of the application working and details about what the applciation can offer.

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

Our website has two home pages, one for patients and one for carers. They are both follow the same style where notifications and reminders appear at the top of the page, their profile picture, username and option to edit their profile in the top left. Also down the side is the connections modal, a search option to search other users, a search box to search the NHS website and a settings link to the settings page.

The connections modal, shows in tables all the incoming, outgoing and completed connection. You have the ability to delete current connections or cancel incoming and outgoing ones. To complete an incoming connection a user is required to enter in a 4 digit code provided by the connector in the modal.

Underneath the notifications on the this page is all the active patients prescriptions and upcoming appointments.

All icons are from `font awesome <http://fortawesome.github.io/Font-Awesome/>`_,
which a user can click to take them to the respective page.


------------------------
dashboardCarer.html
------------------------
*This page is only for carers.*

As mentioned above, it follows exactly the same format and the only difference is instead of showing the active prescriptions it shows all the carer's current patients.

------------------------
editProfile.html
------------------------
This is a page for both carers and patients where they can each edit their own profile. Users are able to upload a profile picture, change there firtsname, surname, email address, gender and date of birth. This can all be done by a simple form with validation on each field.

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
changePassword.html
------------------------
The change password page can be accessed from a logged in user. Within the settings the are able to change their current password by filling in the form.

------------------------
resetpassword.html
------------------------
Reset password can only be accessed via the email sent to the user to change their password. This page automatically fills in the username and asks for the user to enter in other details in order to change their password.

Once this is completed the user clicks submit to complete the password change

------------------------
resetpasswordnowquestion.html
------------------------
This page will appear when a users password is about to expire in the next couple of days. A user will be asked whether they wish to reset their password then or delay the change until the password runs out.


------------------------
expiredpassword.html
------------------------
The expired password page is for all users when their password has expired they will be directed to this page on login where they will be forced to change their password if they wish to carry on using the site. The reason behind this is for security of data. The page consists of a form asking for the new password and to confirm the new password.

------------------------
myPatients.html
------------------------
*This page is only for carers.*

My Patients is a page that only carers can view. It shows every patient they are connect to in a list.

If you click on each patient a modal drops down to list two options: Prescription and Appointments.
Click on the Prescriptions link and it will open up another modal showing two tabs: 'Active' prescriptions for the respective patient and 'Upcoming & Expired' prescriptions for the patient.
Active prescriptions will show green, upcoming blue and expired red.

If you click on either of tab boxes showing the appointment details, it will open up another modal giving you the option to edit the details.

If you click on the 'Appointments' tab this will open up another modal listing all that patients non private appointments.
There are options here to update and delete current appointments.
On the top left had side there is also the option to add new appointments for that patient.

------------------------
carerAppointments.html
------------------------
*This page is only for carers.*

This page can be found from a carer's home page by click on the calendar. This page list all the carer's personal appointments.
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

-----------------------
correspondence.html
-----------------------
*This page is only for carers.*

This page can be accessed via the carer dashboard and clicking on a respective patient and the 'Notes'. Carers are able to add notes on their patient visits which their respective patient is able view. Carers are also able to delete comments made.

-----------------------
patientNotes.html
-----------------------
*This page is only for Patients.*

This page can be accessed from the patients dashboard on the link 'visit notes'. This page displays the notes the carer has added about them and their visit.

-----------------------
contactUs.html
-----------------------
This page can be accessed by clicking on the 'contact us' in the footer. It has a link the JustHealth twitter and a form which had the current users firstname, surname and email automatically filled in. A user can fill in the message field and click submit for an email to be send to JustHealth.

------------------------
faq.html
------------------------
This page holds a list of questions with on click toggles displaying the answers to the questions.

------------------------
template.html
------------------------
Template.html is the design used to structure every other page, this page creates the header, footer, container and links jQuery, Font Awesome, DataTables plugin and Our resources.
Inside the footer there are modals to the terms and conditions, site map, references and the privacy policy.

------------------------
searchNHSDirect.html
------------------------
This page has a form with a search box which sends a POST request to the NHS webiste and searches their website. The result is displayed in a new window.

------------------------
settings.html
------------------------
This page holds basic details on the users and has links in a table for the user to change their password, deactivate their account and to connect JustHealth. These are all links which will take the user to a seperate pages.

------------------------
error pages
------------------------
All the error pages below have the same image and style, however they contain different text indicating to the user which error has been caused.

400- Request Malformed page

401- Unauthorised Access page

404- Not found error page

internal error page

-------------------------
Admin Pages
-------------------------
*This page is for admin users only*

The admin portal is all on one html page, it can be accessed by entering in admin credentials on the main login page. The page is divided into tabs with the navigation menu down the left hand side. Clicking on the different headings will dynamically change the content.

Home tab- general content about the admin portal describing the features.

Users- A list of all the active users registered on the database. On this page you are able to delete and edit users accounts.

Medication- This tab lists all the current medication on the system, you can also add new names of medication is they aren't found in the list.

Deactivation- Tab to list the current reasons for user deactivation and to be able to add a new deactivation reason to the list of options.

Statistics- This tab has a pie chart of the different deactivation reasons and a bar chart of the total number of carers and patients registered on the system.

Twitter- A list of all tweets @JustHealthSupport has been mentioned in and where #JustHealth has been mentioned.

Register new admin- A form for a current admin to be able to register a new admin account. The reason for this is to ensure security and that current admins can approve and register a new admin.
