from treelib import Tree, Node
def split_path(paths):
    path_list = paths.split("/")
    repath_list=[]
    for path in path_list:
        if path.find("?") != -1:
            repath_list.append(path.split("?")[0])
        elif path != "":
            repath_list.append(path)

    return repath_list


def resolution_line(x):
    dict = {}
    path_list = split_path(x)
    return path_list
def duplicate_removal(tup1):
    list_path1=[]
    list_path = tup1[1]
    for i in range(len(list_path)):
        path1=list_path[i]
        flag = 1
        for j in range(i+1, len(list_path)):
            path2=list_path[j]
            if(path1 == path2):
                flag = 0
                break
        if(flag == 1 and path1!= []):
            list_path1.append(path1)
    return (tup1[0],list_path1)
def count_gov_url(tup2):
    return (tup2[0],len(tup2[1]))
class Nodex():
    def __init__(self,num):
        self.num = num
def build_tree():
    tree = Tree()
    tree.create_node('Root', 'root', data=Nodex('3'));
    tree.create_node('child1', 'child1', parent='root');
    tree.create_node('child2', 'child2', parent='root');
    tree.create_node('child3', 'child3', parent='root');
    tree.create_node('child4', 'child4', parent='child1');
    return tree
def build_tree1(tup3):

    tree = Tree()
    tree.create_node('Root', tup3[0]);
    path_list = tup3[1]
    for i in range(len(path_list)):
        path = path_list[i]
        for j in range(len(path)):
            if j == 0 and path[j]!= []:
                parent_chlidren = tree.is_branch(tup3[0])
                if parent_chlidren.__contains__(path[0]) == False:
                    row_col_str = "_"+str(i)+str(j)
                    tree.create_node(path[j],path[j]+row_col_str,parent=tup3[0])

            elif j > 0 and path[j]!=[]:
                parent_row_col_str = "_"+str(i)+str(j-1)
                parent_chlidren = tree.is_branch(path[j-1]+parent_row_col_str)
                if parent_chlidren.__contains__(path[j]) == False:
                    row_col_str = "_" + str(i) + str(j)
                    tree.create_node(path[j], path[j]+str(count), path[j-1])

    return tree


if __name__ == '__main__':
    # str1 = "www.sasac.gov.cn/n2588025/n2588119/index.html?t=1573435313677"
    # pa = resolution_line(str1)
    # print(pa)
    #####
    # tup1 = (u'tybb.mof.gov.cn',[[u'printasyncwork'], [u'dnaserver'],[],[u'dnaserver'],[u'printasyncwork'],[u'printasyncwork']])
    # tup2 = (u'www.nkj.moa.gov.cn', [[u'ggzt', u''], [u'dwhz', u''], [u'tongji']])
    # list_path = duplicate_removal(tup1)
    # print(list_path)
    # print(count_gov_url(tup2))
    ###
    # tree = build_tree()
    # tree.show()
    #
    # print(tree.contains("child4"))
    # print(tree.is_branch("child1"))
    # list = ["aa","bb","c",0]
    # print(list.__contains__("aa"))
#########################################
    tup3 = ("gov",[["1","2"],["2","4"]])
    # tree1 = build_tree1(tup3)
    # tree1.show()
    tree =  Tree()
    tree.create_node("gov",0)
    tree.create_node("122", 1, parent=0)
    tree.create_node("2222", 2, parent=1)
    print(tree.is_branch(0))
    # print(tree.)
    tree.show()