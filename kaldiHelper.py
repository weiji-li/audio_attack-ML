import numpy as np
import os
import time
import random
import subprocess
from scipy.io.wavfile import write

class kaldiHelper():

    def __init__(self, tmp_dir=None, test_dir=None):
        self.tmp_dir = tmp_dir
        self.test_dir = test_dir

        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        


    def data_prepare(self, audio_list, utt_id_list=None, spk_id_list=None, audio_dir=None, debug=False):

        data_dir = self.tmp_dir + "/data"

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        

        spk_id_list = spk_id_list if spk_id_list else [f for f in sorted(os.listdir(self.test_dir + "/test/wav")) if not f.startswith('.')]
        utt_id_list = []

        # wav.scp, utt2spk, spk2utt
        utt2spk_file = open(data_dir + "/utt2spk", "w")
        spk2utt_file = open(data_dir + "/spk2utt", "w")
        wav_file = open(data_dir + "/wav.scp", "w")
        for spk_id in spk_id_list:
            spk2utt_file.write(spk_id + " ")
            for dir_id in sorted(os.listdir(self.test_dir + "/test/wav/" + spk_id)):
                if dir_id.startswith("."):
                    continue
                for f in sorted(os.listdir(self.test_dir + "/test/wav/" + spk_id + "/" + dir_id)):
                    if f.startswith("."):
                        continue
                    utt_id = f.replace(".wav", " ")
                    id = spk_id + "-" + dir_id + "-" + utt_id
                    if not "test" in spk_id:
                        utt_id_list.append(id)
                    utt2spk_file.write(id)
                    utt2spk_file.write(spk_id)
                    utt2spk_file.write("\n")

                    spk2utt_file.write(id)

                    wav_file.write(id)
                    wav_file.write(self.test_dir + "/test/wav/" + spk_id + "/" + dir_id + "/" + f)
                    wav_file.write("\n")


            spk2utt_file.write("\n")
        
        test_size = len(audio_list)
        origin_list = random.sample(utt_id_list, test_size)

        trials = open(data_dir + "/trials", "w")
        for origin, test in zip(origin_list, audio_list):
            trials.write(origin)
            trials.write(test + "\n")
        
        # fix dir
        ''' Note: every time we execuate the shell script in utils/, steps/ or sid/, 
            we need to change the current directory to pre_model_dir.
            To avoid mistask, we should make all the dirs (e.g., audio_dir, log_dir) in absoulute path
        '''
        # current_dir = os.path.abspath(os.curdir)
        # os.chdir(self.pre_model_dir)

        # fix_dir_command = self.pre_model_dir + "/utils/fix_data_dir.sh " + audio_dir
        # args = shlex.split(fix_dir_command)
        # p = subprocess.Popen(args) if debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # p.wait()

        # os.chdir(current_dir)

        self.fix_data_dir()

        return utt_id_list

    def fix_data_dir(self, tmp_dir=None):
        tmp_dir = tmp_dir if tmp_dir else self.tmp_dir + "/data"
        subprocess.call(["./utils/fix_data_dir.sh", tmp_dir])
        print("done")
    

if __name__ == "__main__":
    audio_list = [
        'test_impulse-test-test_1 target', 
        'test_impulse-test-test_2 nontarget', 
        'test_impulse-test-test_3 target', 
        'test_impulse-test-test_4 nontarget', 
        'test_impulse-test-test_5 target', 
        'test_impulse-test-test_6 nontarget', 
        'test_impulse-test-test_7 target ', 
        'test_impulse-test-test_8 nontarget', 
        'test_impulse-test-test_9 target', 
        'test_impulse-test-test_10 nontarget'
    ]
    helper = kaldiHelper("./test_data", "./test_tmp")
    helper.data_prepare(audio_list)