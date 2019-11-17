#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
typedef long long ABC;
int main(int argc,char* argv[])
{
	int myrank=0,numproc,i,n=0,first,last;
	ABC prod=1,root=0,result=1;
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
	MPI_Comm_size(MPI_COMM_WORLD,&numproc);
	if(myrank==root)
	{
		printf("enter the value of n:\n");
		scanf("%d",&n);
	}
	MPI_Bcast(&n,1,MPI_LONG_LONG,root,MPI_COMM_WORLD);
	first=(myrank*n)/numproc;
	last=((myrank+1)*n)/numproc;
	for(i=first+1;i<=last;i++)
		prod*=i;
	MPI_Reduce(&prod,&result,1,MPI_LONG_LONG,MPI_PROD,root,MPI_COMM_WORLD);
	if(myrank==root)
		printf("factorial od %d is %d",n,result);
	MPI_Finalize();
}
	
