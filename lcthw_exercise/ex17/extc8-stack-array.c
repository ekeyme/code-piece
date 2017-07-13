#include <stdio.h>
#include <assert.h>

#define MAX_SIZE 100

struct Stack
{
	int top;
	int node[MAX_SIZE];
};

struct Stack Init_stack()
{
	struct Stack stk = {.top=0};
	return stk;
}

int empty(struct Stack *stk)
{
	return stk->top == 0;
}

void push(struct Stack *stk, int x)
{
	assert(stk->top < MAX_SIZE);

	stk->node[stk->top] = x;
	stk->top++;
}

int pop(struct Stack *stk)
{
	int i = stk->node[stk->top];
	stk->top--;
	return i;
}


int main(int argc, char const *argv[])
{
	/* code */
	return 0;
}