from Fraction import Fraction

if __name__ == '__main__':
    print('Welcome to Fun with Fractions!')
    while True:
        user_input = input('Enter Number of Iterations (integers > 0)')
        try:
            if int(user_input) > 0:
                break
            else:
                continue
        except:
            continue

    total_H = Fraction(0, 1)
    total_T = Fraction(1, 1)
    total_Z = Fraction(2, 1) - Fraction(1, 1)

    for n in range(1, int(user_input)+1):

        total_H += Fraction(1, n)
        total_T += Fraction(1, 2)**n
        total_Z -= Fraction(1, 2)**n

    print('H({})={}'.format(user_input, total_H))
    print('H({})~={:.8f}'.format(user_input, total_H.approximate()))
    print('T({})={}'.format(user_input, total_T))
    print('T({})~={:.8f}'.format(user_input, total_T.approximate()))
    print('Z({})={}'.format(user_input, total_Z))
    print('Z({})~={:.8f}'.format(user_input, total_Z.approximate()))

    for b in range(2, 9):
        total_B = Fraction(0, 1)
        for n in range(1, int(user_input)+1):
            total_B += Fraction(1, n)**b
        print('R({},{})={}'.format(user_input,b,total_B))
        print('R({},{})~={:.8f}'.format(user_input,b,total_B.approximate()))
