"""
naive_bayes.py
==============
Utilities for computing Naive Bayes token likelihoods and class priors from a
token-frequency DataFrame whose rows are tokens and columns are categories.

WHY THE KeyError OCCURS
-----------------------
``DataFrame.iterrows()`` yields ``(index_label, row_series)`` pairs, so:

    for (row, column) in token_freq.iterrows():
        # 'row'    -> the token name  (e.g. "experience")
        # 'column' -> a pandas Series of per-category counts for that token
        #             e.g. Series([357, 528, 449, …], index=["Data science", …])

When you then write ``total_of_documents[column]``, pandas treats the entire
Series of *numeric count values* (357, 528, …) as index labels to look up in
``total_of_documents``, whose index contains *category name strings*.
Since integer counts are not valid category-name keys, pandas raises:

    KeyError: "None of [Index([357, 528, …], dtype='int64')] are in the [index]"

The fix is to index ``total_of_documents`` by **column name strings** instead
of by the Series of count values.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Vectorised approach (preferred)
# ---------------------------------------------------------------------------

def compute_token_likelihoods(token_freq: pd.DataFrame, alpha: float = 1) -> pd.DataFrame:
    """Return a smoothed likelihood table P(token | category).

    For every (token, category) pair the likelihood is:

        P(token | Ck) = (count(token, Ck) + alpha)
                        / (total_tokens_in_Ck + V * alpha)

    where V = vocabulary size (number of unique tokens).

    Parameters
    ----------
    token_freq : pd.DataFrame
        Rows are tokens, columns are categories, values are occurrence counts.
    alpha : float
        Laplace (add-alpha) smoothing parameter. Default is 1.

    Returns
    -------
    pd.DataFrame
        Same shape as ``token_freq``; each cell is P(token | category).

    Notes
    -----
    This table contains *likelihoods*, not full posterior probabilities.
    To classify a new document you still need to multiply these likelihoods
    by the class prior P(Ck) (see :func:`compute_class_priors`).
    """
    vocabulary_size = token_freq.shape[0]
    total_per_category = token_freq.sum(axis=0)          # one value per category
    denominator = total_per_category + vocabulary_size * alpha

    # Broadcasting: (token_freq + alpha) has shape (V, K);
    # dividing by denominator (shape K) along axis=1 aligns correctly.
    token_likelihoods = (token_freq + alpha).div(denominator, axis=1)
    return token_likelihoods


# ---------------------------------------------------------------------------
# Loop-based approach (for illustration / debugging)
# ---------------------------------------------------------------------------

def compute_token_likelihoods_loop(
    token_freq: pd.DataFrame, alpha: float = 1
) -> pd.DataFrame:
    """Row-by-row equivalent of :func:`compute_token_likelihoods`.

    This version is slower but makes the per-cell formula explicit.
    The critical fix compared to the original broken snippet is that the inner
    loop iterates over ``token_freq.columns`` (category *name* strings) and
    indexes ``total_per_category`` by those names, not by raw count values.
    """
    vocabulary_size = token_freq.shape[0]
    total_per_category = token_freq.sum(axis=0)

    likelihoods = token_freq.copy().astype(float)

    for token, row_vals in token_freq.iterrows():        # token = row label
        for category in token_freq.columns:              # category = column label
            likelihoods.loc[token, category] = (
                row_vals[category] + alpha
            ) / (total_per_category[category] + vocabulary_size * alpha)

    return likelihoods


# ---------------------------------------------------------------------------
# Class priors  P(Ck)
# ---------------------------------------------------------------------------

def compute_class_priors(doc_labels: pd.Series) -> pd.Series:
    """Compute P(Ck) = proportion of training documents belonging to class Ck.

    Parameters
    ----------
    doc_labels : pd.Series
        A Series of class/category labels, one per training document.

    Returns
    -------
    pd.Series
        Index = unique class labels, values = prior probabilities (sum to 1).

    Example
    -------
    >>> labels = pd.Series(["Data science", "Data science", "ML", "NLP"])
    >>> compute_class_priors(labels)
    Data science    0.50
    ML              0.25
    NLP             0.25
    dtype: float64
    """
    counts = doc_labels.value_counts()
    return counts / counts.sum()
