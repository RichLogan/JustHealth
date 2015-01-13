package justhealth.jhapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.Spinner;

import java.util.HashMap;

public class Register extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);

        Button registerButton = (Button) findViewById(R.id.register);
        registerButton.setOnClickListener(
            new View.OnClickListener() {
                public void onClick(View view) {
                    sendRegister();
                }
            }
        );

        //TODO: Link to Terms and Conditions
    }

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

        //Gender
        Boolean ismale = null;
        int id = ((RadioGroup) findViewById(R.id.sex)).getCheckedRadioButtonId();
        if (id == R.id.male) {
            ismale = true;
        } else if (id == R.id.female) {
            ismale = false;
        }
        details.put("ismale", ismale.toString());

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
            post(details);
        } else {
            Feedback.toast("Terms and Conditions must be accepted", false, getApplicationContext());
        }
    }

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
        alert.setNegativeButton("Go to email", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                Intent emailLauncher = new Intent(Intent.ACTION_VIEW);
                emailLauncher.setType("message/rfc822");
                try{
                    startActivity(Intent.createChooser(emailLauncher, ""));
                } catch(ActivityNotFoundException e){
                    Feedback.toast("No email client found", false, getApplicationContext());
                }
            }
        });
        alert.setPositiveButton("Okay", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                startActivity(new Intent(Register.this, Login.class));
            }
        });
        alert.show();
    }

    //validation on password and confirm password
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

