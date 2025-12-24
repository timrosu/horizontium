# horizontium
 
CLI interface for automating T-2 horizont portal with selenium

## What does this do?

Currently it allows setting redirection number for T-2 phone number.

## Configuration

Create `horizont.conf` file in conf directory. Use template here:
```
username: <t-2_horizont_username>
password: <t-2_horizont_password>
t2_number: <same_as_username_in_many_cases>
redirect_number: <your_number(supported forms: 38623456789 and 123456789)>
```

There is currently no authentication validating logic. If it fails, you can try commenting out `options.add_argument("--headless")` in 42nd line of horizontium.py and look where flow stops.

## Installation

Clone repo and enter the directory:
```sh
git clone https://github.com/timrosu/horizontium
cd horizontium
```

On Linux/Unix/MacOS run `install.sh`, on Windows run `install.bat`.

## Roadmap

- [X] distribute code into multiple files
- [ ] add option for overriding data from config
- [ ] add option for using natively installed webdriver
- [ ] use selenium only for login process
	- [ ] capture auth cookie
	- [ ] do everything else natively with requests
- [ ] separate code into client (horizontium) and library (libhorizont) repo
