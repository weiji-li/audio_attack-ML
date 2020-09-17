# Weekly Report
Victor Li's weekly update in each week (report from previous week coming soon).

## 9.10 - 9.17
### For this week:
1. Finsih the `kaldihelper.py` part in the GD attack system;
2. It includes functionality:
    1. data prepartion
    2. helper function for make_mfcc, compute_vad, extract_ivectors
    3. Score cleanup (which return all the scores we need for attack)
```
source path.sh && python kaldiHelper.py
------------ python Kaldi Helper: data_prepare ------------
------------ python Kaldi Helper: data_prepare Done ------------

------------ python Kaldi Helper: make_mfcc ------------
./steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj 1 --cmd run.pl ./tmp/data ./tmp/make_mfcc ./tmp/mfcc
utils/validate_data_dir.sh: Successfully validated data-directory ./tmp/data
./steps/make_mfcc.sh: [info]: no segments file exists: assuming wav.scp indexed by utterance.
./steps/make_mfcc.sh: Succeeded creating MFCC features for data
------------ python Kaldi Helper: make_mfcc Done ------------

------------ python Kaldi Helper: compute_vad ------------
./sid/compute_vad_decision.sh --nj 1 --cmd run.pl ./tmp/data ./tmp/make_vad ./tmp/vad
Created VAD output for data
------------ python Kaldi Helper: compute_vad Done ------------

------------ python Kaldi Helper: extract_ivectors ------------
./sid/extract_ivectors.sh --nj 1 --cmd run.pl exp/extractor ./tmp/data ./tmp/ivectors
./sid/extract_ivectors.sh: extracting iVectors
./sid/extract_ivectors.sh: combining iVectors across jobs
./sid/extract_ivectors.sh: computing mean of iVectors for each speaker and length-normalizing
------------ python Kaldi Helper: extract_ivectors Done ------------

------------ python Kaldi Helper: get_score ------------
------------ python Kaldi Helper: get_score Done ------------

compute-eer ./tmp/tmp_scores
LOG (compute-eer[5.5.690~1-9b4dc]:main():compute-eer.cc:136) Equal error rate is 0%, at threshold 4.5798
0id10270-5sJomL_D0_g-00001	test_impulse-test1-test_1	6.7788	target
id10270-x6uYqmx31kE-00008	test_impulse-test1-test_2	-23.35532	nontarget
id10270-OXdd7Gmluts-00001	test_impulse-test1-test_3	7.712383	target
id10270-OXdd7Gmluts-00003	test_impulse-test1-test_4	-11.48767	nontarget
id10270-8jEAjG6SegY-00030	test_impulse-test1-test_5	7.428626	target
id10270-5r0dWxy17C8-00017	test_impulse-test1-test_6	-14.08226	nontarget
id10270-8jEAjG6SegY-00018	test_impulse-test1-test_7	4.579799	target
id10270-GWXujl-xAVM-00026	test_impulse-test1-test_8	-6.215351	nontarget
id10270-5r0dWxy17C8-00012	test_impulse-test1-test_9	7.6927	target
id10270-8jEAjG6SegY-00037	test_impulse-test1-test_10	-1.919195	nontarget
```
### For next week:
1. Start working on simple attack algorithm
2. Reading some papers on adavasarial attack

### Notes:

### Meeting:


## 9.3 - 9.10
### For this week:
1. Work on `kaldihelper.py` part in the GD attack system;
2. Finish the data preparation part for Kaldihelper;

### For next week:
1. Finish the `kaldihelper.py` part which get rid of all shell script

### Notes:
- The coding has a lot of parts

### Meeting:
- Keep a Weekly report note (which is here)