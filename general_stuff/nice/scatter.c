#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
int numnodes,myid,mpi_err;
#define mpi_root 0
 void init_it(int *argc,char **argv)
 {	
   mpi_err = mpi_init(argc,argv);	
   mpi_err = MPI_Comm_size(MPI_COMM_WORLD, &numnodes);	
   mpi_err = MPI_Comm_rank(MPI_COMM_WORLD, &myid);
 }
int main(int argc, char *argv[])
 {	
   int *myray, *send_ray, *back_ray;	
   int count;	
   int size, mysize, i, k,j, total;	
   init_it(&argc,&argv);	
   count = 4;	
   myray = (int*)malloc(count * sizeof(int));		
   if(myid == mpi_root)	
    {		
      size = count * numnodes;		
      send_ray = (int*)malloc(size * sizeof(int));		
      back_ray = (int*)malloc(numnodes * sizeof(int));
          for(i = 0 ; i < size ; i++)		
            { 			
              send_ray[i] = i;			
              printf("send_ray = %d\n",send_ray[i]);		
            }	
     }	
   mpi_err = MPI_Scatter(send_ray,count,MPI_INT,myray,count,MPI_INT,mpi_root,MPI_COMM_WORLD);	
   total = 0;	
   for(i = 0 ; i < count ; i++)	
     {		
       total = total + myray[i];		
       printf("myray = %d\n",myray[i]);	
     }
  printf("myid = %d  total = %d\n",myid,total);	
  mpi_err = MPI_Gather(&total,1,MPI_INT,back_ray,1,MPI_INT,mpi_root,MPI_COMM_WORLD);	
   if(myid == mpi_root)	
     {		
         total = 0;				
         for(i =0; i < numnodes ; i++)			
         total = total + back_ray[i];		
         printf("results from all processors = %d\n",total);	
     } 	
   mpi_err = MPI_Finalize();
 }

