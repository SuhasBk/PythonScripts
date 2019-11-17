#include <stdio.h>
#include <stdlib.h>
#include<mpi.h>

int account1[50];

void insert_sorted (long *sorted, int count, long value, int account)
{
int i = 0;
account1[count]=account;
sorted[count] = value;
if (count == 0) return;
for (i = count;i >= 0; i--) {
if (value > sorted[i-1])
{
sorted[i] = sorted[i-1];
account1[i]=account1[i-1];
}
else break;
}
sorted[i] = value;
account1[i]=account;
}


int main (int nargs, char *args[])
{
int temp[10],size, rank,gath_buf[10];
FILE *infile = NULL;
int acc_no,loan;
long sorted[1024];
long value;
int count = 0;
int err,tot,i = 0;
MPI_Init(&nargs, &args);
MPI_Comm_size(MPI_COMM_WORLD, &size);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

infile = fopen ("bank.txt", "r");
if (NULL == infile) {
perror ("fopen");
return -1;
}
err = MPI_Scatter(&infile,1,MPI_INT,&tot,1,MPI_INT,0,MPI_COMM_WORLD);

while (!feof (infile)) {
fscanf (infile, "%d %d\n",&acc_no,&loan); 
insert_sorted (sorted, count, loan,acc_no); 
++count; 
}

for(i=0;i<count;i++){
temp[i]=sorted[i];
}

//err=MPI_Gather(&temp,1,MPI_INT,&gath_buf,1,MPI_INT,0,MPI_COMM_WORLD);
if (rank==0){
for(i=0;i<count;i++){
printf("result from all processors is Amount:%d  Account no.: %d   \n",sorted[i],account1[i]);
}}

if (infile) {
fclose (infile);
infile = NULL;
}
MPI_Finalize();
return 0;
} 
