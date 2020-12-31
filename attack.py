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
    def __init__(self, audio_list):
        self.audio_list = audio_list
        
        self.audio_path = "./new_test/test_attack/tmp2/"
        self.helper = kaldi(tmp_dir = "./tmp", test_dir = "./new_test", debug = False)
        self.helper.data_prepare(self.audio_list)

        # init_score = self.helper.run()
        # print(init_score)
        # self.delta = np.abs(init_score / 10)
        # print(self.delta)
        # self.threshold = init_score + self.delta
        # print(self.threshold)
        self.threshold = 0.
        self.adver_thresh = 10
        self.debug = False

        print("finish settting up")

    def fgsm_attack(self):
        print(self.helper.run())

        for i in range(10):
            filename = "original_" + str(i+1) + ".wav"
            attack_filename = "fgsm_attack_" + str(i+1) + ".wav"

            fs, audio = read(self.audio_path + filename)
            lr = 0.0001
            estimate_grad = np.random.rand(audio.shape[0])
            # final_loss, estimate_grad, adver_loss, score = self.get_grad(audio)
            # print(final_loss.shape)
            # print(estimate_grad.shape)
            # print(adver_loss.shape)
            # print(final_loss, estimate_grad, adver_loss, score)
            new_audio = audio + lr * estimate_grad
            write(self.audio_path + "fgsm_attack_tmp.wav", fs, new_audio)

            args = ["sox", self.audio_path + "fgsm_attack_tmp.wav", "-t", "wav", "-r", "16000", "-b", "16", self.audio_path + attack_filename]
            p = subprocess.Popen(args) if self.debug else subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(args)
            p.wait()


        print(self.helper.run())
        # TODO: transform the data (line 71)

    def loss_fn(self, audios=None, fs=16000, bits_per_sample=16, n_jobs=10, debug=False):
        score = self.helper.run()
        score = np.array([score])
        print(self.threshold - score)
        loss = np.maximum(self.threshold - score, -1 * self.adver_thresh)
        return loss, score # loss is (samples_per_draw + 1, 1)

    def get_grad_1(self, audio, fs=16000, bits_per_sample=16, n_jobs=10, debug=False, sigma=0.001, samples_per_draw=50):

        if len(audio.shape) == 1:
            audio = audio[:, np.newaxis]
        elif audio.shape[0] == 1:
            audio = audio.T
        else:
            pass

        print(audio.shape)
        
        N = audio.size

        noise_pos = np.random.normal(size=(N, 1))
        noise = np.concatenate((noise_pos, -1. * noise_pos), axis=1)
        noise = np.concatenate((np.zeros((N, 1)), noise), axis=1)
        noise_audios = sigma * noise + audio
        print(noise_audios.shape)
        write(self.audio_path + "test0.wav", fs, noise_audios)
        loss, scores = self.loss_fn(noise_audios, fs=fs, bits_per_sample=bits_per_sample, n_jobs=n_jobs, debug=debug) # loss is (samples_per_draw + 1, 1)
        adver_loss = loss[0]
        print(loss.shape)
        # score = scores[0]
        # loss = loss[1:, :]
        # noise = noise[:, 1:]
        # final_loss = np.mean(loss)
        # estimate_grad = np.mean(loss.flatten() * noise, axis=1, keepdims=True) / sigma # grad is (N,1)
        # return final_loss, estimate_grad, adver_loss, score # scalar, (N,1)
        estimate_grad = np.mean(loss * noise, axis=1, keepdims=True) / sigma
        return estimate_grad

    def get_grad(self, audio, fs=16000, bits_per_sample=16, n_jobs=10, debug=False):

        if len(audio.shape) == 1:
            audio = audio[:, np.newaxis]
        elif audio.shape[0] == 1:
            audio = audio.T
        else:
            pass
        
        N = audio.size
        self.samples_per_draw = 1
        self.sigma = 0.001

        noise_pos = np.random.normal(size=(N, self.samples_per_draw // 2))
        noise = np.concatenate((noise_pos, -1. * noise_pos), axis=1)
        noise = np.concatenate((np.zeros((N, 1)), noise), axis=1)
        noise_audios = self.sigma * noise + audio
        loss, scores = self.loss_fn(noise_audios, fs=fs, bits_per_sample=bits_per_sample, n_jobs=n_jobs, debug=debug) # loss is (samples_per_draw + 1, 1)
        score = scores[0]
        adver_loss = loss[0]
        # adver_loss = loss
        loss = loss #changed loss = loss[1:, :]
        noise = noise[:, 1:]
        final_loss = np.mean(loss)
        estimate_grad = np.mean(loss.flatten() * noise, axis=1, keepdims=True) / self.sigma # grad is (N,1)
    
        return final_loss, estimate_grad, adver_loss, score # scalar, (N,1)

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
    audio_list = [
        {'id': 'test_attack-tmp2-original_1', 'label': True},
        {'id': 'test_attack-tmp2-original_2', 'label': False},
        {'id': 'test_attack-tmp2-original_3', 'label': True},
        {'id': 'test_attack-tmp2-original_4', 'label': False},
        {'id': 'test_attack-tmp2-original_5', 'label': True},
        {'id': 'test_attack-tmp2-original_6', 'label': False},
        {'id': 'test_attack-tmp2-original_7', 'label': True},
        {'id': 'test_attack-tmp2-original_8', 'label': False},
        {'id': 'test_attack-tmp2-original_9', 'label': True},
        {'id': 'test_attack-tmp2-original_10', 'label': False},
        {'id': 'test_attack-tmp2-fgsm_attack_1', 'label': True},
        {'id': 'test_attack-tmp2-fgsm_attack_2', 'label': False},
        {'id': 'test_attack-tmp2-fgsm_attack_3', 'label': True},
        {'id': 'test_attack-tmp2-fgsm_attack_4', 'label': False},
        {'id': 'test_attack-tmp2-fgsm_attack_5', 'label': True},
        {'id': 'test_attack-tmp2-fgsm_attack_6', 'label': False},
        {'id': 'test_attack-tmp2-fgsm_attack_7', 'label': True},
        {'id': 'test_attack-tmp2-fgsm_attack_8', 'label': False},
        {'id': 'test_attack-tmp2-fgsm_attack_9', 'label': True},
        {'id': 'test_attack-tmp2-fgsm_attack_10', 'label': False},
    ]
    attack = Attack(audio_list)
    attack.fgsm_attack()


if __name__ == "__main__":
    main()
