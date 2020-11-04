"""
# Initialize
audio = None

# Loop
while True:
    decision, score = get_score(audio)
    if decision == 1:
        return score, count, audio
    grad = get_grad(audio)
    loss = None
    audio += lr * grad

    print(score, loss, grad, audio)
"""

from kaldiHelper import kaldiHelper as kaldi
from scipy.io.wavfile import read, write
import numpy as np
import copy
import subprocess

class Attack():
    def __init__(self):
        audio_list = [
            {
                'id': 'test_attack-tmp-test',
                'label': False,
            },  
        ]
        self.audio_path = "./new_test/test_attack/tmp/"
        self.helper = kaldi(tmp_dir = "./tmp", test_dir = "./new_test", debug = False)
        self.helper.data_prepare(audio_list)

        init_score = self.helper.run()
        print(init_score)
        self.delta = np.abs(init_score / 10)
        self.threshold = init_score + self.delta
        self.adver_thresh = 0.1
        self.debug = False

    def loss_fn(self, audios=None, fs=16000, bits_per_sample=16, n_jobs=10, debug=False):
        score = self.helper.run()
        # score_max = np.max(score, axis=1, keepdims=True) # (samples_per_draw + 1, 1)
        loss = np.maximum(self.threshold - score, -1 * self.adver_thresh)
        return loss, score # loss is (samples_per_draw + 1, 1)

    def get_grad(self, audio, fs=16000, bits_per_sample=16, n_jobs=10, debug=False, sigma=0.001, samples_per_draw=50):

        if len(audio.shape) == 1:
            audio = audio[:, np.newaxis]
        elif audio.shape[0] == 1:
            audio = audio.T
        else:
            pass
        
        N = audio.size

        noise_pos = np.random.normal(size=(N, samples_per_draw // 2))
        noise = np.concatenate((noise_pos, -1. * noise_pos), axis=1)
        noise = np.concatenate((np.zeros((N, 1)), noise), axis=1)
        noise_audios = sigma * noise + audio
        loss, scores = self.loss_fn(noise_audios, fs=fs, bits_per_sample=bits_per_sample, n_jobs=n_jobs, debug=debug) # loss is (samples_per_draw + 1, 1)
        # adver_loss = loss[0]
        # score = scores[0]
        # loss = loss[1:, :]
        # noise = noise[:, 1:]
        # final_loss = np.mean(loss)
        # estimate_grad = np.mean(loss.flatten() * noise, axis=1, keepdims=True) / sigma # grad is (N,1)
        # return final_loss, estimate_grad, adver_loss, score # scalar, (N,1)
        estimate_grad = np.mean(loss * noise, axis=1, keepdims=True) / sigma
        return estimate_grad

    def attack(self, lr=0.001):
        audio_path = self.audio_path
        fs, audio = read(audio_path + "test.wav")
        write(audio_path + "test_0.wav", fs, audio)
        for i in range(10):
            fs, audio = read(audio_path + "test.wav")
            adver = copy.deepcopy(audio)

            # Gradient 
            """
            adver = adver + lr * grad
            """
            grad = self.get_grad(adver)
            grad = np.squeeze(grad)
            adver = adver + lr * grad

            filename = audio_path + "test_" + str(i) + ".wav"
            write(filename, fs, adver)

            args = ["sox", filename, "-r", "16000", audio_path + "tmp.wav"]
            p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p.wait()

            args = ["sox", audio_path + "tmp.wav", "-b", "16", audio_path + "test_" + str(i) + ".wav"]
            p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p.wait()

            print(self.helper.run())


def main():
    attack = Attack()
    attack.attack()
    # audio_list = [
    #     {
    #         'id': 'test_attack-tmp-test_2',
    #         'label': False,
    #     },  
    # ]
    # audio_path = "./new_test/test_attack/tmp/test_2.wav"
    # helper = kaldi(tmp_dir = "./tmp", test_dir = "./new_test", debug = False)
    # helper.data_prepare(audio_list)
    # for i in range(10):
    #     fs, audio = read(audio_path)
    #     adver = copy.deepcopy(audio)

    #     # Gradient 
    #     """
    #     adver = adver + lr * grad
    #     """
    #     for j in range(audio.shape[0]):
    #         adver[j] = audio[j] + 1000


    #     write(audio_path, fs, adver)
    #     print(helper.run())

if __name__ == "__main__":
    main()
