import numpy as np


def select_coreset_frequency(
        P: np.array,
        SP: np.array,
        coreset_size: int,
        W_in: np.array = None,
) -> (np.array, np.array):
    """
    P, SP, W_in - all the same type: numpy
    :param P:  your points. if you have labels: from the shape X|y
    :param SP: your points sensitivity.
    :param coreset_size: the size of desired coreset
    :param W_in: weights of P. if not wighted input - ones(n)
    :return:
    """
    n = P.shape[0]
    assert coreset_size <= n
    if W_in is None:
        W_in = np.ones(n)

    prob = SP / SP.sum()
    indices_set = set()
    indices_list = []

    cnt = 0
    while len(indices_set) < coreset_size:
        i = np.random.choice(a=n, size=1, p=prob).tolist()[0]
        indices_list.append(i)
        indices_set.add(i)
        cnt += 1

    hist = np.histogram(indices_list, bins=range(n + 1))[0].flatten()
    indices_list = np.nonzero(hist)[0]
    C = P[indices_list, :]

    W_out = (W_in[indices_list].T * hist[indices_list]).T
    W_out = (W_out.T / (prob[indices_list] * cnt)).T
    return C, W_out


def select_coreset(A: np.array, SP: np.array, coreset_size: int) -> (np.array, np.array):
    """
    :param A: nx(d+1) points. can be torch\numpy
    :param SP: numpy array of nx1 sensitivities for each p in A
    :param coreset_size: size of the coreset
    :return:
    C: subset of A of size coreset_size x (d+1)
    W: weights of each c in C
    """
    n = len(A)
    sp_sum = SP.sum()
    sp_normed = SP / sp_sum
    # replace: False -> unique values, True  -> with reps
    C_ind = np.random.choice(a=range(0, n), size=coreset_size, p=sp_normed, replace=True)
    C = A[C_ind]
    W = sp_sum / (coreset_size * SP[C_ind])
    return C, W


def main():
    return


if __name__ == '__main__':
    main()
