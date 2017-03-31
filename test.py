import scipy as sp
from scipy import stats

'''
#데이터 분류 시작
d = open("test.data","w+")
t = open("test.test","w+")

cnt = 0

for line in open("test_total.data"):
    if cnt < 5000:
        d.writelines(line)
    else:
        t.writelines(line)
    cnt += 1

d.close()
t.close()

# 데이터 분류 끝
'''

############################## 트리 정의부분 #####################################


class Tree:
    child_dic = {}
    attr_name = str()
    test_case_list = []
    parent = None
    except_attr_list = []
    yes_or_no = None
    e_num = 0
    p_num = 0

    def change_attr_name(self, name):
        self.attr_name = name

    def __init__(self, attr_name, child_dic=None):
        self.attr_name = attr_name
        self.child_dic = child_dic

    def set_parent(self, parent):
        self.parent = parent

    def set_child_dic(self, c):
        self.child_dic = c

    def add_except_list(self, e):
        self.except_attr_list.append(e)

    def set_im_parent(self):
        for k in self.child_dic.keys():
            self.child_dic[k].set_parent = self

    def is_finish(self):
        for t in self.test_case_list:
            if t.split(',')[0] is 'e':
                self.e_num += 1
            else:
                self.p_num += 1

        if self.e_num is 0 and self.p_num is not 0:
            self.yes_or_no = 'no'

        elif self.e_num is not 0 and self.p_num is 0:
            self.yes_or_no = 'yes'

############################## 트리 정의부분 끝#####################################

def process(test_case):

    for t in test_case:
        test_attr = t.split(",")  # 방금 넣은 케이스의 결과 값

        if test_attr[0] is 'e':
            for i in range(0, 22):
                table[attributes[i] + "_" + str(test_attr[i + 1]) + "_plus"] = table.get(
                    attributes[i] + "_" + str(test_attr[i + 1]) + "_plus", 0) + 1
        else:
            for i in range(0, 22):
                table[attributes[i] + "_" + str(test_attr[i + 1]) + "_minus"] = table.get(
                    attributes[i] + "_" + str(test_attr[i + 1]) + "_minus", 0) + 1

    #print("test_case : ", end="")
    #print(test_case)

    attributes_ent = {}

    attributes_ent = find_attr_ent(attributes)
    print(table)
    print(attributes_ent)
    print(find_highest_ent(attributes_ent))

    return find_highest_ent(attributes_ent)

def make_child_tree(data_name, attr_list):
    child_tree_dic = {}

    for att in attr_list:
        child_tree_dic[data_name+ "_" + att] = Tree(data_name+ "_" + att)

    return child_tree_dic

def find_attr_ent(attributes):
    attributes_ent = {}

    for atts in attributes:  # 모든 Attribute들을 돌면서
        atts_plus = 0
        atts_minus = 0
        atts_total = 0

        for classes in attributes_class[atts]:  # 해당 Attr.의 클래스(b, x, s, f같은)를 돌면서
            atts_plus += table.get(atts + "_" + classes + "_plus", 0)
            atts_minus += table.get(atts + "_" + classes + "_minus", 0)

        atts_total = atts_plus + atts_minus  # 해당 Attr.의 +와 -개수를 구함.
        Ent = cal_ent(atts_total, atts_plus, atts_minus)

        for classes in attributes_class[atts]:  # 해당 Attr.의 클래스(b, x, s, f같은)를 돌면서
            class_minus = table.get(atts + "_" + classes + "_minus", 0)  # 플러스 마이너스 개수를 통해
            class_plus = table.get(atts + "_" + classes + "_plus", 0)  # 엔트로피를 구하는 함수

            total_classes_num = class_plus + class_minus
            print(atts + "_" + classes + "_total",end="")
            print(total_classes_num)

            Ent -= (total_classes_num / atts_total) * cal_ent(total_classes_num, class_plus, class_minus)

        attributes_ent[atts] = Ent

    return attributes_ent

