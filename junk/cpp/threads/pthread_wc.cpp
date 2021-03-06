
/* https://computing.llnl.gov/tutorials/pthreads/ */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>

#if 0
#include <string>
using std::string;
#endif

/*
 * find ~/src/pytof -name '*.py' -o -name '*.cpp' | /usr/bin/time xargs wc -l
 */

int total = 0;
pthread_mutex_t mutexsum;

void *lc(void *fn_void)
{
   int lines = 0;
   char* fn = (char*) fn_void;
   struct stat st;
   stat(fn, &st);

   // char* buffer = new char[st.st_size+1];
   char* buffer = (char*) calloc(st.st_size + 1, sizeof(char));
   FILE* fo = fopen(fn, "r");
   fread(buffer, 1, st.st_size, fo);
   // buffer[st.st_size] = '0';

#if 1
   char* start = buffer;
   for (;;) {
	   start = strchr(start, '\n');
	   if (start == NULL) break;
	   start++;
	   lines += 1;
   }
#else
   string in(buffer);
   size_t start = 0;
   size_t end;
   while ((end = in.find('\n', start)) != string::npos) {
 	   lines += 1;
	   start = end + 1;
   }
#endif

   pthread_mutex_lock (&mutexsum);
   total += lines;
   printf("%10d %s\n", lines, fn);
   pthread_mutex_unlock (&mutexsum);
   
   // delete [] buffer;
   free(buffer);
   fclose(fo);
   pthread_exit(NULL);
}

int main (int argc, char *argv[])
{
   pthread_t threads[argc];
   void *status;
   int rc;
   unsigned t;

   pthread_mutex_init(&mutexsum, NULL);

   for(t = 1; t < argc; t++){
      // printf("In main: creating thread %d\n", t);
      rc = pthread_create(&threads[t], NULL, lc, (void *) argv[t]);
      if (rc){
         printf("ERROR; return code from pthread_create() is %d\n", rc);
         exit(-1);
      }
   }

   // Join
   for(t = 1; t < argc; t++){
      rc = pthread_join(threads[t], &status);
      if (rc){
         printf("ERROR; return code from pthread_join() is %d\n", rc);
         exit(-1);
      }
   }
   printf("%10d total\n", total);

   pthread_mutex_destroy(&mutexsum);
   pthread_exit(NULL);
}

