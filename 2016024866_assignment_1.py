import pdb
class Maze:
    def __init__(self):
        self.input=""
        self.output=""
        self.key=[]
        self.row=0
        self.col=0
        self.start=0
        self.finish=0
        self.num=0
        self.map=[]
class Key:
    def __init__(self,row,col,d_s,idx,dist):
        self.row=row
        self.col=col
        self.dist_from_start=d_s
        self.dist_to_finish=0
        self.dist_to_keys=[]
        self.visit=[]
        self.idx=idx
        self.dist=dist
class Goal:
    def __init__(self,row,col,dist,idx):
        self.row=row
        self.col=col
        self.idx=idx
        self.dist=dist

d_row=[-1,0,1,0] # 북, 동, 남, 서의 순서로 탐색
d_col=[0,1,0,-1]
def readfile(map):
    file=open(map.input,'r')
    temp=file.readline()
    temp=temp.split()
    map.num=int(temp[0])
    map.row=int(temp[1]) # m
    map.col=int(temp[2]) # n
    map.map=[[0 for i in range(map.col)] for j in range(map.row)]
    # pdb.set_trace()
    for i in range(map.row):
        temp=file.readline()
        temp=temp.strip()
        temp=temp.replace('\t',"")
        temp=temp.replace(' ',"")
        # temp=temp.split()
        temp=list(temp)
        for j in range(map.col):
            map.map[i][j]=temp[j]
            if temp[j] =='1' or temp[j] =='2':
                continue
            elif temp[j]=='3':
                map.start=(i,j)
            elif temp[j]=='4':
                map.finish=(i,j)
            elif temp[j]=='6':
                map.key.append((i,j))
            else:
                continue
    file.close()
def movable(visit,maze,r,c):
    if r>=0 and r < maze.row and c >=0 and c <maze.col: #미로를 벗어나지 않으면서
        if maze.map[r][c]!='1':# 벽이 아니고
            if visit[r][c] ==0: # 방문한 적이 없는 곳이면
                return 1
    return 0
def find_path(maze,visit,end_row,end_col):
    global d_row,d_col
    path=[(end_row,end_col)]
    current_row=end_row
    current_col=end_col
    # pdb.set_trace()
    while visit[current_row][current_col] >1:
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if next_row>=0 and next_row < maze.row and next_col >=0 and next_col <maze.col:
                if visit[next_row][next_col]==visit[current_row][current_col]-1:
                    path.append((next_row,next_col))
                    current_row=next_row
                    current_col=next_col
                    break
    # pdb.set_trace()
    path.reverse()
    return path
def perm(lst,n):
	ret = []
	if n > len(lst): return ret

	if n==1:
		for i in lst:
			ret.append([i])
	elif n>1:
		for i in range(len(lst)):
			temp = [i for i in lst]
			temp.remove(lst[i])
			for p in perm(temp,n-1):
				ret.append([lst[i]]+p)

	return ret
def dfs(maze):
    start_point=maze.start
    key_path=[ [] for i in range(len(maze.key))]
    finish_path=[]
    path=[]
    global d_row,d_col
    visit= [[[0 for i in range(maze.col)] for j in range(maze.row)] for k in range(len(maze.key)+1)]
    visit[0][start_point[0]][start_point[1]] = 1
    current_row=start_point[0]
    current_col=start_point[1]
    check_move=0
    time=0
    check_key=0
    while check_key<len(maze.key):
        key_path[check_key].append((current_row,current_col))
        while key_path[check_key]:
            if maze.map[current_row][current_col]=='6':
                check_key+=1
                maze.map[current_row][current_col]='2'
                visit[check_key][current_row][current_col]=visit[check_key-1][current_row][current_col]+1
                break
            check_move=0
            for i in range(4):
                next_row=current_row+d_row[i]
                next_col=current_col+d_col[i]
                if movable(visit[check_key],maze,next_row,next_col)==1:
                    key_path[check_key].append((next_row,next_col))
                    visit[check_key][next_row][next_col]=visit[check_key][current_row][current_col]+1
                    current_row=next_row
                    current_col=next_col
                    check_move=1
                    time+=1
                    break
            if check_move==0:
                key_path[check_key].pop()
                current_row=key_path[check_key][-1][0]
                current_col=key_path[check_key][-1][1]
    finish_path.append((current_row,current_col))
    while finish_path:
        if maze.map[current_row][current_col]=='4':
            break
        check_move=0
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if movable(visit[check_key],maze,next_row,next_col)==1:
                finish_path.append((next_row,next_col))
                visit[check_key][next_row][next_col]=visit[check_key][current_row][current_col]+1
                current_row=next_row
                current_col=next_col
                check_move=1
                time+=1
                break
        if check_move==0:
            finish_path.pop()
            current_row=finish_path[-1][0]
            current_col=finish_path[-1][1]
    for i in range(len(maze.key)):
        path+=key_path[i]
    path+=finish_path
    for row,col in path:
        maze.map[row][col]='5'
    maze.output=maze.output+"_dfs.txt"
    file=open(maze.output,'w')
    for i in range(maze.row):
        file.write(''.join(maze.map[i])+'\n')
    # pdb.set_trace()
    file.write("length="+str(len(path)-check_key-1)+"\n")
    file.write("time="+str(time)+"\n")
    # pdb.set_trace()
    file.close()
