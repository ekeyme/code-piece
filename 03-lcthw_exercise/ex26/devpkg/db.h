#ifndef _db_h
#define _db_h

#define DB_FILE "/tmp/.devpkg/db"
#define DB_DIR "/tmp/.devpkg"

int DB_init();
int DB_list();
int DB_update(const char *url);
int DB_find(const char *url);

#endif