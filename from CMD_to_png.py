#!/usr/bin/env python
# coding: utf-8

# In[1]:


# コマンドライン引数
import sys
args = sys.argv
target_HP = args[1]
#target_HP = "HP:0001249", "HP:0001250"


# In[2]:


import pronto
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from graphviz import Digraph
from IPython.display import Image


# In[3]:


#ont = pronto.Ontology('hp.obo')
ont = pronto.Ontology('https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo')


# superclass

# In[4]:


# superclassタームを抽出
sup_target_HP_list = list(ont[target_HP].superclasses()) # 自分（HP:0001249）を入れる場合は引数不要（デフォルト）
sup_target_HP_list


# In[5]:


# 抽出したタームを階層ごとに分ける

# まず全階層の箱superclass_layer_listと、その中に階層ごとの箱superclass_●layer_listを作っておく


superclass_layer_list =[]

for i in range(1,10000):
    exec("superclass_"+str(i)+"layer_list" + " = list(ont[target_HP].superclasses(distance="+str(i)+"))")
    if list(ont[target_HP].superclasses(distance=i-1)) == list(ont[target_HP].superclasses(distance=i)):
        print("Max depth:" + str(i-1))         
        break;
        
    superclass_layer_list.append("superclass_"+str(i)+"layer_list")

max_len=i


# In[6]:


# 1つ前のlayerのものをひいていく その階層のタームだけが残る
for i in range(max_len-2,0,-1):
    print(i)
    exec("superclass_"+str(i+1)+"layer_list" "= set("+superclass_layer_list[i]+") - set(" + superclass_layer_list[i-1]+ ")")


# In[7]:


target_HP_rep=target_HP.replace(':', '')


# In[8]:


# 階層ごとの箱subclass_●layer_listにタームを振り分ける

for i,superclasslist in enumerate(superclass_layer_list):
    exec("superclass_"+str(i+1)+"layer_list_id = eval(superclasslist)")
    exec("superclass_"+str(i+1)+"layer_list_id = [s.id for s in superclass_"+ str(i+1) +"layer_list_id]")
    exec("superclass_"+str(i+1)+"layer_list_id = [s.replace(':', '') for s in superclass_" +str(i+1)+"layer_list_id]")
    exec("superclass_"+str(i+1)+"layer_list_id = list(reversed(superclass_"+str(i+1)+"layer_list_id))")

# enumerate()関数の引数にリストなどのイテラブルオブジェクトを指定する
# インデックス番号, 要素の順に取得できる


# In[9]:


from graphviz import Digraph
import networkx as nx

G = Digraph(format="png")


# In[10]:


# 関数の定義 subclassでのノードの設定

def connected_judge(HP_1,HP_2,replaced=True):
    # HP_1 parentid
    # HP_2 parentid
    if replaced:
        HP_1 = HP_1.replace('HP', 'HP:')
        HP_2 = HP_2.replace('HP', 'HP:')
    HP_2_list = list(ont[HP_2].superclasses(distance=1))
    HP_2_list = [s.id for s in HP_2_list]
    return HP_1 in HP_2_list


# In[11]:


# superclassでのエッジの設定

# subclass_1layer_listとそれ以外に分けて処理

for superclasslist in superclass_layer_list:
    tmplist = eval(superclasslist+"_id")
    if superclasslist == 'superclass_1layer_list':
        for hp_node_ind_1 in range(len(tmplist)-1):
            G.edge(tmplist[hp_node_ind_1],target_HP_rep)
            before_list = copy.copy(tmplist)
            
    else:
        for hp_id_super_class in tmplist:
            for hp_id_sub_class_candidate in before_list:
                if connected_judge(hp_id_super_class,hp_id_sub_class_candidate,replaced=True):
                    G.edge(hp_id_super_class,hp_id_sub_class_candidate)
        before_list = copy.copy(tmplist)     


# In[12]:


G.node(target_HP_rep, shape="ellipse", style="filled", fillcolor="lightblue2")


# In[13]:


G.render()
G.view()
#!dot -T png Digraph.gv > test.png
#Image('test.png')


# In[14]:


# HP:0001249の場合
# HP:0012638の中に、HP0012759とHP0011446のchildnodeが２つあることを確認

list(ont["HP:0012638"].subclasses(distance=1))


# subclass

# In[15]:


# subclassタームを抽出
sub_target_HP_list = list(ont[target_HP].subclasses()) 


# In[16]:


# 抽出したタームを階層ごとに分ける

# まず全階層の箱subclass_layer_listと、その中に階層ごとの箱subclass_●layer_listを作っておく

subclass_layer_list =[]

for i in range(1,10000):
    exec("subclass_"+str(i)+"layer_list" + " = list(ont[target_HP].subclasses(distance="+str(i)+"))")
    if list(ont[target_HP].subclasses(distance=i-1)) == list(ont[target_HP].subclasses(distance=i)):
        print("Max depth:" + str(i-1))         
        break;
        
    subclass_layer_list.append("subclass_"+str(i)+"layer_list")

max_len=i


# In[17]:


# 1つ前のlayerのものをひいていく その階層のタームだけが残る
for i in range(max_len-2,0,-1):
    print(i)
    exec("subclass_"+str(i+1)+"layer_list" "= set("+subclass_layer_list[i]+") - set(" + subclass_layer_list[i-1]+ ")")


# In[18]:


# 階層ごとの箱subclass_●layer_listにタームを振り分ける

for i,subclasslist in enumerate(subclass_layer_list):
    exec("subclass_"+str(i+1)+"layer_list_id = eval(subclasslist)")
    exec("subclass_"+str(i+1)+"layer_list_id = [s.id for s in subclass_"+ str(i+1) +"layer_list_id]")
    exec("subclass_"+str(i+1)+"layer_list_id = [s.replace(':', '') for s in subclass_" +str(i+1)+"layer_list_id]")
    exec("subclass_"+str(i+1)+"layer_list_id = list(reversed(subclass_"+str(i+1)+"layer_list_id))")

# enumerate()関数の引数にリストなどのイテラブルオブジェクトを指定する
# インデックス番号, 要素の順に取得できる


# In[19]:


subclass_1layer_list


# In[20]:


# 関数の定義 subclassでのノードの設定

def connected_judge(HP_1,HP_2,replaced=True):
    # HP_1 parentid
    # HP_2 parentid
    if replaced:
        HP_1 = HP_1.replace('HP', 'HP:')
        HP_2 = HP_2.replace('HP', 'HP:')
    HP_2_list = list(ont[HP_2].subclasses(distance=1))
    HP_2_list = [s.id for s in HP_2_list]
    return HP_1 in HP_2_list


# In[21]:


# subclassでのエッジの設定

# subclass_1layer_listとそれ以外に分けて処理

for subclasslist in subclass_layer_list:
    tmplist = eval(subclasslist+"_id")
    if subclasslist == 'subclass_1layer_list':
        for hp_node_ind_1 in range(len(tmplist)-1):
            G.edge(target_HP_rep, tmplist[hp_node_ind_1])
            before_list = copy.copy(tmplist)
            
    else:
        for hp_id_sub_class in tmplist:
            for hp_id_sub_class_candidate in before_list:
                if connected_judge(hp_id_sub_class, hp_id_sub_class_candidate, replaced=True):
                    G.edge(hp_id_sub_class_candidate, hp_id_sub_class)
        before_list = copy.copy(tmplist)   


# In[22]:


G.render()
G.view()
#!dot -T png Digraph.gv > test.png
#Image('test.png')

