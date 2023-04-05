/**
 * @file final_lexical.c
 * @author group 14
 * @brief lexical analyzer for c language
 * @version 0.1
 * @date 2023-03-29
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include<stdio.h>
#include<ctype.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>

#define MAX 100

char keywords[8][10]={"char","do","else","float","for","if","int","while"};
char operators[14][3]={"++","--","==","!=","&&","||","<=","=>","<",">","=","+","-","*"};
char delimiters[9][3]={";","(",")","{","}","[","]",",","."};
char special[1][2]={"#"};

char identifier[MAX][MAX];
char constant[MAX][MAX];
char string[MAX][MAX];
char character[MAX][MAX];
char operator[MAX][MAX];
char delimiter[MAX][MAX];

int i;

int check_keyword(char s[]){
    int i;
    for(i=0;i<8;i++)
        if(strcmp(keywords[i],s)==0)
            return 1;
    return 0;
}

int check_operator(char s[]){
    int i;
    for(i=0;i<14;i++)
        if(strcmp(operators[i],s)==0)
            return 1;
    return 0;
}

int check_delimiter(char s[]){
    int i;
    for(i=0;i<9;i++)
        if(strcmp(delimiters[i],s)==0)
            return 1;
    return 0;
}

int check_special(char s[]){
    int i;
    for(i=0;i<5;i++)
        if(strcmp(special[i],s)==0)
            return 1;
    return 0;
}

void lexical_analyzer(){
    int i=0,j=0,k=0,l=0,m=0,n=0,o=0,p=0,q=0;
    char ch;
    FILE *fp;
    fp=fopen("input.txt","r");
    if(fp==NULL){
        printf("File not found");
        exit(0);
    }
    while((ch=fgetc(fp))!=EOF){ //while not end of file
        
       character[i][0]=ch; 


       if(isalpha(ch)){ //if character is alphabet
            j=0; 
            while(isalnum(ch)){ 
                identifier[k][j]=ch; 
                j++; 
                ch=fgetc(fp); 
            }
            identifier[k][j]='\0'; 
            if(check_keyword(identifier[k])==1){
                printf("keyword: %s\n",identifier[k]);
            } 
            else{
                printf("identifier: %s\n",identifier[k]);
            } 

        } 
         //if character is operator
        else if(ch=='!' || ch=='&' || ch=='|' || ch=='<' || ch=='>' || ch=='+' || ch=='-' || ch=='*' || ch=='/' || ch=='%' || ch=='='){
            j=0; 
            while(ch=='!' || ch=='&' || ch=='|' || ch=='<' || ch=='>'|| ch=='+' || ch=='-' || ch=='*' || ch=='/' || ch=='%' || ch=='='){
                operator[k][j]=ch; 
                j++; 
                ch=fgetc(fp);
            }
            operator[k][j]='\0'; 
            printf("operator: %s\n",operator[k]);
        }
        
        //if character is integer
        else if(isdigit(ch)){
            j=0; 
            while(isdigit(ch)){ 
                constant[k][j]=ch; 
                j++; 
                ch=fgetc(fp); 
            }
            //if character is float
            if(ch=='.'){
                constant[k][j]=ch; 
                j++; 
                ch=fgetc(fp); 
                while(isdigit(ch)){ 
                    constant[k][j]=ch; 
                    j++; 
                    ch=fgetc(fp); 
                }
                constant[k][j]='\0'; 
                printf("float: %s\n",constant[k]);
            }else{
                constant[k][j]='\0'; 
                printf("integer: %s\n",constant[k]);}
            
           
        }

     

        //if character is string
        else if(ch=='"'){
            j=0; 
            ch=fgetc(fp); 
            while(ch!='"'){ 
                string[k][j]=ch;                
                j++; 
                ch=fgetc(fp); 
            }
            string[k][j]='\0'; 
            printf("string: %s\n",string[k]);
        }

        //if character is special character
        else if(check_special(character[0])==1){
            k=0,j=0; 
            special[k][j]=ch;
            j++;
             
            printf("special character: %s\n",special[k]);
        }


       
        //if character is delimiter
        else if(check_delimiter(character[0])==1){
            j=0; 
            delimiter[k][j]=ch;
            j++;
            delimiter[k][j]='\0'; 
            printf("delimiter: %s\n",delimiter[k]);
        }

        //if character is space or tab
        else if(ch==' '||ch=='\t'){
            //do nothing
        }
    } 
}

int main(){
    
    lexical_analyzer();
    return 0;
}
