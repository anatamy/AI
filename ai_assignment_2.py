import math
#import pdb
#class
class coor:
    def __init__(self,k,num,input):
        self.n=k
        self.num_of_point=num
        self.input=input
        self.output=input[:-4]+"_output.txt"
        self.point_list=[]
class point:
    def __init__(self,x_,y_):
        self.x=x_
        self.y=y_
        self.pair=(x_,y_)
class cluster:
    def __init__(self):
        self.elements=[]
        self.sim_list=[]
    def len(self):
        return len(self.elements)
    # def show(self):
    #     for i in range(self.len()):
    #         print(self.elements[i])
#--------------------------
result=[]
#--------------------------
#read file
def readfile(input):
    file=open(input,'r')
    temp=file.readline()
    temp=temp.split()
    new_coor=coor(int(temp[0]),int(temp[1]),input)
    for i in range(new_coor.num_of_point):
        temp=file.readline()
        temp=temp.split(',')
        new_point=point(int(temp[0]),int(temp[1]))
        new_coor.point_list.append(new_point)
    file.close()
    return new_coor
#get cos_similarity
def get_cos(a,b):
    T=a.x*b.x+a.y*b.y
    P=math.sqrt(math.pow(a.x,2)+math.pow(a.y,2))*math.sqrt(math.pow(b.x,2)+math.pow(b.y,2))
    return float('%0.4f' % float(T/P))
    #return float(T/P)
# merge_clusters
def merge_cluster(matrix,A_idx,B_idx,root,type):
    root.elements[A_idx].elements.extend(root.elements[B_idx].elements)
    del root.elements[B_idx]
    if type =='single':
        for i in range(len(matrix)):
            matrix[A_idx][i]=max(matrix[A_idx][i],matrix[B_idx][i])
            matrix[i][A_idx]=max(matrix[i][A_idx],matrix[i][B_idx])
    elif type =='complete':
        for i in range(len(matrix)):
            matrix[A_idx][i]=min(matrix[A_idx][i],matrix[B_idx][i])
            matrix[i][A_idx]=min(matrix[i][B_idx],matrix[i][B_idx])
    elif type == 'average':
        for i in range(len(matrix)):
            matrix[A_idx][i]=round((matrix[A_idx][i]+matrix[B_idx][i])/2,4)
            matrix[i][A_idx]=round((matrix[i][A_idx]+matrix[i][B_idx])/2,4)
    else:
        return -1
    for i in range(len(matrix)):
        del matrix[i][B_idx]
    del matrix[B_idx]
    return matrix,root
#make write data and print into cmd
def end_cluster(output,ans,span_list,type):
    global result
    marker='--------------------------------------------------'
    if type=='single':
        # temp='---\n'+'single\n'+'clusters: '+str(ans[0])+', '+str(ans[1])+', '+str(ans[2])+'\nspan: '+str(span_list[0])+', '+str(span_list[1])+'\n'
        temp='single clusters\n'
        temp+=marker+'\n'
        temp+='cluster1: '+str(ans[0])+'\nlen_cluster1: '+str(len(ans[0]))+'\n'+marker
        temp+='\ncluster2: '+str(ans[1])+'\nlen_cluster2: '+str(len(ans[1]))+'\n'+marker
        temp+='\ncluster3: '+str(ans[2])+'\nlen_cluster3: '+str(len(ans[2]))+'\n'+marker
        temp+='\nsingle_span: ['+str(span_list[0])+', '+str(span_list[1])+']\n'+marker+'\n\n'
        print('single clustering')
        print('----------------------------------------------')
    elif type=='complete':
        # temp='---\n'+'complete\n'+'clusters: '+str(ans[0])+', '+str(ans[1])+', '+str(ans[2])+'\nspan: '+str(span_list[0])+', '+str(span_list[1])+'\n'
        temp='complete clusters\n'
        temp+=marker+'\n'
        temp+='cluster1: '+str(ans[0])+'\nlen_cluster1: '+str(len(ans[0]))+'\n'+marker
        temp+='\ncluster2: '+str(ans[1])+'\nlen_cluster2: '+str(len(ans[1]))+'\n'+marker
        temp+='\ncluster3: '+str(ans[2])+'\nlen_cluster3: '+str(len(ans[2]))+'\n'+marker
        temp+='\naverage_single_span: ['+str(span_list[0])+', '+str(span_list[1])+']\n'+marker+'\n\n'
        print('complete clustering')
        print('----------------------------------------------')
    elif type=='average':
        # temp='---\n'+'average\n'+'clusters: '+str(ans[0])+', '+str(ans[1])+', '+str(ans[2])+'\nspan: '+str(span_list[0])+', '+str(span_list[1])+'\n'
        temp='complete clusters\n'
        temp+=marker+'\n'
        temp+='cluster1: '+str(ans[0])+'\nlen_cluster1: '+str(len(ans[0]))+'\n'+marker
        temp+='\ncluster2: '+str(ans[1])+'\nlen_cluster2: '+str(len(ans[1]))+'\n'+marker
        temp+='\ncluster3: '+str(ans[2])+'\nlen_cluster3: '+str(len(ans[2]))+'\n'+marker
        temp+='\naverage_span: ['+str(span_list[0])+', '+str(span_list[1])+']\n'+marker+'\n\n'
        print('average clustering')
        print('----------------------------------------------')
    else:
        return -1
    print('cluster1: ',ans[0])
    print('----------------------------------------------')
    print('len_cluster1: ',len(ans[0]))
    print('----------------------------------------------')
    print('cluster2: ',ans[1])
    print('----------------------------------------------')
    print('len_cluster2: ',len(ans[1]))
    print('----------------------------------------------')
    print('cluster3: ',ans[2])
    print('----------------------------------------------')
    print('len_cluster3: ',len(ans[2]))
    print('----------------------------------------------')
    print('span: ',span_list)
    print('----------------------------------------------\n\n')
    result.append(temp)
