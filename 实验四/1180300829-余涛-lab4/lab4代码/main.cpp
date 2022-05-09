#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <queue>
#include <stack>

using namespace std;

struct node			//the node of the set of storing all pattern strings.
{
	char current_ch;
	char pre_ch;
} pattern_set[100][100];

struct next_table_node		//next table's node
{
	int state;
	int character;
} next_table[256];

struct output_node		//output table's node
{
	int state;
	char str[100];
	bool available;
} output[256];

struct result_node		//result table's node
{
	int pos;
	int state;
}result[100];

queue<int>q;
int ch_appear[256];

int base[256];
int check[256];

int fail[256];
int current_state = 0;
int father_state = 0;

int to_insert[256];
int index = 0;
int cur_node_num = 0;
int next_table_node_num = 0;
int input_num = 0;
char input[100][100];
int jj = 0;
int current_pos;

void build_table();
int goto_func(int state, int c);
void fail_func();
void output_func();

int main()
{
	char pattern_path[50];// = "patterns.txt";
	char text_path[50];// = "test.txt";
	cout << "Please input the patterns' path:";
	cin >> pattern_path;
	cout << "Please input the test's path:";
	cin >> text_path;
	FILE* file = freopen(pattern_path, "r", stdin);
	memset(input, 0, sizeof(input));
	int row_len;
	int i = 0;
	cout << endl;
	cout << "All patterns are as follows:" << endl;
	while (!feof(file))			//build pattern strings table
	{
		scanf(" %s", input[i]);
		row_len = strlen(input[i]);
		for (int j = 0; j < row_len; j++)
		{
			pattern_set[i][j].current_ch = input[i][j];
			cout << pattern_set[i][j].current_ch;
			if (!j)
				pattern_set[i][j].pre_ch = 0;
			else
				pattern_set[i][j].pre_ch = pattern_set[i][j - 1].current_ch;
		}
		i++;
		cout << endl;
	}
	input_num = i;
	memset(ch_appear, 0, sizeof(ch_appear));
	for (int i = 0; i < input_num; i++)//initialize
	{
		ch_appear[pattern_set[i][0].current_ch] = 1;
	}
	for (int j = 0; j < 256; j++)
	{
		if (ch_appear[j])
		{
			q.push(j);
			to_insert[index++] = j;
		}
	}
	cur_node_num = index;
	build_table();

	int k = 1;
	while (!q.empty())
	{
		memset(ch_appear, 0, sizeof(ch_appear));
		int qhead = q.front();
		q.pop();
		cur_node_num--;
		for (int i = 0; i < input_num; i++)
		{
			if (pattern_set[i][k].current_ch == 0)
				continue;
			if (qhead == pattern_set[i][k].pre_ch)
				ch_appear[pattern_set[i][k].current_ch] = 1;
		}
		for (int j = 0; j < 256; j++)
		{
			if (ch_appear[j])
			{
				q.push(j);
				to_insert[index++] = j;
				next_table_node_num++;
			}
		}
		build_table();
		if (!cur_node_num)
		{
			cur_node_num = next_table_node_num;
			k++;
			next_table_node_num = 0;
		}
	}
	cout << "next table:" << endl;
	for (int i = 0; i <= 12; i++)
	{
		cout << next_table[i].state << " ";
	}
	cout << endl;
	cout << "base table:" << endl;
	for (int i = 0; i <= current_state; i++)
	{
		cout << base[i] << " ";
	}
	cout << endl;
	cout << "check table:" << endl;
	for (int i = 0; i <= 12; i++)
	{
		cout << check[i] << " ";
	}
	fail_func();
	cout << endl;
	cout << "fail:" << endl;
	for (int i = 0; i <= current_state; i++)
	{
		cout << fail[i] << " ";
	}
	output_func();
	char text[100];
	cout << endl;
	file = freopen(text_path, "r", stdin);
	fgets(text, 100, file);
	cout << "The text to be matched is:";
	cout << text << endl;
	int nowState = goto_func(0, text[0]);
	//printf("%d ", nowState);
	result[jj].state = nowState;
	result[jj++].pos = 1;
	for (current_pos = 1; current_pos < (int)strlen(text); current_pos++)
	{
		nowState = goto_func(nowState, text[current_pos]);
		//printf("%d ", nowState);
		result[jj].state = nowState;
		result[jj++].pos = current_pos + 1;
	}
	cout << "\nAll detected patterns are as follows:" << endl;
	for (int j = 0; j < jj; j++)
	{
		for (int i = 0; i <= current_state; i++)
		{
			if (output[i].available == 1 && output[i].state == result[j].state)
				cout << result[j].pos - strlen(output[i].str) << "    " << output[i].str << endl;
		}
	}
	getchar();
	fclose(stdin);
	return 0;
}

void build_table()		//build next table,base table and check table
{
	int j = 1;
	for (; j < 256; j++)
	{
		if (!next_table[j].state)
			break;
	}
	base[father_state] = j - (to_insert[0]);
	bool flag = 1;
	while (flag)
	{
		int p = 0;
		for (; p < index; p++)
		{
			if ((next_table[base[father_state] + to_insert[p]].state) != 0)
				break;
		}
		if (p == index)
			flag = 0;
		else
			base[father_state]++;
	}
	for (int i = 0; i < index; i++)
	{
		next_table[base[father_state] + to_insert[i]].state = ++current_state;
		next_table[base[father_state] + to_insert[i]].character = to_insert[i];
		check[current_state] = father_state;
	}

	memset(to_insert, 0, sizeof(0));
	index = 0;
	father_state++;
}

void fail_func()			//build failure table
{
	for (int i = 0; i <= current_state; i++)
	{
		if (!check[i]) continue;
		else
		{
			for (int j = 0; j < 256; j++)
			{
				if (next_table[j].state == i)
				{
					fail[i] = goto_func(fail[check[i]], next_table[j].character);
					break;
				}
			}
		}
	}
}

int goto_func(int state, int c)			//build goto function
{
	int t = next_table[base[state] + c].state;
	if (check[t] == state)
		return t;
	else if (state == 0)
		return 0;
	else
	{
		result[jj].state = fail[state];
		result[jj++].pos = current_pos;
		return goto_func(fail[state], c);
	}
}

void output_func()			//build output function
{
	char keng1[256];
	for (int i = 1; i <= current_state; i++)
	{
		memset(keng1, 0, sizeof(keng1));
		output[i].state = i;
		int temp = i;
		int _num = 0;
		while (temp)
		{
			for (int j = 0; j < 256; j++)
			{
				if (temp == next_table[j].state)
				{
					keng1[_num++] = next_table[j].character;
					break;
				}
			}
			temp = check[temp];
		}
		int k = 0;
		for (int p = _num - 1; p >= 0; p--)
		{
			output[i].str[k++] = keng1[p];
		}
		for (int q = 0; q < input_num; q++)
		{
			if (!strcmp(input[q], output[i].str))
			{
				output[i].available = 1;
				break;
			}
		}
	}
}
