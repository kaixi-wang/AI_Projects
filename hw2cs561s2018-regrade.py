# -*- coding: utf-8 -*-
# Input format:
# <GROUP COUNT>: The number of groups for the 2018 FIFA World Cup draw.
# <POT COUNT>: The number of pots for the 2018 FIFA World Cup draw.
# <POTS DIVISION>: It contains <POTS COUNT> lines:
#    where the first line is a comma-separated list of the teams belonging to Pot 1, and
#    the following lines show the teams of Pots 2 to <POTS COUNT>, respectively.
# <TEAMS CONFEDERATION>: It contains 6 lines where each line begins with the name of one of the continental confederations 
#    (AFC, CAF, CONCACAF, CONMEBOL, OFC, or UEFA) followed by a colon “:” 
#    and then the names of the teams from this continental confederation separated by commas “,”. 
#    If there is no team from a continental confederation, it is denoted by “None”.

filename='32.txt'
solution=''
roster={} # key=[team], value=[conference][pot]
pots={} # dict with key=pot number, value=teams
conference={} # dict with key=conference, value=teams
def removeValues(aList, n):
    return [ i for i in aList if i != n ]
    
def invert(d): #Turn {a:x, b:x} into {x:[a,b]}
    r = {}
    for key, values in d.items():
        for val in values:
            if val!='None':
                r.setdefault(val,key)
    return r

def findIndex(theList, item): #gives index of item within list of lists
    for ind in xrange(len(theList)) :
        if item in theList[ind]:
            return [ind, theList[ind].index(item)] 
    
def isSolvable(filename):
    solution=''
    info=getInfo(filename)
    group_count=int(info[0])
    pot_count=int(info[1])
    pots_size=[0] # pot_size(0)=max pot size
    for pot in range(1,pot_count+1):
        pots[pot]=info[pot+1].split(',')
        pots_size.append(len(pots[pot]))
    #make list of conference by decreasing size
    conference_size=[] # conference_size(0)=max length of a conference 
    for c in range(0,6):
        conf,teams=info[c+2+pot_count].split(':')
        if 'None' not in teams:
            conference[conf]=teams.split(',')
            l=len(conference[conf])
            conference_size.append([conf,l])
    conference_size.sort(key=lambda x: x[1])
    conference_size.reverse()
    
    solution='Yes'        
    if max(pots_size)>group_count:
        solution='No'
    
    if conference_size[0][1]>group_count:
        if len(conference['UEFA'])>(2*group_count):
            solution= 'No'
            
        elif conference_size[0][0]!='UEFA':
            solution='No'
    
    return solution
   
    
def getConf(t,roster):
    c=roster[t][1]
    return c
    
def getPot(t,roster):
    p=roster[t][0]
    return p
    
def createRoster(conference,pots): #build roster dict{} in which key=team, value=[pot,conference]
    roster={}
    conf_by_team=invert(conference)
    pot_by_team=invert(pots)
    for k,v in conf_by_team.items(): 
        if k in pot_by_team:
            roster[k]=[pot_by_team[k]]
            roster[k].append(v)
    return roster
    

def getInfo(filename):
    with open(filename) as f:
        i= f.read().splitlines()
        f.close()
    return i
    
def output(solvable,groups):
    with open('output.txt', 'w') as f_out:
        f_out.write(solvable)
        if solvable=='Yes':
            for teams in groups:
                if 0 in teams:
                    groupings='None'
                else:
                    group=''
                    for t in teams:
                        group+= str(t[0])+','
                    groupings=group[0:-1]
                f_out.write('\n'+groupings)
            
        f_out.close()
    return
   

    
