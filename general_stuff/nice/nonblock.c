#include<mpi.h>
#include<stdio.h>
#include<stdlib.h>
int main(int argc,char *argv[])
  {
    int numtasks,rank,next,prev,buf_send[2],buf_rcv[2],tag1=1,tag2=2;
    MPI_Request reqs[4];
    MPI_Status stats[2];
    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&numtasks);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    prev=rank-1;
    next=rank+1;
    if(rank==0)
      prev=numtasks-1;
    if(rank==(numtasks-1))
      next=0;
    buf_send[0]=10;
    buf_send[1]=20;
    MPI_Irecv(&buf_rcv[0],1,MPI_INT,prev,tag1,MPI_COMM_WORLD,&reqs[0]);
    MPI_Irecv(&buf_rcv[1],1,MPI_INT,next,tag2,MPI_COMM_WORLD,&reqs[1]);
    MPI_Isend(&buf_send[0],1,MPI_INT,prev,tag2,MPI_COMM_WORLD,&reqs[2]);
    MPI_Isend(&buf_send[1],1,MPI_INT,next,tag1,MPI_COMM_WORLD,&reqs[3]);
    MPI_Waitall(4,reqs,stats);
    printf("Task %d communicated with task %d and %d\n",rank,prev,next);
    MPI_Finalize();
  }
