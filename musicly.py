import sys, time, os
from logic import create_driver, play_playlist, create_playlist, download
from audio_player import AudioPlayer

if len(sys.argv) == 1:
    error  = '''
Usage: ./musicly.py <SUBCOMMAND>

SUBCOMMANDS:
    play:       ./musicly.py play <Song Title>
    download:   ./musicly.py download <Song Title>
    playlist:   ./musicly.py playlist <SUBCOMMAND>
'''

    print(error)
    sys.exit(1)

if sys.argv[1] == "play":
    if len(sys.argv) != 3:
        print("Usage: ./musicly.py play <Song Title>")
    else:
        driver = create_driver()
        video_title = sys.argv[2].replace(" ", "-")
        length = download(driver, sys.argv[2], f"/tmp/{video_title}.mp3")

        sound = AudioPlayer(f"/tmp/{video_title}.mp3")
        sound.play()
        driver.quit()
        time.sleep(length)

elif sys.argv[1] == "download":
    if len(sys.argv) != 3:
        print("Usage: ./musicly.py download <Song Title>")
    else:
        driver = create_driver()
        filename = sys.argv[2].replace(" ", "-")
        length = download(driver, sys.argv[2], f"{filename}.mp3")
        driver.quit()

elif sys.argv[1] == "playlist":
    if len(sys.argv) == 2:
        error = '''
Usage: ./musicly.py playlist <SUBCOMMAND>

SUBCOMMANDS:
    gen:        ./musicly.py playlist gen <Playlist Spec>
    play:       ./musicly.py playlist play <Playlist Folder> [--shuffle]
'''
        print(error)

    else:
        if sys.argv[2] == "gen":
            if len(sys.argv) == 3:
                print("Usage: ./musicly.py playlist gen <Spec File>")
            elif len(sys.argv) == 4:
                driver = create_driver()
                create_playlist(driver, sys.argv[3])
                driver.quit()
        elif sys.argv[2] == "play":
            if len(sys.argv) == 3:
                print("Usage: ./musicly.py playlist play <Info File>")
            else:
                if len(sys.argv) >= 4:
                    args = sys.argv[4:]
                    volume = 1
                    shuffle = False
                    
                    for arg in args:
                        if arg == "--shuffle":
                            shuffle = False
                        if arg.startswith("--volume="):
                            volume = float(arg.replace("--volume=", ""))

                    play_playlist(sys.argv[3], shuffle = shuffle, volume = volume)
