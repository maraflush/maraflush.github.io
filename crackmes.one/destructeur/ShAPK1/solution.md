= Solution for destructeur's ShAPK1
mara <mara@localhost.local>
:toc:
:numbered:
:nofooter:
:source-highlighter: pygments

== Analysis

The program is an apk file, so probably an Android program.
We used <<<jadx>>, to analyze the binary.

Three classes are present :

- BuildConfig
- MainActivity
- R

The *MainActivity* classe is insteresting for us. It contains, three methods :

- onCreate
- encrypt
- check

*onCreate* called by the Android runtime to create the GUI controls, *encrypt* and *check* are used by the application logic.
The *check* aims to validate if the code entered are correct or not.

[source, java, linenums]
----
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
----

This line is interesing :

[source, java]
----
if (Arrays.equals(Base64.encode(MainActivity.this.encrypt(obj.getBytes(StandardCharsets.UTF_8)), 2), MainActivity.this.getResources().getString(R.string.secret).getBytes(StandardCharsets.UTF_8))) {
----

To validate the challenge, we need to have a code which equals to __R.string.secrets__. __R.string.secrets__ is a string located in Resource :  __Resources->resource.arsc->string.xml__. It's value is :

[source,xml]
----
    <string name="secret">NQALCgEDDDEzUjpTBwocBgcDPTIIGwIK</string>
----

The conditional test use the encrypt function to encode the code entered before compare it with the right hardcoded code.

[source,java,linenums]
-----
    public byte[] encrypt(byte[] bArr) {
        byte[] bytes = getResources().getString(R.string.key).getBytes(StandardCharsets.UTF_8);
        int length = bytes.length;
        byte[] bArr2 = new byte[bArr.length];
        for (int i = 0; i < bArr.length; i++) {
            bArr2[i] = (byte) (bArr[i] ^ bytes[i % length]);
        }
        return bArr2;
    }
-----

The function *encrypt* take a parameter, our code entered, the __bytes__ array is a key pointed by __R.string.key__ and available in  __Resources->resource.arsc->string.xml__.

It's value is :

[source,xml]
----
    <string name="key">beginning</string>
----

The *encrypt* function xored each characters of __bArr__ with __bArr2__ for each iterations.

WARNING: the __bArr2__ can be short than __bArr__ so a modulo with the key length (__bArr2__)  is applied to avoid the bound array overflow

== Keygen

You will find an unencrypt script in python language to find the original code :

[source,python,linenums]
----
include::keygen.py[]
----

[bibliography]
== References

- [[[jadx]]] https://github.com/skylot/jadx/
