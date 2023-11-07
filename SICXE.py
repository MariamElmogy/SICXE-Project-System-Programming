'''
    Name: Mariam Mohamed ElMogy
    Reg#: 19101076
'''
import converter
import re
labels_list = []
instruction_list = []
reference_list = []
LocCtr = []
Obj_Code = []
symbol = []
address = []
format1 = []
format2 = []
format3 = []
format4 = []
ref_split = []
instr_split = []
reg1 = []
reg2 = []
Header = []
T_record = []
End = []
k = 0
r = 0
l = 0
i = 0
j = 0
f = 0


def readTheFile():
    file = open('inSICXE.txt', "r")

    for line in file:
        data = line.split()
        words_in_line = len(line.split())
        if words_in_line == 3:
            labels_list.append(data[0])
            instruction_list.append(data[1])
            reference_list.append(data[2])
        elif words_in_line == 1:
            labels_list.append("\t")
            instruction_list.append(data[0])
            reference_list.append("\t")
        elif words_in_line == 2:
            labels_list.append("\t")
            instruction_list.append(data[0])
            reference_list.append(data[1])
    file.close()


def locationCounter():
    l = reference_list[0]
    location_format = '{:0<4}'.format(l)
    LocCtr.append(location_format)
    LocCtr.append(location_format)
    j = 0
    for i in range(1, len(labels_list)):
        StrLocation = LocCtr[i]
        location_counter = int(StrLocation, 16)
        if instruction_list[i].upper() != 'End'.upper():

            if instruction_list[i].upper() == 'RESW'.upper():
                LocCtr.append(format((int(reference_list[i]) * 3) + location_counter, '04X'))

            elif instruction_list[i].upper() == 'RESB'.upper():
                LocCtr.append(format((int(reference_list[i]) * 1) + location_counter, '04X'))

            elif instruction_list[i].upper() == 'BYTE'.upper():
                if reference_list[i].startswith('C'.lower()) or reference_list[i].startswith('C'.upper()):
                    LocCtr.append(format((len(reference_list[i]) - 3) + location_counter, '04X'))
                elif reference_list[i].upper().startswith('X'.upper()):
                    LocCtr.append(format(int((len(reference_list[i]) - 3) / 2) + location_counter, '04X'))

            elif instruction_list[i].upper() == 'BASE'.upper():
                LocCtr.append(format(location_counter, '04X'))

            elif instruction_list[i].upper() == 'WORD'.upper():
                if reference_list[i].find(','):
                    ref = len(reference_list[i].split(',')) * 3
                    LocCtr.append(format(location_counter + ref, '04X'))
            elif instruction_list[i].startswith('+'):
                format4.append(instruction_list[i])
                LocCtr.append(format(location_counter + 4, '04X'))

            for j in range(len(converter.OPTAB)):
                if instruction_list[i].upper() == (converter.OPTAB[j][0]):
                    if converter.OPTAB[j][1] == '3':
                        format3.append(instruction_list[i])
                        LocCtr.append(format(location_counter + 3, '04X'))
                        break
                    elif converter.OPTAB[j][1] == '2':
                        format2.append(instruction_list[i])
                        LocCtr.append(format(location_counter + 2, '04X'))
                        break
                    elif converter.OPTAB[j][1] == '1':
                        format1.append(instruction_list[i])
                        LocCtr.append(format(location_counter + 1, '04X'))
                        break


def symbolTable():
    for i in range(len(labels_list)):
        if labels_list[i].startswith("\t") or instruction_list[i].startswith("START".upper()):
            pass
        else:
            symbol.append(labels_list[i])
            address.append(LocCtr[i])

