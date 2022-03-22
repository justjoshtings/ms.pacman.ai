import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

def make_temp_dat():
    cols = ['Score', 'Loss']
    temp_score = np.random.randint(low = 0, high = 2000, size = 1000000)
    temp_loss = np.random.random(size = 1000000)
    df = pd.DataFrame(data = np.array([temp_score, temp_loss]).T, columns = cols)
    df.to_csv('tempdat.csv')
    return df

def save_plot():
    df = pd.read_csv('/Users/sahara/Documents/GW/CloudComputing/ms.pacman.ai/tempdat.csv')
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (12,8))
    rand = np.random.randint(low = 0, high = 100000)
    last_round = df.Score[rand]
    avg_round = df.Score.mean()
    axes[0].bar(height = [last_round, avg_round], x = [1,2], color = ['mediumseagreen', 'lightcoral'])
    axes[0].set_xticks([1,2])
    axes[0].set_xticklabels(['Last Round Score', 'Average Score'])
    axes[0].set_ylabel('Round Score')

    sns.lineplot(y = df.Loss[0:20], x = np.arange(0, 20), ax = axes[1], color = 'red')
    axes[1].set_xlim((0,20))
    fig.suptitle('Test Plot')
    sns.despine()
    fig.savefig('/Users/sahara/Documents/GW/CloudComputing/ms.pacman.ai/tempfig.png')

def load_plot():
    fig = mpimg.imread('/Users/sahara/Documents/GW/CloudComputing/ms.pacman.ai/tempfig.png')
    return fig

def make_plot():
    df = pd.read_csv('/Users/sahara/Documents/GW/CloudComputing/ms.pacman.ai/tempdat.csv')
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (12,8))
    rand = np.random.randint(low = 0, high = 100000)
    last_round = df.Score[rand]
    avg_round = df.Score.mean()
    axes[0].bar(height = [last_round, avg_round], x = [1,2], color = ['mediumseagreen', 'lightcoral'])
    axes[0].set_xticks([1,2])
    axes[0].set_xticklabels(['Last Round Score', 'Average Score'])
    axes[0].set_ylabel('Round Score')

    sns.lineplot(y = df.Loss[0:20], x = np.arange(0, 20), ax = axes[1], color = 'red')
    axes[1].set_xlim((0,20))
    fig.suptitle('Test Plot')
    sns.despine()
    return fig