def find_highest_ent(attributes_ent):
    max_Ent = 0
    max_key = None

    for k in attributes_ent.keys():
        if max_Ent < attributes_ent[k]:
            max_Ent = attributes_ent[k]
            max_key = k

    return max_key

def cal_ent(total_num, plus_num, minus_num):
    if total_num is 0 or plus_num is 0 or minus_num is 0:
        return 0

    return -(plus_num/total_num*sp.log2(plus_num/total_num) + minus_num/total_num*sp.log2(minus_num/total_num))

test_case = []

table = {}

attributes = []             #Attribute들의 List
attributes_index_dic = {}   #Attribute들의 index(테스트케이스에서 순서)를 dict.으로 나타냄
attributes_class = {}       #Key : Attribute들, Values : 해당 Attr.의 클래스 (b,c,x)들의 리스트

class_flag = True

for l in open("agaricus-lepiota.names"):
    if class_flag:
        E = l.split(",")[0]
        P = l.split(",")[1].rstrip(".")
        ind = 0
        class_flag = False

    else:
        attributes.append(l.split(":")[0])
        attributes_index_dic[l.split(":")[0]] = ind
        attributes_class[l.split(":")[0]] = (l.split(":")[1].rstrip(".\n")).split(",")

    ind += 1

print(attributes)
print("attributes_index_dic : ", end="")
print(attributes_index_dic)

#table의 index로는 attributes[i]_attributes_class_plus/minus로 되어있다.
#ex) cap-shape_x_minus, cap-color_n_plus

for line in open("test.data","r"):
    test_case.append(line.rstrip("\n"))
    test_attr = str(test_case[-1]).split(",")       #방금 넣은 케이스의 결과 값

    if test_attr[0] is 'e':
        for i in range(0,22):
            table[attributes[i] + "_" + str(test_attr[i+1]) + "_plus"] = table.get(
                attributes[i] + "_" + str(test_attr[i+1]) + "_plus", 0) + 1
    else:
        for i in range(0,22):
            table[attributes[i] + "_" + str(test_attr[i+1]) + "_minus"] = table.get(
                attributes[i] + "_" + str(test_attr[i+1]) + "_minus", 0) + 1

#print("test_case : ", end="")
#print(test_case)

attributes_ent = {}

attributes_ent = find_attr_ent(attributes)

Root = Tree(find_highest_ent(attributes_ent), make_child_tree(find_highest_ent(attributes_ent), attributes_class[find_highest_ent(attributes_ent)]))
Root.add_except_list(find_highest_ent(attributes_ent))

test_attr = str(test_case[-1]).split(",")
print(test_attr)
print(table)
print("attributes_class : ",end="")
print(attributes_class)
print(attributes_ent)
print(find_highest_ent(attributes_ent))
print("root :", end="")

he = find_highest_ent(attributes_ent)

for classes in attributes_class[he]:
    print(str(he) + "_" + classes + "_minus : " + str(table.get(he + "_" + classes + "_minus", 0)))
    print(str(he) + "_" + classes + "_plus : " + str(table.get(he + "_" + classes + "_plus", 0)))


attr_testcase_dic = {}
he_attr_index = attributes_index_dic[he]

for t in test_case:
    test_attr = str(t).split(",")
    if attr_testcase_dic.get(test_attr[he_attr_index], 0) is 0:
        attr_testcase_dic[test_attr[he_attr_index]] = [t]

    else:
        l = attr_testcase_dic.get(test_attr[he_attr_index])
        l.append(t)
        attr_testcase_dic[test_attr[he_attr_index]] = l

for k in attr_testcase_dic.keys():
    Root.child_dic[he+"_"+k].test_case_list = attr_testcase_dic[k]

Root.set_im_parent()

Root.child_dic['odor_n'].is_finish()
print(Root.child_dic['odor_n'].attr_name)
print(Root.child_dic['odor_n'].yes_or_no)

table = {}
next_child = process(Root.child_dic['odor_n'].test_case_list)

Root.child_dic['odor_n'].set_child_dic(make_child_tree(next_child, attributes_class[next_child]))