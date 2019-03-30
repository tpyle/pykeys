# pykeys
A simple password manager on the command line

## Description
pykeys works with the following modes:
* add: store an existing password in the manager   
* create: create a new password   
* lookup: retrieve a password
* remove: remove a stored password
* dump: print out all passwords

## Usage
`pykeys <mode> <options>`
Where `<mode>` is one of the modes above

Each mode takes in it's own options:
### add
`pykeys add <loc> <password>`
* `<loc>` is the location the password goes to
* `<password>` is the password to use

### create
`pykeys create [-d] [-c <loc>] [-l <length>] [-s <specials>] [-n <numbers>] [-u <uppercases>]`
* `-d` is to use the default values for the quantities (length of 16, 4 special characters, 4 numbers, 4 uppercase characters, and 4 lowercase characters
* `-c` is to specify the location this is used for. If none is provided, the user will be prompted
* `-l` is to specify the length of the password. If not provided, and no `-d`, the user will be prompted
* `-s` is to specify the number of special characters. If not provided, and no `-d`, the user will be prompted
* `-n` is to specify the number of numbers. If not provided, and no `-d`, the user will be prompted
* `-u` is to specify the number of uppercase characters. If not provided, and no `-d`, the user will be prompted

### lookup
`pykeys lookup <loc>`
* `<loc>` should be the value of the password to lookup

### remove
`pykeys remove <loc>`
* `<loc>` should be the value of the location to remove the password from

### dump
