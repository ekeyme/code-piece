#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

struct Address{
	int id;
	int set;
	char *name;
	char *email;
};

struct Database{
	int MAX_DATA;
	int MAX_ROWS;
	struct Address **rows;
};

struct Connection{
	FILE *file;
	struct Database *db;
};


void Database_close(struct Connection *conn);


void die(const char *message, struct Connection *conn)
{
	if (errno){
		perror(message);
	}else{
		printf("ERROR: %s\n", message);
	}
	Database_close(conn);

	exit(1);
}

void Address_print(struct Address *addr)
{
	printf("%d %s %s\n", 
		addr->id, addr->name, addr->email);
}

void fwrite_and_die(void *prt, size_t size, int num, FILE *f, struct Connection *conn)
{
	int rc = fwrite(prt, size, num, f);
	if (rc != num) die("Failed to write database.", conn);
}

void fread_and_die(void *prt, size_t size, int num, FILE *f, struct Connection *conn)
{
	int rc = fread(prt, size, num, f);
	if (rc != num) die("Failed to load database.", conn);
}

void *malloc_and_die(size_t size, struct Connection *conn)
{
	void *prt = malloc(size);
	if (!prt) die("Memory error", conn);
	return prt;
}

void Database_write(struct Connection *conn)
{
	rewind(conn->file);

	// save MAX_DATA
	fwrite_and_die(&conn->db->MAX_DATA, sizeof(conn->db->MAX_DATA), 1, conn->file, conn);

	// save MAX_ROWS
	fwrite_and_die(&conn->db->MAX_ROWS, sizeof(conn->db->MAX_ROWS), 1, conn->file, conn);

	// save Address
	int i = 0;
	struct Address *addr;
	for (i = 0; i < conn->db->MAX_ROWS; i++){
		addr = conn->db->rows[i];
		fwrite_and_die(&addr->id, sizeof(addr->id), 1, conn->file, conn);
		fwrite_and_die(&addr->set, sizeof(addr->set), 1, conn->file, conn);
		fwrite_and_die(addr->name, conn->db->MAX_DATA+1, 1, conn->file, conn);
		fwrite_and_die(addr->email, conn->db->MAX_DATA+1, 1, conn->file, conn);
	}

	int rc = fflush(conn->file);
	if (rc == -1) die("Cannot flush database.", conn);
}

void Database_load(struct Connection *conn)
{
	// retrieve MAX_DATA
	fread_and_die(&conn->db->MAX_DATA, sizeof(conn->db->MAX_DATA), 1, conn->file, conn);

	// retrieve MAX_ROWS
	fread_and_die(&conn->db->MAX_ROWS, sizeof(conn->db->MAX_ROWS), 1, conn->file, conn);

	// retrieve addresses
	conn->db->rows = malloc_and_die(sizeof(conn->db->rows)*conn->db->MAX_ROWS, conn);
	struct Address *addr = NULL;
	int i = 0;
	int len = conn->db->MAX_DATA+1;
	for (i = 0; i < conn->db->MAX_ROWS; i++){
		addr = conn->db->rows[i] = malloc_and_die(sizeof(struct Address), conn);
		addr->name = malloc_and_die(len, conn);
		addr->email = malloc_and_die(len, conn);
		fread_and_die(&addr->id, sizeof(addr->id), 1, conn->file, conn);
		fread_and_die(&addr->set, sizeof(addr->set), 1, conn->file, conn);
		fread_and_die(addr->name, len, 1, conn->file, conn);
		fread_and_die(addr->email, len, 1, conn->file, conn);
	}
}

struct Connection *Database_open(const char *filename, char mode)
{
	struct Connection *conn = malloc_and_die(sizeof(struct Connection), NULL);

	conn->db = malloc_and_die(sizeof(struct Database), conn);

	if (mode == 'c'){
		conn->file = fopen(filename, "w");
	}else{
		conn->file = fopen(filename, "r+");

		if (conn->file){
			Database_load(conn);
		}
	}

	if (!conn->file) die("Failed to open the file", conn);

	return conn;
}

void Database_close(struct Connection *conn)
{
	if (conn){
		if (conn->file) fclose(conn->file);
		if (conn->db){
			if (conn->db->rows){
				int i = 0;
				for (i = 0; i < conn->db->MAX_ROWS; i++){
					if (conn->db->rows[i]){
						if (conn->db->rows[i]->name) free(conn->db->rows[i]->name);
						if (conn->db->rows[i]->email) free(conn->db->rows[i]->email);
						free(conn->db->rows[i]);
					}
				}
				free(conn->db->rows);
			}
			free(conn->db);
		}
		free(conn);
	}
}

void Database_create(struct Connection *conn, int MAX_DATA, int MAX_ROWS)
{
	conn->db->MAX_DATA = MAX_DATA;
	conn->db->MAX_ROWS = MAX_ROWS;

	int i = 0;
	void *ref = NULL;
	int len = conn->db->MAX_DATA+1;
	struct Address *addr = NULL;
	conn->db->rows = malloc_and_die(sizeof(conn->db->rows)*MAX_ROWS, conn);
	for (i = 0; i < conn->db->MAX_ROWS; i++){
		addr = conn->db->rows[i] = malloc_and_die(sizeof(struct Address), conn);

		addr->id = i;
		addr->set = 0;
		addr->name = malloc_and_die(len, conn);
		ref = memset(addr->name, '\0', len);
		if (!ref) die("Memory error", conn);

		addr->email = malloc_and_die(len, conn);
		ref = memset(addr->email, '\0', len);
		if (!ref) die("Memory error", conn);
	}
}

void Database_set(struct Connection *conn, int id, const char *name, const char *email)
{
	struct Address *addr = conn->db->rows[id];
	if (addr->set) die("Already set, delete it first.", conn);

	addr->set = 1;
	char *res = strncpy(addr->name, name, conn->db->MAX_DATA);
	// demonstrate the strncpy bug
	if (!res) die("Name copy failed", conn);
	// append null char
	addr->name[conn->db->MAX_DATA] = '\0';

	res = strncpy(addr->email, email, conn->db->MAX_DATA);
	if (!res) die("Email copy failed", conn);
	addr->email[conn->db->MAX_DATA] = '\0';
}

void Database_get(struct Connection *conn, int id)
{
	struct Address *addr = conn->db->rows[id];

	if (addr->set){
		Address_print(addr);
	}else{
		die("ID is not set", conn);
	}
}

void Database_delete(struct Connection *conn, int id)
{
	conn->db->rows[id]->set = 0;
	conn->db->rows[id]->name[0] = '\0';
	conn->db->rows[id]->email[0] = '\0';
}

void Database_list(struct Connection *conn)
{
	int i = 0;
	struct Database *db = conn->db;

	for (i = 0; i < conn->db->MAX_ROWS; i++){
		struct Address *cur = db->rows[i];

		if (cur->set){
			Address_print(cur);
		}
	}
}

int main(int argc, char *argv[])
{
	if (argc < 3) die("USAGE: ex17 <dbfile> <action> [action params]", NULL);

	char *filename = argv[1];
	char action = argv[2][0];
	struct Connection *conn = Database_open(filename, action);
	int id = 0;

	if (argc > 3 && action != 'c'){
		id = atoi(argv[3]);
		if (id >= conn->db->MAX_ROWS) die("There's not that many records.", conn);
	}

	switch (action){
		case 'c':
			if (argc != 5) die("Both MAX_DATA and MAX_ROWS are required", conn);
			Database_create(conn, atoi(argv[3]), atoi(argv[4]));
			Database_write(conn);
			break;

		case 'g':
			if (argc != 4) die("Need an id to get", conn);

			Database_get(conn, id);
			break;

		case 's':
			if (argc != 6) die("Need id, name, email to set", conn);

			Database_set(conn, id, argv[4], argv[5]);
			Database_write(conn);
			break;

		case 'd':
			if (argc != 4) die("Need id to delete", conn);

			Database_delete(conn, id);
			Database_write(conn);
			break;

		case 'l':
			Database_list(conn);
			break;
		default:
			die("Invalid action, only: c=create, g=get, d=del, l=list", conn);
	}

	Database_close(conn);

	return 0;
}
