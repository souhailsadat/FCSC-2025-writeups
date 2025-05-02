import gdb

# Base class with shared variables and logic for both breakpoints
class b(gdb.Breakpoint):
    # Allowed characters for the frag (hex characters)
    charset = [car for car in "0123456789abcdef"]
    # fragments being tested
    frags = ['']
    # Validated fragment candidates at current position
    new_frags = []
    # State variables to control flow
    stop = True
    start = True
    end = False
    # Indices for iterating over charset and current frags
    i_frag = 0
    i_charset = 0
    # Currently tested flag fragment
    frag = ""
    # Current character position in frag being brute-forced
    position = 62  # starts from end, goes backward until position 5
    # Expected color values for comparison
    colors = [0, 0, 0, 0, 0, 9, 6, 3, 6, 7, 6, 5, 7, 4, 6, 2, 7, 7, 2, 9, 6, 7, 7, 5, 1, 6, 2, 8, 4, 3, 6, 8, 5, 4, 9, 2, 9, 1, 2, 7, 1, 1, 4, 4, 2, 5, 4, 8, 6, 1, 6, 7, 4, 9, 1, 9, 5, 4, 3, 9, 9, 9, 3, 0]


# Write breakpoint: injects candidate password into memory before check
class WriteBreakpoint(b):
    def stop(self):
        if b.start:
            return False  # Skip at the very first call
        if not b.stop:
            b.stop = True
            return False  # Skip if 'stop' was reset
        else:
            # Create new candidate frag using charset and current state
            b.frag = b.charset[b.i_charset] + b.frags[b.i_frag]
            # Construct full password string, padding with zeroes
            password = 'FCSC{' + '0' * (b.position - 5) + b.frag + '}'
            # Inject the password into target memory
            gdb.execute(f'set {{char[65]}} 0x5555557bf260 = "{password}\\0"', to_string=True)
            # Set password length
            gdb.execute(f'set *(int*)0x5555557bf360 = 64', to_string=True)
            b.stop = False
            return False  # Continue execution without stopping

# Read breakpoint: reads memory to verify if the injected password was correct
class ReadBreakpoint(b):
    def stop(self):
        if b.start:
            b.start = False
            return False  # Skip the first time
        if not b.stop:
            return False  # Skip if waiting for next write
        if b.end == True:
            return True  # End reached, halt debugger

        # Read the current color values from the stack
        addr = int(gdb.parse_and_eval("$rbp - 0x80"))
        mem = list(gdb.inferiors()[0].read_memory(addr, 64).tobytes())

        # Final character: check 2 bytes
        if b.position == 62:
            if (mem[b.position] == b.colors[b.position] and mem[b.position+1] == b.colors[b.position+1]):
                b.new_frags.append(b.frag)
        # First character (position 5): if match, frag is found
        elif b.position == 5:
            if (mem[b.position] == b.colors[b.position]):
                print(f'The flag is: FCSC{{{b.frag}}}')
                b.end = True
                b.stop = False   # Found the frag, stop injecting
                return False
        # All other positions: check single byte
        else:
            if (mem[b.position] == b.colors[b.position]):
                b.new_frags.append(b.frag)

        # Move to next character in charset
        b.i_charset += 1
        if b.i_charset == 16:  # Finished charset for current prefix
            b.i_frag += 1
            b.i_charset = 0
            if b.i_frag == len(b.frags):  # All combinations tried for this position
                b.i_frag = 0
                b.position -= 1  # Move backward in the frag
                b.frags = b.new_frags.copy()
                b.new_frags = []

        return False 

# Load binary into GDB
gdb.execute('file ./coloratops')

# Set breakpoints at password write and result read
br1 = WriteBreakpoint("*main+1306")
br2 = ReadBreakpoint("*0x000055555555de29")

# Start program execution
gdb.execute('run')
