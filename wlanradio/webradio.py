import time
import serial
import subprocess

playlistfile = "playlists/playlist.m3u"

def get_playlist():
    with open(playlistfile) as fh:
        bf = fh.read()
    playlist = []
    for line in bf.splitlines():
        if len(line) > 0 and not line.strip().startswith("#"):
            playlist.append(line)
    return playlist


def execute(playlistpos=None, volume=None):
    mpc = ["mpc"]
    if playlistpos:
        print(playlistpos)
        r = subprocess.run(mpc + ["play", str(playlistpos)], capture_output=True)
        print(r.stderr, r.stdout)
        if len(r.stderr) > 0:
            return r.stderr[:16]
        return r.stdout[:16]
    elif volume:
        r = subprocess.run(mpc + ["volume", str(volume)], capture_output=True)
        print(r.stderr, r.stdout)
        if len(r.stderr) > 0:
            return r.stderr[:16]
        return str(volume)
    else:
        r = subprocess.run(mpc + ["current"], capture_output=True)
        print(r.stderr, r.stdout)
        if len(r.stderr) > 0:
            return r.stderr[:16]
        return r.stdout[:16]


def main():
    volume = 70
    subprocess.run(["mpc", "clear"])
    subprocess.run(["mpc", "volume", str(volume)])
    subprocess.run(["mpc", "load", "playlist"])
    subprocess.run(["mpc", "volume", str(volume)])
    update = True
    tstart = 0
    playing = 1
    playlist = get_playlist()
    print(len(playlist))
    device = '/dev/ttyUSB0'
    baudrate = 115200
    with serial.Serial(device, baudrate, timeout=None) as connection:
        # \x15 is Ctrl-U
        # \x16 is Ctrl-V
        title = execute(playlistpos=playing)
        volumestr = execute(volume=volume)
        time.sleep(2)
        while True:
            if update:
                connection.write(bytes("\x03{title}\x16Volume {volume}".format(title=title.decode("ascii"), volume=volumestr), "ascii"))
                connection.flush()
                update = False
            if connection.in_waiting > 0:
                command = connection.readline()
                print(command)
                update = True
                if command.startswith(b"c+"):
                    playing = playing + 1 if playing < len(playlist) else 1
                    title = execute(playlistpos=playing)
                elif command.startswith(b"c-"):
                    playing = playing - 1 if playing > 1 else len(playlist)
                    title = execute(playlistpos=playing)
                elif command.startswith(b"v+"):
                    volume = volume + 1 if volume < 100 else 100
                    volumestr = execute(volume=volume)
                elif command.startswith(b"v-"):
                    volume = volume - 1 if volume > 0 else 0
                    volumestr = execute(volume=volume)
            if time.time() - tstart > 2:
                title = execute()
                update = True
                tstart = time.time()


if __name__ == '__main__':
    main()