def bfs(maze):
    global d_row, d_col
    path=[]
    start_queue=[maze.start]
    current_row,current_col=maze.start
    start_visit= [[0 for i in range(maze.col)] for j in range(maze.row)]
    start_visit[maze.start[0]][maze.start[1]] = 1
    start_to_keys=[0 for i in range(len(maze.key))]
    finish_point=0
    key_node=[]
    key_idx=0
    time=0
    check_move=0
    check_finish=0
    check_key=0
    while start_queue:
        for i in range(4): #복동남서 탐색
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if movable(start_visit,maze,next_row,next_col)==1:
                start_queue.insert(0,(next_row,next_col))
                start_visit[next_row][next_col]=start_visit[current_row][current_col]+1
                time+=1
                if maze.map[next_row][next_col]=='6':
                    check_key+=1
                    key_node.append(Key(next_row,next_col,start_visit[next_row][next_col],key_idx,0))
                    key_node[key_idx].visit=[[0 for i in range(maze.col)] for j in range(maze.row)]
                    key_node[key_idx].dist_to_keys=[0 for i in range(len(maze.key))]
                    start_to_keys[key_idx]=start_visit[next_row][next_col]
                    key_idx+=1
                if maze.map[next_row][next_col]=='4':
                    finish_point=(next_row,next_col)
                    check_finish=1
        if check_finish==1 and check_key==len(maze.key):
            break
        current_row,current_col=start_queue.pop(0)

    for k in range(key_idx):
        temp=[(key_node[k].row,key_node[k].col)]
        current_row,current_col=temp[0]
        check_key=0
        check_finish=0
        while temp:
            for i in range(4): #복동남서 탐색
                next_row=current_row+d_row[i]
                next_col=current_col+d_col[i]
                if movable(key_node[k].visit,maze,next_row,next_col)==1:
                    temp.insert(0,(next_row,next_col))
                    key_node[k].visit[next_row][next_col]=key_node[k].visit[current_row][current_col]+1
                    time+=1
                    if maze.map[next_row][next_col]=='6':
                        check_key+=1
                        for j in key_node:
                            if j.row==next_row and j.col==next_col:
                                key_node[k].dist_to_keys[j.idx]=key_node[k].visit[next_row][next_col]
                    if maze.map[next_row][next_col]=='4':
                        key_node[k].dist_to_finish=key_node[k].visit[next_row][next_col]
                        check_finish=1
                if check_finish==1 and check_key==len(maze.key):
                    break
            current_row,current_col=temp.pop(0)
#--------------------------------------------------------------------------------
    arr=[i for i in range(len(maze.key))]
    tries=perm(arr,len(arr))
    length=[0 for i in range(len(tries))]
    idx=-1
    next_idx=-1
    min=100000
    min_idx=-1
    short_path=[]
    for i in range(len(tries)):
        temp=list(tries[i])
        idx=temp.pop(0)
        length[i]=start_to_keys[idx]
        while temp:
            next_idx=temp.pop(0)
            length[i]+=key_node[idx].dist_to_keys[next_idx]
            idx=next_idx
        length[i]+=key_node[idx].dist_to_finish
        if min> length[i]:
            min=length[i]
            min_idx=i
#----------------------------------------------------------------------------------------
    path_idx=-1
    next_path_idx=-1
    temp=list(tries[min_idx])
    path_idx=temp.pop(0)
    short_path+=find_path(maze,start_visit,key_node[path_idx].row,key_node[path_idx].col)
    while temp:
        next_path_idx=temp.pop(0)
        short_path+=find_path(maze,key_node[path_idx].visit,key_node[next_path_idx].row,key_node[next_path_idx].col)
    short_path+=find_path(maze,key_node[next_path_idx].visit,finish_point[0],finish_point[1])
    for row,col in short_path:
        maze.map[row][col]='5'
    maze.map[maze.start[0]][maze.start[1]]='3'
    maze.map[finish_point[0]][finish_point[1]]='4'
    maze.output=maze.output+"_BFS_output.txt"
    file=open(maze.output,'w')
    for i in range(maze.row):
        file.write(''.join(maze.map[i])+'\n')
    file.write("length="+str(len(short_path)-1)+"\n")
    file.write("time="+str(time)+"\n")
    file.close()
def gbfs(maze):
    global d_row, d_col
    path=[]
    queue=[maze.start]
    current_row,current_col=maze.start
    start_to_keys=[0 for i in range(len(maze.key))]
    finish_point=0
    key_node=[]
    key_idx=0
    time=0
    key_order=[]
    temp_finish=[100000 for i in range(4)]
    next_min=100000
    next_min_idx=-1
    next_temp_idx=-1
    for i in range(maze.row):
        for j in range(maze.col):
            if maze.map[i][j] =='4':
                finish_point=(i,j)
            elif maze.map[i][j] =='6':
                dist=abs(i-maze.start[0])+abs(j-maze.start[1])
                key_node.append(Key(i,j,0,key_idx,dist))
                key_idx+=1
    temp_dist=[[100000 for i in range(4)] for j in range(key_idx)]
    start_visit=[[[0 for i in range(maze.col)] for j in range(maze.row)]for k in range(key_idx+1)]
    start_visit[0][maze.start[0]][maze.start[1]] = 1
    visit_idx=0
    goals=list(key_node)
    goal_idx=key_idx
#--------------------------------------------------------------------
    while queue:
        queue_idx=queue.index((current_row,current_col))
        queue.pop(queue_idx)
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if movable(start_visit[visit_idx],maze,next_row,next_col)==1:
                queue.insert(0,(next_row,next_col))
                start_visit[visit_idx][next_row][next_col]=start_visit[visit_idx][current_row][current_col]+1
                time+=1
                for j in range(len(key_node)):
                    temp_dist[j][i]=abs(key_node[j].row-next_row)+abs(key_node[j].col-next_col)
            else:
                for j in range(len(key_node)):
                    temp_dist[j][i]=100000
        next_min=100000
        for i in range(4):
            for j in range(len(key_node)):
                if next_min > temp_dist[j][i]:
                    next_min= temp_dist[j][i]
                    next_min_idx=i
                    next_temp_idx=j
        current_row=current_row+d_row[next_min_idx]
        current_col=current_col+d_col[next_min_idx]
        path.append((current_row,current_col)) #디버깅
        if next_min==100000:
            for i in range(len(queue)):
                for j in range(len(key_node)):
                    if next_min > (abs(key_node[j].row-queue[i][0])+ abs(key_node[j].col-queue[i][1])):
                        temp_idx=i
                        temp_node=j
            current_row,current_col=queue[i]
        for i in range(len(key_node)):
            key_node[i].dist=abs(key_node[i].row-current_row)+abs(key_node[i].col-current_col)
            if key_node[i].row == current_row and key_node[i].col == current_col:
                queue=[(current_row,current_col)]
                visit_idx+=1
                start_visit[visit_idx][current_row][current_col]=1
                key_order.append(key_node[i].idx)
                key_node.pop(i)
                break
        if not key_node:
            break
        if start_visit[0][2][1] ==4:
            pdb.set_trace()
    dist_to_finish=abs(finish_point[0]-current_row)+abs(finish_point[1]-current_col)
    check_debug=0