def objectCode():
    e = 0
    for c in range(len(instruction_list)):
        if instruction_list[c].upper() != 'End'.upper():
            if instruction_list[c].upper() == 'RESW'.upper() or instruction_list[c].upper() == 'RESB'.upper() \
                    or instruction_list[c].upper() == 'START'.upper() or instruction_list[c].upper() == 'BASE'.upper():
                Obj_Code.append("\t")

            elif instruction_list[c].upper() == 'BYTE'.upper():
                if reference_list[c].upper().startswith('C'.upper()):
                    tmp = reference_list[c]
                    split_variable = tmp[2:len(tmp) - 1]
                    ASCII_values = [ord(character) for character in split_variable]
                    for c in range(len(ASCII_values)):
                        ASCII_values.append(format(ASCII_values[c], 'X'))
                    listToStr = ''.join([str(elem) for elem in ASCII_values])
                    Obj_Code.append(listToStr[6:])

                elif reference_list[c].upper().startswith('X'.upper()):
                    tmp = reference_list[c]
                    split_variable = tmp[2:len(tmp) - 1]
                    Obj_Code.append(split_variable)

            else:
                for k in range (len(converter.OPTAB)):
                    if converter.OPTAB[k][0] == instruction_list[c]:
                        opFormat = converter.OPTAB[k][1]
                        opcode = converter.OPTAB[k][2]
                        if instruction_list[c].upper().startswith('RSUB'.upper()):
                            opcode_binary = convertOPCODE(converter.OPTAB[k][2])
                            b = 0
                            p = 0
                            i = 1
                            n = 1
                            disp = "0000"
                            formats(opcode_binary, n, i, x, b, p, e, disp, '03X')

                        # FORMAT 2
                        elif opFormat == "2":
                            for f in range(len(format2)):
                                # for k i
                                if instruction_list[c].upper() == format2[f].upper():
                                    for r in range(len(converter.REG)):
                                        if reference_list[c] == converter.REG[r][0]:
                                            opcode = converter.OPTAB[k][2]
                                            con = opcode + str(r) + str("0")
                                            Obj_Code.append(con)
                                            break

                                        elif any(m in "," for m in reference_list[c]):
                                            ref_split = reference_list[c].split(',')
                                            l = 0
                                            while l < len(ref_split):
                                                if ref_split[l] == converter.REG[r][0]:
                                                    reg1.append(converter.REG[r][1])
                                                    l += 1
                                                else:
                                                    r += 1
                                            con = str(opcode) + str("".join(reg1))
                                            Obj_Code.append(con)
                                            break

                                        else:
                                            continue
                                    break
                            break

                        elif opFormat == "3":
                            e = 0
                            symbolTable()
                            opcode_binary = convertOPCODE(converter.OPTAB[k][2])
                            if reference_list[c].startswith('#'):
                                i = 1
                                n = 0
                                # x = 0
                                if reference_list[c].endswith(',X'):
                                    x = 1

                                    for f in range(len(symbol)):
                                        index_base = instruction_list.index("BASE")
                                        ref = reference_list[index_base]
                                        index_ref = symbol.index(ref)
                                        base = address[index_ref]
                                        sym_word = re.search(r"\w+", symbol[f])
                                        if reference_list[c].split(',X')[0].split('#')[1] == sym_word.group():
                                            TA = address[f]
                                            pc = LocCtr[c + 1]
                                            disp_addr = int(TA, 16) - int(pc, 16)
                                            disp_hex = format(disp_addr, '03X')
                                            if -2048 <= disp_addr <= 2047:  # pc
                                                p = 1
                                                b = 0
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                                                break
                                            else:
                                                b = 1
                                                p = 0
                                                disp_addr = int(TA, 16) - int(base, 16)
                                                disp_hex = format(disp_addr, '03X')
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, '03X')
                                                break
                                else:
                                    x = 0
                                    for j in range(len(labels_list)):
                                        if reference_list[c].split('#')[1] == labels_list[j]:
                                            for f in range(len(symbol)):
                                                sym_word = re.search(r"\w+", symbol[f])
                                                if reference_list[c].split('#')[1] == sym_word.group():
                                                    TA = address[f]
                                                    pc = LocCtr[c + 1]
                                                    disp_addr = int(TA, 16) - int(pc, 16)
                                                    disp_hex = format(disp_addr, '03X')
                                                    if -2048 <= disp_addr <= 2047:  # pc
                                                        p = 1
                                                        b = 0
                                                    else:
                                                        b = 1
                                                        p = 0
                                                    formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                                                    break
                                        elif reference_list[c].split('#')[1].isnumeric():
                                            p = 0
                                            b = 0
                                            x = 0
                                            disp = hashtag_number(reference_list[c].split("#")[1], "03X")
                                            formats(opcode_binary, n, i, x, b, p, e, disp, '03X')
                                            break
                                        else:
                                            continue



                            elif reference_list[c].startswith('@'):
                                n = 1
                                i = 0
                                if reference_list[c].endswith(',X'):
                                    x = 1

                                    for f in range(len(symbol)):
                                        index_base = instruction_list.index("BASE")
                                        ref = reference_list[index_base]
                                        index_ref = symbol.index(ref)
                                        base = address[index_ref]
                                        sym_word = re.search(r"\w+", symbol[f])
                                        if reference_list[c].split(',X')[0].split('@')[1] == sym_word.group():
                                            TA = address[f]
                                            pc = LocCtr[c + 1]
                                            disp_addr = int(TA, 16) - int(pc, 16)
                                            disp_hex = format(disp_addr, '03X')
                                            if -2048 <= disp_addr <= 2047:  # pc
                                                p = 1
                                                b = 0
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                                                break
                                            else:
                                                b = 1
                                                p = 0
                                                disp_addr = int(TA, 16) - int(base, 16)
                                                disp_hex = format(disp_addr, '03X')
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, '03X')
                                                break
                                else:
                                    for f in range(len(symbol)):
                                        sym_word = re.search(r"\w+", symbol[f])
                                        if reference_list[c].split('@')[1] == sym_word.group():
                                            TA = address[f]
                                            pc = LocCtr[c + 1]
                                            disp_addr = int(TA, 16) - int(pc, 16)
                                            disp_hex = format(disp_addr, '03X')
                                            if -2048 <= disp_addr <= 2047:  # pc
                                                p = 1
                                                b = 0
                                            else:
                                                b = 1
                                                p = 0
                                            formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                                            break


                            elif reference_list[c].endswith(',X'):
                                n = 1
                                i = 1
                                x = 1

                                for f in range(len(symbol)):
                                    index_base = instruction_list.index("BASE")
                                    ref = reference_list[index_base]
                                    index_ref = symbol.index(ref)
                                    base = address[index_ref]
                                    sym_word = re.search(r"\w+", symbol[f])
                                    if reference_list[c].split(',X')[0] == sym_word.group():
                                        TA = address[f]
                                        pc = LocCtr[c + 1]
                                        disp_addr = int(TA, 16) - int(pc, 16)
                                        disp_hex = format(disp_addr, '03X')
                                        if -2048 <= disp_addr <= 2047:  # pc
                                            p = 1
                                            b = 0
                                            formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                                            break
                                        else:
                                            b = 1
                                            p = 0
                                            disp_addr = int(TA, 16) - int(base, 16)
                                            disp_hex = format(disp_addr, '03X')
                                            formats(opcode_binary, n, i, x, b, p, e, disp_hex, '03X')
                                            break

                            else:
                                n = 1
                                i = 1
                                x = 0
                                for f in range(len(symbol)):
                                    index_base = instruction_list.index("BASE")
                                    ref = reference_list[index_base]
                                    index_ref = symbol.index(ref)
                                    base = address[index_ref]

                                    sym_word = re.search(r"\w+", symbol[f])

                                    if reference_list[c] == sym_word.group():

                                        TA = address[f]
                                        pc = LocCtr[c + 1]
                                        disp_addr = int(TA, 16) - int(pc, 16)
                                        disp_hex = format(disp_addr, '03X')
                                        if -2048 <= disp_addr <= 2047:  # pc
                                            p = 1
                                            b = 0
                                            if disp_addr < 0:
                                                negative_opcode = '{:X}'.format(disp_addr & (2 ** 12 - 1))
                                                formats(opcode_binary, n, i, x, b, p, e, negative_opcode, '03X')
                                                break

                                            else:
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, '03X')
                                                break
                                        else:
                                            b = 1
                                            p = 0
                                            if reference_list[c].startswith(ref):
                                                disp_addr = int(TA, 16) - int(base, 16)
                                                disp_hex = format(disp_addr, '03X')
                                                formats(opcode_binary, n, i, x, b, p, e, disp_hex, '3X')
                                                break

                        elif opFormat == "1":
                            Obj_Code.append(opcode)
                        break


                    elif instruction_list[c].startswith('+'):
                        e = 1
                        opcode_binary = convertOPCODE(converter.OPTAB[k][2])
                        instr_split = instruction_list[c].split('+')
                        if instr_split[1] == converter.OPTAB[k][0]:
                            # '''IF THE REFERENCE OF THE FORMAT 4 STARTS WITH #  '''
                            if reference_list[c].startswith('#'):  # if it starts with # it is immediate
                                i = 1
                                n = 0
                                p = 0
                                b = 0
                                for j in range(len(labels_list)):  # To cover the 2 conditions of #
                                    # '''IF REFERENCE OF # FOLLOWED BY NUMBER'''
                                    if not reference_list[c].split('#')[1] == labels_list[j]:
                                        disp = hashtag_number(reference_list[c], '05x')

                                formats(opcode_binary, n, i, x, b, p, e, disp, 'X')
                                break

                            else:
                                n = 1
                                i = 1
                                p = 0
                                b = 0
                                symbolTable()
                                for j in range(len(address)):
                                    if reference_list[c] == symbol[j]:
                                        TA = address[j]
                                        pc_base = LocCtr[c + 1]
                                        disp_addr = int(TA, 16) - int(pc_base, 16)

                                        if 0 <= disp_addr or disp_addr <= 4095:
                                            disp_addr = "0" + TA
                                            formats(opcode_binary, n, i, x, b, p, e, disp_addr, 'X')
                                        else:
                                            formats(opcode_binary, n, i, x, b, p, e, disp_addr, 'X')

                                        break
                                break

                    else:
                        continue

        else:
            Obj_Code.append("\t")
            break


