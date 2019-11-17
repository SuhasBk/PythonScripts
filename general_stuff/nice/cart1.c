#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

#define mpi_root 0

int main(int argc,char *argv[])
{
	int hdims=2,a,dims[2];
	dims[0]=2;
	dims[1]=4;	
	int period[2]={0,0},rank,proc,coord[2],rank2,i,j;
	
	MPI_Init(&argc,&argv);
	MPI_Comm newcomm;
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&proc);
	MPI_Cart_create(MPI_COMM_WORLD,hdims,dims,period,0,&newcomm);

	if(rank==mpi_root)
	{
		printf("Enter rank:\n");
		scanf("%d",&a);
		MPI_Cart_coords(newcomm,a,hdims,coord);
		printf("coordinates are:%d%d\n",coord[0],coord[1]);
		printf("Enter the coordinates:\n");
		scanf("%d%d",&coord[0],&coord[1]);
		MPI_Cart_rank(newcomm,coord,&rank2);
		printf("rank %d",rank2);
	}

	MPI_Finalize();
}




