#!/usr/bin/python
import Crypto.Cipher.AES
import Crypto.Util.Counter
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import sys
import getpass
import os, random, struct
import StringIO
import json

from pyfunctions import parse_args, psucceed, pfail, phelp
phelp = phelp.phelp
parse_args = parse_args.parse_args
psucceed = psucceed.psucceed
pfail = pfail.pfail

old = raw_input
def raw_input(prompt=None):
    if prompt:
        sys.stderr.write(str(prompt))
        return old()

def encrypt_file(key, in_string, out_filename, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
           The encryption key - a string that must be
           either 16, 24 or 32 bytes long. Longer keys
           are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
        
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = len(in_string) #os.path.getsize(in_filename)

    infile=StringIO.StringIO(in_string)
    with open(out_filename, 'wb') as outfile:
        outfile.write(struct.pack('<Q', filesize))
        outfile.write(iv)

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += ' ' * (16 - len(chunk) % 16)
            
            outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
        
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        
        outfile=StringIO.StringIO()
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            outfile.write(decryptor.decrypt(chunk))
                
        outfile.truncate(origsize)
        return outfile.getvalue()

def getCurrentDict():
    global internal_dict, hpass
    tries=0
    internal_dict = dict()
    hpass=None
    
    while True:
        password=getpass.getpass()#raw_input("Please Enter Your Password: ")
        h = SHA256.new()
        h.update(password)
        hpass = h.digest()
        if ( os.path.isfile ( FILE_NAME ) ):
            try:
                internal_dict = json.loads(decrypt_file(hpass,FILE_NAME)) #"doggodoggodoggoy",FILE_NAME))
                break
            except:
                tries += 1
                if tries >= 3:
                    pfail("Too Many Failures")
        else:
            break

    #return (hpass,internal_dict)


def createPin():
    res = parse_args(description,[{"name": "pin", "description": "Specifies the pin-create mode"},
                                  {"name": "defaults", "flag": "-d", "description": "Use the default value (4 numbers).", "optional": True},
                                  {"name": "length", "flag": "-n", "description": "The length of the pin", "has_value": True, "optional": True, "type": int},
                                  {"name": "location", "flag": "-l", "description": "The location to add it to", "has_value": True, "optional": True}])
    getCurrentDict()
    length=None
    location=None
    if res.get("defaults"):
        length=4
    loc = res.get("location")
    if loc == None:
        loc=raw_input("Location: ")
    loc = "{}/pin".format(loc)
    if loc in internal_dict:
        pfail ( "Location {} already exists".format(loc) )
    length = res.get("length",length)
    if length == None:
        length=int(raw_input("Length: "))
    password=""
    random.seed()
    while len ( password ) < length:
        password += random.choice("0123456789")
    internal_dict[loc] = password
    print password
    
                     
def createPass():
    res = parse_args(description,[{"name": "create", "description": "Specifies the create mode"},
                                  {"name": "defaults", "flag": "-d", "description": "Use the default values (16 characters, 4 of each). Values may be overwritten by CL args", "optional": True},
                                  {"name": "location", "flag": "-c", "description": "The location to add it to", "has_value": True, "optional": True},
                                  {"name": "length", "flag": "-l", "description": "The length of the password", "has_value": True, "optional": True, "type": int},
                                  {"name": "specials", "flag": "-s", "description": "The number of special characters to use", "has_value": True, "optional": True, "type": int},
                                  {"name": "numbers", "flag": "-n", "description": "The number of numbers to use", "has_value": True, "optional": True, "type": int},
                                  {"name": "uppers", "flag": "-u", "description": "The number of upper case characters to use", "has_value": True, "optional": True, "type": int}])
    getCurrentDict()
    length = None
    nums = None
    specs = None
    uppers = None
    if res.get("defaults"):
        length = 16
        nums = 4
        specs = 4
        uppers = 4
    loc = res.get("location")
    if loc == None:
        loc=raw_input("Location: ")
    if loc in internal_dict:
        pfail ( "Location {} already exists".format(loc) )
    length = res.get("length",length)
    if length == None:
        length=int(raw_input("Length: "))
    nums = res.get ( "numbers", nums )
    if nums == None:
        nums=int(raw_input("Numbers: "))
    specs = res.get ( "specials", specs )
    if specs == None:
        specs=int(raw_input("Specials: "))
    uppers = res.get ( "uppers", uppers )
    if uppers == None:
        uppers=int(raw_input("Uppercase Letters: "))
    if length < nums + specs + uppers:
        pfail("Error: Lengths not possible")
    toadds=[]
    i=0
    while i < nums:
        toadds.append(1)
        i += 1
    i = 0
    while i < specs:
        toadds.append(2)
        i += 1
    i = 0
    while i < uppers:
        toadds.append(3)
        i += 1
    while len ( toadds ) < length:
        toadds.append(0)
    password=""
    random.seed()
    numCharMap={0:"abcdefghijklmnopqrstuvwxyz",1:"0123456789",2:"!@#$%^&*",3:"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    while len ( password ) < length:
        n = random.randint(0,len(toadds)-1)
        nc = toadds.pop(n)
        password += random.choice(numCharMap[nc])
    internal_dict[loc] = password
    print password
        
        
description="pykeys is a utility for storing and accessing encrypted passwords"
if ( len ( sys.argv ) <= 1 ):
    phelp(description,[("<mode>","The mode to use, one of add|create|remove|lookup")])
    exit(1)
    
mode = sys.argv[1].lower()

if mode not in ["add","remove","lookup","create","dump", "pin"]:
    phelp(description,[("<mode>","The mode to use, one of add|create|remove|lookup|dump|pin")])
    exit(1)

    
USER = os.environ['USER']
FILE_NAME = "/home/{}/.keys".format(USER)
hpass = None
internal_dict = None
                
if mode == "add":
    res=parse_args(description,[{"name": "add", "description": "Specifies the add mode"},
                                {"name":"loc", "description": "The element this password corresponds to"},
                                {"name": "pas", "description": "The password to add"}])
    getCurrentDict()
    loc = res["loc"]
    pas = res["pas"]
    if loc not in internal_dict:
        internal_dict[loc] = pas
    else:
        pfail("Error: Entry already exists")
elif mode == "remove":
    res = parse_args(description,[{'name': 'remove', 'description': 'Specifies the remove mode'},
                                  {'name': 'loc', "description": "The element to remove"}])
    getCurrentDict()
    loc = res["loc"]
    if loc in internal_dict:
        del internal_dict[loc]
        psucceed(loc)
    else:
        pfail("Error: No such entry")
elif mode == "create":
    createPass()
elif mode== "pin":
    createPin()
elif mode == "lookup":
    res = parse_args(description,[{'name': 'lookup', 'description': 'Specifies the lookup mode'},
                                  {'name': 'loc', "description": "The element to lookup"}])
    getCurrentDict()
    loc = res["loc"]
    if loc in internal_dict:
        print internal_dict[loc]
        if loc + "/pin" in internal_dict:
            print internal_dict[loc+"/pin"]
    elif loc + "/pin" in internal_dict:
        print internal_dict[loc+"/pin"]
    else:
        pfail("Error: No such entry")
elif mode == "dump":
    getCurrentDict()
    for loc in internal_dict:
        print "{} {}".format(loc,internal_dict[loc])

encrypt_file(hpass,
             json.dumps(internal_dict),
             FILE_NAME)
