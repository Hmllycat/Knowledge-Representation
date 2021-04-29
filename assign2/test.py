#!/usr/bin/env python
# coding: utf-8

# In[1]:


from treelib import Tree, Node
from ALCQ_expand import expand
from NNF import nnf


# In[ ]:


# get rid of TBox
def reduction(ABox, TBox):
    
    dic = {}
    for box in TBox:
        infor = box.split("≡")
        dic[infor[0]] = infor[1]
    
    new_ABox = []
    for box in ABox:
        for key in dic:
            while key in box:
                box = box.replace(key, dic[key])
        new_ABox.append(box)
        
    return new_ABox


# In[ ]:


def subsu(theory):
    
    A, B = theory.split(" BELONGto ")
    return f"ad({A}, not({B}))(a)"


# In[ ]:


def contradict(a, tree1):
    
    ABox = [i.identifier for i in tree1.leaves(a)]
    for box in ABox:
        box1 = box.split("  ")
        for b in box1:
            if f"not{b}" in box1 or f"not({b[0]})({b[1:]})" in box1:
                break
        if "<" in box:
            for b in box1:
                if "<" in b:
                    idx = b.index("(")
                    number = int(b[2:idx-1])
                    count = 0
                    role = b[idx-1]
                    for c in box1:
                        if role in c:
                            count += 1
                    if count > number:
                        break
        return "yes"
    return "no"


# In[ ]:


def tableau(ABox, TBox):
    
    """
    expand ABox to be complete and check if it is consistent.
    
    return True if it is consistent,
    return False if it is not.
       
    """
    new_ABox = reduction(ABox, TBox)
    nnf_ABox = ""
    for i in range(len(new_ABox)):
        nnf_ABox += f"{nnf(new_ABox[i])}  "
    nnf_ABox = nnf_ABox[:-2]
#     print(f"nnf   {nnf_ABox}")
    a, tree1 = expand(nnf_ABox)
    
    return contradict(a, tree1)


# In[ ]:


ABox = ["H(joe, ann)", "H(joe, eva)", "H(joe, mary)", "P.T(joe)", "T(ann)", "T(eva)", "T(mary)", "T(joe)"]
TBox = ["P≡<=2H"]
tableau(ABox, TBox)


# In[ ]:


# ∀r.∀s.A ⊓ ∃r.∀s.B ⊓ ∀r.∃s.C ⊑ ∃r.∃s.(A ⊓ B ⊓ C)
theory = "ad(FORALL(r, FORALL(s, A)), EXISTS(r, FORALL(s, B)), FORALL(r, EXISTS(s, C))) BELONGto EXISTS(r, EXISTS(s, ad(A, B, C)))"
ABox = [subsu(theory)]
TBox = ""
tableau(ABox, TBox)


# In[ ]:


# ∀r.∀s.A ⊓ (∃r.∀s.¬A ⊔ ∀r.∃s.B) ⊑ ∀r.∃s.(A ⊓ B) ⊔ ∃r.∀s.¬B
theory = "ad(FORALL(r, FORALL(s, A)), or(EXISTS(r, FORALL(s, not(A))), FORALL(r, EXISTS(s, B)))) BELONGto or(FORALL(r, EXISTS(s, ad(A, B))), EXISTS(r, FORALL(s, not(B))))"
ABox = [subsu(theory)]
TBox = ""
tableau(ABox, TBox)

