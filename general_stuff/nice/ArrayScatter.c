#include<mpi.h>
#include<stdio.h>


int main(int argc, char **argv)
{
	int rank, proc,finalsum=0,total, a[50],local_array[20],result_array[20],i,part,mpi_err,n;


	MPI_Init(&argc,&argv);

	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&proc);

	if(rank==0)
	{
		printf("\n\nPLEASE ENTER THE SIZE OF ARRAY\n");
		scanf("%d", &n);
		if((n%proc)!=0)
		{
			printf("SORRY n SHOULD BE DIVISIBLE BY NUMBER OF PROCESSES\n");
			return(0);
		}
	
		printf("\n\nPLEASE ENTER ARRAY ELEMENTS\n");
		for(i=0;i<n;i++)
			scanf("%d",&a[i]);

	}

	MPI_Bcast(&n,1,MPI_INT,0,MPI_COMM_WORLD);
	 MPI_Barrier(MPI_COMM_WORLD);

	part=n/proc;

	

	mpi_err=MPI_Scatter(a,part,MPI_INT,local_array,part,MPI_INT,0,MPI_COMM_WORLD);
	
	
	total=0;
		
	


	for(i=0;i<part;i++)
		total+=local_array[i];

	printf("\n\nHI IAM PROCESS %d and MY SUM IS %d\n",rank,total);

	 MPI_Barrier(MPI_COMM_WORLD);

	mpi_err=MPI_Gather(&total,1,MPI_INT,result_array,1,MPI_INT,0,MPI_COMM_WORLD);

	if(rank==0)
	{
		for(i=0;i<proc;i++)
			finalsum+=result_array[i];

		printf("\n\nFINAL SUM IS == %d\n",finalsum);

	}
	MPI_Finalize();

}
