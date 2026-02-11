import matplotlib.pyplot as plt
from IPython import display

plt.ion()#Interactive

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf()) #Display figure 
    plt.clf() #Clear figure

    plt.title('Snake Training', fontsize=16)
    plt.xlabel('Game Number', fontsize=12)
    plt.ylabel('Score', fontsize=12)

    plt.plot(scores, label='Score', marker='o', linestyle='-', color='blue')
    plt.plot(mean_scores, label='Mean Score', marker='x', linestyle='--', color='green')

    if scores:
        plt.text(len(scores) - 1, scores[-1], str(scores[-1]), color='blue', fontsize=10, ha='right')
    if mean_scores:
        plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]), color='green', fontsize=10, ha='right')

    plt.show(block=False)
    plt.pause(.1)