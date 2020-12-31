import os
import time
import random
import subprocess
import shutil
import shlex

class kaldiHelper():

    def __init__(self, tmp_dir=None, test_dir=None, cur_dir=None, num_jobs=1, train_cmd="run.pl", debug = True):
        self.tmp_dir = tmp_dir
        self.test_dir = test_dir
        self.cur_dir = os.path.abspath(cur_dir) if cur_dir else os.path.abspath(".")
        self.num_jobs = num_jobs
        self.train_cmd = train_cmd
        self.debug = debug

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir) 

        os.mkdir(tmp_dir)
        


    def data_prepare(self, audio_list, utt_id_list=None, spk_id_list=None, audio_dir=None, debug=False):
        if self.debug:
            print("------------ python Kaldi Helper: data_prepare ------------")
        data_dir = self.tmp_dir + "/data"

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        

        spk_id_list = spk_id_list if spk_id_list else [f for f in sorted(os.listdir(self.test_dir)) if not f.startswith('.')]
        utt_id_list = []

        # wav.scp, utt2spk, spk2utt
        utt2spk_file = open(data_dir + "/utt2spk", "w")
        spk2utt_file = open(data_dir + "/spk2utt", "w")
        wav_file = open(data_dir + "/wav.scp", "w")
        for spk_id in spk_id_list:
            spk2utt_file.write(spk_id + " ")
            for dir_id in sorted(os.listdir(self.test_dir + "/" + spk_id)):
                if dir_id.startswith("."):
                    continue
                for f in sorted(os.listdir(self.test_dir + "/" + spk_id + "/" + dir_id)):
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
                    wav_file.write(self.test_dir + "/" + spk_id + "/" + dir_id + "/" + f)
                    wav_file.write("\n")

            spk2utt_file.write("\n")
        
        test_size = len(audio_list)
        random.seed(123)
        origin_list = random.sample(utt_id_list, test_size)

        trials = open(data_dir + "/trials", "w")
        for origin, audio in zip(origin_list, audio_list):
            trials.write(origin)
            audio_id = audio["id"] 
            label = "target" if audio["label"] else "nontarget"
            trials.write(audio_id + " " + label + "\n")
        
        # fix dir
        # self.fix_data_dir()

        if self.debug:
            print("------------ python Kaldi Helper: data_prepare Done ------------\n")
        return utt_id_list

    def fix_data_dir(self, tmp_dir=None):
        debug = False
        current_dir = os.path.abspath(os.curdir)
        os.chdir(self.cur_dir)

        fix_dir_command = self.cur_dir + "/utils/fix_data_dir.sh " + self.tmp_dir + "/data"
        args = shlex.split(fix_dir_command)
        if self.debug:
            print(args)
        p = subprocess.Popen(args) if debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()

        # os.chdir(current_dir)

    def make_mfcc(self, config = "conf/mfcc.conf"):
        if self.debug:
            print("------------ python Kaldi Helper: make_mfcc ------------")
        args = ["./steps/make_mfcc.sh"]
        args.extend(["--write-utt2num-frames", "true"])
        args.extend(["--mfcc-config", config])
        args.extend(["--nj", str(self.num_jobs)])
        args.extend(["--cmd", self.train_cmd])
        args.extend([self.tmp_dir + "/data", self.tmp_dir + "/make_mfcc", self.tmp_dir + "/mfcc"])
        p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        if self.debug:
            print("------------ python Kaldi Helper: make_mfcc Done ------------\n")

    def compute_vad(self):
        if self.debug:
            print("------------ python Kaldi Helper: compute_vad ------------")
        args = ["./sid/compute_vad_decision.sh"]
        args.extend(["--nj", str(self.num_jobs)])
        args.extend(["--cmd", self.train_cmd])
        args.extend([self.tmp_dir + "/data", self.tmp_dir + "/make_vad", self.tmp_dir + "/vad"])
        p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        if self.debug:
            print("------------ python Kaldi Helper: compute_vad Done ------------\n")
    
    def extract_ivectors(self):
        if self.debug:
            print("------------ python Kaldi Helper: extract_ivectors ------------")
        args = ["./sid/extract_ivectors.sh"]
        args.extend(["--nj", str(self.num_jobs)])
        args.extend(["--cmd", self.train_cmd])
        args.extend(["exp/extractor", self.tmp_dir + "/data", self.tmp_dir + "/ivectors"])
        p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        if self.debug:
            print("------------ python Kaldi Helper: extract_ivectors Done ------------\n")

    def get_score(self):
        if self.debug:
            print("------------ python Kaldi Helper: get_score ------------")
        args = [self.train_cmd]
        args.extend(["exp/scores/log/test_scoring.log"])
        args.extend(["ivector-plda-scoring", "--normalize-length=true"])
        args.extend(["ivector-copy-plda --smoothing=0.0 exp/ivectors_train/plda - |"])
        tmp = "ark:ivector-subtract-global-mean exp/ivectors_train/mean.vec scp:tmp/ivectors/ivector.scp ark:- | transform-vec exp/ivectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |"
        args.extend([tmp, tmp])
        tmp = "cat '" + self.tmp_dir + "/data/trials' " + "| cut -d\  -f 1,2 |"
        args.extend([tmp, self.tmp_dir + "/scores"])
        p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        if self.debug:
            print("------------ python Kaldi Helper: get_score Done ------------\n")
    
    def compute_eer(self, scores, audio_list):
        args = ["compute-eer"]
        input_file = self.tmp_dir + "/tmp_scores"
        with open(self.tmp_dir + "/tmp_scores", "w+") as f:
            input = ""
            for score, audio in zip(scores, audio_list):
                input += score['score']
                input += " "
                input += audio['id']
                input += "\n"
                f.write(input)
                score['label'] = "target" if audio["label"] else "nontarget"
        args.append(input_file)
        p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait()
        return scores
    
    def score(self):
        scores = []
        with open(self.tmp_dir + "/scores") as f:
            lines = f.readlines()
            for line in lines:
                score = {}
                line_split = line.split()
                score['origin'] = line_split[0]
                score['test'] = line_split[1]
                score['score'] = line_split[2]
                scores.append(score)
        return scores

    def run(self):
        self.make_mfcc()
        self.compute_vad()
        self.extract_ivectors()
        self.get_score()
        print(self.score())
        return float(self.score()[0]["score"])

def main():
    audio_list = [
        {'id': 'test_background-test1-test_1', 'label':True}, 
        {'id': 'test_background-test1-test_2', 'label':False}, 
        {'id': 'test_background-test1-test_3', 'label':True}, 
        {'id': 'test_background-test1-test_4', 'label':False}, 
        {'id': 'test_background-test1-test_5', 'label':True}, 
        {'id': 'test_background-test1-test_6', 'label':False}, 
        {'id': 'test_background-test1-test_7', 'label':True}, 
        {'id': 'test_background-test1-test_8', 'label':False}, 
        {'id': 'test_background-test1-test_9', 'label':True}, 
        {'id': 'test_background-test1-test_10', 'label':False}, 
    ]
    helper = kaldiHelper(tmp_dir = "./tmp", test_dir = "./new_test")
    helper.data_prepare(audio_list)
    helper.make_mfcc()
    helper.compute_vad()
    helper.extract_ivectors()
    helper.get_score()
    scores = helper.score()
    scores = helper.compute_eer(scores, audio_list)

    for score in scores:
        print("\t".join([score['origin'], score['test'], score['score'], score['label']]))

if __name__ == "__main__":
    main()
