'''
Christopher Morris
14289226

File contains the Media, Movie, Song, Picture that is called by the main.py file
'''


import abc

#Main Media Class
class Media(metaclass=abc.ABCMeta):

    def __init__(self, type, name , rating):
        self.__type = type
        self.__name = name
        self.setRating(rating)

    @abc.abstractmethod
    def __str__(self):
        return '\n{}: {} ({}/10 rating)'.format(self.getType(), self.getName(), self.getRating())
        # Force every subclass of media to override __str__ method

    # Getters
    def getType(self): #Get type of media (movie, song, picture, etc.)
        return self.__type

    def getName(self): #Get name of media file
        return self.__name

    def getRating(self): #Get rating of media file
        return self.__rating

    def getDisplay(self): #Get display function
        self.__display()
        # A generalized function that calls the different play or show functions of the subclasses
        # It is used in the process function in __main__

    def setType(self, type): #Set type for media file
        self.__type = type

    def setName(self, name): #Set Name of media file
        self.__name = name

    def setRating(self, rating): #Set rating, which makes sure the rating is an integer, and rounds any non-interger ratings
        try:
            self.__rating = int(rating)
        except:
            rating = float(rating)
            self.__rating = round(rating) #Makes the non-integer ratings integer

    def setDisplay(self, function): #set display function
        self.__display = function


class Movie(Media):
    def __init__(self, args, name, rating):
        super().__init__(type = 'Movie', name = name, rating = rating) #Call to Media __init__
        self.setDisplay(self.play) #sets generalized display function inherited by media to self.play
        self.__director = args[0]
        self.__runtime = args[1]

    def __str__(self): #Overides print by calling Media's __str__ and adding another line with the Movie specific __str__
        super_str = super().__str__()
        return super_str + '\n\tDirector: {}, Run time: {} minutes long.'.format(self.getDirector(), self.getRuntime())

    def play(self): #Play function used to 'play' the movie.
        print('\nPlaying {} by {}\n'.format(self.getName(), self.getDirector()))

    def getDirector(self): #Get director of movie
        return self.__director

    def getRuntime(self): #Get Runtime of movie
        return self.__runtime

    def setDirector(self, director): #Set director of movie
        self.__director = director

    def setRuntime(self, runtime): #Set runtime of movie
        self.__runtime = runtime


class Song(Media):

    def __init__(self, args, name, rating):
        super().__init__(type = 'Song', name = name, rating = rating) #Call to Media __init__
        self.setDisplay(self.play) #Sets generalized display function to self.play
        self.__artist = args[0]
        self.__album = args[1]

    def __str__(self): #Overides print by calling Media's __str__ and adding another line with the Song specific __str__
        super_str = super().__str__()
        return super_str + '\n\tBy {}, Album: {}'.format(self.getArtist(), self.getAlbum())

    def play(self): #Play function to 'play' the song
        print('\nPlaying {} by {}\n'.format(self.getName(), self.getArtist()))

    def getArtist(self): #Get song's artist
        return self.__artist

    def getAlbum(self): #Get song's album
        return self.__album

    def setArtist(self, artist): #Set song's artist
        self.__artist = artist

    def setAlbum(self, album): #Set song's album
        self.__album = album

class Picture(Media):

    def __init__(self, args, name, rating):
        super().__init__(type = 'Picture', name = name, rating = rating) #Call to Media __init__
        self.setDisplay(self.show) #Sets generalized display function to self.show
        self.setResolution(args[0])

    def __str__(self): #Overides print by calling Media's __str__ and adding another line with the Picture specific __str__
        super_str = super().__str__()
        return super_str + '\n\tResolution: {}'.format(self.getResolution())

    def show(self): #show function to 'show' the picture. The different name is the reason for the display function.
        print('\nShowing {}.png\n'.format(self.getName()))

    def getResolution(self): #Get pictures resolution
        return self.__resolution

    def setResolution(self, resolution):# Sets resolution and makes sure the resolution is a minimum of 200 dpi
        if float(resolution) >= 200:
            self.__resolution = '{} dpi'.format(resolution)
        else:
            print('Invalid picture resolution, must be above 200 dpi, \nincreasing quality of picture to reach minimum resolution')
            self.__resolution = 200
