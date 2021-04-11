#!/usr/bin/env python
# coding: utf-8

# In[1]:


def check(s):
    
    """return two dictionarys 
        first one whose key is index of "(", value is index of ")" 
        second one whose key is index of ")", value is index of "(" 
    
       for example: 
       check("3*{3+[(2-3)*(4+5)]}") 
       will return 
       {6: 10, 12: 16}, {10: 6, 16: 12}
       
    """
    
    left_token, right_token = "(", ")"
    left_token_idx = {}
    right_token_idx = {}
    arr = []
    left_idx = []
    count = 0
    for c in s:
        if c == left_token:
            arr.append(c)
            left_idx.append(count)
            
        elif c == right_token:
            left_token_idx[left_idx[-1]] = count
            right_token_idx[count] = left_idx[-1]
            arr.pop()
            left_idx.pop()
        count += 1
        
    return left_token_idx, right_token_idx


# In[ ]:




