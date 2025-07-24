# horizontium
 
CLI interface for automating T-2 horizont portal with selenium

## What does this do?

Currently it allows setting redirection number for T-2 phone number.

## Configuration

Create `horizont.conf` file. Use template here:
```
username: <t-2_horizont(old_system)_username_from_pam>
password: <t-2_horizont(old_system)_password_from_pam>
t2_number: <same_as_username_in_our_case>
redirect_number: <your_number_WITHOUT_1ST_DIGIT!>
```
