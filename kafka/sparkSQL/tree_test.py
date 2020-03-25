
class node():
    def __init__(self,root = None):
        self.root = root
        self.children = {}
        self.evil = False
class Tree():

    def __init__(self):
        self.root = node("root")
        self.traval_path = []
    """
    插入节点
    tree.insert(["aaa","bbb","ccc"])
    tree.insert(["aaa", "bbb", "ddd"])
    tree.insert(["ccc", "bbb", "ddd"])
    tree.insert(["ccc", "bbb", "ddd"])
    """
    def insert(self,path_list=[]):
        """
        path_list=["aaa","bbb","ccc"]
        """
        current = self.root
        for i in range(len(path_list)):
            path = path_list[i]
            if path not in current.children.keys():
                current.children[path] = node(path)
                current = current.children[path]
            else:
                current = current.children[path]
            if i == len(path_list) - 1:
                current.evil = True
    """
    遍历树的所有路径 深度遍历
    ['root/aaa/bbb/ccc', 'root/aaa/bbb/ddd', 'root/ccc/bbb/ddd']
    """
    def traval(self,parent,root,tmp=[]):
        # current = self.root
        current = root
        # print(current.root)
        # tmp.append(current.root)
        path = parent + "/" + current.root if parent!= "" else parent+current.root
        if len(current.children.keys()) == 0:
            tmp.append(path)
            return
        if len(current.children.keys()) > 0:
            for child in current.children.keys():
                self.traval(path,current.children[child],tmp)
        return tmp
    """
    判断是否为恶意url
    """
    def is_evil(self,path_list):
        flag = True
        current = self.root
        for i in range(len(path_list)):
            path = path_list[i]
            if path in current.children.keys():
                current = current.children[path]
            else:
                flag = False
                break
        return current.evil and flag

if __name__ == '__main__':
    tree = Tree()
    tree.insert(["aaa","bbb","ccc"])
    tree.insert(["aaa", "bbb", "ddd"])
    tree.insert(["ccc", "bbb", "ddd"])
    tree.insert(["ccc", "bbb", "ddd"])
    lii = tree.traval("",tree.root,[])
    print(lii)

    path = ["aaa","bbb","ccc"]
    print(tree.is_evil(path))
    path = ["ccc", "bbb", "ddd"]
    print(tree.is_evil(path))
    path = ["aaa", "bbb", "dd"]
    print(tree.is_evil(path))
    path = ["aaa", "bbb"]
    print(tree.is_evil(path))
    path = ["tt", "bbb", "dd"]
    print(tree.is_evil(path))




