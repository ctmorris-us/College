#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>


int main(int argc, char** argv) {
 	
	FILE *fp;
	char ch, pastch ;
	
	int sizeList = 0;
	int channel = 0;
	int endList = 0;
	int validList = 1;
	int num7 = 0;
	int numF = 0;
	
	if (argc == 2) {
		fp = fopen(argv[1], "r");	
	}
	else if (argc == 1) {
		fp = stdin;
	}
	else {
		printf("Not valid Input\n");
	}
	if(fp ==  NULL) {
  			printf("File not found. \n");
	}
  	else {
		while(1) {

			ch = fgetc(fp);
			
			if (ch == EOF) {
				break;
			}
			else if (ch == '\n') {
				endList = 1;			
			}

			sizeList = sizeList + 1;
			
			if (sizeList == 1) {
					channel = 0;
				if (ch == 'E') {
					channel = 1;				
				}
				else if (ch == 'P') {
					channel = 2;
				}
				else if (ch == 'Q') {
					channel = 3;
				}
				else if (ch == 'M') {
					channel = 4;
				}
				else {
					validList = 0;
				}
				printf("%c", ch);
				continue;
			}

			if (channel == 1) {
				if (ch == 'F') {
					numF = numF + 1;
				}

				if ( endList == 0) {
					if ( (ch != '0') && (ch != '1') && (ch != '2') && (ch != 'F')) {
						validList = 0;
					}
				}
				else {
					if ( numF != 1 ) {
						validList = 0;
					}
				}
			}

			if ((endList == 0) && (channel == 2)) {
				if ((ch != 'B') && (ch != 'C' )) {   
					validList = 0;
				}
			}

			if (channel == 3) {
				if ((endList == 0) && (ch != '6') && (ch != '7')) {
					validList = 0;
				}
				if ( ch == '7') {
					num7 = num7 + 1;
				}
				if (( endList == 1) && (num7%2 == 0)) {
					validList = 0;
				}
			}
				
			if (channel == 4){
				if ((endList == 0) &&( isdigit(ch) == 0 ) && (sizeList != 4)){
					validList = 0;
				}
				if ((endList == 0) && (sizeList == 4) && (validList == 1)) {
					if (ch == 'E') {
						channel = 1;				
					}
					else if (ch == 'P') {
						channel = 2;
					}
				}
				if ((endList == 1) && (sizeList <= 4)) {
					validList = 0;
				}
			}	
			
			pastch = ch;
			if (ch != '\n') {
				printf("%c", ch);
			}
			if (endList == 1) {
				if (validList == 1) {
					printf(" OK");
				}
				else {
					printf(" Fail");
				}
				printf("\n");

				sizeList = 0;
				endList = 0;
				validList = 1;
				num7 = 0;
				numF = 0;
				channel = 0;

			}
		}
		if (argc == 2) {
			fclose(fp);	
		}
	}
	return 0;
}