def main():
    info=getInfo(filename)
    group_count=int(info[0])
    pot_count=int(info[1])
    pots_size=[0] 
    for pot in range(1,pot_count+1):
        pots[pot]=info[pot+1].split(',')
        pots_size.append(len(pots[pot]))
    
    #make list of conference by decreasing size
    conference_size=[] # conference_size(0)=max length of a conference 
    for c in range(0,6):
        conf,teams=info[c+2+pot_count].split(':')
        if 'None' not in teams:
            conference[conf]=teams.split(',')
            l=len(conference[conf])
            conference_size.append([conf,l])
    conference_size.sort(key=lambda x: x[1])
    
    
    pots_list=[0] # list of teams indexed by pot number
    pots_copy=pots.copy()
    for k,v in pots_copy.items(): 
        pots_list.append(v)
    conf_list=[] # list of possible conferences from which next selected team can be from
    for con,num in conference_size: 
        conf_list.append([num,con])
    conf_list.sort(reverse=True)
    c_list=[] #conference list without number of teams in descending order
    for n,c in conf_list: 
        c_list.append(c)
        if c=='UEFA':
            c_list.append(c)
    roster=createRoster(conference,pots)
    groups=[[0 for x in range(1)] for y in range(group_count)] 
    c_list_groups={}
    for n in range(0,group_count):
        c_list_groups[n]=c_list[:]
    p_list_groups={}
    for n in range(0, group_count):
        p_list_groups[n]=range(1, pot_count+1)
    group=0
    for p in pots.copy(): #for each pot number...
        pot_number=p        
        while len(pots_list[pot_number])>0: #assign teams within each pot to groups...
            team=pots_list[pot_number][0] #specific team
            x_conf=getConf(team,roster)# conference to which team belongs to
            x_pot=getPot(team,roster)# pot to which team belongs to
            attempt=[] #list of attempts
            filled=False
            failed=False
            while len(attempt)<=(group_count*2) and filled==False:
                if failed==False:
                    attempt.append(group)
                    if (x_conf in c_list_groups[group]) and (x_pot in p_list_groups[group]):
                        if 0 in groups[group]:
                            groups[group]=[[team,x_conf,x_pot]]
                            filled=True
                        else:
                            groups[group].append([team,x_conf,x_pot])
                            filled=True
                        c_list_groups[group].remove(x_conf) # remove team conf from conf list of possible teams
                        p_list_groups[group].remove(x_pot) # remove team pot from list of possible pots
                        pots_list[pot_number].remove(team) #  remove team from pots list of possible teams
              
                    if len(attempt)>(group_count+1):
                        failed=True
                        continue
                    if group<(group_count-1):
                        group+=1
                    elif group==(group_count-1):
                        group=0
                        
                if failed==True:
                    swap1=team
                    
                    try:
                        s_x,i=findIndex(c_list_groups.values(),x_conf)# finds index within list of conf where current team can go
                        swap_group=s_x #new group where team will fit
                        swap2= groups[swap_group][-1] #team that will be displaced
                        groups[swap_group][-1]=[swap1,x_conf,x_pot] #displace swap2 with swap1 (failed to place team)
                        c_list_groups[swap_group].remove(x_conf)
                        pots_list[pot_number].remove(team) #remove team from need-assignment pot
                        
                        team=swap2[0] #reassign team                 
                        x_conf=swap2[1] #displaced team changed to current/working team
                        x_pot=swap2[2]
    
                        if (x_conf in c_list_groups[group]) and (x_pot in p_list_groups[group]):
                            groups[group].append([team,x_conf,x_pot])
                            c_list_groups[group].remove(x_conf) # remove team conf from conf list of possible teams
                            p_list_groups[group].remove(x_pot) # remove team pot from list of possible pots
                            filled=True
                        else:    
                            pots_list[x_pot].append(team) #add displaced group back into need-assignment pot
                            c_list_groups[group].append(x_conf)
                            failed=False
                            attempt=[]
                            
                    except TypeError:
                        print groups
                        print 'c_list_groups.values(): ',c_list_groups.values()
                        print 'x_conf: ',x_conf
                        return

             
    return groups

problem=isSolvable(filename)
if problem=='No':
    output(problem,0)
else:
    g=main()
    output(problem, g)
print g
  