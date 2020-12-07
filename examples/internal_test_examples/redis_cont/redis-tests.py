#!/usr/bin/env python
# coding: utf-8

# In[16]:


import redis


# In[17]:


from redis.sentinel import Sentinel
sentinel = Sentinel([('redis-sentinel', '26379')], socket_timeout=0.1)


# In[18]:


master = sentinel.master_for('mymaster', socket_timeout=0.1, password='redis')


# In[19]:


master.set('1', '1')


# In[11]:


#r = redis.Redis(password='redis', port=26379)


# In[12]:


#r.set('test','test')


# In[9]:


#r.get('test')


# In[ ]:




