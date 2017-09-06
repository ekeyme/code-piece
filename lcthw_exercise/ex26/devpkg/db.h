#ifndef _db_h
#define _db_h

#define DB_FILE "/home/mozz/vm-share/.devpkg/db"
#define DB_DIR "/home/mozz/vm-share/.devpkg"

int DB_init();
int DB_list();
int DB_update(const char *url);
int DB_file(const char *url);

#endif