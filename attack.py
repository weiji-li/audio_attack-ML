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