def formats(opcode_binary, n, i, x, b, p, e, disp_hex, f):
    con = opcode_binary + str(n) + str(i) + str(x) + str(b) \
          + str(p) + str(e)
    decimal_representation = int(con, 2)
    objc = format(decimal_representation, f)
    Obj_Code.append(objc + str(disp_hex))

def header():
    for i in range(len(labels_list)):
        location_counter = []
        StrLocation = LocCtr[0]  # Start Location
        location_counter.append(int(StrLocation, 16))  # Add it in location_counter
        StrLocation = LocCtr[i]  # End
        location_counter.append(int(StrLocation, 16))  # Add it in location_counter
        length = location_counter[1] - location_counter[0]
    Header.append((labels_list[0] + str(0) + str(0) + LocCtr[0] + format(length, '06x')))
    print("-------------------------------------------\n")
    print("H --> ", Header[0])

def text_record():
    s = 1
    t = 0

    while s < len(Obj_Code)-1:
        start_address = LocCtr[s]
        sum = 0
        cnt = 0
        if not(instruction_list[s] == 'RESW' or instruction_list[s] == 'RESB' or instruction_list[s] == 'END'):
            T_record.append(format(int(start_address, 16), '06X'))
            v = s
            k = v

            while v < len(Obj_Code) and sum < 29:
                if instruction_list[v] == 'RESW' or instruction_list[v] == 'RESB' or instruction_list[v] == 'END':
                    break

                else:
                    object_text = "".join(Obj_Code[v]).replace("\t", "")  # 17202D69202D....

                    t_digits = [str(object_text[idx: idx + 2]) for idx in range(0, len(object_text), 2)]
                    v += 1
                    sum += len(t_digits)

            record_length = format((int(LocCtr[v], 16) - int(start_address, 16)), '02X')
            s = v - 1
            T_record.append(record_length)

            while k < len(Obj_Code) and cnt < 29:
                if instruction_list[k] == 'RESW' or instruction_list[k] == 'RESB' or instruction_list[k] == 'END':
                    break

                else:
                    object_text = "".join(Obj_Code[k]).replace("\t", "")  # 17202D69202D....
                    t_digits = [str(object_text[idx: idx + 2]) for idx in range(0, len(object_text), 2)]
                    T_record.append(Obj_Code[k])
                    k += 1
                    cnt += len(t_digits)
            while t < len(T_record):
                if T_record[t].startswith('\t'):
                    del T_record[t]

                t += 1
            print("T --> ", T_record)
            del (T_record[:v + 1])
        s += 1



