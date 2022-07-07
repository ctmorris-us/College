# Question Class made to store questions, answers, and correct answers.
# It takes in a list that has 5 entries, the first is the question, the next four are the possible answers.
# And the last one is the correct answer index (etc. 1, 2, 3,4 )

class Question():
    def __init__(self, qa_list):
        self.__question = qa_list[0] #Stores Question
        self.__answers  = qa_list[1:5] #Stores Answers in a list
        self.__correct  = qa_list[5] #Stores single correct answer index

    def getQuestion(self):
        # Getter Method to return encapsulated question
        return self.__question

    def getAnswers(self):
        # Getter Method to return encapsulated answers
        return self.__answers

    def getCorrect(self):
        # Getter Method to return encapsulated correct answer index
        return self.__correct

    def __str__(self):
        # String method that prints out the question and properly formatted answers
        mystr = self.__question
        for counter, answer in enumerate(self.__answers, 1):
            mystr += '\n{}.  {}'.format(counter, answer)
        return mystr
