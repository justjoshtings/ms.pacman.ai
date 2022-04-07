# ms.pacman.ai - Group3
## George Washington University, Cloud Computing - DATS6450, Spring 2022

![pacman](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/pacman_demo.gif)

# Project Description
Train an AI agent to play Ms. Pacman from Atari 2600.

![mspacman_env](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/mspacman_environment.png)
## Table of Contents
1. [Team Members](#team_members)
2. [How to Run](#instructions)
3. [Folder Structure](#structure)
4. [Background and Related Works](#background)
5. [Architecture](#architecture)
6. [Results](#results)
7. [Presentation](#presentation)
8. [References](#references)
9. [Licensing](#license)

# <a name="team_members"></a>
## Team Members
* [Sahara Ensley](https://github.com/Saharae)
* [Adam Kritz](https://github.com/adamkritz)
* [Joshua Ting](https://github.com/justjoshtings)

# <a name="instructions"></a>
## How to Run

[See web_app README.](https://github.com/justjoshtings/ms.pacman.ai/blob/main/web_app/README.md#setup)

# <a name="structure"></a>
## Folder Structure
1. assets: assets of web-app
2. GPU script: for training model on GPU machine
3. logs: logs of web-app
4. model_building: testing for initial model building
5. stream_test: testing for streaming service during gameplay
6. stream_test_react: testing for connecting streaming to react front end
7. web_app: main web-app directory
8. web_app_test: testing for web-app

# <a name="background"></a>
## Background and Related Works
* Mnih et al. 2013 Playing Atari with Deep Reinforcement Learning<sup>4</sup>
* Deep Reinforcement Learning, DeepMind Blog Post 2016<sup>11</sup>
* Schrittwieser et al. 2020 Mastering Atari, Go, chess and shogi by planning with a learned model<sup>12</sup>
* MuZero: Mastering Go, Chess, Shogi, and Atari without Rules, DeepMind Blog Post 2020<sup>13</sup>

# <a name="architecture"></a>
## Architecture

#### Learning Network Architecture
![DQN-architecture](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/DQN_architecture.png)
#### Streaming Service Architecture
![streaming-architecture](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/streaming_architecture.png)
#### Web-App Architecture
![web-app-architecture](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/web_app_architecture.png)
#### Cloud Architecture
![cloud-architecture](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/Cloud_architecture.png)
# <a name="results"></a>
## Results

![gameresults_1](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/gameresults_1.png)
![gameresults_2](https://github.com/justjoshtings/ms.pacman.ai/blob/main/assets/architecture/gameresults_2.png)

# <a name="presentation"></a>
## Presentation
[Google Slide Presentation](https://docs.google.com/presentation/d/1lLTH2cRfMQij-Yyh8kd9iWwK3bEgYDN4M8Zy29MZSV8/edit?usp=sharing)
# <a name="references"></a>
## References
1. [OpenAI Gym](https://github.com/openai/gym)
```
@misc{1606.01540,
  Author = {Greg Brockman and Vicki Cheung and Ludwig Pettersson and Jonas Schneider and John Schulman and Jie Tang and Wojciech Zaremba},
  Title = {OpenAI Gym},
  Year = {2016},
  Eprint = {arXiv:1606.01540},
}
```
2. [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment)
```
@Article{bellemare13arcade,
    author = {{Bellemare}, M.~G. and {Naddaf}, Y. and {Veness}, J. and {Bowling}, M.},
    title = {The Arcade Learning Environment: An Evaluation Platform for General Agents},
    journal = {Journal of Artificial Intelligence Research},
    year = "2013",
    month = "jun",
    volume = "47",
    pages = "253--279",
}
```
3. [Keras-RL](https://github.com/keras-rl/keras-rl)
```
@misc{plappert2016kerasrl,
    author = {Matthias Plappert},
    title = {keras-rl},
    year = {2016},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/keras-rl/keras-rl}},
}
```
4. [Playing Atari with Deep Reinforcement Learning, Mnih et al., 2013](https://arxiv.org/abs/1312.5602)
5. [Deep Reinforcement Learning with Double Q-learning, van Hasselt et al., 2015](https://arxiv.org/abs/1509.06461)
6. [Continuous Deep Q-Learning with Model-based Acceleration, Gu et al., 2016](https://arxiv.org/abs/1603.00748)
7. [Dueling Network Architectures for Deep Reinforcement Learning, Wang et al., 2016](https://arxiv.org/abs/1511.06581)
8. [Prioritized Experience Replay, Schaul et al., 2016](https://arxiv.org/abs/1511.05952)
9. [Rainbow: Combining Improvements in Deep Reinforcement Learning, Hessel et al., 2017](https://arxiv.org/abs/1710.02298)
10. [Noisy Networks for Exploration, Fortunato et al., 2018](https://arxiv.org/abs/1706.10295)
11. [Deep Reinforcement Learning, DeepMind Blog Post 2016](https://deepmind.com/blog/article/deep-reinforcement-learning)
12. [Schrittwieser et al. 2020 Mastering Atari, Go, chess and shogi by planning with a learned model](https://www.nature.com/articles/s41586-020-03051-4.epdf?sharing_token=kTk-xTZpQOF8Ym8nTQK6EdRgN0jAjWel9jnR3ZoTv0PMSWGj38iNIyNOw_ooNp2BvzZ4nIcedo7GEXD7UmLqb0M_V_fop31mMY9VBBLNmGbm0K9jETKkZnJ9SgJ8Rwhp3ySvLuTcUr888puIYbngQ0fiMf45ZGDAQ7fUI66-u7Y%3D)
13. [MuZero: Mastering Go, Chess, Shogi, and Atari without Rules, DeepMind Blog Post 2020](https://deepmind.com/blog/article/muzero-mastering-go-chess-shogi-and-atari-without-rules)

# <a name="license"></a>
## Licensing
* MIT License
