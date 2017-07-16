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

	stk->node[stk->top++] = x;
}

int pop(struct Stack *stk)
{
	assert(!empty(stk));
	
	int i = stk->node[--stk->top];
	return i;
}


int main(int argc, char const *argv[])
{
	struct Stack stk = Init_stack();
	struct Stack *stkp = &stk;
	assert(empty(stkp));

	push(stkp, 1);
	push(stkp, 2);

	printf("%d\n", pop(stkp));
	printf("%d\n", pop(stkp));
	assert(empty(stkp));
	pop(stkp);
	return 0;
}