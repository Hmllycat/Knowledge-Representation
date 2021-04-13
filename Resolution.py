#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Token import check
from FOL_SKOLEM import skl
from MGU import mgu


# In[10]:


def resolution(query):
    
    theory = skl(query)

#     move universals to the front(eliminate all universals)
    while "EXISTS" or "FORALL" in theory:
        left_tok_idx, right_tok_idx = check(theory)
        if "FORALL" in theory:
            idx = theory.index("FORALL")
        elif "EXISTS" in theory:
            idx = theory.index("EXISTS")
        else:
            break
        scope = theory[idx:left_tok_idx[idx+6]+1]
        comma_idx = scope.index(",")
        theory = theory.replace(scope, scope[comma_idx+2:-1])
#         print(theory)
    
    theory = "not("+ theory +")"
    theory = skl(theory)
    
#     distribute ∨ over ∧ using ((A ∧ B) ∨ C) ↔ ((A ∨ C) ∧ (B ∨ C))
    for i in range(len(theory)):
        left_tok_idx, right_tok_idx = check(theory)
        if theory[i:i+2] == "or":
            scope = theory[i:left_tok_idx[i+2]+1]
            idx = scope.index(",")
            if "ad" in scope:
                for j in range(len(scope)-3):
                    if scope[j:j+2] == "ad":
                        ad_scope = theory[i+j:left_tok_idx[i+j+2]]
                        comma_idx = ad_scope.index(",")
                        A = ad_scope[3:comma_idx]
                        B = ad_scope[comma_idx+2:-1]
                        if idx > comma_idx:
                            C = scope[idx+2:-1]
                        else:
                            C = scope[3:idx]
                        theory.replace(scope, "ad("+"or("+A+", "+C+"), "+"or("+B+", "+"))")
#         print(theory)

#     remove duplicates and return kb
    know_base = [theory]
    while "ad" in know_base[0]:
        left_tok_idx, right_tok_idx = check(know_base[0])
        i = know_base[0].index("ad")
        scope = know_base[0][i+3:left_tok_idx[i+2]]
        prefix_idx = scope.index("(") + i+3
        prefix = scope[:left_tok_idx[prefix_idx]-2]
        suffix = scope[left_tok_idx[prefix_idx]:]
#         print(prefix,suffix)
        know_base.append(prefix)
        know_base.append(suffix)
        know_base.pop(0)
        
    print(know_base)
    for base in know_base.copy():
        if "not" in base:
            new_base = base[4:-1]
            for other_base in know_base.copy():
                if mgu(other_base, new_base) == "unifiable" and base in know_base:
                    know_base.remove(base)
                    know_base.remove(other_base)
    if know_base == []:
        return "valid"
    else:
        return "not valid"


# In[11]:


query = input("Please enter your theory: for example: EXISTS(x, ENTAIL(D(x), FORALL(y, D(y))))")
result = resolution(query)
print(result)


# In[ ]:




