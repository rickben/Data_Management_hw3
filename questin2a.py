import os
import sys


def LoadData(files_name_list):
    list_of_ranks_and_order = [[[], {}]]*len(files_name_list)
    total_order = {}
    for filename in files_name_list:
        with open(filename) as f:
            data = f.readlines()

        ranks = {}
        order = []
        for lines in data:
            if lines[len(lines) - 1] == '\n':
                lines = lines[:-1]
            params = lines.split(",")
            name = params[0]
            score = params[1]
            index = int(params[2])
            ranks[name] = float(score)
            order.append(name)
            if name not in total_order:
                total_order[name] = [index]
            else:
                total_order[name].append(index)
        list_of_ranks_and_order[index-1] = [ranks, order]  # index starts from 1
    # add all rank that do not appear in all the files:
    for i in range(0, len(files_name_list)):
        ranks_i = list_of_ranks_and_order[i][0]
        order_i = list_of_ranks_and_order[i][1]
        for elem in total_order:
            if elem not in order_i:
                list_of_ranks_and_order[i][0][elem] = float(ranks_i[min(ranks_i.keys(), key=(lambda k: ranks_i[k]))])
                list_of_ranks_and_order[i][1].append(elem)

    # print(list_of_ranks_and_order)
    return list_of_ranks_and_order


def aggr_func(list_of_ranks_and_order, num_of_files, i, j):
    list_of_rank_order_i_j = []
    order_j = list_of_ranks_and_order[j][1]
    for t in range(0, num_of_files):
        list_of_rank_order_i_j.append(list_of_ranks_and_order[t][0][order_j[i]])
        # rank_t(order_j[i])
    # print(list_of_rank_order_i_j)
    return max(list_of_rank_order_i_j)


def FaginAlg(list_of_ranks_and_order, k):
    # list_of_ranks_and_order = { .... {k: [ranks-k,order-k]} ... } (list of lists)
    # ranks-k = data-k[0]
    # order-k = data-k[1]
    # seen-k = {}
    # seen = { .... {k: seen-k} ... } (list of lists)
    # print("in alg")
    # print(list_of_ranks_and_order)
    num_of_files = len(list_of_ranks_and_order)
    seen_all = {}
    seen = [{} for _ in range(num_of_files) ]  # a list of dicts
    ranks_aggr = {}
    i = 0
    stop = 0
    while stop != 1:
        for j in range(0, num_of_files):
            flag = 0
            if stop:
                break
            order_j = list_of_ranks_and_order[j][1]
            # print("order_j: ")
            # print(order_j)
            ranks_aggr[order_j[i]] = aggr_func(list_of_ranks_and_order, num_of_files, i, j)
            # print("ranks_aggr: ")
            # print(ranks_aggr)
            # print(seen)
            seen[j][order_j[i]] = 1
            # print("seen")
            # print(seen)
            # print("order_j[i]")
            # print(order_j[i])
            for t in range(0, num_of_files):
                if stop:
                    break
                if t != j and order_j[i] not in seen[t]:
                    # print("in it")
                    # print(t)
                    flag = 1
            if flag:
                # print("flag")
                # print(flag)
                continue
            seen_all[order_j[i]] = ranks_aggr[order_j[i]]
            # print("seen_all")
            # print(seen_all)
            # print("len -seen all")
            # print(len(seen_all))
            # print("k")
            # print(k)
            if len(seen_all) >= k:
                stop = 1
        i = i + 1

    return sorted(ranks_aggr.items(), key=lambda x: x[1], reverse=True)[0:k]


def full_fagin_alg(files_name_list, k):
    list_of_ranks_and_order = LoadData(files_name_list)
    return FaginAlg(list_of_ranks_and_order, k)


def main():
    if len(sys.argv) != 3:
        print("Usage: python question2a.py files_zip_string")
        sys.exit(1)
    try:
        files_name_list = []
        k = int(sys.argv[1])
        dir = sys.argv[2]
        for file in os.listdir(dir):
            # print(file)
            files_name_list.append(dir+"/"+file)
        # print(files_name_list)
        res = full_fagin_alg(files_name_list, k)
        # print(res)
        # 2b:
        with open("question2b.txt", "a") as f:
            f.write("B:\n")
            f.write("k: %d\n" % int(k))
            f.write('\n'.join('%s %s' % x for x in res))
    except Exception as e:
        print("Error: %s\nplease try again with other files zip" % e.args)


if __name__ == "__main__":
    main()
