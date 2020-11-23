from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
import numpy as np
import sys
from progress.bar import IncrementalBar
from getavgs import get_subreddit_from_id

# load averages
def load_averages(filename):
    ids = []
    bf_averages = []
    df_averages = []
    with open(filename, "r") as avgs_file:
        lines = avgs_file.readlines()
    for line in lines:
        _id, bf_list_str, df_list_str = line.split(":")
        ids.append(_id)
        bf_averages.append([int(x) for x in df_list_str.strip('][\n').split(', ')])
        df_averages.append([int(x) for x in bf_list_str.strip('][\n').split(', ')])
    return ids, df_averages, bf_averages

def overall_averages(arr):
    # takes in a 2d array and creates a 1d array
    # with a length equal to the max subarray of arr,
    # consisting of the averages for each column
    result = []
    max_subarray_size = max([len(x) for x in arr])
    for j in range(max_subarray_size):
        for i in range(len(arr)):
            try:
                result[j] += arr[i][j]
            except IndexError:
                try:
                    result[j] += 0
                except IndexError:
                    result.append(0)
    for j in range(len(result)):
        result[j] = result[j]//len(arr)
    return result

# create plot
def plot_values(title, ids, averages, x, y, n):
    plt.subplot(x, y, n)
    for i in range(len(averages)):
        x = np.arange(0, len(averages[i]), 1)
        plt.plot(x, averages[i], ".:", label=ids[i], alpha=0.3, markersize=5)
    y = overall_averages(averages)
    x = np.arange(1, len(y)+1, 1)
    plt.plot(x, y, "b-", label=ids[i])
    #plt.ylim([0,150])
    plt.xlim([1,30])
    plt.xlabel("Comment level")
    plt.ylabel("Average score")
    plt.title(title)
    #plt.legend()

if __name__ == "__main__":
    ids = []
    bf_averages = []
    df_averages = []
    for input_file in sys.argv[1:]:
        _ids, _bf_averages, _df_averages = load_averages(input_file.rstrip())
        ids.append(_ids)
        bf_averages.append(_bf_averages)
        df_averages.append(_df_averages)

    bar = IncrementalBar('Progress', max=len(ids))
    for i in range(len(ids)):
        plot_values(get_subreddit_from_id(ids[i][0]), ids[i], df_averages[i], 1, 1, 1)
        bar.next()
    bar.finish()
    plt.show()
