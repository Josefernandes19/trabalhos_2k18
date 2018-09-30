#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define COLUNAS 1024

int menu(){
    int escolha;
    printf("------ M E N U  D E  O P Ç Õ E S ------\n");
    printf("1 - Passa Alta\n");
    printf("2 - Passa Baixa\n");
    printf("3 - Sobel\n");
    printf("4 - Prewitt\n");
    printf("5 - Roberts\n");
    printf("6 - Isotrópico\n");
    printf("7 - Sair\n");
    printf("Escolha uma das opções acima, digitando seu numero: ");
    fflush(stdout);
    scanf("%d", &escolha);
    printf("\n");
    return escolha;
}

int verificamax(int var){
  if (var > 255){
    var=255;
  }
  return var;
}

int verificamin(int var){
  if (var < 0){
    var=0;
  }
  return var;
}

double verificadoublemax(double var){
  if (var > 255){
    var=255;
  }
  return var;
}

double verificadoublemin(double var){
  if (var < 0){
    var=0;
  }
  return var;
}

int gradiente(int var1, int var2){
  return sqrt((var1*var1)+(var2*var2));
}

int gradientedouble(double var1, double var2){
  return sqrt((var1*var1)+(var2*var2));
}

void salvararq(int imagem[][COLUNAS], int li, int cl){
    FILE *arqueevo;
    char nome[40];
    int i, j;
    printf("Digite o nome do arquivo e a extensão desejada, sem espaçamento. (Exemplo: arquivo.pgm): ");
    scanf("%s", &nome);
    arqueevo = fopen(nome, "w");
    if (arqueevo == NULL)
    {
        printf("Erro ao abrir ou criar o arquivo!\n");
    }
    else
    {
       fprintf(arqueevo, "P2\r\n# 'Aqui cabe um comentário.' \r\n%d %d\r\n255\r\n", cl, li);
        for(i = 0; i < li; i++)
        {
            for(j = 0; j < cl; j++)
            {
                fprintf(arqueevo, "%d ", imagem[i][j]);
            }
            fprintf(arqueevo, "\r\n");
        }
    }
    fclose(arqueevo);
}

void passaalta(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
    int i, j, valor, w, q;
    int linha = 0;
    int coluna = 0;
    int mask[3][3] = {{-1,-1,-1},{-1,8,-1},{-1,-1,-1}};
    for (i = 1; i < (li-1); i++){
        for (j = 1; j < (co-1); j++){
          valor = 0;
            for(q=(i-1); q<=(i+1); q++){
                for(w=(j-1); w<=(j+1); w++){
                  valor = valor+(mask[linha][coluna]*imagem[q][w]);
                  coluna++;
                }
                linha++;
                coluna=0;
            }//testando valores acima do maximo de um PGM
            if (valor > 255){
              valor=255;
            }//testando valores abaixo do minimo de um PGM
            if(valor < 0){
              valor=0;
            }
            aux[i][j] = valor;
            linha=0;
            coluna=0;
        }
        linha=0;
        coluna=0;
    }
    salvararq(aux, li, co);
}

void passabaixa(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
  int i, j, valor, w, q;
  for (i = 1; i < (li-1); i++){
      for (j = 1; j < (co-1); j++){
          valor = 0;
          for(q=(i-1); q<=(i+1); q++){
              for(w=(j-1); w<=(j+1); w++){
                valor = valor+imagem[q][w];
              }
          }
          aux[i][j] = valor/9;
      }
  }
  salvararq(aux, li, co);
}

void sobel(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
  int i, j, valor, w, q, valor1, valor2;
  int linha = 0;
  int coluna = 0;
  int mask1[3][3] = {{-1,0,1},{-2,0,2},{-1,0,1}};
  int mask2[3][3] = {{-1,-2,-1},{0,0,0},{1,2,1}};
  for (i = 1; i < (li-1); i++){
      for (j = 1; j < (co-1); j++){
        valor1=0;
        valor2=0;
          for(q=(i-1); q<=(i+1); q++){
              for(w=(j-1); w<=(j+1); w++){
                valor1 = valor1+(mask1[linha][coluna]*imagem[q][w]);
                valor2 = valor2+(mask2[linha][coluna]*imagem[q][w]);
                coluna++;
              }
              linha++;
              coluna=0;
          }
          valor1 = verificamax(valor1);
          valor1 = verificamin(valor1);
          valor2 = verificamax(valor2);
          valor2 = verificamin(valor2);
          aux[i][j] = gradiente(valor1, valor2);
          linha=0;
          coluna=0;
      }
      linha=0;
      coluna=0;
  }
  salvararq(aux, li, co);
}

