#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Token import check


# In[2]:


def check_signature(theory, signature):
    
    op = ["FORALL", "EXISTS", "ENTAIL", "not", "or", "ad"]
    last_two = [i[-2:] for i in op].append("((")
    const = []
    var = []
    func = {}
    rela = {}
    left_tok_idx, right_tok_idx = check(theory)
    sorted_idx = sorted(left_tok_idx.values())
    for i in range(len(sorted_idx)-1):
        if theory[i-2:i] not in last_two:
            if theory[i-1].islower():
                func[theory[i-1]] = theory[i:left_tok_idx[i]].count(",")+1
            else:
                rela[theory[i-1]] = theory[i:left_tok_idx[i]].count(",")+1
    for i in range(len(theory)):
        if theory[i:i+6] in ["FORALL", "EXISTS"]:
            var.append(theory[i+7])
        elif theory[i] in func.keys() or rela.keys():
            ari = theory[i+2:left_tok_idx[i+1]].split(", ")
    for value in ari:
        if value not in var:
            const.append(value)
    
    for key in func.keys():
        if key in signature["function"]:
            if func[key] != signature["function"][key]:
                raise ValueError(f"function {key} not match!")
            else:
                raise ValueError(f"function {key} not exists!")
                
    for key in rela.keys():
        if key in signature["relation"]:
            if rela[key] != signature["relation"][key]:
                raise ValueError(f"relation {key} not match!")
            else:
                raise ValueError(f"relation {key} not exists!")
    
    for key in const:
        if key not in signature["constanst"]:
            raise ValueError(f"constant {key} not exists!")


# In[1]:


def skl(theory):
    
    #   eliminate → using (A → B) ↔ (¬A ∨ B)
    while "ENTAIL" in theory:
        left_tok_idx, right_tok_idx = check(theory)
        entail_idx = theory.index("ENTAIL")
        target = theory[entail_idx+7:left_tok_idx[entail_idx+6]]
        pre_idx = target.index("(")+(entail_idx+7)
        prefix = theory[entail_idx+7:left_tok_idx[pre_idx]+1]
        theory = theory.replace(prefix, "not(" + prefix + ")")
        theory = theory.replace("ENTAIL", "or")
#         print(theory)
        
#     push ¬ inwards using ¬(A ∧ B) ↔ (¬A ∨ ¬B) and ¬∀x(A) ↔ ∃x(¬A) 
    while "not(or" or "not(ad" or "not(EXISTS" or "not(FORALL" in theory:
        left_tok_idx, right_tok_idx = check(theory)
        if "not(EXISTS" in theory:
            not_idx = theory.index("not(EXISTS")
            target = theory[not_idx+14: left_tok_idx[not_idx+3]+1]
            theory = theory.replace("not(EXISTS", "FORALL").replace(target, "not(" + target)
        elif "not(FORALL" in theory:
            not_idx = theory.index("not(FORALL")
            target = theory[not_idx+14: left_tok_idx[not_idx+3]+1]
            theory = theory.replace("not(FORALL", "EXISTS").replace(target, "not(" + target)
        elif "not(or"  in theory:
            not_idx = theory.index("not(or")
            target = theory[not_idx+7:left_tok_idx[not_idx+6]]
            pre_idx = target.index("(") + (not_idx+7)
            prefix = theory[not_idx+7: left_tok_idx[pre_idx]+1]
            su_idx = left_tok_idx[pre_idx]+3
            suffix = theory[su_idx:left_tok_idx[not_idx+6]]
            theory = theory.replace("not(or", "ad").replace(prefix, "not("+prefix+")").replace(suffix, "not("+suffix+")")
        elif "not(ad"  in theory:
            not_idx = theory.index("not(ad")
            target = theory[not_idx+7:left_tok_idx[not_idx+6]]
            pre_idx = target.index("(") + (not_idx+7)
            prefix = theory[not_idx+7: left_tok_idx[pre_idx]+1]
            su_idx = left_tok_idx[pre_idx]+3
            suffix = theory[su_idx:left_tok_idx[not_idx+6]]
            theory = theory.replace("not(ad", "or").replace(prefix, "not("+prefix+")").replace(suffix, "not("+suffix+")")
        else:
            break
#         print(theory)
        
    while "not(not" in theory:
        left_tok_idx, right_tok_idx = check(theory)
        idx = theory.index("not(not")
        target = theory[idx:left_tok_idx[idx+3]+1]
        theory = theory.replace(target, theory[idx+8:left_tok_idx[idx+7]])
#         print(theory)
        
#     standardize variables: each quantifier gets its own variable
#     eliminate all existential quantifiers
    var_number = [0]
    fun_number = [0]
    limit_exist = []
    for i in range(len(theory)-7):
        left_tok_idx, right_tok_idx = check(theory)
        if theory[i:i+6] == "FORALL":
            all_scope = theory[i:left_tok_idx[i+6]+1]
            if "EXISTS" in all_scope:
                for j in range(len(all_scope)-7):
                    if all_scope[j:j+6] == "EXISTS":
                        exist_scope = theory[j+i:left_tok_idx[i+j+6]]
                        var_idx = j+7
                        if all_scope[var_idx+2] != "(":
                            new = exist_scope.replace(all_scope[var_idx], "f"+str(fun_number[-1])+"("+"v"+str(var_number[-1])+")")
                        else:
                            new = exist_scope.replace("f"+str(fun_number[-1])+"(", "f"+str(fun_number[-1])+"("+"v"+str(var_number[-1])+",")
                        theory = theory.replace(exist_scope, new)
                        fun_number.append(fun_number[-1]+1)
            left_tok_idx, right_tok_idx = check(theory)
            all_scope = theory[i:left_tok_idx[i+6]+1]
            var = theory[i+7]
            standard = all_scope.replace(var, "v"+str(var_number[-1]))
            theory = theory.replace(all_scope, standard)
            if "EXISTS" in standard:
                for j in range(len(standard)-7):
                    if standard[j:j+6] == "EXISTS":
                        limit_exist.append(i+j)
            var_number.append(var_number[-1]+1)
        elif theory[i:i+6] == "EXISTS" and i not in limit_exist:
            exist_scope = theory[i:left_tok_idx[i+6]+1]
            var = theory[i+7]
            standard = exist_scope.replace(var, "const"+str(var_number[-1]))
            theory = theory.replace(exist_scope, standard)
            var_number.append(var_number[-1]+1)
#         print(theory)
    
    return theory


# In[ ]:




