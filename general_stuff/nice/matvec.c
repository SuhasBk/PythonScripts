#include<stdio.h>
#include<mpi.h>
 int main(int argc,char *argv[])
{
 int a[4][4],b[4],rec_buf[4],gathered_arr[4],size,rank,i,j,sum=0,k,prod;
 MPI_Init(&argc,&argv);
 MPI_Comm_rank(MPI_COMM_WORLD,&rank);
 MPI_Comm_size(MPI_COMM_WORLD,&size);
 if(rank==0)
{
        printf("enter matrix\n");
       	for(i=0;i<4;i++)
	       	for(j=0;j<4;j++)
			scanf("%d",&a[i][j]);
	printf("enter b matrix\n");
	for(i=0;i<4;i++)
		scanf("%d",&b[i]);
}
 MPI_Scatter(&a,4,MPI_INT,rec_buf,4,MPI_INT,0,MPI_COMM_WORLD);
 MPI_Bcast(&b,4,MPI_INT,0,MPI_COMM_WORLD);
 for(i=0;i<size;i++)
{
	printf("my rank=%d,rec_buf=%d\n",rank,rec_buf[i]);
}

 for(i=0;i<size;i++)
{
        printf("my rank=%d,b=%d\n",rank,b[i]);
}

 for(j=0;j<4;j++)
{
	sum=sum+(rec_buf[j]*b[j]);
}

 printf("RANK=%d AND RES=%d\n",rank,sum);
 MPI_Gather(&sum,1,MPI_INT,gathered_arr,1,MPI_INT,0,MPI_COMM_WORLD);
 if(rank==0)
{
 for(i=0;i<4;i++)
 printf("%d\t",gathered_arr[i]);
}
			
 MPI_Finalize();
}

