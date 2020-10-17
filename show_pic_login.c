#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>

typedef struct BGR_S {
    unsigned char B;
    unsigned char G;
    unsigned char R;
}BGR;

int load_pic(unsigned int *width, unsigned int *height, BGR **stream, char *pic_file_name) {
    FILE *pic_file = NULL;
    unsigned int size;
    unsigned int offset;
    unsigned int sup;
    unsigned int i;

    pic_file = fopen(pic_file_name, "rb");
    if (pic_file == NULL) {
        printf("open file failed !\n");
        return 0;
    }

    fseek(pic_file, 2, SEEK_SET);
    fread(&size, sizeof(unsigned int), 1, pic_file);
    printf("%-15s%u\n", "file size:", size);

    fseek(pic_file, 10, SEEK_SET);
    fread(&offset, sizeof(unsigned int), 1, pic_file);
    printf("%-15s%u\n", "offset:", offset);

    fseek(pic_file, 18, SEEK_SET);
    fread(width, sizeof(unsigned int), 1, pic_file);
    printf("%-15s%u\n", "width:", *width);

    fseek(pic_file, 22, SEEK_SET);
    fread(height, sizeof(unsigned int), 1, pic_file);
    printf("%-15s%u\n", "height:", *height);

    *stream = (BGR *)malloc(*width * *height * 3);
    if (*stream == NULL) {
            printf("malloc error !");
            return 0;
    }

    sup = (4 - ((*width * 3) % 4)) % 4; // 填充长度
    printf("%-15s%u\n", "sup:", sup);

    for (i = 0; i < *height; i++) {
        fseek(pic_file, offset, SEEK_SET);
        fread((*stream + *width * i), (*width) * sizeof(BGR), 1, pic_file);
        offset += *width * 3 + sup;
    }
    fclose(pic_file);

    return 1;
}

int e2b(unsigned char in) {
    return in>127?1:0;
}

void print_color(FILE *motd, BGR bgr_f, BGR bgr_b) {
    int color_f, color_b;
    color_f = 30 + e2b(bgr_f.B) * 4 + e2b(bgr_f.G) * 2 + e2b(bgr_f.R);
    color_b = 40 + e2b(bgr_b.B) * 4 + e2b(bgr_b.G) * 2 + e2b(bgr_b.R);
    fprintf(motd, "%c[%d;%dm▀", 0x1B, color_f, color_b);
    return;
}

int main (int argc, char *argv[]) {
    char *pic_file_name = NULL;
    unsigned int width;
    unsigned int height;
    BGR *stream;
    BGR BLACK = {0, 0, 0};
    struct winsize ws;
    unsigned int shell_width;
    unsigned int loop_width;
    double ratio;
    int i, j;

    char *motd_filename = "/etc/motd";
    FILE *motd;

    switch (argc) {
    case 1:
        printf("Useage: %s XXX.bmp\n", argv[0]);
        return 0;
    case 2:
        pic_file_name = (char *)malloc(strlen(argv[1]) + 1);
        pic_file_name = argv[1];
        break;
    default:
        printf("Useage: %s XXX.bmp\n", argv[0]);
        return 0;
    }

    motd = fopen(motd_filename, "wb, ccs=UTF-8");
    if (motd == NULL) {
        printf("%-15s%s\n", "open motd failed !:");
        return -1;
    }

    printf("%-15s%s\n", "pic file:", pic_file_name);

    if (load_pic(&width, &height, &stream, pic_file_name) == 0) {
        printf("load pic fialed !\n");
        return -1;
    }

    ioctl(0, TIOCGWINSZ, &ws);
    shell_width = ws.ws_col;
    shell_width = 100;
    printf("%-15s%u\n", "shell width:", shell_width);

    ratio = (double)width / shell_width;
    loop_width = shell_width;

    printf("%-15s%lf\n", "ratio:", ratio);
    printf("%-15s%u\n", "loop width:", loop_width);

    for (i = 0; i < height; i += (unsigned int)(2 * ratio + 0.5)) {
        for (j = 0; j < loop_width; j++) {
            if (i + (unsigned int)(ratio + 0.25) >= height){
                print_color(motd, stream[width * (height - i - 1) + (unsigned int)(j * ratio)], BLACK);   
                continue;
            }
            print_color(motd, stream[width * (height - i - 1) + (unsigned int)(j * ratio)], stream[width * (height - i - (unsigned int)(ratio + 0.25) - 1) + (unsigned int)(j * ratio)]);   
        }
        fprintf(motd, "%c[39;49m\n", 0x1B);
    }

    fclose(motd);
    return 0;
}
