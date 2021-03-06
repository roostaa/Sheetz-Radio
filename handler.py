# this file is responsible for sporify api calls
import platform             #Used for OS detection
import os                   #Used for running commands in the system shell
import math                 #Used for meth
import spotipy              #Used to interact with Spotify API
import spotipy.util as util #Used to authenticate Spotify API tokens
import xFunctions           #Extra miscellaneous functions
#from main import doDebugShit

"""NOTE: you need to set your Spotify API credentials as environment variables as of right now, this will be worked out in the future..."""
def authRoutine():

    # this part is essential, but who understands their own code less than those who write it?
    scope = " "

    # promps user to enter username, required to get user token from spotify
    username = input("Username: ")
    global token
    token = util.prompt_for_user_token(username,scope)

    # probably shouldn't happen but you never know
    if not token:
        print("Can't get token for", username)

# searches spotify for the current song, fetches metadata of song
def metaFetch(song,artist):

    # initiates connection with user token and makes query with the song name/artist
    spInteract = spotipy.Spotify(auth=token)
    queryResults = spInteract.search(q='track:'+song+' artist:'+artist,type='track')
    if doDebugShit:
        print('hi still doing debug shit fuck me in the asshole please and thank you (use mayo as lube)')
    # beware beyond this point...
    dataA = queryResults["tracks"]

    if dataA["total"]>0:

        # The following code goes from the full API result down to more and more specific entries in either a dict or list.
        # Don't question it
        dataB = dataA["items"]
        dataC = dataB[0]
        dataD = dataC["album"]
        dataE = dataD["images"]
        dataF = dataE[0]
        dataG = dataF["url"]            #ALBUM ART
        dataH = dataD["release_date"]   #RELEASE DATE
        dataI = dataC["popularity"]     #POPULARITY
        dataJ = dataC["duration_ms"]    #DURATION IN MILLISECONDS
        dataK = dataD["name"]           #ALBUM TITLE
        dataL = dataC["preview_url"]    #MP3 PREVIEW

        # converts duration into something more readable
        durationSeconds = (dataJ / 1000)
        durationSecondsRemainder = (durationSeconds % 60)
        durationMinutes = math.floor(durationSeconds / 60)

        if math.floor(durationSecondsRemainder) < 10:
            duration = ""
            durationSecondsRemainder_2 = "0" + str(math.floor(durationSecondsRemainder))
            duration = str(durationMinutes) + ":" + durationSecondsRemainder_2
        duration = ""
        duration = str(durationMinutes) + ":" + str(math.floor(durationSecondsRemainder))

        #TODO fix issue where trying to run twice in the duration of a song will crash the program

        if enablePreview:
            import vlc      #use pip install python-vlc to get this package
            player = vlc.MediaPlayer(dataL)
            player.play()
        else:
            print("Your computer is running Windows or macOS and is incompatible with Python-VLC. No song preview will be played.")
        #TODO figure out how to get cava or something to work in the same terminal...

        xFunctions.screenRefresh()

        print("Track Data:\nTitle: ",song,"\nArtist: ",artist,"\nAlbum: ",dataK,"\nRelease Date: ",dataH,"\nPopularity: ",dataI,"\nSong Duration: ", duration)
    else:
        print("No track data found in Spotify database.")
