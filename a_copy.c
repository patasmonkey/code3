#include<stdio.h>
#include<stdlib.h>
int yan(int a){
  if(a==0)return 1;
  return (yan(a-1)+a+1)%2;
}
int main(){
  int i,j,a=0,b[10],c[10],d[10][10],k;
  for(i=0;i<10;i++){
    c[i]=i;
    scanf("%d",&b[i]);
    for(j=1;j<10;j++){
      if(j%2)a+=i+j;
      d[i][j]=d[b[i]][abs(c[j])]+d[i][j-1]+yan(a);
      if(d[i][j]<100)goto p;
      if(d[i][j]<100)break;
      if(d[i][j]<100)return 1;
    }
    for(j=0;j<10;j++){
      for(k=0;k<10;k++){
	c[j]+=b[k];
      }
    }
  }
  p:
  ;
  printf("%d",a);
  return 0;
}
