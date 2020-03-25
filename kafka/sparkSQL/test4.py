
def build_tree(path_tup):
    #path_list = [["1","2","3"],["1","2","4"],["1","2","5"],["2","4"],["2","5"],["2","6"]]
    Root = {path_tup[0]: {}}
    path_list = path_tup[1]
    for i in range(len(path_list)):
        paths = path_list[i]
        current = Root[path_tup[0]]
        for j in range(len(paths)):
            if paths[j] not in current.keys():
                current[paths[j]] = {}
                current = current[paths[j]]
            else:
                current = current[paths[j]]
    return Root
def tt(path):

    count_path_list={}
    # path = {'root': {'1': {'2': {'3': {}, '4': {}, '5': {}}}, '2': {'4': {}, '5': {}, '6': {}}}}
    count_paths2("", path,count_path_list)
    return count_path_list
# count_path_list = {}
# def count_paths1(parent, root):
#     # root = {}
#     if len(root.keys()) == 0:
#         return
#     for key in root.keys():
#         pathcount = len(root[key].keys())
#         path = parent+"/"+key if parent != "" else parent+key
#         global count_path_list
#         if path not in count_path_list.keys() and pathcount != 0:
#             count_path_list[path] = pathcount
#         count_paths1(path,root[key])

def count_paths2(parent,root,tmp):
    # root = {}
    if len(root.keys()) == 0:
        return
    for key in root.keys():
        pathcount = len(root[key].keys())
        path = parent+"/"+key if parent != "" else parent+key
        if path not in tmp.keys() and pathcount != 0:
            tmp[path] = pathcount
        count_paths2(path,root[key],tmp)
    return tmp
if __name__ == '__main__':

    tup3 = (u'www.sasac.gov.cn',
  [[u'n2588025', u'n2588119', u'index.html'],
   [u'n2588025', u'n2588129', u'index_2603340_48.html'],
   [u'n2588025', u'n2588134', u'index.html'],
   [u'n2588025', u'n2588129', u'index_2603340_602.html']])
    print(build_tree(tup3))
  #   path = build_tree(tup3)
    # path = {'root': {'1': {'2': {'3': {}, '4': {}, '5': {}}}}}
    # path = {'root': {'1': {'2': {'3': {}, '4': {}, '5': {}}}, '2': {'4': {}, '5': {}, '6': {}}}}
    # path = {u'www.yyj.moa.gov.cn': {u'zcjd': {u'': {}}}}
    #count_paths2("",path)
    # print(count_paths2("",path,{}))
    # path1 = {u'www.yyj.moa.gov.cn': {u'zcjd1': {u'': {}}}}
    # print(count_paths2("",path1,{}))
    # count_paths1("", path1)
    # print(count_path_list)
    # print(tt())

    # {'www.sasac.gov.cn': {'n2588025': {'n2588119': {'index.html': {}},
    #                                    'n2588129': {'index_2603340_48.html': {}, 'index_2603340_602.html': {}},
    #                                    'n2588134': {'index.html': {}}}}}