#-----------------------------------------------------------------------
    while queue:
        queue_idx=queue.index((current_row,current_col))
        queue.pop(queue_idx)
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if movable(start_visit[visit_idx],maze,next_row,next_col)==1:
                queue.insert(0,(next_row,next_col))
                start_visit[visit_idx][next_row][next_col]=start_visit[visit_idx][current_row][current_col]+1
                time+=1
                temp_finish[i]=(abs(finish_point[0]-next_row)+abs(finish_point[1]-next_col))
            else:
                temp_finish[i]=100000
        next_min=100000
        for i in range(4):
            if next_min > temp_finish[i]:
                next_min= temp_finish[i]
                next_min_idx=i
        current_row=current_row+d_row[next_min_idx]
        current_col=current_col+d_col[next_min_idx]
        temp_idx=-1
        if next_min==100000:
            for i in range(len(queue)):
                if next_min > (abs(finish_point[0]-queue[i][0])+ abs(finish_point[1]-queue[i][1])):
                    temp_idx=i
            current_row,current_col=queue[i]
        pos=(current_row,current_col)
        path.append((current_row,current_col)) #디버깅
        if current_row==finish_point[0] and current_col==finish_point[1]:
            break
    #---------------------------------------------------------------------------------
    short_path=[]
    for i in range(len(key_order)):
        short_path+=find_path(maze,start_visit[i],goals[key_order[i]].row,goals[key_order[i]].col)
    short_path+=find_path(maze,start_visit[i+1],finish_point[0],finish_point[1])
    for row,col in short_path:
        maze.map[row][col]='5'
    maze.map[maze.start[0]][maze.start[1]]='3'
    maze.map[finish_point[0]][finish_point[1]]='4'
    maze.output=maze.output+"_GBFS_output.txt"
    file=open(maze.output,'w')
    for i in range(maze.row):
        file.write(''.join(maze.map[i])+'\n')
    file.write("length="+str(len(short_path)-key_idx-1)+"\n")
    file.write("time="+str(time)+"\n")
    file.close()
def a_star(maze):
    global d_row, d_col
    path=[]
    queue=[maze.start]
    current_row,current_col=maze.start
    start_to_keys=[0 for i in range(len(maze.key))]
    finish_point=0
    key_node=[]
    key_idx=0
    time=0
    key_order=[]
    temp_finish=[100000 for i in range(4)]
    finish_value=[100000 for i in range(4)]
    next_min=100000
    next_min_idx=-1
    next_temp_idx=-1
    for i in range(maze.row):
        for j in range(maze.col):
            if maze.map[i][j] =='4':
                finish_point=(i,j)
            elif maze.map[i][j] =='6':
                dist=abs(i-maze.start[0])+abs(j-maze.start[1])
                key_node.append(Key(i,j,0,key_idx,dist))
                key_idx+=1
    temp_dist=[[100000 for i in range(4)] for j in range(key_idx)]
    temp_value=[[100000 for i in range(4)] for j in range(key_idx)]
    start_visit=[[[0 for i in range(maze.col)] for j in range(maze.row)]for k in range(key_idx+1)]
    start_visit[0][maze.start[0]][maze.start[1]] = 1
    visit_idx=0
    goals=list(key_node)
    goal_idx=key_idx
#--------------------------------------------------------------------------------------------------------
    while queue:
        #Queue에서 다음 노드를 받아옴.
        queue_idx=queue.index((current_row,current_col))
        queue.pop(queue_idx)
        #현재 노드에서 움직일 수 있는 장소를 탐색
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            #움직일 수 있는 경우
            if movable(start_visit[visit_idx],maze,next_row,next_col)==1:
                queue.insert(0,(next_row,next_col))
                start_visit[visit_idx][next_row][next_col]=start_visit[visit_idx][current_row][current_col]+1
                time+=1
                #이동한 node와 key사이의 거리를 측정
                for j in range(len(key_node)):
                    temp_dist[j][i]=abs(key_node[j].row-next_row)+abs(key_node[j].col-next_col)
                    temp_value[j][i]=temp_dist[j][i]+start_visit[visit_idx][current_row][current_col]
            #움직일 수 없는 경우
            else:
                for j in range(len(key_node)):
                    temp_dist[j][i]=100000
                    temp_value[j][i]=100000
        #temp_dist배열(현재 확장된 노드와 key 사이의 거리를 정리한 배열)에서 최소값을 추출
        next_min=100000
        for i in range(4):
            for j in range(len(key_node)):
                if next_min > temp_value[j][i]:
                    next_min= temp_value[j][i]
                    next_min_idx=i
                    next_temp_idx=j
        current_row=current_row+d_row[next_min_idx]
        current_col=current_col+d_col[next_min_idx]
        #현재 상황에서 확장할 수 없는 경우(막다른 길)
        #Queue에서 node를 받아서 다음 노드를 찾아줌
        if next_min==100000:
            for i in range(len(queue)):
                for j in range(len(key_node)):
                    if next_min > (abs(key_node[j].row-queue[i][0])+ abs(key_node[j].col-queue[i][1])):
                        temp_idx=i
                        temp_node=j
            current_row,current_col=queue[i]
        #현재 이동한 노드가 Key위치인지 확인
        for i in range(len(key_node)):
            key_node[i].dist=abs(key_node[i].row-current_row)+abs(key_node[i].col-current_col)
            if key_node[i].row == current_row and key_node[i].col == current_col:
                #queue를 초기화
                queue=[(current_row,current_col)]
                visit_idx+=1
                start_visit[visit_idx][current_row][current_col]=1
                key_order.append(key_node[i].idx)
                key_node.pop(i)
                break
        #모든 키를 찾은경우 다음단계로 진행
        if not key_node:
            break
