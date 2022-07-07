'''
Christopher Morris
14289226

main program file that contains all the main functions to run the media program.
'''

from media import Movie, Song, Picture

# Pause Function that allows for better appearance on menu.
def pause():
    input('\nPress any key to return back to the menu.')
    return

#Function called for Playing/showing specific, user inputed media
def process(name, type):
    for item in media_list:
        if item.getType() == type:
            if item.getName().lower() == name: #Uses lower to make case insensitive
                item.getDisplay() #Use for display function to not have to include running if-elif statements
                return
    print('\n{} is not in the media library.\n'.format(name))

# Function used to display all of the media, Includes media type
def display_all():
    for item in media_list:
        print(item)

# Function used to display only the selected media type
def display_selected(type):
    for item in media_list:
        if item.getType() == type:
            print(item)

# Function used to display the window screen
def menu_option_display():
    print('\nMedia Library Options:')
    print('1: Display all items in the Library.')
    print('2: Display only the Movies.')
    print('3: Display only the Songs. ')
    print('4: Display only the Pictures.')
    print('5: Play a Specific Movie.')
    print('6: Play a Specific Song.')
    print('7: Show a Specific Picture.')
    print('8: Exit the Library and Quit the Program.')

# Function that inputs and checks whether the user's input is an integer between 1-8 inclusive
def verify_user_input():
    while True:
        user_input = input('\nSelect an Option (1-8):\n')
        try: #Checks if user's input is an integer and between 1-8 inclusive
            user_input = int(user_input)
            if 1 <= user_input <= 8:
                return user_input
            else:
                print('Invalid: Input must be in between an integer 1-8')
                continue
        except: #Reinputs user_input is not an integer and not between 1-8
            print('Invalid: Input must be in between an integer 1-8')
            continue


if __name__ == '__main__':

    with open('media.txt', 'r') as file: #Opens media.txt file
        media_list = []
        while True: #Generalized so that it doesn't have to be 12 media items
            temp = file.readline()[:-1].split(',')
            media_type = temp[0]
            if media_type == 'Movie':
                media_list.append(Movie(temp[3::], name = temp[1], rating = temp[2])) #Calls Movie class
            elif media_type == 'Song':
                media_list.append(Song(temp[3::], name = temp[1], rating = temp[2])) #Calls Song class
            elif media_type == 'Picture':
                media_list.append(Picture(temp[3::], name = temp[1], rating = temp[2]))#Calls Pictures
            elif media_type == 'End': #Included at end of media.txt file so that media file doesn't have to be 12 items
                break
            else:
                print('There was an error, invalid input')


    available_media = ['Movie', 'Song', 'Picture'] #Available media list
    while True:
        menu_option_display() #Prints out menu
        user_input = verify_user_input() #Get's user's input

        if user_input == 1:
            display_all() #Calls display all
            pause()
        elif 2 <= user_input <= 4:
            display_selected(available_media[user_input - 2])
            pause() #Calls display selected type
        elif 5 <= user_input <= 7:
            type = available_media[user_input-5] #Uses available media list and position on menu (options 5, 7)
            user_search = input('\nPlease type the name of the {} you would to find (Not case sensitive):\n'.format(type.lower()))
            process(user_search.lower(), type)
            pause() #Inputs user's name of movie and then calls process() to check for movie
        elif user_input == 8: #Done if user wants to exit
            print('\nThank you, have a nice day.')
            break #Ends program
