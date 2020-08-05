. ./path.sh

export train_cmd="run.pl"

rm ./utils && ln -s $KALDI_ROOT/egs/wsj/s5/utils ./
rm ./steps && ln -s $KALDI_ROOT/egs/wsj/s5/steps ./
rm ./sid && ln -s $KALDI_ROOT/egs/sre08/v1/sid ./
rm -r ./test_data