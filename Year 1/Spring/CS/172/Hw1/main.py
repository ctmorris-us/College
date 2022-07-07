# Main program that imports the Question class from question.py
# It opens and reads the text file 'QA.txt' and creates a temporary list that is then fed into the Question class.
# The list is formatted so that the first entry is the question, the next four are the answers, and the last is the correct answer index.
# A final list is made with each of the instances of the Question class stored in it.

from question import Question

if __name__ == '__main__':
    with open('QA.txt', 'r') as file: #Opens QA.txt
        question_list = [] #list made to store the questions.
        for j in range(10): #For the 10 questions
            temp_list = [] #Temporary list
            for i in range(6):
                temp_list.append(file.readline()[:-1]) #Removes the \n from the text
            question_list.append(Question(temp_list)) #Appends instance of the Question class with the list fed into it

    print('Welcome to Game of Thrones Trivia (Spoilers Warning)')
    print('--------------------------------------------------- ')

    player_scores = [0,0] #First score is player1 and second is player2
    player = 0 #Index to keep track of the player number
    for question in question_list:
        print('\nPlayer {} here is your question:'.format(player%2 + 1)) #
        print(question,'\n') #prints question using the Question __str__ method

        possible_answers = ['1','2','3','4'] #list to check to see if the user inputs a possible answer choice

        while True: #Loop to make sure the user inputs a possible answer choice.
            user_answer = input('Enter your answer: ')
            if not user_answer in possible_answers:
                print('Error: your answer has to be a value between 1 and 4. Try Again.')
                continue
            else:
                break

        if user_answer == question.getCorrect(): #Calls Question getCorrect method which returns the index of the correct answer
            print('Excellent! You Score!')
            player_scores[player%2] += 1 #If correct increases the player's score by 1
        else:
            print('That is incorrect. Better luck with the next question.')

        player += 1 #Increases the player index to go to the next player

    print('\nAnd the final scores are:') #Prints the final score and each of the player's score
    print('Player 1:', player_scores[0])
    print('Player 2:',player_scores[1])

    if player_scores[0] == player_scores[1]: #Checks to see who the winner is or if there's a tie.
        print('Player 1 and Player 2 tie!')
    elif player_scores[0] > player_scores[1]:
        print('Player 1 wins!')
    elif player_scores[0] < player_scores[1]:
        print('Player 2 wins!')
