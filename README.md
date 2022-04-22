# CS146 Final Project: Mahjong Data Models

## Summary

This repository shows the finding of a statistical model that researches the trends in the score, win rate, and rank of the top-ranked Mahjong Soul player, BUTA野郎. First, a web crawler was built to scrap data out of the MajSoul Stats website that hosts statistics from the popular online Japanese Mahjong game, Mahjong Soul. Then, two different models were built, including a simple Bayesian linear regression model and an extension model that includes additional. Finally, test statistics and train-test splits were conducted to compare and understand the efficacy of the modeling. The result shows that the marginal improvement of players through time in terms of the score is minimal.

## Get Started

1. Create virtual environment
```sh
python -m venv .venv
```

2. Download dependencies
```sh
pip install -r requirements.txt
```

3. Start running the notebooks!