import matplotlib
import os

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Chart of response times per client for Star and Tree Topology per 100 requests", fontsize=18, y=0.95)


def plotter1(request_no, none_list, random_list, rr_list, top, client, n):
    plt.plot(request_no, none_list, color='red', label="No Load Balancing")
    plt.plot(request_no, random_list, label="Random Load Balancing")
    plt.plot(request_no, rr_list, label="Round Robin Load Balancing")
    plt.title('Response times of the ' + client + " client under the " + top.capitalize() + " topology", fontsize=10)
    # plt.xlabel('Request Number', fontsize=14)
    plt.ylabel('Response Time (ms)', fontsize=10)
    if n == 6:
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower right')


request_no = []
for i in range(0, 100):
    request_no.append(i + 1)

test_dict = {'c1': ['star', 'tree'], 'c2': ['star', 'tree'], 'c3': ['star', 'tree']}

n = 0
for client in test_dict:
    for top in test_dict[client]:
        ax = plt.subplot(3, 2, n + 1)
        none_file = open("./Log/log-" + client + '-' + top + "-none.txt", "r").readlines()
        none_list = [float(i) * 1000 for i in none_file]
        random_file = open("./Log/log-" + client + '-' + top + "-random.txt", "r").readlines()
        random_list = [float(i) * 1000 for i in random_file]
        rr_file = open("./Log/log-" + client + '-' + top + "-rr.txt", "r").readlines()
        rr_list = [float(i) * 1000 for i in rr_file]
        n += 1
        plotter1(request_no, none_list, random_list, rr_list, top, client, n)

path = "./Charts"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

plt.show()
plt.savefig('./Charts/response_times.png')
plt.clf()

plt.figure(figsize=(12, 12))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Comparison of response times per client for each topology", fontsize=18, y=0.95)

n = 0
for client in test_dict:
    rr_dict = {}
    for top in test_dict[client]:
        rr_file = open("./Log/log-" + client + '-' + top + "-rr.txt", "r").readlines()
        rr_dict[top] = [float(i) * 1000 for i in rr_file]

    plt.style.use("fivethirtyeight")
    ax = plt.subplot(3, 1, n + 1)
    for top in rr_dict:
        plt.plot(request_no, rr_dict[top], label=top.capitalize() + " Topology")
    plt.title('Comparison of response times between Star and Tree Topologies for the ' + client + " client",
              fontsize=10)
    plt.ylabel('Response Time (ms)', fontsize=10)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, loc='lower right')
    n += 1

plt.show()
plt.savefig('./Charts/rr_comparison.png')
plt.clf()

plt.figure(figsize=(6, 12))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Comparison of each Topology per client", fontsize=18, y=0.95)
labels = ['star', 'tree']
colors = ['lightblue', 'lightgreen']

n = 1
for client in test_dict:
    ax = plt.subplot(3, 1, n)
    rr_dict = {}
    data = []
    for top in test_dict[client]:
        rr_file = open("./Log/log-" + client + '-' + top + "-rr.txt", "r").readlines()
        rr_dict[top] = [float(i) * 1000 for i in rr_file]
        data.append([float(i) * 1000 for i in rr_file])
    plt.style.use("fivethirtyeight")
    bp = ax.boxplot(data, notch=True,  # notch shape
                    vert=True,  # vertical box alignment
                    patch_artist=True,  # fill with color
                    labels=labels)
    plt.ylim(100, 200)
    plt.ylabel('Response Time (ms)', fontsize=8)
    plt.title('Comparison between the Star and Tree Topologies for the ' + client + " client",
              fontsize=8)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    n += 1

plt.show()
plt.savefig('./Charts/rr_comparison2.png')
plt.clf()
