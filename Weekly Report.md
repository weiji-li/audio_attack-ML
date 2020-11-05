# Weekly Report
Victor Li's weekly update in each week (report from previous week coming soon).

## 10.22 - 11.5
### For this week:
1. Finish a very simple gradient-descent attack
   - It could bascially work, but not achieve a good result
   - It includes a gradient-descent process, a gradient-estimation process and the previous kaldi wrapper I made
2. Read one presentation and one paper on audio and adversarial attack
   - formatted notes here (https://docs.google.com/document/d/15i8fyfTacinSDe8HwBDyj22knmqGT-UjY289vozt1C0/edit)
3. Took a look at the FGSM attack
    - It relates to Neural Network stuffs that I am just learning in my ML class. I am thinking of making use of it in my audio attack. 
### For next week:
1. Think about some ways to improve the gradient-descent 
2. Continue my paper reading plan

### Notes:

### Meeting:
1. Looking at more directions on Audio 
2. Neal might work on some audio-related projects

## 9.24 - 10.22
### For this week:
1. Read one paper and one blog on audio and adversarial attack
   1. formatted notes here (https://docs.google.com/document/d/15i8fyfTacinSDe8HwBDyj22knmqGT-UjY289vozt1C0/edit)
2. Start writing code for a simple gradient-descent attack (follow other's code)

### For next week:
1. Finish code for a simple gradient-descent attack
2. Read two more papers

### Notes:
1. Helloworld adversarial attack
2. FGSM attack (simplest) -> projected gradient descent (max depth constraints) -> 
3. Tutorial -- https://adversarial-ml-tutorial.org/

### Meeting:

## 9.17 - 9.24
### For this week:
1. Read the paper "Who is Real Bob? Adversarial Attacks on Speaker Recognition Systems"
2. Try to take a formatted notes (https://docs.google.com/document/d/15i8fyfTacinSDe8HwBDyj22knmqGT-UjY289vozt1C0/edit)

### For next week:

### Notes:
1. The algorithms in paper is quite hard to me right now. 

### Meeting:
1. biweekly
2. baseline: replicate existing attacks
3. RNN, CNN
4. batch gradient descent 
5. Citation and the equation 
6. Experiment the code in backend
7. Three passes: 
   1. abstract + intro + conclusion
   2. main + results
   3. methods + techniques

## 9.10 - 9.17
### For this week:
1. Finsih the `kaldihelper.py` part in the GD attack system;
2. It includes functionality:
    1. data prepartion
    2. helper function for make_mfcc, compute_vad, extract_ivectors
    3. Score cleanup (which return all the scores we need for attack)
### For next week:
1. Start working on simple attack algorithm
2. Reading some papers on adavasarial attack

### Notes:

### Meeting:
1. Have different hypothesis for algorithm ideas.
    - Could use form of LaTex or slides to report 
    - Learn different attack methods from papers
    - Think of unique novel ideas
    - Compare with recent works
2. Coding
    - Get familiar with audio GD attack
    - Put experiment to later


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