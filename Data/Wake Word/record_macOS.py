import wave
import pyaudio
import os
import time

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2.5

# some prompts for the user to reduce line width
NOISE_MSG = "Noise Level - Quiet (Q) Moderate (M) Loud (L): "
LAST_MSG = "If finished recording, type (q). Otherwise, type anything else: "

quit_inp = 0 # var for quitting out of program

# program loop
while (quit_inp != 'q'):
    feat_type = 0 # wake or not wake work label
    gender = 0 # gender label
    end_desc_sess = 0 # ends the current description session

    # ensures proper input of either ww or notww
    while not(feat_type == "ww" or feat_type == "notww"):
        feat_type = input("WW or NotWW: ").lower()

    # ask for name regardless of WW or NotWW
    # helps for adding "_{}.wav".format(last_name) later
    first_name = input("First Name: ").lower() # used for labeling file
    last_name = input("Last Name: ").lower() # ''

    if (feat_type == "ww"):
        target_dir = "Wake Word" # used for setting the correct directory
        ww_noise = 0

        # ensures proper input
        while not (gender == "m" or gender == "f"):
            gender = input("Male (m) or Female (f): ").lower()

        # labeling brief description
        ww_descr = (input("Enter the description: ").lower()).replace(" ","-")

        # labeling the recording location
        ww_loc = (input("Location: ").lower()).replace(" ","-")

        while not(ww_noise == 'q' or ww_noise == 'm' or ww_noise == 'l'):
            ww_noise = input(NOISE_MSG).lower()

    else:
        target_dir = "Not Wake Word"
        nww_noise = 0
        nww_descr = ((input("Enter description: ")).lower()).replace(" ","-")
        nww_loc = (input("Location: ").lower()).replace(" ","-")

        while not(nww_noise == 'q' or nww_noise == 'm' or nww_noise == 'l'):
            nww_noise = input(NOISE_MSG).lower()

    # description session loop
    #while (end_desc_sess != 'e'):
    while (1):

        p = pyaudio.PyAudio()

        frames = []

        print("Recording in\n3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("**RECORDING**")

        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
                        input = True, output = True, frames_per_buffer = CHUNK)

        for i in range(0,int(RATE/CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("**RECORDING ENDED**")

        # while(input("Play Audio (p): ").lower() == 'p'):
        #     for values in frames:
        #         stream.write(values)

        stream.stop_stream()
        stream.close()

        p.terminate()

        # if (input("To delete, type (d): ").lower() == 'd'):
        #     pass
        if(True):
        # else:
            curr_time = time.strftime("%m%d%Y%H%M%S", time.localtime())

            if (feat_type == "ww"):
                file_name = "ww_" + gender + "_" + ww_descr + "_" + ww_loc
                file_name += "_" + ww_noise + "_" + last_name + "_"
                file_name += first_name + "_" + curr_time
                file_name += "_{}.wav".format(last_name)

            else:
                file_name = "notww_" + nww_descr + "_" + nww_loc
                file_name += "_" + nww_noise + "_" + curr_time
                file_name += "_{}.wav".format(last_name)

            print(file_name + " has been saved.")

            path = os.path.join(os.getcwd() , target_dir , file_name)

            wf = wave.open(path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

        #end_desc_sess = input("If finished with description session, type (e); otherwise, type anything else: ").lower()

    quit_inp = input(LAST_MSG).lower()