#use nearest
def single_cluster(coor):
    root=make_root(coor)
    matrix=make_matrix(root)
    max_sim=-1
    A_idx=-1
    B_idx=-1
    span_list=[]
    ans=[]
    while True:
        #check end point
        if root.len() ==3:
            span_list.append(max_sim)
            for i in range(root.len()):
                # pdb.set_trace()
                temp=[]
                for j in range(len(root.elements[i].elements)):
                    temp.append(root.elements[i].elements[j].pair)
                ans.append(temp)
        if root.len() ==2:
            span_list.append(max_sim)
            break
        #re_init
        max_sim=-1
        A_idx=-1
        B_idx=-1
        #find single cluster node
        for i in range(root.len()):
            for j in range(root.len()):
                if i==j:
                    continue
                if max_sim <matrix[i][j]:
                    A_idx=i
                    B_idx=j
                    max_sim=matrix[i][j]
        matrix,root=merge_cluster(matrix,A_idx,B_idx,root,'single')
    #print, file_print
    end_cluster(coor.output,ans,span_list,'single')
#use fartherest
def complete_cluster(coor):
    root=make_root(coor)
    matrix=make_matrix(root)
    max_sim=-1
    A_idx=-1
    B_idx=-1
    span_list=[]
    ans=[]
    while True:
        #check end point
        if root.len() ==3:
            span_list.append(max_sim)
            for i in range(root.len()):
                # pdb.set_trace()
                temp=[]
                for j in range(len(root.elements[i].elements)):
                    temp.append(root.elements[i].elements[j].pair)
                ans.append(temp)
        if root.len() ==2:
            span_list.append(max_sim)
            break
        #re_init
        max_sim=-1
        A_idx=-1
        B_idx=-1
        #find single cluster node
        for i in range(root.len()):
            for j in range(root.len()):
                if i>=j:
                    continue
                if max_sim<matrix[i][j]:
                    A_idx=i
                    B_idx=j
                    max_sim=matrix[i][j]
        matrix,root=merge_cluster(matrix,A_idx,B_idx,root,'complete')
    #print, file_print
    end_cluster(coor.output,ans,span_list,'complete')
#use avg
def average_cluster(coor):
    root=make_root(coor)
    matrix=make_matrix(root)
    span_list=[]
    ans=[]
    while True:
        #check end point
        if root.len() ==3:
            span_list.append(max_sim)
            for i in range(root.len()):
                # pdb.set_trace()
                temp=[]
                for j in range(len(root.elements[i].elements)):
                    temp.append(root.elements[i].elements[j].pair)
                ans.append(temp)
        if root.len() ==2:
            span_list.append(max_sim)
            break
        max_sim=-1
        A_idx=-1
        B_idx=-1
        for i in range(root.len()):
            for j in range(root.len()):
                if i>=j:
                    continue
                if max_sim<matrix[i][j]:
                    A_idx=i
                    B_idx=j
                    max_sim=matrix[i][j]
        matrix,root=merge_cluster(matrix,A_idx,B_idx,root,'average')
    end_cluster(coor.output,ans,span_list,'average')
#make root, base of clustering
def make_root(coor):
    root=cluster()
    for i in coor.point_list:
        new_cluster=cluster()
        new_cluster.elements.append(i)
        root.elements.append(new_cluster)
    return root
#make cos_similarity matrix
def make_matrix(root):
    matrix= [[0 for i in range(root.len())] for j in range(root.len())]
    for i in range(root.len()):
        for j in range(root.len()):
            matrix[i][j]=get_cos(root.elements[i].elements[0],root.elements[j].elements[0])
    for i in range(root.len()):
        for j in range(root.len()):
            if i==j:
                matrix[i][j]=-10
    return matrix
#write file
def make_output(coor):
    global result
    f=open(coor.output,'w')
    f.write('coor: '+str(coor.n)+'\nnum: '+str(coor.num_of_point)+'\n--------------------------------------------------\n\n')
    for i in result:
        f.write(i)
    result=[]
#do clustering
def do_cluster():
    for i in range(4):
        input= "CoordinatePlane_"+str(i+1)+'.txt'
        data=readfile(input)
        single_cluster(data)
        complete_cluster(data)
        average_cluster(data)
        make_output(data)

if __name__ == '__main__':
    do_cluster()
