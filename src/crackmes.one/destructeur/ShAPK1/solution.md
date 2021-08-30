# Solution for destructeur's ShAPK1
mara <mara@localhost.local>

## Analysis

The program is an apk file, so probably an Android program.
We used jad[^1], to analyze the binary.

Three classes are present :

- BuildConfig
- MainActivity
- R

The `MainActivity` classe is insteresting for us. It contains, three methods :

- onCreate
- encrypt
- check

`onCreate` called by the Android runtime to create the GUI controls, `encrypt` and `check` are used by the application logic.
The `check` aims to validate if the code entered are correct or not.

```java
   public void check() {
        Button button = (Button) findViewById(R.id.check);
        this.checkButton = button;
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                TextView textView = (TextView) MainActivity.this.findViewById(R.id.messageText);
                String obj = ((EditText) MainActivity.this.findViewById(R.id.passwordInput)).getText().toString();
                if (Arrays.equals(Base64.encode(MainActivity.this.encrypt(obj.getBytes(StandardCharsets.UTF_8)), 2), MainActivity.this.getResources().getString(R.string.secret).getBytes(StandardCharsets.UTF_8))) {
                    textView.setText("YES! PASSWORD IS CORRECT!!");
                } else {
                    textView.setText("PASSWORD IS WRONG!!");
                }
            }
        });
    }
````

This line is interesing :

```java
if (Arrays.equals(Base64.encode(MainActivity.this.encrypt(obj.getBytes(StandardCharsets.UTF_8)), 2), MainActivity.this.getResources().getString(R.string.secret).getBytes(StandardCharsets.UTF_8))) {
```

To validate the challenge, we need to have a code which equals to `R.string.secrets`. `R.string.secrets` is a string located in Resource :  `Resources->resource.arsc->string.xml`. It's value is :

```xml
    <string name="secret">NQALCgEDDDEzUjpTBwocBgcDPTIIGwIK</string>
```

The conditional test use the encrypt function to encode the code entered before compare it with the right hardcoded code.

```java
    public byte[] encrypt(byte[] bArr) {
        byte[] bytes = getResources().getString(R.string.key).getBytes(StandardCharsets.UTF_8);
        int length = bytes.length;
        byte[] bArr2 = new byte[bArr.length];
        for (int i = 0; i < bArr.length; i++) {
            bArr2[i] = (byte) (bArr[i] ^ bytes[i % length]);
        }
        return bArr2;
    }
```

The function `encrypt` take a parameter, our code entered, the `bytes` array is a key pointed by `R.string.key` and available in  `Resources->resource.arsc->string.xml`.

It's value is :

```xml
    <string name="key">beginning</string>
````

The `encrypt` function xored each characters of `bArr` with `bArr2` for each iterations.

> **WARNING:** the `bArr2` can be short than `bArr` so a modulo with the key length (`bArr2`)  is applied to avoid the bound array overflow

## Keygen

You will find an unencrypt script in python language to find the original code :

```python
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import base64

BEGINNING = "beginning"
SERIAL = "NQALCgEDDDEzUjpTBwocBgcDPTIIGwIK"

serial_b64decoded = base64.b64decode(SERIAL)
serial_b64decoded_length = len(serial_b64decoded)

beginning_length = len(BEGINNING)
original_serial = ""

for i in range(serial_b64decoded_length):
    xored_value = (serial_b64decoded[i] ^ 
        ord(BEGINNING[i % beginning_length]))
    original_serial += chr(xored_value)

# the original code 
print(original_serial)
````


[^1]: https://github.com/skylot/jadx/