def end():
    End.append(str(0) + str(0) + LocCtr[0])
    print("E --> ", End[0])


def convertOPCODE(opcodeHex):
    convert_binary = []
    end_length = len(opcodeHex) * 4
    hex_as_int = int(opcodeHex, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    x = [(a) for a in str(padded_binary)]
    for i in range(6):
        convert_binary.append(x[i])
    concatenate_binary = "".join(convert_binary)
    return concatenate_binary


def printData():
    for i in range(len(labels_list)):
        if instruction_list[i].startswith("Start".upper()) or instruction_list[i].startswith("Start".lower()):
            print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "\t\t|", reference_list[i], "\t\t|", Obj_Code[i])
        elif len(labels_list[i]) <= 3:
            print(LocCtr[i], '|', labels_list[i], "\t\t|", instruction_list[i], "\t\t|", reference_list[i], "\t\t|", Obj_Code[i])
        elif len(reference_list[i]) == 4:
            print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "\t\t|", reference_list[i], "\t\t|", Obj_Code[i])
        elif len(instruction_list[i]) == 5 and len(reference_list[i]) == 1:
            print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "\t|", reference_list[i], "\t\t|", Obj_Code[i])
        else:
            print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "\t\t|", reference_list[i], "\t\t|", Obj_Code[i])


def hashtag_number(value, x):
    value = value.replace("#", "")
    value = int(value)
    hex_as_int = format(value, x)
    return hex_as_int

def indexed(opcode_binary, n, i, x, b, p, e, c):
    for f in range(len(symbol)):
        index_base = instruction_list.index("BASE")
        ref = reference_list[index_base]
        index_ref = symbol.index(ref)
        base = address[index_ref]
        sym_word = re.search(r"\w+", symbol[f])
        if reference_list[c].split(',X')[0].split('#')[1] == sym_word.group():
            TA = address[f]
            pc = LocCtr[c + 1]
            disp_addr = int(TA, 16) - int(pc, 16)
            disp_hex = format(disp_addr, '03X')
            if -2048 <= disp_addr <= 2047:  # pc
                p = 1
                b = 0
                formats(opcode_binary, n, i, x, b, p, e, disp_hex, 'X')
                break
            else:
                b = 1
                p = 0
                disp_addr = int(TA, 16) - int(base, 16)
                disp_hex = format(disp_addr, '03X')
                formats(opcode_binary, n, i, x, b, p, e, disp_hex, '03X')
                break

def main():
    readTheFile()
    locationCounter()
    objectCode()
    printData()

    header()
    text_record()
    end()

main()

