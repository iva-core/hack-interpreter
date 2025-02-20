'''example hack reads:

@1
M=A
@3
D=A
@5
M=D
@2
0;JMP

'''

a_reg = 0
d_reg = 0

program_counter = 0

ram = [0]*(2**15 - 1)

def interpret_a_instruction(instr: str):
    global a_reg, program_counter
    a_reg = int(instr, base=2)
    program_counter += 1

def interpret_c_instruction(instr: str):
    global a_reg, d_reg, ram, program_counter
    assert instr[0:3] == '111' # checking that the top three bits are ones
    instr = instr[3:]
    a_or_m = instr[0]
    comp = instr[1:7]
    dest = instr[7:10]
    jump = instr[10:]

    if a_or_m:
        my_var = a_reg
    else:
        my_var = ram[a_reg]
    match comp:
        case '101010':
            my_value = 0
        case '111111':
            my_value = 1
        case '111010':
            my_value = -1
        case '001100':
            my_value = d_reg
        case '110000':
            my_value = my_var
        case '001101':
            my_value = not(d_reg)
        case '110001':
            my_value = not(my_var)
        case '001111':
            my_value = (d_reg * -1)
        case '110011':
            my_value = (my_var * -1)
        case '011111':
            my_value = (d_reg + 1)
        case '110111':
            my_value = (my_var + 1)
        case '001110':
            my_value = (d_reg - 1)
        case '110010':
            my_value = (my_var - 1)
        case '000010':
            my_value = (d_reg + my_var)
        case '010011':
            my_value = (d_reg - my_var)
        case '000111':
            my_value = (my_var - d_reg)
        case '000000':
            my_value = (d_reg & my_var)
        case '010101':
            my_value = (d_reg | my_var)
        case _:
            raise Exception(f'{comp} is not a valid computation. ')

    match jump:
        case '000':
            pass
        case '001':
            if my_value > 0:
                program_counter = a_reg - 1
        case '010':
            if my_value == 0:
                program_counter = a_reg - 1
        case '011':
            if my_value >= 0:
                program_counter = a_reg - 1
        case '100':
            if my_value < 0:
                program_counter = a_reg - 1
        case '101':
            if my_value != 0:
                program_counter = a_reg - 1
        case '110':
            if my_value <= 0:
                program_counter = a_reg - 1
        case '111':
            program_counter = a_reg - 1
        case _:
            raise Exception(f'{jump} is not a valid jump. ')

    if dest[2] == '1':
        ram[a_reg] = my_value
    if dest[1] == '1':
        d_reg = my_value
    if dest[0] == '1':
        a_reg = my_value

    program_counter += 1
            

# reading from .hack file

hack_array = []

with open('example.hack', 'r') as my_file:
    hack_array = (my_file.readlines())

for x in range(0, len(hack_array)):
    hack_array[x] = hack_array[x].strip()


while True:
    if program_counter >= (len(hack_array)):
        break
    current = hack_array[program_counter]
    if current[0] == '0':
        interpret_a_instruction(current)
    else: 
        interpret_c_instruction(current)
    print(f'A: {a_reg}, M: {ram[a_reg]}, D: {d_reg}, PC: {program_counter}')
    input()



