sleep 30
cd /home/pi
rm -f webradio.log
sudo /usr/bin/python3 webradio.py > webradio.log 2>&1
