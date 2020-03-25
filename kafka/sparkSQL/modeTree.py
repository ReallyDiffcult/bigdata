class ModelTree():
    # 第一层树，创建树是必须指定根结点，不支持创建空树。
    # 整颗树存储在tree_dict中，key为root，value为children_dict
    # children_dict中存储所有的子节点，个数不确定，动态添加
    def __init__(self, root):
        self.tree_dict = {}
        self.children_dict = {}
        self.root = root
        self.tree_dict[self.root] = self.children_dict

    # 获取根结点的方法
    def get_root(self):
        return self.root

    # 添加子节点
    def add_child(self, *args):
        # 子节点中存储两个值，属性名称attr和对应的属性子树对象attrObj
        attr = args[0]
        value = args[1]
        # 如果已经有某颗属性子树，则获取attrObj对象，添加新的value值
        if attr in self.children_dict.keys():
            attrObj = self.children_dict[attr]
            attrObj.add_value_child(value)
        # 否则创建一颗新的子树
        else:
            attrObj = AttributeChildTree(attr)
            attrObj.add_value_child(value)
            self.children_dict[attr] = (attrObj)

    # 获取某颗特定子树的对象
    def get_single_child(self, attr):
        return self.children_dict[attr]

    # 获取所有子树/子节点
    def get_all_children(self):
        return self.children_dict

    # 获取整颗树
    def get_tree(self):
        return self.tree_dict


# 第二层，属性子树
class AttributeChildTree():
    # 初始化方法，创建树时必须指定根结点，不允许创建空树，根结点的值为属性名称
    # children_dict存储所有的子节点，子节点包括两个值，一个是该属性的某个值，一个是该值出现的次数
    # 属性子树中的sum值，统计该子树一共获取了多少个值，方便之后根据该值计算每个值出现的频率
    def __init__(self, root):
        # root is attr, children are value-frequency pairs
        self.root = root
        self.value_dict = {}
        self.children_dict = {}
        self.sum = 0

    # 该方法在整颗树都创建完成之后，所有子节点都添加完毕之后调用。
    # 当然没有添加完毕，也可以达到同样的效果。将把子节点中存储的count值替换为frequency
    def __refresh__(self):
        # call this function after all the attributes added, will refresh apperance to frequency
        for value, apperance in self.children_dict.items():
            frequency = round(apperance / self.sum, 4)
            self.children_dict[value] = frequency

    # 增加子节点，如果已经存在某个value，count+1，否则创建新的value子树。每增加一个value，sum+1
    def add_value_child(self, value):
        if value in self.children_dict.keys():
            self.sum += 1
            self.children_dict[value] += 1  # apperance +1
        else:
            self.sum += 1
            self.children_dict[value] = 1

    # 获取根结点
    def get_root(self):
        return self.root

    # 获取全部子节点
    def get_children(self):
        return self.children_dict

class Node():

    def __init__(self,root):
        self.root = root  #当前根节点
        self.children_dict = {}
        self.num = 0
    def get_child(self):
        return self.children_dict
    def add_child(self):
        pass
def insert_node(tree, value):
    #tree = Node("root")
    if tree == None:
        tree = Node(value)
        return tree
    child_dict = tree.children_dict
    if value not in child_dict.keys():
        new_node = Node(value)
        tree.children_dict[value] = new_node
        return tree
    if value in child_dict.keys():
        child_node = child_dict[value]
        insert_node(child_node,value)


def build_tree(child_list):
    tree = Node("root")
    print(tree.get_child())
    for i in range(len(child_list)):
        child = child_list[i]
        insert_node(tree, child)
    return tree
if __name__ == '__main__':
    child_list = ["1","2","3"]
    tree = build_tree(child_list)
    print(tree.children_dict.keys())
    print(Node(tree.children_dict["1"]).get_child())



# class Tree_test():
#
#     def __init__(self,root):
#         self.root = Node(root)
#         self.parent = ""
#
#     def add_child(self, child):
#         if child not in self.root.children.keys():
#             Node(child)




