#!/usr/bin/env python
# coding: utf-8

# In[1]:


from treelib import Tree, Node
from NNF import check


# In[ ]:


def expand(ABox):
    
    tree = Tree()
    a = ABox
    
    # ⊓-rule
    while "ad" in a:
#         print(a)
        left_tok_idx = check(a)
        ad_idx = a.index("ad")
        lis = a.split("  ")
        for i in range(len(lis)):
            if "ad" in lis[i]:
                target_box = lis[i]
                break
#         print("target box", target_box)
        target = a[ad_idx+3:left_tok_idx[ad_idx+2]]
#         print("target")
#         print(target)
        exclude_area = []
        for key in left_tok_idx.keys():
            if key > ad_idx+2 and left_tok_idx[key] < left_tok_idx[ad_idx+2]:
                exclude_area.extend([i for i in range(key, left_tok_idx[key])])
        
        comma_lis = []
        for i in range(len(a)):
            if a[i] == "," and i > ad_idx and i < left_tok_idx[ad_idx+2]:
                if i not in exclude_area:
                    comma_lis.append(i)
    
        sorted_comma = sorted(comma_lis)
#         print("comma         ", sorted_comma)
        ad_object = []
        for i in range(len(sorted_comma)-1):
            ad_object.append(a[sorted_comma[i]+2:sorted_comma[i+1]])
        ad_object.append(a[ad_idx+3:sorted_comma[0]])
        ad_object.append(a[sorted_comma[-1]+2:left_tok_idx[ad_idx+2]])
        
        replace = ""
        for obj in ad_object:
            expand_target = target_box.replace(f"ad({target})", obj)
            replace += f"{expand_target}  "
#         print(replace[:-2])
        a = a.replace(target_box, replace[:-2])

    
    
    tree.create_node(identifier = a)
    a1 = a
    # ⊔-rule
    while "or(" in a1:
#         print(a1)
        left_tok_idx = check(a1)
        ad_idx = a1.index("or")
        lis = a1.split("  ")
        for i in range(len(lis)):
            if "or" in lis[i]:
                target_box = lis[i]  
                break
        target = a1[ad_idx+3:left_tok_idx[ad_idx+2]]
        exclude_area = []
        for key in left_tok_idx.keys():
            if key > ad_idx+2 and left_tok_idx[key] < left_tok_idx[ad_idx+2]:
                exclude_area.extend([i for i in range(key, left_tok_idx[key])])
        
        comma_lis = []
        for i in range(len(a1)):
            if a1[i] == "," and i > ad_idx and i < left_tok_idx[ad_idx+2]:
                if i not in exclude_area:
                    comma_lis.append(i)
    
        sorted_comma = sorted(comma_lis)
#         print("comma         ", sorted_comma)
        ad_object = []
        for i in range(len(sorted_comma)-1):
            ad_object.append(a1[sorted_comma[i]+2:sorted_comma[i+1]])
        ad_object.append(a1[ad_idx+3:sorted_comma[0]])
        ad_object.append(a1[sorted_comma[-1]+2:left_tok_idx[ad_idx+2]])
        
        repeat = []
        for leaf in tree.leaves(a).copy():
#             tree.show()
            if target_box in leaf.identifier:
                replace = ""
                for obj in set(ad_object):
                    expand_target = target_box.replace(f"or({target})", obj)
                    b = a1.replace(target_box, expand_target)
#                     print("add                              ",b)
                    if b in repeat:
                        continue
                    node_b = Node(identifier = b)
                    tree.add_node(node_b, parent = leaf.identifier)
                    replace += f"{expand_target}  "
                    repeat.append(b)
                a1 = a1.replace(target_box, replace[:-2])

    # ∀-rule
    for leaf in tree.leaves(a):
        condition = leaf.identifier
        lis = condition.split("  ")
#         print(lis)
        for i in range(len(lis)):
            box = lis[i]
            if "FORALL" in box:
                while "FORALL" in box:
    #                 print(lis)
                    left_tok_idx = check(box)
                    all_idx = box.index("FORALL")
                    target = box[all_idx+7: left_tok_idx[all_idx+6]]
                    instance = box[-2]
                    role, con = target.split(", ", 1)
    #                 print("instance", instance)
    #                 print(con)
                    if f"{role}({instance}, " in condition:
                        idx = condition.index(f"{role}({instance}, ")
                        token_idx = f"{role}({instance}, ".index("(")
                        var = condition[idx+token_idx+1: left_tok_idx[idx+token_idx]].split(", ", 1)[1]
                        if f"{con}({var})" not in condition:
                            box = condition.replace(f"FORALL({target})", f"{con}({var})  {con}")
                        else:
                            box = condition.replace(f"FORALL({target})", f"{con}")
                    else:
                        box = condition.replace(f"FORALL({target})", f"{con}")
                    condition = box
                    lis = condition.split("  ")
                    box = lis[i]

                node_b = Node(identifier = condition)
                tree.add_node(node_b, parent = leaf.identifier)
  
    # ≤ rule and choose rule
    for leaf in tree.leaves(a):
        if "<=" in leaf.identifier:
            lis = leaf.identifier.split("  ")
            for i in range(len(lis)):
                if "<=" in lis[i]:
                    role = lis[i].split(".")[0][-1]
                    target = lis[i]
            b = ""
            for value in lis:
                if role not in b and role in lis:
                    b += f"{lis[i]}  "
                if role not in lis:
                    b += f"{lis[i]}  "
            
            node_b = Node(identifier = b[:-2])
            tree.add_node(node_b, parent = leaf.identifier)
            
    # ∃-rule
    count = 1
    for leaf in tree.leaves(a):
        condition = leaf.identifier
        lis = condition.split("  ")
        for i in range(len(lis)):
            box = lis[i]
            if "EXISTS" in box:
                while "EXISTS" in box:
                    left_tok_idx = check(box)
                    all_idx = box.index("EXISTS")
                    target = box[all_idx+7: left_tok_idx[all_idx+6]]
                    instance = box[-2]
                    role, con = target.split(", ", 1)
                    if f"{role}({instance}, " not in condition:
                            box = condition.replace(f"EXISTS({target})", f"{con}({instance}{count})  {role}({instance}, {instance}{count})  {con}")
                    else:
                        box = condition.replace(f"EXISTS({target})", f"{con}")
                    condition = box
                    lis = condition.split("  ")
                    box = lis[i]

                node_b = Node(identifier = condition)
                tree.add_node(node_b, parent = leaf.identifier)
                count += 1
        
     # ≥ rule
    for leaf in tree.leaves(a):
        if ">=" in leaf.identifier:
            lis = leaf.identifier.split("  ")
            for i in range(len(lis)):
                if ">=" in lis[i]:
                    left_tok_idx = check(lis[i])
                    idx = lis[i].index("(")
                    instance = lis[i][left_tok_idx[idx]+2:-1]
                    role = lis[i].split(".")[0][-1]
                    target = lis[i]
                    number_idx1 = lis[i].index("=")
                    number_idx2 = lis[i].index(role)
                    number = lis[i][number_idx1+1:number_idx2]
            b = ""
            for value in range(int(number)):
                b += f"{role}({instance},{instance, value})  "
            
            node_b = Node(identifier = b[:-2])
            tree.add_node(node_b, parent = leaf.identifier)
            
    return a, tree

