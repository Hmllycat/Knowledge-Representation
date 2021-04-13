#!/usr/bin/env python
# coding: utf-8

# In[4]:


from Token import check    


# In[113]:


def mgu(P, Q):
    left_tok_P, right_tok_P = check(P)
    left_tok_Q, right_tok_Q = check(Q)
    
    sorted_P = sorted(list(left_tok_P.keys()))
    sorted_Q = sorted(list(left_tok_Q.keys()))
    fi = []
    DS = {}
    P_slice = P[sorted_P[0]+1:left_tok_P[sorted_P[0]]].split(",", 1)
    Q_slice = Q[sorted_Q[0]+1:left_tok_Q[sorted_Q[0]]+1].split(",", 1)
    DS[P_slice[0]] = Q_slice[0]
    if "," in P_slice[1] and Q_slice[1]:
        P_slice = P[sorted_P[2]+1:left_tok_P[sorted_P[2]]].split(",", 1)
        Q_slice = Q[sorted_Q[1]+1:left_tok_Q[sorted_Q[1]]].split(",", 1)
        DS[P_slice[0]] = Q_slice[0]
        DS[P_slice[-1]] = Q_slice[-1]
        
    update = [key+"|"+value for key,value in DS.items()]
    for key in DS:
        print(update)
        if key in P:
            P = P.replace(key, DS[key])
            update.remove(key+"|"+DS[key])
    
    if P == Q:
        return "not unifiable"
    else:
        return "unifiable"


# In[114]:


P = input("Please enter your first predicate, for example: P(g(z),f(a,z))")
Q = input("Please enter your first predicate, for example: P(y,f(x,y))")
mgu(P,Q)


# In[ ]:





# In[ ]:




