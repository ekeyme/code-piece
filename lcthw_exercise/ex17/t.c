#include <stdio.h>

struct Packet
{
    short PacketSize;
    short Type;
};

struct SizeValidity
{
    short SizeEnc;
};

struct SendEncSecureCode
{
    struct Packet header;
    short EncSecurityToken;
    int lTime;
    struct SizeValidity ending;
};

int main(int argc, const char *argv[])
{
	struct SendEncSecureCode sendpacket;
	sendpacket.header.PacketSize = sizeof(struct SendEncSecureCode);
	printf("%d\n", sendpacket.header.PacketSize);
	return 0;
}
