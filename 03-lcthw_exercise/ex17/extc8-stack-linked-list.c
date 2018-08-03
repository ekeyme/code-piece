#include <stdio.h>
#include <errno.h>
#include <assert.h>
#include <stdlib.h>


struct Node
{
	int head;
	struct Node *tail;
};


struct Stack
{
	int size;
	struct Node *node;
};


void free_node(struct Node *node)
{
	if (node){
		if (node->tail){
			free_node(node->tail);
		}
		free(node);
	}
}


void free_stk(struct Stack *stk)
{
	if (stk){
		if (stk->node){
			free_node(stk->node);
		}
		free(stk);
	}
}


void die(const char *msg, struct Stack *stk)
{
	if (errno){
		perror(msg);
	}else{
		printf("ERROR: %s\n", msg);
	}

	free_stk(stk);
	exit(1);
}


void *malloc_and_die(size_t size, struct Stack *stk)
{
	void *prt = malloc(size);
	if (!prt) die("Memory error", stk);
	return prt;
}


struct Stack *Init_stack()
{
	struct Stack *stk = malloc_and_die(sizeof(struct Stack), NULL);
	stk->size = 0;
	stk->node = NULL;
	return stk;
}


int empty(struct Stack *stk)
{
	return stk->size == 0;
}


void push(struct Stack *stk, int x)
{
	struct Node *node = malloc_and_die(sizeof(struct Node), stk);
	node->head = x;
	node->tail = stk->node;
	stk->node = node;
	stk->size++;
}


int pop(struct Stack *stk)
{
	if (empty(stk)){
		die("stack is empty", stk);
	}

	stk->size--;
	struct Node *node = stk->node;
	int x = node->head;
	stk->node = node->tail;
	free(node);
	return x;
}


int main(int argc, char const *argv[])
{
	struct Stack *stk = Init_stack();
	assert(empty(stk));

	push(stk, 1);
	push(stk, 2);

	printf("%d\n", pop(stk));
	printf("%d\n", pop(stk));
	assert(empty(stk));
	push(stk, 3);
	printf("%d\n", pop(stk));
	free_stk(stk);
	return 0;
}
