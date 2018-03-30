rm -f nbmodel.txt
rm -f nboutput.txt
rm -f nblearn.pyc
python nblearn.py data/train-labeled.txt

python nbclassify.py data/dev-text.txt
python metric.py data/dev-key.txt nboutput.txt

rm -f nboutput.txt
printf "\n\n\n"
printf "Running on unseen data\n\n"

python nbclassify.py test_data.txt
python metric.py new_tagged_data.txt nboutput.txt
