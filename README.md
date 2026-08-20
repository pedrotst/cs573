# CS 573 — Data Mining (Purdue, 2023)

Machine learning and data mining coursework: classifiers implemented from scratch, then deep
models in PyTorch.

## What's worth reading

**[`proj1`](proj1) — a Naive Bayes classifier written from scratch.**
[`nbc.py`](proj1/nbc.py) implements the classifier with Laplacian smoothing, alongside the
whole supporting pipeline: discretisation and binning ([`databin.py`](proj1/databin.py)),
preprocessing, train/test splitting, and plotting. No classifier library involved — the
model is the code.

**[`FMnist_New_Setting.ipynb`](FMnist_New_Setting.ipynb) — PyTorch on Fashion-MNIST.**
A GAN, plus agglomerative and hierarchical clustering via scipy and scikit-learn, evaluated
with normalised mutual information and confusion matrices.

**[`proj2`](proj2), [`proj3`](proj3), [`proj5`](proj5)** — further assignments as notebooks.

## Caveats

Coursework, written to deadlines. Datasets are included where the assignments shipped them.
