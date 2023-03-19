#include<stdio.h>
#include<cmath>
using namespace std;


int main(){
	int n = 1000;
	int check[1001] = { false };

	check[0] = check[1] = true;
	for (int i = 2; i < sqrt(1000); i++){
		if (check[i] == false){
			for (int j = i + i; j <= 1000; j += i){
				check[j] = true;
			}
		}
	}

	for (int i = 1; i <= n; i++){
		if (!check[i]) printf("%d ", i);
	}
	


	return 0;
}
