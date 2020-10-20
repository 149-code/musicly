from selenium import webdriver
from pydub import AudioSegment
from audio_player import AudioPlayer
import pytube, os, threading, random, time
from pynput import keyboard
import Quartz

def create_driver():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome("chromedriver", options = op)

    return driver

def get_youtube_url(driver, title):
    title = title.replace(" ", "+")
    URL = f"https://www.youtube.com/results?search_query={title}"
    driver.get(URL)

    elements = driver.find_elements_by_class_name("ytd-item-section-renderer")
    link = elements[0].find_element_by_xpath('//div/div/div/div/h3/a').get_attribute("href")

    return link

def download_from_youtube_url(link, filename):
    yt = pytube.YouTube(link)
    stream = yt.streams.get_audio_only()
    stream.download("/tmp")

    audio_seg = AudioSegment.from_file(f"/tmp/{stream.default_filename}", "mp4")
    audio_seg = audio_seg[:(yt.length * 1000)]

    audio_seg.export(filename, format="mp3")
    return yt.length

def download(driver, title, filename):
    link = get_youtube_url(driver, title)
    length = download_from_youtube_url(link, filename)
    return length

def handler(pid, output, link, filename):
    while True:
        try:
            filename = filename.replace(" ", "-")
            length = download_from_youtube_url(link, filename)
            output[pid] = length
            break
        except:
            print(f"download failed for song {pid}, retrying")

def create_playlist(driver, spec_filename):
    with open(spec_filename, "r") as file:
        content = file.read().split("\n")
    video_titles = [i for i in content if i != ""]

    playlist_name = spec_filename.replace(".spec", "")
    os.mkdir(playlist_name)

    video_urls = [get_youtube_url(driver, i) for i in video_titles]
    work = [(video_urls[i], os.path.join(playlist_name, video_titles[i])) for i in
            range(len(video_titles))]

    threads = []
    video_legnths = [None] * len(video_titles)
    for i in range(len(video_titles)):
        threads.append(threading.Thread(target = handler, args = (i, video_legnths, video_urls[i],
            os.path.join(playlist_name, f"{video_titles[i]}.mp3"))))
        threads[-1].start()

    for thread in threads:
        thread.join()

    with open(os.path.join(playlist_name, "playlist.info"), "w") as info_file:
        for num in range(len(video_titles)):
            filename = video_titles[num].replace(" ", "-")
            info_file.write(f"{video_legnths[num]},{filename}.mp3\n")

EventMediaKeysSubtype = 8
mediaPause = 16
mediaSkipForward = 19
mediaSkipBackwards = 20

input_handler_chan = []
def play_playlist(filepath, shuffle = False, volume = 1.0):
    global input_handler_chan

    with open(os.path.join(filepath, "playlist.info")) as file:
        entries = file.read().split("\n")
        entries.remove("")

    entries = [i.split(",", 1) for i in entries]

    if shuffle:
        random.shuffle(entries)

    while True:
        song_index = 0
        paused = False
        while song_index < len(entries):
            length = float(entries[song_index][0])
            name = entries[song_index][1]
            print(name)
            player = AudioPlayer(os.path.join(filepath, name), volume=volume)
            player.play()

            listener = keyboard.Listener(darwin_intercept = input_handler)
            listener.start()

            while player.elapsed_time() < player.duration() - 0.1:
                if not input_handler_chan:
                    time.sleep(0.1)
                    continue
                message = input_handler_chan.pop()

                if message == mediaSkipForward:
                    song_index += 1
                    player.stop()
                    break

                if message == mediaSkipBackwards:
                    song_index -= 1
                    player.stop()
                    break

                if message == mediaPause:
                    if not paused:
                        player.pause()
                    else:
                        player.resume()
                    paused = not paused
 
            else:
                song_index += 1
                player.stop()

mediaIsPressed = {"Forwards": False, "Backwards": False, "Pause": False}
def input_handler(event_type, event):
    global input_handler_chan, mediaIsPressed

    if event_type == Quartz.NSSystemDefined:
        sys_event = Quartz.NSEvent.eventWithCGEvent_(event)

        if sys_event.subtype() == EventMediaKeysSubtype:
            key = ((sys_event.data1() & 0xffff0000) >> 16)

            if key == mediaPause:
                mediaIsPressed["Pause"] = not mediaIsPressed["Pause"]
                if not mediaIsPressed["Pause"]:
                    input_handler_chan.append(mediaPause)
                return

            if key == mediaSkipForward:
                mediaIsPressed["Forwards"] = not mediaIsPressed["Forwards"]
                if not mediaIsPressed["Forwards"]:
                    input_handler_chan.append(mediaSkipForward)
                return

            if key == mediaSkipBackwards:
                mediaIsPressed["Backwards"] = not mediaIsPressed["Backwards"]
                if not mediaIsPressed["Backwards"]:
                    input_handler_chan.append(mediaSkipBackwards)
                return

    return event
