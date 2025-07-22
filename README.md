# horizont-cli
 
CLI interface for T-2 horizont portal

## What does this do?

Currently it allows setting redirection number for T-2 phone number.

## Pipeline for setting redirections

1. send `username` and `password` headers to https://horizont.t-2.net/prijava and extract PHPSESSID cookie.

2. get current settings by sending to https://horizont.t-2.net/nastavitve/telefonija forms below:
```
group: nastavitve
handler: telefonija
number_selector: '<t-2_number>'
```

3. set redirect number by sending to https://horizont.t-2.net/nastavitve/telefonija forms below:
```
group: nastavitve
handler: telefonija
action: preusmeritve
number_selector: '<t-2_number>'
CFU_menu: A
CFU_c_number: '<your_number>'
CFB_menu: D
CFNR_menu: D
CFNA_menu: D
CW_menu: D
shrani: Shrani
```
