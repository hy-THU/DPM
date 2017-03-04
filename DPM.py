import math
import random
import time


#####################    Data Generation    ################################
x=[]
y=[]
data=[]
average_list=[(2,2),(-2,2),(2,-2),(-2,-2)]
for item in average_list:
    x.append([random.gauss(item[0],1) for i in range(200)])
    y.append([random.gauss(item[1],1) for i in range(200)])

for k in range(len(average_list)):
    for i in range(200):
        data.append((x[k][i],y[k][i],k))
random.shuffle(data)

datafile=open('data','w')
for x,y,truek in data:
    print >>datafile,x,y,truek



    
def multisampling(Prob):
    Prob_sum=sum(Prob)
    Prob=[p/Prob_sum for p in Prob]
    pp=random.random()
    k=0
    P=0.0
    for p in Prob:
        P+=p
        if pp<=P:
            break
        else:
            k+=1
    return k

########################################    DPM    ############################################
time_begin = time.time()

N=len(data)
alpha=100
d=2
tag=[-1]*N
mean=[]
nk=[]
DK=[]
M_dist1=[]
M_dist2=[]
K_count=[]
for loop in range(10):
    prob=[]
    for n in range(N):
        x=data[n]
        k_old=tag[n]
        if k_old>=0:
            nk[k_old]-=1
        prob=[0]*(len(mean)+1)
        for k in range(len(mean)):
            #prob[k]=float(nk[k])/float(N-1+alpha)/(2*math.pi)**(d/2)/math.exp(0.5*sum([(x[i]-mean[k][i])**2 for i in range(d)]))
            if nk[k]==0:
                prob[k]=0.0
            else:
                prob[k]=math.log(float(nk[k])/float(N-1+alpha)/(2*math.pi)**(d/2))-(0.5*sum([(x[i]-mean[k][i])**2 for i in range(d)]))
                prob[k]=math.exp(prob[k])
        #prob[len(mean)]=alpha*math.sqrt(0.5)/(N-1+alpha)/(2*math.pi)**(d/2)/math.exp(0.25*sum([x[i]**2 for i in range(d)]))
        prob[len(mean)]=math.log(alpha*math.sqrt(0.5)/(N-1+alpha)/(2*math.pi)**(d/2))-(0.25*sum([x[i]**2 for i in range(d)]))
        prob[len(mean)]=math.exp(prob[len(mean)])
        k_new=multisampling(prob)
        if k_new==len(nk):
            nk.append(1)
        elif k_new>len(nk):
            print 'fuck'
        else:
            nk[k_new]+=1
        tag[n]=k_new
    for k in range(len(mean)+1):
        ck=0
        k_sum=[0.0,0.0]
        for n in range(N):
            if tag[n]==k:
                ck+=1
                k_sum[0]+=data[n][0]
                k_sum[1]+=data[n][1]
        k_mu=[k_sum[0]/(1+ck),k_sum[1]/(1+ck)]
        k_sigma=1.0/(1+ck)
        if k==len(mean) and ck!=0:
            mean.append([0.0,0.0])
        elif k==len(mean) and ck==0:
            break
        
        mean[k][0]=random.gauss(k_mu[0],k_sigma)
        mean[k][1]=random.gauss(k_mu[1],k_sigma)


    mean_new=[]
    nk_new=[]
    tag_new=[-1]*N
    k_new=0
    for k in set(tag):
        mean_new.append(mean[k])
        nk_new.append(nk[k])
        for n in range(N):
            if(tag[n]==k):
                tag_new[n]=k_new
        k_new+=1
    mean=mean_new
    nk=nk_new
    tag=tag_new

    K_count.append(len(nk))


    DK.append(len(nk)-math.log(float(alpha)/float((1+(N/alpha)))))
    M_dist1.append(sum([math.sqrt(sum([mean[k][i]**2 for i in range(d)])) for k in range(len(nk))]))
    M_dist2.append(sum([math.sqrt(sum([(data[n][i]-mean[tag[n]][i])**2 for i in range(d)])) for n in range(N)]))
    
time_last = time.time() - time_begin

print time_last

resultfile=open('result.m','w')
print >>resultfile, 'mean=['+';'.join('%s,%s' %(x,y) for x,y in mean)+']'
print >>resultfile, 'DK=',DK
print >>resultfile, 'M_dist1=',M_dist1
print >>resultfile, 'M_dist2=',M_dist2
print >>resultfile, 'tag=',tag
print >>resultfile, 'nk=',nk
print >>resultfile, 'K_count=',K_count


graphfile=open('graph.m','w')

print >>graphfile, '''result;'''
print >>graphfile, '''data = load('data');'''
print >>graphfile, 'figure'
print >>graphfile, '''scatter(data(:,1),data(:,2),[], tag, '.'), hold on, scatter(mean(:,1),mean(:,2),70*nk,[0:(length(nk)-1)]', 'O'), hold off, title('RESULT')'''
print >>graphfile, 'figure'
print >>graphfile, 'subplot(4,1,1)'
print >>graphfile, 'plot(K_count)'
print >>graphfile, '''title('K_count/iterations')'''
print >>graphfile, 'subplot(4,1,2)'
print >>graphfile, 'plot(DK)'
print >>graphfile, '''title('DK/iterations')'''
print >>graphfile, 'subplot(4,1,3)'
print >>graphfile, 'plot(M_dist1)'
print >>graphfile, '''title('M_dist1/iterations')'''
print >>graphfile, 'subplot(4,1,4)'
print >>graphfile, 'plot(M_dist2)'
print >>graphfile, '''title('M_dist2/iterations')'''



datafile.close()
resultfile.close()
graphfile.close()
##################################################################### evaluation###############################################################
t=0
f=0

for n in range(N):
    
    if data[n][d]==tag[n]:
        t+=1
    else:
        f+=1
print float(t)/float(N)
print 'done'

            
