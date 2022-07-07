# user_int = 0
#
# print('Welcome to Prime Generator')
# while True:
#     try:
#         user_int = input('Enter a number:\n')
#         user_int = int(user_int)
#         break
#     except ValueError:
#         continue
#
# for i in range(2, user_int + 1):
#     prime = True
#     for j in range(i-1, 1, -1):
#         if i % j == 0:
#             prime = False
#     if prime == True:
#         print(i, 'is a prime number.')

# import sys
#
# def getInt(question):
#     while True:
#         try:
#             user_int = input(question)
#             user_int = int(user_int)
#             break
#         except ValueError:
#             if user_int.lower() == 'exit':
#                 sys.exit()
#             print('Not a Number.')
#             continue
#     return user_int
#
#
# def binaryStr(num,bits):
#     binary_str = []
#     for i in range(bits):
#         binary_str.append(str(num % 2))
#         num = num // 2
#     binary_str.reverse()
#     binary_num = ''.join(binary_str)
#     return binary_num
#
# print('Welcome to Binary Printer')
# print('Enter exit to quit at any time.')
#
# while True:
#     user_num = getInt('Enter a Positive Int:\n')
#     user_bit = getInt('Number of Bits:\n')
#     print('As Binary:', binaryStr(user_num, user_bit))


# import sys
#
# print('Welcome to Book Analyzer v0.1')
#
# file_name = input('Enter File Name to Read:\n')
#
# try:
#     with open(file_name, 'r') as user_file:
#         user_letter = input('Letter to search for:\n')
#
#         if (not user_letter.isalpha()) or (len(user_letter) != 1):
#             raise ValueError('A single letter is required.')
#
#         user_pos = input('Enter Position (0 for first letter):\n')
#         if not user_pos.isdigit():
#             raise ValueError('A number is required.')
#         user_pos = int(user_pos)
#
#         count = 0
#         for line in user_file:
#             for word in line.split():
#                 if len(word) > user_pos:
#                     if word[user_pos].lower() == user_letter:
#                         count += 1
#         print('There are %d words with %s in position %d' %(count, user_letter, user_pos))
#
# except OSError:
#     print('Error: Could Not Open File.')
#     sys.exit(0)
# except ValueError as exception:
#     print('Error:', exception)
#     sys.exit(0)
# 
# import sys
#
# print('Welcome to a fun word replacement game.')
# file_name = input('Enter the name of the file to use:\n')
# vowels = ['a','e','i','o','u']
#
# def check_word(word):
#     if '-' in word:
#         word = word.split('-')
#         word = ' '.join(word)
#     if word[-1] != ']':
#         temp_ending = word[-1]
#         word = word[1:-2]
#     else:
#         temp_ending = ''
#         word = word[1:-1]
#     user_input = input('Please give %s %s\n' %('an' if word[0] in vowels else 'a', word))
#     user_input = user_input + temp_ending
#     return user_input
#
#
# try:
#     user_file = open(file_name, 'r')
# except OSError:
#     print('Error Bad File Name')
#     sys.exit(0)
#
# madlib = []
# for line in user_file:
#     for word in line.split():
#         if word[0] == '[':
#             word = check_word(word)
#         madlib.append(word)
#
# print('Here is your story:')
# print('-' * 20)
# print(' '.join(madlib))
# user_file.close()
