%data generation
average_list=[15,19;-11.4,4;4.2,-17.4;-18.2,-6];
data=[;];
for i=1:size(average_list,1)
    x=normrnd(average_list(i,1),1,2000,1);
    y=normrnd(average_list(i,2),1,2000,1);
    new_data=cat(2,x,y);
    new_data(:,3)=i;%the 3rd column is the true k
    new_data(:,4)=0;%the 4th column is the prediction of k
    data=cat(1,data,new_data);
    
end
temp=randperm(size(data,1));
data=data(temp,:);% rearrange the points randomly



%DP
N=size(data,1);% # of points
%tag=zeros[N]; % initialization of every point's cluster
nk=[]; % # of points for each cluster
k_sum=[0,0]; % sum of each culster
mean=[0,0];
prob=[];

alpha=0.1;
D=2;% # of dimension of the data
for loop=1:10 % iteration for 100 times
    K=length(nk);
    for n=1:N
        
        point=data(n,[1,2]);
        k_old=data(n,4);
        if k_old>0
            nk(k_old)=nk(k_old)-1;
            k_sum(k_old,:)=k_sum(k_old,:)-data(n,[1,2]);
            
            if nk(k_old)==0 % remove the cluster which has no point
                nk(k_old)=[];
                k_sum(k_old,:)=[];
                mean(k_old,:)=[];
                for i=1:N
                    if data(i,4)>k_old
                        data(i,4)=data(i,4)-1;
                    end
                end
            elseif nk(k_old)<0
                'fuck'
            end
        end % remove the current point from its former cluster
        
        K=length(nk);
        prob=[];
        for k=1:K
            prob(k)=nk(k)/(N-1+alpha)/(2*pi)^(D/2)/exp(0.5*sum((point-mean(k,:)).^2));
        end
        prob(K+1)=alpha*sqrt(0.5)/(N-1+alpha)/(2*pi)^(D/2)/exp(0.25*sum(point.^2));
        K;
        prob;
        k_new=multisampling(prob);
        if k_new==(K+1)% assigned to a new cluster
            nk(k_new)=1;
            k_sum(k_new,:)=data(n,[1,2]);
        else %assigned to an existing cluster
            nk(k_new)=nk(k_new)+1;
            k_sum(k_new,:)=k_sum(k_new,:)+data(n,[1,2]);
        end
        data(n,4)=k_new;
        
        K=length(nk);
        for k=1:K
            k_mu=k_sum(k,:)./nk(k);
            mean(k,1)=normrnd(k_mu(1),1/nk(k),1,1);
            mean(k,2)=normrnd(k_mu(2),1/nk(k),1,1);
        end
    end
    K_count(loop)=K;
end



%evaluation
t=0;
for n=1:N
    if data(n,3)==data(n,4)
        t=t+1;
    end
end
'accuracy = '
t/N
mean
K
nk
%plot graph
figure
scatter(data(:,1),data(:,2),[],data(:,4),'.'),hold on,scatter(mean(:,1),mean(:,2),nk.*7,[1:K]', 'O'), hold off, title('RESULT')
    
        
            
        