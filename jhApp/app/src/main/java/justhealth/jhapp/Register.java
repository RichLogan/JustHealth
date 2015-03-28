package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.IconTextView;
import android.widget.Spinner;

import java.util.HashMap;

public class Register extends Activity {

    /**
     * This method runs when the page is first loaded. Sets the correct xml layout and sets the
     * correct action bar. Onclick listener for the register button.
     * runs the method that checks for a change of the spinners.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Register");

        Button registerButton = (Button) findViewById(R.id.register);
        registerButton.setOnClickListener(
            new View.OnClickListener() {
                public void onClick(View view) {
                    sendRegister();
                }
            }
        );

        // Spinner listeners
        initSpinners();

        //TODO: Link to Terms and Conditions
    }

    /**
     * This checks for when the gender and account type spinners are changed. When they changed it
     * changes the icon that is next to the SpinnerView.
     */
    private void initSpinners() {
        // Gender Spinner
        final Spinner genderSpinner = (Spinner) findViewById(R.id.gender);
        genderSpinner.setOnItemSelectedListener(new OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                String selected = genderSpinner.getSelectedItem().toString();
                IconTextView genderIcon = (IconTextView) findViewById(R.id.genderIcon);
                if (selected.equals("Male")) {
                    genderIcon.setText("{fa-male}");

                }
                else if (selected.equals("Female")) {
                    genderIcon.setText("{fa-female}");
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                // TODO Auto-generated method stub
            }
        });

        // Account Type Spinner
        final Spinner typeSpinner = (Spinner) findViewById(R.id.accountType);
        typeSpinner.setOnItemSelectedListener(new OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                String selected = typeSpinner.getSelectedItem().toString();
                IconTextView typeIcon = (IconTextView) findViewById(R.id.accountTypeIcon);
                if (selected.equals("Patient")) {
                    typeIcon.setText("{fa-user}");

                }
                else if (selected.equals("Carer")) {
                    typeIcon.setText("{fa-user-md}");
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                // TODO Auto-generated method stub
            }
        });
    }

    /**
     * This is executed when the register button is pressed. Gathers the information from all of the
     * text boxes and checks that they are all filled out.
     * Checks that the terms and conditions are checked and if so, runs the post method. If not,
     * toasts back to the user.
     */
    private void sendRegister() {

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("username", ((EditText) findViewById(R.id.username)).getText().toString());
        details.put("firstname", ((EditText) findViewById(R.id.firstName)).getText().toString());
        details.put("surname", ((EditText) findViewById(R.id.surname)).getText().toString());
        details.put("dob", ((EditText) findViewById(R.id.dob)).getText().toString());
        details.put("email", ((EditText) findViewById(R.id.email)).getText().toString());

        // Check empty
        for (String value : details.values()) {
            if (value == null || value.equals("")) {
                Feedback.toast("All fields must be filled out", false, getApplicationContext());
                return;
            }
        }

        //Sets the value of the spinner: gender
        String ismale = "false";
        Spinner gender = (Spinner)findViewById(R.id.gender);
        String genderValue = gender.getSelectedItem().toString();
        if (genderValue.equals("Male")) {
            ismale = "true";
        }
        details.put("ismale", ismale);

        //Account Type
        final Spinner accountTypeSpinner = (Spinner) findViewById((R.id.accountType));
        final String accountType = String.valueOf(accountTypeSpinner.getSelectedItem());
        details.put("accounttype", accountType.toLowerCase());

        //Password
        String password = ((EditText) findViewById(R.id.password)).getText().toString();
        String confirmPassword = ((EditText) findViewById(R.id.confirmPassword)).getText().toString();

        if (((CheckBox) findViewById(R.id.tsandcs)).isChecked()) {
            details.put("password", password);
            details.put("confirmpassword", confirmPassword);
            details.put("terms", "on");
            System.out.println(details);
            post(details);
        } else {
            Feedback.toast("Terms and Conditions must be accepted", false, getApplicationContext());
        }
    }

    /**
     * Makes the post request to the JustHealth API to register the user.
     * If successful, alerts the user, and redirects them to the login page.
     *
     * @param details HashMap of the details of the user to be registered.
     */
    public void post(HashMap<String, String> details) {
        String response  = Request.post("registerUser", details, getApplicationContext());

        // Registration Failed
        if (!response.equals("True")) {
            Feedback.toast(response, false, getApplicationContext());
            return;
        }

        // Registration Successful
        AlertDialog.Builder alert = new AlertDialog.Builder(Register.this);
        alert.setTitle("Registration Successful!");
        alert.setMessage("Please check your email for a verification link. ");
        alert.setPositiveButton("Okay", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                startActivity(new Intent(Register.this, Login.class));
            }
        });
        alert.show();
    }

    //

    /**
     * THIS METHOD IS NOT IN USE
     * validation on password and confirm
     * @param password the password
     * @param confirmPassword the password in the confirm password field
     *
     * @return Boolean whether the two passwords match.
     */
    public boolean isPasswordValid(String password, String confirmPassword) {
        boolean status = false;
        if (confirmPassword != null && password != null) {
            if (password.equals(confirmPassword)) {
                status = true;
            }
        }
        return status;
    }
}

