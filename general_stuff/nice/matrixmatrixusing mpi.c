#include<stdio.h>
#include<mpi.h>
#define SIZE 4

int A[SIZE][SIZE],B[SIZE][SIZE],AR[SIZE][SIZE],C[SIZE][SIZE],CR[SIZE][SIZE],n;

void fill_matrix(int m[SIZE][SIZE])
{
	static int n=0;
	int i,j;
	
	for(i=0;i<SIZE;i++)
	for(j=0;j<SIZE;j++)
	scanf("%d",&m[i][j]);
}

void print_matrix(int m[SIZE][SIZE])
{
	int i,j=0;
	for(i=0;i<SIZE;i++)
	{
		printf("\n\t| ");
		for(j=0;j<SIZE;j++)
		printf("%2d\t",m[i][j]);
		printf("|");
	}
}


int main(int argc,char *argv[])
{
	int myrank,p,from,to,i,j,k;
	int  tag=666;
	MPI_Status status;
	
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
	MPI_Comm_size(MPI_COMM_WORLD,&p);
	{
		if(n%p!=0)
		{
			if(myrank==0)
			printf("matrix size not divisible by number of processors\n");
			MPI_Finalize();
			exit(-1);
		}

	from=myrank*SIZE/p;
	to=(myrank+1)*SIZE/p;

	if(myrank==0)
	{
		
		printf("PLEASE ENTER FIRST MATRIX OF SIZE 4*4\n");
		fill_matrix(A);
		printf("PLEASE ENTER SECOND MATRIX OF SIZE 4*4\n");
		fill_matrix(B);
	}

	MPI_Bcast(B,SIZE*SIZE,MPI_INT,0,MPI_COMM_WORLD);
	MPI_Scatter(A,SIZE*SIZE/p,MPI_INT,AR[from],SIZE*SIZE/p,MPI_INT,0,MPI_COMM_WORLD);

	printf("computing slice %d (from row %d to %d)\n",myrank,from,to-1);
	for(i=from;i<to;i++)
	for(j=0;j<SIZE;j++)
	{
		C[i][j]=0;
		for(k=0;k<SIZE;k++)
		C[i][j]+=AR[i][k]*B[k][j];
	}

	MPI_Gather(C[from],SIZE*SIZE/p,MPI_INT,CR,SIZE*SIZE/p,MPI_INT,0,MPI_COMM_WORLD);
	
	if(myrank==0)
	{
		printf("\n\n");
		print_matrix(A);
		printf("\n\n\t      *\n");
		print_matrix(B);
		printf("\n\n\t      =\n");
		print_matrix(CR);
		printf("\t\n\n");
	}
	MPI_Finalize();
	return 0;
}
}

		



