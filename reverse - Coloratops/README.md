# Coloratops

**Link:** [https://hackropole.fr/fr/challenges/reverse/fcsc2025-reverse-coloratops/](https://hackropole.fr/fr/challenges/reverse/fcsc2025-reverse-coloratops/)

**Category:** reverse

**Difficulty:** ⭐⭐

**Description:** A graphical binary `coloratops` asks for a password.

**Goal:** Reverse-engineer how the password is validated and find the correct flag.

# TL;DR

The binary uses SDL for GUI and font rendering. The flag is validated by comparing the color of each character in the input string against a palette of 10 colors. We reverse the color-matching logic and brute-force the valid string using a GDB Python script.

# **Initial Analysis**

First, we check the binary type:

![image](https://github.com/user-attachments/assets/b54bf4e2-b96d-45c1-b815-6f119f8eebd6)

The binary is a 64-bit ELF, stripped and dynamically linked.

When executed, it displays a window with a password input field. The allowed characters are hexadecimal digits along with `FCSC{}`, suggesting that the password is the flag itself.

Each time a character is entered, the color of the previous character changes. Only the penultimate character's color is updated, while the rest of the string remains unchanged. Another notable feature is a 60-second timer—once it reaches zero, the program exits.

![image 1](https://github.com/user-attachments/assets/8a045568-e85b-4395-a09a-fd0a87ec1b3c)

# Decompilation

We used Binary Ninja for static analysis. Here's a breakdown of the decompiled code:

### **Initialization**

The GUI is built using SDL (Simple DirectMedia Layer). The program initializes SDL subsystems and TTF (TrueType Font), creates a window titled "FCSC 2025 - Coloratops," and sets up a renderer and audio device. It also initializes a clock using `SDL_GetTicks()`.

```c
0000a0fa        if (SDL_Init(0x20))
0000a0fa        {
0000a110            SDL_Quit();
0000a101            return 1;
0000a0fa        }
...             ...
0000a130        if (TTF_Init() == 0xffffffff)
0000a130        {
0000a16b            SDL_Quit();
0000a137            return 1;
0000a130        }
0000a16b        data_26b1e0 = SDL_CreateWindow("FCSC 2025 - Coloratops", 0x2fff0000, 0x2fff0000, 0x4b0, 0x2ae, 0x14);
...             ...
0000a218        data_26b210 = SDL_OpenAudioDevice(0, 0, &var_88, &data_26b220, 0xb);
...             ...
0000a23c        SDL_StartTextInput();
...             ...
0000a27d        data_26b370 = SDL_GetTicks();
```

### **Main Event Loop**

The program enters an SDL event loop that runs until a flag (`i`) is set to `0`. Inside this loop, it continuously polls for events (e.g., keyboard input):

```c
0000a271        int32_t i = 1;
0000aa7b        while (i)
0000aa7b        {
0000aa7b            int32_t var_d8;
0000a5ef            while (SDL_PollEvent(&var_d8))
0000a5ef            {
...											...
0000a5ef            }
...									...
0000aa7b        }
...             ...
0000ab78        SDL_Quit();
0000ab7d        return 0;
0000a0e2    }
```

The following events are handled

- **SDL_QUIT (0x100):** Exits the program by setting `i = 0`.
    
    ```c
    0000a5ef                if (var_d8 == 0x100)
    0000a295                    i = 0;
    ```
    
- **SDL_TEXTINPUT (0x303):** Handles character input. The password is stored in `data_26b260`, and its length is tracked in `data_26b360`. Only characters in `FCSC{}abcdef0123456789` are accepted, with a maximum length of 64. This suggests the flag format is `FCSC{XXX}`, where `XXX` is a 58-digit hexadecimal string.
    
    ```c
    0000a293                else if (var_d8 == 0x303)
    0000a2ac                {
    0000a2b2                    void var_cc;
    0000a2b2                    
    0000a357                    for (int64_t j = 0; j < strlen(&var_cc); j += 1)
    0000a357                    {
    0000a357                        if (data_26b360 <= 0x3f && strchr("FCSC{}abcdef0123456789", (int32_t)*(uint8_t*)(j + &var_cc)) && data_26b360 <= 0xfe)
    0000a2ca                        {
    0000a305                            int64_t rax_22 = data_26b360;
    0000a310                            data_26b360 = rax_22 + 1;
    0000a32f                            (&data_26b260)[rax_22] = *(uint8_t*)(j + &var_cc);
    0000a340                            (&data_26b260)[data_26b360] = 0;
    0000a2ca                        }
    0000a357                    }
    0000a2ac                }
    ```
    
- **SDL_KEYDOWN (0x300):** Handles special keys like `backspace` (delete a character) and `Ctrl+C` (clear input).
    
    ```c
    0000a2ac                else if (var_d8 == 0x300)
    0000a376                {
    0000a3a4                    int32_t var_c4;
    0000a3a4                    int16_t var_c0;
    0000a3a4                    
    0000a3a4                    if (var_c4 == 8 && !((uint32_t)var_c0 & 0xc0) && data_26b360)
    0000a3a4                    {
    0000a3b1                        data_26b360 -= 1;
    0000a3c6                        (&data_26b260)[data_26b360] = 0;
    0000a3ca                        continue;
    0000a3a4                    }
    0000a3a4                    
    0000a3eb                    if (var_c4 == 0x71 && (uint32_t)var_c0 & 0xc0)
    0000a3eb                    {
    0000a3ed                        i = 0;
    0000a3f4                        continue;
    0000a3eb                    }
    0000a3eb                    
    0000a415                    if (var_c4 == 0x63 && (uint32_t)var_c0 & 0xc0)
    0000a415                    {
    0000a42b                        memset(&data_26b260, 0, 0x100);
    0000a430                        data_26b360 = 0;
    0000a43b                        continue;
    0000a415                    }
    0000a415                    
    0000a45c                    if (var_c4 == 8 && (uint32_t)var_c0 & 0xc0)
    0000a45c                    {
    0000a472                        memset(&data_26b260, 0, 0x100);
    0000a477                        data_26b360 = 0;
    0000a482                        continue;
    0000a45c                    }
    0000a45c                    
    0000a490                    if (var_c4 == 0x1b)
    0000a490                    {
    0000a4a6                        memset(&data_26b260, 0, 0x100);
    0000a4ab                        data_26b360 = 0;
    0000a490                    }
    0000a490                    else if (var_c4 == 0x20)
    0000a4c4                    {
    0000a4cf                        data_26b374 ^= 1;
    0000a4dd                        int32_t rax_50;
    0000a4dd                        rax_50 = !data_26b374;
    0000a4ed                        SDL_PauseAudioDevice((uint64_t)data_26b210, (uint64_t)rax_50);
    0000a4c4                    }
    0000a4c4                    else if (var_c4 == 0x76 && (uint32_t)var_c0 & 0xc0)
    0000a500                    {
    0000a51d                        char* rax_56 = SDL_GetClipboardText();
    0000a51d                        
    0000a52b                        if (rax_56)
    0000a52b                        {
    0000a531                            for (void* j_1 = nullptr; j_1 < strlen(rax_56); j_1 += 1)
    0000a5ca                            {
    0000a5ca                                if (data_26b360 <= 0x3f && strchr("FCSC{}abcdef0123456789", (int32_t)*(uint8_t*)((char*)j_1 + rax_56)) && data_26b360 <= 0xfe)
    0000a549                                {
    0000a58d                                    int64_t rax_65 = data_26b360;
    0000a598                                    data_26b360 = rax_65 + 1;
    0000a5a9                                    (&data_26b260)[rax_65] = *(uint8_t*)(rax_56 + j_1);
    0000a5ba                                    (&data_26b260)[data_26b360] = 0;
    0000a549                                }
    0000a5ca                            }
    0000a5ca                            
    0000a5e0                            SDL_free(rax_56);
    0000a52b                        }
    0000a500                    }
    0000a376                }
    ```
    

### **Password Validation**

After processing events, the program performs checks on the password:

1. Verifies it starts with `FCSC{` and ends with `}`.
2. Calls `sub_9c77()` for further validation.

A boolean (`data_26b368`) is initialized to `1` and set to `0` if any check fails.

```c
0000a5fc            data_26b368 = 1;
0000a61d            data_26b368 &= (uint32_t)(data_26b260 == 0x46);  // 'F'
0000a63a            data_26b368 &= (uint32_t)(data_26b261 == 0x43);  // 'C'
0000a657            data_26b368 &= (uint32_t)(data_26b262 == 0x53);  // 'S'
0000a674            data_26b368 &= (uint32_t)(data_26b263 == 0x43);  // 'C'
0000a691            data_26b368 &= (uint32_t)(data_26b264 == 0x7b);  // '{'
0000a6bd            data_26b368 &= (uint32_t)(*(uint8_t*)(data_26b360 + 0x26b25f) == 0x7d);  // '}'
0000a6c3            data_26b1e8;
0000a6df            data_26b368 &= sub_9c77();  // Further validation
```

### **Rendering Logic**

A timer tracks the time since launch, and if 60 seconds pass, `data_26b36c` is set to `1`, indicating a timeout.

```c
0000a7d6            uint32_t rax_116 = (SDL_GetTicks() - data_26b370) / 0x3e8;
0000a7d6            
0000a7ea            if (rax_116 > 0x3b && !data_26b36c)
0000a7ec                data_26b36c = 1;
```

Text in `data_26b208` is rendered and colored using `TTF_RenderText_Blended`, then converted to a texture and displayed with `SDL_RenderCopy`.

```c
0000a700            if (!data_26b36c)
0000a700            {
0000a706                rbx = 0xff;
0000a70d                *(uint8_t*)((char*)rbx)[1] = 0xff;
0000a737                void* rax_101 = TTF_RenderText_Blended(data_26b208, &data_26b260, (uint64_t)rbx | 0xff0000 | 0xff000000, &data_26b260);
0000a737                
0000a745                if (rax_101)
0000a745                {
0000a75d                    var_20_1 = SDL_CreateTextureFromSurface(data_26b1e8, rax_101);
...                         ...
0000a745                }
0000a700            }
0000a700            
0000a7a6            SDL_SetRenderDrawColor(data_26b1e8, 0, 0, 0, 0xff);
0000a7b5            SDL_RenderClear(data_26b1e8);
```

the program then takes the input text in buffer `data_26b208`, renders it with a specific color and create a texture from it.

In order to update the screen, the program chooses different textures depending on several conditions, renders all of them at the new screen with `SDL_RenderCopy()`, and finally calls     `SDL_RenderPresent()` to display the new screen. We explain the different renderings:

To update the screen, the program selects different textures based on several conditions, renders them using `SDL_RenderCopy()`, and finally calls `SDL_RenderPresent()` to display the new frame. Below are the different rendering steps:

- **Sound icon:** The program checks a boolean `data_26b374` to determine whether sound is enabled or disabled, then selects the appropriate icon to display.
    
    ```c
    0000a8d4            if (!data_26b374)
    0000a91d                SDL_RenderCopy(data_26b1e8, data_26b250, 0, U"\n\n22");
    0000a8d4            else
    0000a8f6                SDL_RenderCopy(data_26b1e8, data_26b248, 0, U"\n\n22");
    ```
    
- **Timer:** The program calculates the number of seconds the number of seconds remaining from a 60-second countdown and renders it using a TTF font with a specified color.
    
    ```c
    0000a92a            if (!data_26b36c)
    0000a92a            {
    0000a957                void s;
    0000a957                snprintf(&s, 8, "%2d ", (uint64_t)(0x3c - rax_116));
    0000a962                int32_t rcx_3;
    0000a962                rcx_3 = 0xff;
    0000a969                *(uint8_t*)((char*)rcx_3)[1] = 0xff;
    0000a97a                int32_t var_13c = rcx_3 | 0xff0000 | 0xff000000;
    0000a994                void* rax_135 = TTF_RenderText_Blended(data_26b208, &s);
    0000a994                
    0000a9a2                if (!rax_135)
    0000a9a2                    break;
    0000a9a2                
    0000a9b9                int64_t rax_137 = SDL_CreateTextureFromSurface(data_26b1e8, rax_135);
    ...                     ...
    0000aa24                SDL_RenderCopy(data_26b1e8, rax_137, 0, &var_f8);
    0000aa30                SDL_DestroyTexture(rax_137);
    0000a92a            }
    ```
    
- **Background image:** If time is up (`data_26b36c` is true), a "you lose" image is rendered. Otherwise, the program checks `data_26b368`, which indicates whether the entered password is correct. If the password is incorrect, a default image is shown. If it is correct, a hash is computed from the password via `sub_9e2e()`, and then `sub_982a()` decrypts a "success" image using that hash, which is rendered to the screen.
    
    ```c
    0000a7fe            if (data_26b36c)
    0000a820                SDL_RenderCopy(data_26b1e8, data_26b1f8, 0, &(*U"\n\n22")[4]);
    0000a7fe            else if (data_26b368)
    0000a832            {
    0000a876                void var_138;
    0000a876                sub_9e2e(&data_26b260, data_26b360, &var_138);
    0000a876                
    0000a885                if (!data_26b200)
    0000a8a2                    sub_982a(data_26b1e8, &data_26b200, &var_138);
    0000a8a2                
    0000a8c7                SDL_RenderCopy(data_26b1e8, data_26b200, 0, &(*U"\n\n22")[4]);
    0000a832            }
    0000a832            else
    0000a854                SDL_RenderCopy(data_26b1e8, data_26b1f0, 0, &(*U"\n\n22")[4]);
    ```
    
- **Input field:** Text in `data_26b208` is rendered and colored using `TTF_RenderText_Blended`, then converted to a texture and displayed with `SDL_RenderCopy`.
    
    ```c
    0000a700            if (!data_26b36c)
    0000a700            {
    0000a706                rbx = 0xff;
    0000a70d                *(uint8_t*)((char*)rbx)[1] = 0xff;
    0000a737                void* rax_101 = TTF_RenderText_Blended(data_26b208, &data_26b260, (uint64_t)rbx | 0xff0000 | 0xff000000, &data_26b260);
    0000a745                if (rax_101)
    0000a745                {
    0000a75d                    var_20_1 = SDL_CreateTextureFromSurface(data_26b1e8, rax_101);
    ...                         ...
    0000a745                }
    0000a700            }
    ...                         ...
    0000aa44            if (var_20_1 && !data_26b36c)
    0000aa63                SDL_RenderCopy(data_26b1e8, var_20_1, 0, &var_98);
    0000aa63            
    0000aa72            SDL_RenderPresent(data_26b1e8);
    ```
    

### Flag checking

All that remains is to dive into the heart of the program: the `sub_9c77()` function, which performs the flag validation.

The function creates 64 small graphics surfaces and reads pixel data from each using `SDL_RenderReadPixels()`. Each pixel is processed via `sub_9c32()`, which matches the pixel color against a 10-color palette. The index of the first matching color (0–9) is stored in a buffer `var_88`.

```c
00009c77        void var_88;
00009c93        memset(&var_88, 0xff, 0x40);
00009c93        
00009dd4        for (int32_t i = 0; i <= 0x3f; i += 1)
00009dd4        {
00009dd4            int32_t var_30_1 = 0x25f;
00009cd5            void* rax_5 = SDL_CreateRGBSurfaceWithFormat(0, 0x10, 0x20, 0x20, 0x16462004);
...                 ...
00009d42            SDL_RenderReadPixels(data_26b1e8, &var_98, rdx_2, rcx_1, (uint64_t)rdi_1);
00009d4b            void* rax_15 = *(uint64_t*)((char*)rax_5 + 0x20);
00009d53            char var_d_1 = 0xff;
00009d53            
00009db1            for (int32_t j = 0; j <= 0x1f; j += 1)
00009db1            {
00009db1                for (int32_t k = 0; k <= 0xf; k += 1)
00009da7                {
00009da7                    if (var_d_1 == 0xff)
00009d9c                        var_d_1 = sub_9c32(*(uint32_t*)((char*)rax_15 + ((int64_t)(k + (j << 4)) << 2)));
00009da7                }
00009db1            }
00009db1            
00009dbc            *(uint8_t*)(&var_88 + (int64_t)i) = var_d_1;
00009dc7            SDL_FreeSurface(rax_5);
00009dd4        }
```

After collecting 64 values, the function compares each byte in `var_88` against an expected sequence stored in `data_b420`. If all values match, the function returns `1`; otherwise, it returns `0`.

```c
00009dda        int32_t var_1c_1 = 1;
00009dda        
00009e27        for (int64_t i_1 = 0; i_1 <= 0x3f; i_1 += 1)
00009e27        {
00009e27            int32_t rax_33;
00009e14            rax_33 = (uint32_t)*(uint8_t*)(i_1 + &var_88) == *(uint32_t*)((i_1 << 2) + &data_b420);
00009e1a            var_1c_1 &= (uint32_t)rax_33;
00009e27        }
00009e27        
00009e29        return (uint64_t)var_1c_1;
```

### **Color Palette Matching**

**About `sub_9c32()`:** The `sub_9c32()` function checks if a pixel matches any of 10 predefined colors in a palette at `data_b520`. It returns the index of the match, or `-1` if the color isn’t found.

```c
00009c32    int64_t sub_9c32(int32_t arg1)
00009c32    {
00009c32        int64_t result = 0;
00009c6e        while (true)
00009c6e        {
00009c6e            if (result > 9)
00009c70                return 0xffffffff;
00009c5c            if (arg1 == *(uint32_t*)((result << 2) + &data_b520))
00009c5c                break;
00009c64            result += 1;
00009c6e        }
00009c5e        return result;
00009c32    }
```

The color palette contains these RGBA values:

![image 2](https://github.com/user-attachments/assets/d02100d1-744b-45c4-96a3-b3538a138dd4)

Now it’s more clear, the flag validation is as follows. 64 rectangle is constructed, each corresponding to a character in the password. The pixels colors of the character are compared to a color palet of 10 colors, and the index of the matching color in the palet is returned and compared to an expected value in the buffer `data_b420`. So `0xb420` stores a 64 sequence of colors that the password must respect:

So, the flag validation works as follows: For each of the 64 characters in the flag, a surrounding surface is rendered. The function finds the first pixel whose color matches one of the palette entries, i.e, the color of the character. The index of this color (0–9) is compared to a reference value in `data_b420`.

Here’s what the expected color indices at `data_b420` look like:

![image 3](https://github.com/user-attachments/assets/e68ecdf2-7c73-486a-af30-39c5cc8a0044)

A neat observation: the first 5 values and the last one are `0x00`, which corresponds to white (`0xFFFFFFFF`)—index 0 in the color palette. These likely map to the characters `FCSC{` at the start and `}` at the end of the flag.

# Solution

At this point, the solution became clear: we need to find a 64-character password (58 hex digits inside `FCSC{}`). This password must produce the exact color sequence stored in the buffer at address `0xb420`.

Upon analyzing the code, we noticed that the only instruction responsible for rendering colored text is `TTF_RenderText_Blended()`. This means the logic for assigning colors to characters is not implemented directly in the program, but rather handled internally by the TTF font rendering. As a result, we decided to brute-force candidate passwords to find one that matches the expected color sequence.

### Removing the timer

To bypass the 60-second limit, we patch the binary (using HxD) to replace `1` with `0` in the timer check:

```c
0000a7d6            uint32_t rax_116 = (SDL_GetTicks() - data_26b370) / 0x3e8;
0000a7d6            
0000a7ea            if (rax_116 > 0x3b && !data_26b36c)
0000a7ec                data_26b36c = 1;   // replace 1 with 0
```

Which corresponds to the following assembly instruction:

```nasm
0000a7ec    c705760b260001000000      mov dword [rel data_26b36c], 0x1
```

Before:

![image 4](https://github.com/user-attachments/assets/02ce9a79-411b-4cfd-8c9d-f4e16bc58894)

After:

![image 5](https://github.com/user-attachments/assets/59a09071-6265-480c-a36f-1e77ce90d96e)

### Bruteforcing the password

We observed that the color of each character depends both on its position and on the following character. However, the characters `FCSC{` always appear in white, regardless of what follows them. Therefore, we only need to brute-force the remaining characters, starting from the end of the string and working backward.

To automate this process, we decided to write a GDB Python script using two breakpoints:

- **WriteBreakpoint** at `*main+1306`: This is triggered just before the password validation begins. Since we're not using the GUI to input the password, we manually write the candidate password into memory.
- **ReadBreakpoint** at `*0x000055555555de29`: This is triggered when the color values of the new input text are updated in memory. At this point, we read the colors from memory and compare them to the expected color pattern.

Because we need custom logic at each breakpoint, a simple nested Python loop isn’t sufficient. Instead, we used the GDB Python API and defined custom breakpoint classes by subclassing `gdb.Breakpoint`. This allowed us to override the `stop()` method, which is automatically called each time the breakpoint is hit. Inside this method, we implement the desired behavior and return `False` to let the program continue running without pausing.

We defined a base class `b` inheriting from `gdb.Breakpoint`, which holds the state of our bruteforce process. It includes class attributes like:

- `charset`: the set of characters to test (hex digits in this case),
- `frags` and `new_frags`: List storing valid password fragments in the past and current position.
- and various index variables like `i_frag`, `i_charset`, and `position`.
- Control variables (`stop`, `start`, `end`) to manage breakpoint flow.
- Indices (`i_frag`, `i_charset`) to track progress through the charset and fragments.
- `position`: The current character position being tested (starting from the end).
- `colors`: The expected color values for validation.

We observe that each time the password is updated in memory, two breakpoint hits are required to reflect the change in the GUI. Therefore, we use a boolean variable `stop` that alternates between `True` and `False` to indicate whether we should perform an action or simply wait for the next hit.

```python
import gdb

class b(gdb.Breakpoint):
    charset = [c for c in "0123456789abcdef"]
    frags = ['']
    new_frags = []
    stop = True
    start = True
    end = False
    i_frag = 0
    i_charset = 0
    frag = ""
    position = 62  # Start from the end, move backward to position 5
    colors = [0, 0, 0, 0, 0, 9, 6, 3, 6, 7, 6, 5, 7, 4, 6, 2, 7, 7, 2, 9, 6, 7, 7, 5, 1, 6, 2, 8, 4, 3, 6, 8, 5, 4, 9, 2, 9, 1, 2, 7, 1, 1, 4, 4, 2, 5, 4, 8, 6, 1, 6, 7, 4, 9, 1, 9, 5, 4, 3, 9, 9, 9, 3, 0]
```

The logic is straightforward: we start at position 62 with a password of the form `FCSC{000…000p}`, where `p` is the character being tested. The total password length must always be 64 to produce correct color values. For each character in the charset, we attempt a new value for `p` using the index `i_charset`. If the color values match, the fragment is saved to `frags`. Then, we move to the next position and build new fragments by appending characters from the charset to the previously valid ones. The new valid fragments are saved to `new_frags`, and the process repeats.

```python
# Write breakpoint: injects the candidate password into memory
class WriteBreakpoint(b):
    def stop(self):
        if b.start:
            return False  # Skip the very first call
        if not b.stop:
            b.stop = True
            return False  # Wait for the next write
        else:
            b.frag = b.charset[b.i_charset] + b.frags[b.i_frag]
            password = 'FCSC{' + '0' * (b.position - 5) + b.frag + '}'
            gdb.execute(f'set {{char[65]}} 0x5555557bf260 = "{password}\\0"', to_string=True)
            gdb.execute(f'set *(int*)0x5555557bf360 = 64', to_string=True)
            b.stop = False
            return False  # Continue execution

# Read breakpoint: reads memory to check if color pattern is correct
class ReadBreakpoint(b):
    def stop(self):
        if b.start:
            b.start = False
            return False
        if not b.stop:
            return False
        if b.end:
            return True  # Stop execution, flag found

        addr = int(gdb.parse_and_eval("$rbp - 0x80"))
        mem = list(gdb.inferiors()[0].read_memory(addr, 64).tobytes())

        if b.position == 62:
            if (mem[b.position] == b.colors[b.position] and
                mem[b.position + 1] == b.colors[b.position + 1]):
                b.new_frags.append(b.frag)
        elif b.position == 5:
            if mem[b.position] == b.colors[b.position]:
                print(f'The flag fragment is: FCSC{{{b.frag}}}')
                b.end = True
                b.stop = False
                return False
        else:
            if mem[b.position] == b.colors[b.position]:
                b.new_frags.append(b.frag)

        b.i_charset += 1
        if b.i_charset == 16:
            b.i_frag += 1
            b.i_charset = 0
            if b.i_frag == len(b.frags):
                b.i_frag = 0
                b.position -= 1
                b.frags = b.new_frags.copy()
                b.new_frags = []

        return False
```

Once the breakpoint classes are defined, we set them in the main section:

```python
gdb.execute('file ./coloratops')

br1 = WriteBreakpoint("*main+1306")
br2 = ReadBreakpoint("*0x000055555555de29")

gdb.execute('run')
```

You can run the GDB script using: `gdb -q -x solution.py`. It took roughly five minutes to recover the full flag:

![image 6](https://github.com/user-attachments/assets/3c7ebd6b-8f3c-4246-a0ec-87ab8e8849fa)

The complete script is available in the file `solution.py`.
