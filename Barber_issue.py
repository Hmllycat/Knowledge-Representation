#!/usr/bin/env python
# coding: utf-8

# In[9]:


import Resolution


# In[10]:


kb1 = "FORALL(x, ENTAIL(B(x), FORALL(y, ENTAIL(not(S(y, y)), S(x, y)))))"
kb2 = "FORALL(x, FORALL(y, ENTAIL(ad(B(x), S(y, y)), not(S(x, y)))))"
query = "not(EXISTS(B(x)))"
sentence = f"ENTAIL(ad({kb1}, {kb2}), {query})"


# In[11]:


result = Resolution.resolution(sentence)
print(result)


# In[ ]:




