# Solution for nutcake's WhiteRabbit
mara <mara@localhost.local>

## Analysis

The description suggest a hidden function...

Take IDA 7 Freeware [^1], to analyze the binary.

Type `CTRL+E` keys and go to `_start` function, you will see the startup stub
which trigger the main function.

The main function printing only two uninteresting string.

If you press another time the `CTRL+E` keys, you will see a function named
`secret`. This function print a flag but it haven't got any cross references.
How we can go to the `secret`'s function ?

The first idea will be to patch the EntryPoint but the program will crashed.

Another option will to patch the instruction lea rdi, main to lea rdi, secret in
the `_start` function.

> **WARNING:** Beware the nmemonic is position relative.

```assembly
public _start
_start proc near
xor     ebp, ebp
mov     r9, rdx         ; rtld_fini
pop     rsi             ; argc
mov     rdx, rsp        ; ubp_av
and     rsp, 0FFFFFFFFFFFFFFF0h
push    rax
push    rsp             ; stack_end
lea     r8, __libc_csu_fini ; fini
lea     rcx, __libc_csu_init ; init
lea     rdi, main       ; main  <--------- here
call    cs:__libc_start_main_ptr
hlt
_start endp
````

Pick the hexadecimal values of the lea : 0x48, 0x8D, 0x3D, 0x51, 0x01,
0x00, 0x00 .

Often in the 64 bits programming the address are relative. To verify this argue,
we help us of the online encoder/decoder of Jonathan Salwan's website.[^2]

Copy the previous hexadecimal values without the 0x and comma in this website,
select x86(64) in little endian mode and click on the disassemble button. The
result will be :

```assembly
0x0000000000000000: lea rdi, qword ptr [rip + 0x151]
```

Why it's 0x151 ? It's quite simple, look the next formula :

```assembly
address of the main function - address of the lea - size of the instuction of
the lea opcode

0x11D5 - 0x107D - 7 => 0x151
```

> **TIP:** we can type this previous operation at the left of IDC at the bottom of
IDA window, to compute the operation.


Our goal will change the value by the correct position , the position of
secret function. The formula :

```assembly
address of the secret function - address of the lea - size of the instuction of
the lea opcode

0x1145 - 0x107D - 7 => 0xC1
````

Now, via the Jonathan's website [^2], you filling out the form with :

```assembly
0x0000000000000000: lea rdi, qword ptr [rip + 0xc1]
```

Select x86(64) in little endian mode and click on the assemble button. The
result will be :

```
488D3D51010000
```

Fire up a hexadecimal editor and replace the old values by the new one :

```
48 8D 3D 51 01 00 00

by

48 8D 3D C1 00 00 00
```

Now, you can run the program and grab the flag !

## Content in this archive

- hidden.i64     : the hidden analysis
- hidden_mod     : the hidden file patched
- hidden_mod.i64 : the hidden_mod analysis
- solution.html  : the present file.


[^2]: http://shell-storm.org/online/Online-Assembler-and-Disassembler/
[^1]: https://www.hex-rays.com/products/ida/support/download_freeware.shtml
