#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <port> <file>\n", argv[0]);
        return 1;
    }

    int port = atoi(argv[1]);
    char *file = argv[2];

    // 打开文件
    int fd = open(file, O_RDWR | O_CREAT | O_APPEND, 0666);
    if (fd < 0) {
        perror("Failed to open file");
        return 1;
    }

    // 创建 UDP socket
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Failed to create socket");
        return 1;
    }

    // 绑定端口
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Failed to bind socket");
        return 1;
    }

    // 接收并写入数据
    char buffer[BUFFER_SIZE];
    struct sockaddr_in client_addr;
    socklen_t client_addr_len = sizeof(client_addr);

    while (1) {
        ssize_t num_bytes = recvfrom(sockfd, buffer, sizeof(buffer)-1, 0,
                                     (struct sockaddr *)&client_addr, &client_addr_len);
        if (num_bytes < 0) {
            perror("Failed to receive data");
            return 1;
        }

        // 写入数据到文件
        ssize_t bytes_written = write(fd, buffer, num_bytes);
        if (bytes_written < 0) {
            perror("Failed to write to file");
            return 1;
        }
    }

    // 关闭文件和 socket
    close(fd);
    close(sockfd);

    return 0;
}