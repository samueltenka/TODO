plural = lambda l: 's' if len(l) != 1 else ''
def make(todos, results):
    result=[]
    while True:
        i = input().replace('\t',' '*4)
        if i=='exit': break
        result.append(i)
    result = '\n'.join(result)
    if result[0]!='(': result = '(1.0) '+result
    todos.append(result)
    results[:] = []
    print('Item created.')
def search(todos, searchterms):
    '''AND of all searchterms'''
    results = []
    for i,t in enumerate(todos):
        for s in searchterms:
            if s.lower() not in t.lower(): break
        else: results.append((i,t))
    print('Found %d item%s:' % (len(results), plural(results)))
    for j,(i,r) in enumerate(results):
        print('\n%d. %s\n' % (j,r))
    return results
def delete(todos, results, hitlist):
    hitlist.sort(reverse=True)
    for h in hitlist:
        del todos[results[h][0]]
    results[:] = []
    print('Item%s deleted.' % plural(hitlist))
def complete(todos, results, i, fname='history'):
    index = results[i][0]
    with open(fname,'a') as f:
        f.write(todos[index]+'\n\t\n')
    del todos[index]
    print('Congratulations!!')
def priority_of(todo):
    assert(todo[0]=='(')
    close=todo.find(')')
    return float(todo[1:close])
def sort(todos):
    todos.sort(key=priority_of, reverse=True)
    print('Sorted %d item%s.' % (len(todos), plural(todos)))
def adjust(todos, results, adj):
    i,newscore = adj; i=int(i)
    index = results[i][0]
    oldscore = priority_of(todos[index])
    todos[index] = '(%s)%s' % (newscore, todos[index][todos[index].find(')')+1:])
    print('Adjusted score from %s to %s' % (str(oldscore),newscore))

def read(todos, fname='todo'):
    with open(fname) as f:
       todos[:] = [t for t in f.read().split('\n\t\n') if t]
def save(todos, fname='todo'):
    with open(fname,'w') as f:
       f.write('\n\t\n'.join(todos))
    print('Saved %d item%s.' % (len(todos), plural(todos)))
def givehelp(fname='help'):
    with open(fname) as f:
        print(f.read())

import sys
todo_name, history_name = sys.argv[1:3]

import os
todos = []
read(todos); sort(todos)
results=[]
while True:
    try:
       i = input()
       os.system('cls'); print('$',i)
       if i=='exit': save(todos, todo_name); break
       elif i=='make': make(todos, results); sort(todos)
       elif i=='save': save(todos, todo_name)
       elif i and i.split()[0]=='adj': adjust(todos, results, i[3:].split()); sort(todos)
       elif i and i.split()[0]=='del': delete(todos, results, [int(ii) for ii in i[3:].split()])
       elif i and i.split()[0]=='complete': complete(todos, results, int(i[8:]), history_name)
       elif i=='help': givehelp()
       else: results = search(todos, i.split())
    except Exception as E:
        print('Oops! Exception! %s' % str(E))
