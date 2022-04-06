######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0
    # Noise = 0 means Deterministic Search. It goes to its intended direction, i.e. won't fall off the bridge due to randomness. It will always go to right and acquire +10.00 as there is no risk of falling off. 
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.1
    answerNoise = 0
    answerLivingReward = -1
    #negative reward means we want the agent exit as fast as possible. Discount with 0.1 means the discouting effect is high and agent prefers rewards now to rewards later, i.e. it chooses the closer exit with value +1.00. With 0 Noise the agent goes to its intended direction, i.e. won't fall off the cliff. So it chooses the path nest to cliff.

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0
    #Discount with 0.1 and no living reward means the discouting effect is high and agent prefers rewards now to rewards later, it also won't benefit from living longer, i.e. it chooses the closer exit with value +1.00. With 0.1 Noise the agent has a chance to fall off the cliff, so it would aviod choosing the path next to cliff.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = -1
    #negative reward means we want the agent exit. No discount means we encourage distant exit. No noise means it is safe to walk near the cliff.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 1
    answerNoise = 0.2
    answerLivingReward = -1
    #negative reward means we want the agent exit. No discount means we encourage distant exit. Noise with 0.2 means it has a quite high chance to fall off the cliff, so it would aviod choosing the path next to cliff.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0
    answerNoise = 0
    answerLivingReward = 100
    #Reward with 100 means the agent is encouraged to live rather than exit, as the highest value for exit is +10 only. No discount means we encourage agent to walk further. No noise means it is safe to walk near the cliff.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    # No matter how epsilon and learning rate changes, 50 iterations are not enough to find an optimal solution. 
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
