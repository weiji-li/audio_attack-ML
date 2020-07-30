. ./path.sh

test=$1
train_cmd="run.pl"
trials=data/voxceleb1_test/trials

local/make_voxceleb1_v2.pl $test test test_data/data

steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj 40 --cmd "$train_cmd" test_data/data test_data/make_mfcc test_data/mfcc
utils/fix_data_dir.sh test_data/data

sid/compute_vad_decision.sh --nj 40 --cmd "$train_cmd" test_data/data test_data/make_vad test_data/vad
utils/fix_data_dir.sh test_data/data

sid/extract_ivectors.sh --cmd "$train_cmd" --nj 40 exp/extractor test_data/data test_data/ivectors

$train_cmd exp/scores/log/test_scoring.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 exp/ivectors_train/plda - |" \
    "ark:ivector-subtract-global-mean exp/ivectors_train/mean.vec scp:test_data/ivectors/ivector.scp ark:- | transform-vec exp/ivectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean exp/ivectors_train/mean.vec scp:test_data/ivectors/ivector.scp ark:- | transform-vec exp/ivectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "cat '$trials' | cut -d\  -f 1,2 |" test_data/scores || exit 1;

eer=`compute-eer <(local/prepare_for_eer.py data/voxceleb1_test/trials  test_data/scores) 2> /dev/null`;
echo “$eer%”;
 
return 0;