import click

from utils.input_parser import parse_lines


UNIQUE_LEN = {2: 1, 4:4, 3:7, 7:8}


def part_1(lines):
    digit_list = [d for l in lines for d in l.split(' | ')[1].split()]
    known = [d for d in digit_list if len(d) in UNIQUE_LEN.keys()]
    return len(known)


def part_2(lines):
    digit_list = [(l.split(' | ')[0].split(), l.split(' | ')[1].split()) for l in lines]
    outp_list = []
    
    for inp, outp in digit_list:
        known = {UNIQUE_LEN[len(el)]: set(list(el)) for el in inp if len(el) in UNIQUE_LEN.keys()}

        for el in inp:
            char_set = set(list(el))
            if char_set in known.values():
                continue
            
            digit_len = len(char_set)

            if digit_len == 6:
                if not known[1] <= char_set:
                    known[6] = char_set
                elif known[4] <= char_set:
                    known[9] = char_set
                else:
                    known[0] = char_set
        
        for el in inp:
            char_set = set(list(el))
            if char_set in known.values():
                continue

            digit_len = len(char_set)

            if digit_len == 5:
                if known[1] <= char_set:
                    known[3] = char_set
                elif char_set <= known[6]:
                    known[5] = char_set
                else:
                    known[2] = char_set

        outp_num = []
        for el in outp:
            char_set = set(list(el))
            outp_num.extend([str(k) for k, v in known.items() if char_set == v])
        outp_list.append(int(''.join(outp_num)))

    return sum(outp_list)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, prompt='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(8, example=example)))


if __name__ == '__main__':
    main()