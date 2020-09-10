test=$1
num_jobs=1

if [ -n "$(ls -A tmp 2>/dev/null)" ]
then
  rm -r ./tmp
fi

#local/make_voxceleb1_v2.pl $test test tmp/data
python kaldiHelper.py
# ./utils/fix_data_dir.sh tmp/data

# for file in utt2spk spk2utt feats.scp wav.scp; do
#   file=./tmp/data/$file
#   if [ -f $file ]; then
#     echo $file
#     sort -k1,1 -u <$file >$file.tmp
#     mv $file.tmp $file
#   fi
# done

trials=tmp/data/trials

./steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $num_jobs --cmd "$train_cmd" tmp/data tmp/make_mfcc tmp/mfcc
./utils/fix_data_dir.sh tmp/data

./sid/compute_vad_decision.sh --nj $num_jobs --cmd "$train_cmd" tmp/data tmp/make_vad tmp/vad
./utils/fix_data_dir.sh tmp/data

./sid/extract_ivectors.sh --cmd "$train_cmd" --nj $num_jobs exp/extractor tmp/data tmp/ivectors

$train_cmd exp/scores/log/test_scoring.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 exp/ivectors_train/plda - |" \
    "ark:ivector-subtract-global-mean exp/ivectors_train/mean.vec scp:tmp/ivectors/ivector.scp ark:- | transform-vec exp/ivectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean exp/ivectors_train/mean.vec scp:tmp/ivectors/ivector.scp ark:- | transform-vec exp/ivectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "cat '$trials' | cut -d\  -f 1,2 |" tmp/scores

eer=`compute-eer <(local/prepare_for_eer.py $trials tmp/scores) 2> /dev/null`;
echo “$eer%”;
 
return 0;