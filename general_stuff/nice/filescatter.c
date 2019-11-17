#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
int tot,err;
static int n=0,m=0;

int main(int nargs,char *args[])
{
int size,rank,count,i,j,np;
int *send=0;
FILE *fp;
MPI_Init(&nargs,&args);
MPI_Comm_size(MPI_COMM_WORLD,&size);
MPI_Comm_rank(MPI_COMM_WORLD,&rank);
fp=fopen("file.txt","r");
char read,rc;
send=(int *)malloc(m*size*sizeof(int));

while((rc=fgetc(fp))!=EOF)
{ if(rc=='\n')
 n++;
}

fclose(fp);
fp=fopen("file.txt","r");

if(size>n)
{ if(rank==0)

size=n;
}

m=n/size;

int k=0;

for(j=0;j<size;j++)
{ int x=m;

while(x>0)
{ count=0;
while((read=fgetc(fp))!='\n')
{
 if(read==' '||read=='\t')
count++;
}

count++;
send[k]=count;
k++;
x--;
}}

err=MPI_Scatter(&send,1,MPI_INT,&tot,1,MPI_INT,0,MPI_COMM_WORLD);
err=MPI_Gather(&tot,1,MPI_INT,&send,1,MPI_INT,0,MPI_COMM_WORLD);
printf("\n");

if(rank==0)
{ tot=0;
printf("File: file.txt\n");
printf("File has %d lines \n Here each Process reads %d lines \n",n,m);

for(i=0;i<(size*m);i++)
{ printf("No of words in line is %d is %d \n",i+1,send[i]);
tot=tot+send[i];
}

printf("Total words %d \n",tot);
}
fclose(fp);
MPI_Finalize();
return 0;
}





