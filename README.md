**LT;DR;**
* Using online: [vpnry.github.io/ekapassword](https://vpnry.github.io/ekapassword). Or [here](https://ekapassword.pages.dev/)

* Using offline: [download EkaPassword](https://github.com/vpnry/ekapassword/archive/refs/heads/master.zip)

* Archive.org caches: [EkaPassword - caches](https://web.archive.org/web/20220000000000*/https://vpnry.github.io/ekapassword)

## EkaPassword
**EkaPassword** is a **password manager**  web app that doesn't require you to manage a password file. With just one master password, you can generate infinite different passwords for different sites.

It is derived from [NullPass+ by JM Alarcón](https://github.com/jmalarcon/NullPassPlus) and [NullPass by Adam MacLeod](https://github.com/adammacleod/nullpass).

I modified NullPass+ mainly to make sure that each output password will **always includes** a random combination of _(number + upper case + lower case + special)_ characters to meet recent secure password standards.

Since it is no more compatible with the old NullPass family, I give it a new name **EkaPassword**. In pāḷi language, `eka` means 1.


```JavaScript 
// input 
Resource name: 1
Master password: c
Length: 16

// with NullPass+, no number included

=> `DbqCANDm_DrH+CXn` 

// with EkaPassword 

=> `DbqCANDm6sS@+CXn`

```
### Example

> One master password to rule them all.

For accounts at any sites, you can define and use a resource name pattern that makes sense to you.

**Account 1**

-   Resource name:`a@gmail.com`
-   Master password:`yourSecureMasterPassword`
-   Password length: 20

=> Get a unique password for account 1: `r/fLpY6En50fN\BC9zAn`

**Account 2**

Only change the resource name, keep others

-   Resource name:`b@gmail.com`

=> Get a unique password for account 2: `EeLDeDt31D0mY[ZCoZJa`

**Account 3**

-   Resource name:`username@gmail.com@example.com`

=> Get a unique password for account 3: `qEJTHbZhr58eB<pG8kid`

You can also use the generated password for the master password and re-generate password again. Thus, each site will have a different master password.


## Other changes in EkaPassword  v1

1. Password length is now min =  **12**, default = **20**, max = **88**.

2. Update `jsSHA` library to `jsSHA-3.2.0` (2020), and `jquery` to `jquery-3.6.1` (current latest & smaller size).

3. Generate  `v1_ekapassword_standalone.html` file.

This file concatenates all essential JavaScript code and css in one standalone html file which can be used offline on many platforms (including Kindle!?).

SHA512SUM of `v1_ekapassword_standalone.html` (v1 = version 1):

```bash 

sha512sum v1_ekapassword_standalone.html  
922921ec5e05f4c08ece70bdbbb172cac50fa4768e520dc3535cb8bafa06408ba1b4ff7f63fd5a645e4f4855c9495d71e85009750c30e96daa1085153a84712f  v1_ekapassword_standalone.html

```

4. Changed algorithm

Each password will **always include** a random combination of (number + upper case + lower case + special) characters to meet current password standards. 

Its new algorithm is as below:

```JavaScript


var numberStr = "0123456789";
// python string.punctuation
var pyPunctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";

var smallAlphabet = "abcdefghijklmnopqrstuvwxyz";

var bigAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

function hashThisText(text) {
  var jsSHA_version_320 = new jsSHA("SHA-512", "TEXT", {
    encoding: "UTF8",
  });
  jsSHA_version_320.update(text);

  return jsSHA_version_320.getHash("B64");
}

function getLetter(textToHash, fromStr) {
  var hash = hashThisText(textToHash);

  var haf = Math.floor(hash.length / 2);
  var n = hash[haf].charCodeAt(0);

  var x = n % fromStr.length;

  return fromStr.substring(x, x + 1);
}

function get4Chars(nTK) {
  var addNumber = getLetter(nTK + numberStr, numberStr);

  var addSmall = getLetter(nTK + smallAlphabet, smallAlphabet);

  var addBig = getLetter(nTK + bigAlphabet, bigAlphabet);

  var addPunct = getLetter(nTK + pyPunctuation, pyPunctuation);

  var added4C = addNumber + addSmall + addBig + addPunct;

  return added4C;
}

function generatePassword(master, resource, length) {
  // current( input + output) = input for the next step

  var inputToken = length.toString() + master + resource.trim().toLowerCase();

  var hash = hashThisText(inputToken);

  var add4 = get4Chars(inputToken + hash);

  length = Number(length);

  var midPass = Math.floor(length / 2);

  // We removed 4 chars of the original hash, npassw still 88 chars
  var npassw =
    hash.substring(0, midPass) + add4 + hash.substring(midPass + add4.length);

  return npassw.substring(0, length);
}

```

In Python `ekapassword_python.py`:

```python 

'''EkaPassword in python

Tested on Python 3.10.7

https://vpnry.github.io/ekapassword
Ref: jsSHA-3.2.0/test/genHashRounds.py
'''

import math
import hashlib
import binascii


__version__ = 1

NN = "0123456789"
PP = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
SS = "abcdefghijklmnopqrstuvwxyz"
BB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def hash_this(txt):
    s512 = hashlib.sha512()
    byte_txt = txt.encode(encoding='utf-8')
    s512.update(byte_txt)

    res = binascii.b2a_base64(s512.digest(), newline=False)

    return res.decode(encoding='utf-8')


def getch(pre_token, from_str):
    this_hash = hash_this(pre_token)
    haf = math.floor(len(this_hash) / 2)

    ccode = ord(this_hash[haf])
    n = ccode % len(from_str)

    return from_str[n]


def get4ch(pre_token):
    # hash + str => new hash
    # so 4 selected chars will be more random

    n = getch(f'{pre_token}{NN}', NN)
    s = getch(f'{pre_token}{SS}', SS)
    b = getch(f'{pre_token}{BB}', BB)
    p = getch(f'{pre_token}{PP}', PP)

    return f'{n}{s}{b}{p}'


def gen_password(resource, masterpwd, pwd_len):
    resource = str(resource).lower().strip()

    in_token = f'{pwd_len}{masterpwd}{resource}'
    this_hash = hash_this(in_token)

    add4chars = get4ch(in_token + this_hash)

    pwd_len = int(pwd_len)
    haf = math.floor(pwd_len / 2)

    # 4 chars in the original hash are replaced with add4chars
    # so the original hash is now hidden
    res = this_hash[0:haf] + add4chars + this_hash[haf + 4:]

    
    res = res[0:pwd_len]

    return res


if __name__ == '__main__':
    a = gen_password('user@gmail.com', 'testpassword1', 20)
    print(a)  # V13T1aYTQf9yA"r5vZTI

    b = gen_password('user@gmail.com', 'testpassword2', 20)
    print(b)  # zPrm9UdfSz0xE/Vi6x75


```

## Attributions
-   EkaPassword is a derived version of [NullPass+](https://github.com/jmalarcon/NullPassPlus) by JM Alarcón and original [NullPass](https://github.com/adammacleod/nullpass) by Adam MacLeod.
-   Hash library [jsSHA](http://caligatio.github.io/jsSHA/)
-   [Bootstrap](http://getbootstrap.com/)
-   [jQuery](http://jquery.com/)
-   [Favicon generator](https://favicon.io/favicon-generator)
-   [GitHub](https://github.com/)
---

# Original NullPass+ readme

## NullPass+
Infinite complex passwords for all your sites and accounts, just remembering one master password. Off-line: no information transmitted anywhere. Mobile support.

>One password = infinite secure passwords

If you don't want to host this app yourself you can simply visit **[www.jasoft.org/nullpass/](http://www.jasoft.org/nullpass/)** to use it immediately.

## What is this for?

**NullPass+** is a password manager that **doesn't require you to keep your passwords stored anywhere**, and that allows you to have a different complex password for every site or system you use. 

This is accomplished by combining **a single master password** with a site-specific token (often domain name or your email address) to generate a unique password. This password is **cryptographically secure** and your **original password is safe and not recoverable** should an attacker manage to obtain your unique site password. This means an attack on one of the sites you visit will not disclose your password to any other services - keeping your accounts safe.

It uses no Internet connection and doesn't save your passwords anywhere.

If you access it from a **mobile device**, you can choose to pin it to your Home Screen on iOS or Android and you'll get a ready-to-use app that will work offline, even if there's no connection to the Internet.

## Usage
Just enter a domain, email account or other unique resources you want to protect with a password, your unique secure password, the desired length for the password (12 by default), and you're done!

Some advice:

- Try to use a long, non-obvious master password or [pass-phrase](https://en.wikipedia.org/wiki/Passphrase). A passphrase would be even better since they are long, difficult to guess or break by brute force, and easy to remember. This is your key to all your passwords from now on so, keep it secure and don't forget it!
- Use the complete first-level domain name if you're going to use just one account, or the combination of domain name + username if you're using several accounts. For example, if you want to protect your unique Facebook account with NullPass+ use `facebook.com` as the "domain" parameter. However, if you're protecting your Gmail account you should use `youraccount@gmail.com` as the "domain" parameter since you can protect several Gmail accounts with this system. In that way, each one will have its password and will be easy to get from NullPass+.
- Since you're not going to remember any of those generated passwords, use long ones. NullPass+ suggests 12 as the default length, but I typically use 20 or 30 characters long passwords. Try to use the same length always since changing the length changes the whole generated password, not only the "extra" characters you drop in.
- Make a list of the services protected with NullPass+. You can use a simple .txt file saved to your favourite cloud drive (Dropbox, GDrive, pCloud...). Keep there a list of domains used, the user names and the length of the chosen password. In this way, you'll always know exactly how to generate the password again if needed. Although it only contains domain names and lengths and an attacker would not be able to derive any passwords from it it's better to store this list in encrypted storage.

## Derived code & enhancements
This project is derived from the original code by **Adam MacLeod** on [Github](https://github.com/adammacleod/nullpass).

I've upgraded the app with the following enhancements:

- **Support for working offline**. Once you visit the NullPass+ default page once, it can work without any Internet connection. This is especially useful if you plan to use it from a mobile device.
- **Ensure a symbol is always included**: since a lot of accounts require you to include some symbol in your passwords and the original algorithm didn't ensure that I've added a simple way to ensure that a symbol is always used in the password. The character in the middle of the generated password is deterministically substituted by a symbol that changes depending on the Unicode code for the character that is substituted.
- **Support for the app "pinning"** under iOS, Android, Windows Phone, Windows 10... You can just add the app to your home screen in any of these operating systems and you get a nice icon to access it anytime as if it were a native app. It will be shown as a nice icon and open directly.
- **Better support for copying the generated password on mobile devices**: the original code made it difficult to copy the resulting password from a mobile device. Now you can copy it without any problems + I've made the field read-only. Now if you click on it or make it get the focus, the password gets automatically copied to your clipboard (this is very useful in mobile devices, where copying from a disabled field is not always very easy).
- **Basic validation**: if you try to generate a password shorter than 6 characters it will default to 6 (less than that makes no sense). If the length is more than 88 it will change automatically to 88 (the length of the SHA-512 hash string encoded in Base64).