#-----------------------------------------------------------------------------------------------------
    #키를 모두 찾은 이후 목적지를 찾는 과정
    dist_to_finish=abs(finish_point[0]-current_row)+abs(finish_point[1]-current_col)
    check_debug=0
    while queue:
        queue_idx=queue.index((current_row,current_col))
        queue.pop(queue_idx)
        for i in range(4):
            next_row=current_row+d_row[i]
            next_col=current_col+d_col[i]
            if movable(start_visit[visit_idx],maze,next_row,next_col)==1:
                queue.insert(0,(next_row,next_col))
                start_visit[visit_idx][next_row][next_col]=start_visit[visit_idx][current_row][current_col]+1
                time+=1
                temp_finish[i]=(abs(finish_point[0]-next_row)+abs(finish_point[1]-next_col))
                finish_value[i]=temp_finish[i]+start_visit[visit_idx][current_row][current_col]
            else:
                temp_finish[i]=100000
                finish_value[i]=100000
        next_min=100000
        for i in range(4):
            if next_min > finish_value[i]:
                next_min= finish_value[i]
                next_min_idx=i
        current_row=current_row+d_row[next_min_idx]
        current_col=current_col+d_col[next_min_idx]
        temp_idx=-1
        if next_min==100000:
            for i in range(len(queue)):
                if next_min > (abs(finish_point[0]-queue[i][0])+ abs(finish_point[1]-queue[i][1])):
                    temp_idx=i
            current_row,current_col=queue[i]
        pos=(current_row,current_col)
        path.append((current_row,current_col)) #디버깅
        if current_row==finish_point[0] and current_col==finish_point[1]:
            break
#----------------------------------------------------------------------------------------------------
    short_path=[]
    for i in range(len(key_order)):
        short_path+=find_path(maze,start_visit[i],goals[key_order[i]].row,goals[key_order[i]].col)
    short_path+=find_path(maze,start_visit[i+1],finish_point[0],finish_point[1])
    for row,col in short_path:
        maze.map[row][col]='5'
    maze.map[maze.start[0]][maze.start[1]]='3'
    maze.map[finish_point[0]][finish_point[1]]='4'
    maze.output=maze.output+"_A_star_output.txt"
    file=open(maze.output,'w')
    for i in range(maze.row):
        file.write(''.join(maze.map[i])+'\n')
    file.write("length="+str(len(short_path)-key_idx-1)+"\n")
    file.write("time="+str(time)+"\n")
    file.close()
