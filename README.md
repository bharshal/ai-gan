# AI-Gan final repo
AI-Gan is a cool demo application on HiKey 970. The flow is as follows:

![alt text](https://github.com/bharshal/ai-gan/blob/master/flow.png)

Also please see [Block diagram](https://github.com/bharshal/ai-gan/blob/master/block_diagram.png)

Uses MTCNN for Face detection. 
Uses DLib for face alignment. 
Uses FaceNet for generating embeddings. 
Uses pre-trained TF graph for speech recognition.

* code to train speech model for your words can be provided if needed
* no training of models required, only inference performed

### This code is to be run on HiKey970 only. 
To run on x86_64 computer, modifications are required (should be only done if you know what you are doing)

### To run this demo you need to connect 2 Arduino Uno boards to HiKey.
2 bit signals are passed to Arduinos for 4 different statuses

Arduino no. 1: Servo motor for dispenser
````
461  A0
487  A1 
````
Arduino no. 2: For LED indications
````
337  A0
501  A1 
````
### Kernel modules inside sound_drivers folder have to be insmod for microphone to work
Place them in /lib/modules/...  as directory structure present and then insmod them in order
chnage name of kernel as per actual kernel name (found using uname -a) 
````
1)midi
2)hdwep
3)usb-audio
````
Check if modules have been successfully installed using lsmod
````
sudo apt-get install portaudio19-dev
pip install pyaudio; wave; pydub
````

### Check which card mic is using in ````/proc/asound/````
find sound card number being used and change accordingly device index in 
````/utils/sound_record.py````

In ````/etc/modprobe.d/alsa-base.conf```` change the index values on these lines:
````
options snd-usb-audio index=0		to  (whatever index you find on your device)
options snd-bcm2835 index=1		
````


paste .asoundrc in home directory
and reboot
insmod modules again after reboot
											   

### models directory contains all files that are imported/called by the actual code.

### main_in.py and main_out.py have to be run simultaneously in separate terminals

main_in.py has code for input    
````
1)Code to check if a person is present in front of camera or not
2)If person detected, capture face data 
3)Capture voice input, recognise the word and assign it as label 
3)Save data
````

main_out.py has code for recognition   
````
1)Code to check if a person is present in front of camera or not
2)If person detected, recognise him/her and find label
3)Send command to robotic arm only once for each person
````
							       
							       
****Some model files are too big for uploading on git. Contact for details.