void prewitt(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
  int i, j, valor, w, q, valor1, valor2;
  int linha = 0;
  int coluna = 0;
  int mask1[3][3] = {{-1,-1,-1},{0,0,0},{1,1,1}};
  int mask2[3][3] = {{-1,0,1},{-1,0,1},{-1,0,1}};
  for (i = 1; i < (li-1); i++){
      for (j = 1; j < (co-1); j++){
        valor1=0;
        valor2=0;
          for(q=(i-1); q<=(i+1); q++){
              for(w=(j-1); w<=(j+1); w++){
                valor1 = valor1+(mask1[linha][coluna]*imagem[q][w]);
                valor2 = valor2+(mask2[linha][coluna]*imagem[q][w]);
                coluna++;
              }
              linha++;
              coluna=0;
          }
          valor1 = verificamax(valor1);
          valor1 = verificamin(valor1);
          valor2 = verificamax(valor2);
          valor2 = verificamin(valor2);
          aux[i][j] = gradiente(valor1, valor2);
          linha=0;
          coluna=0;
      }
      linha=0;
      coluna=0;
  }
  salvararq(aux, li, co);
}

void roberts(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
  int i, j, valor, w, q, valor1, valor2;
  int linha = 0;
  int coluna = 0;
  int mask1[2][2] = {{-1,0},{0,1}};
  int mask2[2][2] = {{0,-1},{1,0}};
  for (i = 1; i < (li-1); i++){
      for (j = 1; j < (co-1); j++){
        valor1=0;
        valor2=0;
          for(q=(i-1); q<=i; q++){
              for(w=(j-1); w<=j; w++){
                valor1 = valor1+(mask1[linha][coluna]*imagem[q][w]);
                valor2 = valor2+(mask2[linha][coluna]*imagem[q][w]);
                coluna++;
              }
              linha++;
              coluna=0;
          }
          valor1 = verificamax(valor1);
          valor1 = verificamin(valor1);
          valor2 = verificamax(valor2);
          valor2 = verificamin(valor2);
          aux[i][j] = gradiente(valor1, valor2);
          linha=0;
          coluna=0;
      }
      linha=0;
      coluna=0;
  }
  salvararq(aux, li, co);
}

void isotropico(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co){
  int i, j, valor, w, q;
  double valor1, valor2;
  int linha = 0;
  int coluna = 0;
  double mask1[3][3] = {{-1,0,1},{-1.4142,0,1.4142},{-1,0,1}};
  double mask2[3][3] = {{-1,-1.4142,-1},{0,0,0},{1,1.4142,1}};
  for (i = 1; i < (li-1); i++){
      for (j = 1; j < (co-1); j++){
        valor1=0;
        valor2=0;
          for(q=(i-1); q<=(i+1); q++){
              for(w=(j-1); w<=(j+1); w++){
                valor1 = valor1+(mask1[linha][coluna]*imagem[q][w]);
                valor2 = valor2+(mask2[linha][coluna]*imagem[q][w]);
                coluna++;
              }
              linha++;
              coluna=0;
          }
          valor1 = verificadoublemax(valor1);
          valor1 = verificadoublemin(valor1);
          valor2 = verificadoublemax(valor2);
          valor2 = verificadoublemin(valor2);
          aux[i][j] = gradientedouble(valor1, valor2);
          linha=0;
          coluna=0;
      }
      linha=0;
      coluna=0;
  }
  salvararq(aux, li, co);
}

void sair(){
    exit(0);
}

void sac(int imagem[][COLUNAS], int aux[][COLUNAS], int li, int co, int escolha){
    int escinv, esccor;
    switch (escolha){
        case 1:
            passaalta(imagem, aux, li, co);
        break;
        case 2:
            passabaixa(imagem, aux, li, co);
        break;
        case 3:
            sobel(imagem, aux, li, co);
        break;
        case 4:
            prewitt(imagem, aux, li, co);
        break;
        case 5:
            roberts(imagem, aux, li, co);
        break;
        case 6:
            isotropico(imagem, aux, li, co);
        break;
        case 7:
            sair();
        break;
    }
}

int main() {
    FILE *imagem;
    int escolha, li, co, buffer3, i, j;
    static int imageM[1024][1024], aux[1024][1024];
    char buffer[200], buffer2 = 'i', check[10];
    imagem = fopen("imagemO.pgm", "r");
    if (imagem == NULL)
    {
        printf("Erro ao abrir a imagem!\n");
    }
    else
    {
        printf("Imagem aberta com sucesso!\n");
        //le o P2
        fscanf(imagem, "%s", &check);
        strcpy(buffer, "P2");
        if(strcmp (check, buffer) == 0)
        {
            fscanf(imagem, "%s", buffer);
            fgets(buffer, 150, imagem);
            fscanf(imagem, "%d %d", &co, &li);
            fscanf(imagem, "%s", &buffer);
            for(i = 0; i < li; i++)
            {
                for (j = 0; j < co; j++)
                {
                    fscanf(imagem, "%d", &buffer3);
                    imageM[i][j] = buffer3;
                    aux[i][j] = 255;
                }
            }
            while(1)
            {
            escolha = menu();
            sac(imageM, aux, li, co, escolha);
            }
        }
        else
        {
            printf("Formato incorreto de imagem!");
        }
    }
    return 0;
}