def ids(maze):
    start_point=maze.start
    key_path=[ [] for i in range(len(maze.key))]
    finish_path=[]
    path=[]
    global d_row,d_col
    visit= [[[0 for i in range(maze.col)] for j in range(maze.row)] for k in range(len(maze.key)+1)]
    visit[0][start_point[0]][start_point[1]] = 1
    current_row=start_point[0]
    current_col=start_point[1]
    check_move=0
    check_key=0
    time=0
    depth=0
    check_finish=0
    #--------------------------------------------------------------------------
    while check_key<len(maze.key):
        key_path[check_key].append((current_row,current_col))
        while key_path[check_key]:
            # pdb.set_trace()
            if visit[check_key][current_row][current_col] > depth:
                key_path[check_key].pop()
                if key_path[check_key]:
                    current_row,current_col=key_path[check_key][-1]
                else:
                    current_row,current_col=maze.start
                continue
            #키를 찾은경우 해당 지점부터 재탐색
            if maze.map[current_row][current_col]=='6':
                check_key+=1
                maze.map[current_row][current_col]='2'
                visit[check_key][current_row][current_col]=visit[check_key-1][current_row][current_col]+1
                start_point=(current_row,current_col)
                depth=0
                break
            check_move=0
            #상하좌우 움직일 수 있는 경로로 우선탐색
            for i in range(4):
                next_row=current_row+d_row[i]
                next_col=current_col+d_col[i]
                if movable(visit[check_key],maze,next_row,next_col)==1:
                    key_path[check_key].append((next_row,next_col))
                    visit[check_key][next_row][next_col]=visit[check_key][current_row][current_col]+1
                    current_row=next_row
                    current_col=next_col
                    check_move=1
                    time+=1
                    break
            #말을 움직일 수 없는 경우
            if check_move==0:
                key_path[check_key].pop()
                # current_row,current_col=key_path[check_key][-1]
                if key_path[check_key]:
                    current_row,current_col=key_path[check_key][-1]
                else:
                    current_row,current_col=start_point        #goal_depth를 높이면서 시작지점 초기화
        for i in range(maze.row):
            for j in range(maze.col):
                visit[check_key][i][j]=0
        current_row,current_col=start_point
        depth+=1

#-------------------------------------------------------------------------------------------
    finish_path.append((current_row,current_col))
    # pdb.set_trace()
    depth=0
    while True:
        while finish_path:
            # pdb.set_trace()
            if maze.map[current_row][current_col]=='4':
                check_finish=1
                finish_point=(current_row,current_col)
                break
            if visit[check_key][current_row][current_col] > depth:
                finish_path.pop()
                if finish_path:
                    current_row,current_col=finish_path[-1]
                else:
                    current_row,current_col=start_point
                continue
            check_move=0
            for i in range(4):
                next_row=current_row+d_row[i]
                next_col=current_col+d_col[i]
                if movable(visit[check_key],maze,next_row,next_col)==1:
                    finish_path.append((next_row,next_col))
                    visit[check_key][next_row][next_col]=visit[check_key][current_row][current_col]+1
                    current_row=next_row
                    current_col=next_col
                    check_move=1
                    time+=1
                    break
            if check_move==0:
                finish_path.pop()
                if finish_path:
                    current_row,current_col=finish_path[-1]
                else:
                    current_row,current_col=start_point

        if check_finish:
            break
        for i in range(maze.row):
            for j in range(maze.col):
                visit[check_key][i][j]=0
        depth+=1
        current_row,current_col=start_point
        finish_path.append(start_point)
#----------------------------------------------------------------------------------------
    for i in range(len(maze.key)):
        path+=key_path[i]
    path+=finish_path
    for row,col in path:
        maze.map[row][col]='5'
    maze.map[maze.start[0]][maze.start[1]]='3'
    maze.map[finish_point[0]][finish_point[1]]='4'
    maze.output=maze.output+"_IDS_output.txt"
    file=open(maze.output,'w')
    for i in range(maze.row):
        file.write(''.join(maze.map[i])+'\n')
    file.write("length="+str(len(path)-check_key-1)+"\n")
    file.write("time="+str(time)+"\n")
    file.close()

def main():
    Map_list=[]
    for i in range(4):
        Map_list.append(Maze())
        Map_list[i].input="Maze_"+str(i+1)+".txt"
        Map_list[i].output="Maze_"+str(i+1)
        readfile(Map_list[i])
        #ids(Map_list[i])

    Map_list=[]
    for i in range(6):
        Map_list.append(Maze())
        Map_list[i].input="Maze_"+str(i+1)+".txt"
        Map_list[i].output="Maze_"+str(i+1)
        readfile(Map_list[i])
        bfs(Map_list[i])

    Map_list=[]
    for i in range(6):
        Map_list.append(Maze())
        Map_list[i].input="Maze_"+str(i+1)+".txt"
        Map_list[i].output="Maze_"+str(i+1)
        readfile(Map_list[i])
        gbfs(Map_list[i])

    Map_list=[]
    for i in range(6):
        Map_list.append(Maze())
        Map_list[i].input="Maze_"+str(i+1)+".txt"
        Map_list[i].output="Maze_"+str(i+1)
        readfile(Map_list[i])
        a_star(Map_list[i])

if __name__=="__main__":
    main()
