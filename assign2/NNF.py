#!/usr/bin/env python
# coding: utf-8

# In[1]:


def check(s):
    
    """return a dictionary whose key is index of "(", value is index of ")" 
    
       for example: 
       check("3*{3+[(2-3)*(4+5)]}") 
       will return 
       {6: 10, 12: 16}
       
    """
    
    left_token, right_token = "(", ")"
    left_token_idx = {}
    arr = []
    left_idx = []
    count = 0
    for c in s:
        if c == left_token:
            arr.append(c)
            left_idx.append(count)
            
        elif c == right_token:
            left_token_idx[left_idx[-1]] = count
            arr.pop()
            left_idx.pop()
        count += 1
        
    return left_token_idx


# In[2]:


# turn kb into negative negation form
def nnf(theory):
    
    #     push ¬ inwards using ¬(A ∧ B) ↔ (¬A ∨ ¬B) and ¬∀x(A) ↔ ∃x(¬A) 
    while "not(or" or "not(ad" or "not(EXISTS" or "not(FORALL" in theory:
#         print(theory)
        left_tok_idx = check(theory)
        if "not(EXISTS" in theory:
            not_idx = theory.index("not(EXISTS")
            target_idx = theory[not_idx:].index(",")
            target = theory[not_idx+target_idx+2: left_tok_idx[not_idx+3]]
            theory = theory.replace("not(EXISTS", "FORALL", 1).replace(target, f"not({target}")
        elif "not(FORALL" in theory:
            not_idx = theory.index("not(FORALL")
            target_idx = theory[not_idx:].index(",")
            target = theory[not_idx+target_idx+2: left_tok_idx[not_idx+3]]
            theory = theory.replace("not(FORALL", "EXISTS", 1).replace(target, f"not({target}")
        elif "not(or"  in theory:
            not_idx = theory.index("not(or")
            exclude_area = []
            for key in left_tok_idx.keys():
                if key > not_idx+6 and left_tok_idx[key] < left_tok_idx[not_idx+6]:
                    exclude_area.extend([i for i in range(key, left_tok_idx[key])])
            comma_lis = []
            for i in range(len(theory)):
                if theory[i] == "," and i > not_idx+6 and i < left_tok_idx[not_idx+6]:
                    if i not in exclude_area:
                        comma_lis.append(i)   
            sorted_comma = sorted(comma_lis)
            ad_object = []
            for i in range(len(sorted_comma)-1):
                ad_object.append(theory[sorted_comma[i]+2:sorted_comma[i+1]])
            ad_object.append(theory[not_idx+7:sorted_comma[0]])
            ad_object.append(theory[sorted_comma[-1]+2:left_tok_idx[not_idx+6]])
            new_target = ""
            for ob in ad_object:
                new_target += f"not({ob}), "
            target = theory[not_idx+7:left_tok_idx[not_idx+6]]
            theory = theory.replace("not(or", "ad", 1).replace(target, new_target[:-3])
        elif "not(ad"  in theory:
            not_idx = theory.index("not(ad")
            exclude_area = []
            for key in left_tok_idx.keys():
                if key > not_idx+6 and left_tok_idx[key] < left_tok_idx[not_idx+6]:
                    exclude_area.extend([i for i in range(key, left_tok_idx[key])])
            comma_lis = []
            for i in range(len(theory)):
                if theory[i] == "," and i > not_idx+6 and i < left_tok_idx[not_idx+6]:
                    if i not in exclude_area:
                        comma_lis.append(i)
            sorted_comma = sorted(comma_lis)
            ad_object = []
            for i in range(len(sorted_comma)-1):
                ad_object.append(theory[sorted_comma[i]+2:sorted_comma[i+1]])
            ad_object.append(theory[not_idx+7:sorted_comma[0]])
            ad_object.append(theory[sorted_comma[-1]+2:left_tok_idx[not_idx+6]])
            new_target = ""
            for ob in ad_object:
                new_target += f"not({ob}), "
            target = theory[not_idx+7:left_tok_idx[not_idx+6]]
            theory = theory.replace("not(ad", "or", 1).replace(target, new_target[:-3])
        else:
            break
#         print(theory)
    
    #     ¬¬A ↔ A
    while "not(not" in theory:
        left_tok_idx = check(theory)
        idx = theory.index("not(not")
        target = theory[idx:left_tok_idx[idx+3]+1]
        theory = theory.replace(target, theory[idx+8:left_tok_idx[idx+7]])
        
    #     ¬(>=n+1 r.C) ↔ <=n r.C,  ¬(<=n r.C) ↔ (>=n+1 r.C), ¬(>=0 r.C) ↔ bottom
    while "not(>=" or "not(<=" in theory:
        
        if "not(>=0" in theory:
            theory = theory.replace("not(>=0", "bottom(")
        elif "not(>=" in theory:
            idx = theory.index("not(>=")
            theory = theory.replace(theory[idx:idx+7], f"<={float(theory[idx+7])-1}")
        elif "not(<=" in theory:
            idx = theory.index("not(<=")
            theory = theory.replace(theory[idx:idx+7], f">={float(theory[idx+7])+1}")
        else:
            break
    
    return theory

