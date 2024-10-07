// This is a short brainf[ric]k interpreter without input ("," operator)
// it can be tested here: https://code.golf/brainfuck#cpp
#include <cstdio>
#define u(n) (p[f][r]==n)
int f;
int main(int w,char**p){
    for(;++f<w;){
	int m[999]{},r=0,t=0,j,k;
	while(!u(0)){
	    u(46)?putchar(m[t]):0;
	    t+=u(62)-u(60);
	    m[t]+=u(43)-u(45);
	    j=(u(91)&!m[t])-(u(93)&&m[t]);
	    r+=k=u(91)-u(93);
	    for(;j;)j+=u(91),j-=u(93),r+=k;
	    r+=1-k;
	}
    }
}
