from spellchecker import spellchecker

def get_file():
    user_input = input('Please input the name of the file you would like to spell check:\n')
    while True:
        try:
            attempt = open(user_input, 'r')
            return attempt
        except:
            user_input = input('Not a valid input please try again:\n')
            continue

print('Welcome to spell checker.')
user_file = get_file()
SP = spellchecker("english_word.txt")

num_right = 0
num_wrong = 0
for line_number, line in enumerate(user_file, 1):
    for word in line.split():
        if not SP.check(word):
            print('Possible Spelling Error on Line {}: {}'.format(line_number, word))
            num_wrong += 1
        else:
            num_right += 1

percent = round(num_right / (num_wrong + num_right), 4)
print('{:,} words passed spell checker.'.format(num_right))
print('{:,} word failed spell checker.'.format(num_wrong))
print("{}% of the words passed.".format(100 * percent))
