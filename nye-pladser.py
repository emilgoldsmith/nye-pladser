#!/usr/bin/python3
from sys import argv
from random import randint
from csv import reader, writer

def in_pairing(name, pairing):
  for pair in pairing:
    if name in pair:
      return True
  return False

def make_pairing():
  pairing = []
  if len(index_to_name)%2:
    cnt = 0
    lone_student_index = randint(0, len(index_to_name)-1)
    while matrix[lone_student_index][lone_student_index]:
      lone_student_index = randint(0, len(index_to_name)-1)
      if cnt > 100:
        return False
    pairing.append((index_to_name[lone_student_index], index_to_name[lone_student_index]))
  for student in index_to_name:
    if in_pairing(student, pairing):
      continue
    partner_index = randint(0, len(index_to_name)-1)
    cnt = 0
    while (partner_index == name_to_index[student] or
        in_pairing(index_to_name[partner_index], pairing) or
        matrix[partner_index][name_to_index[student]]):
      partner_index = randint(0, len(index_to_name)-1)
      cnt += 1
      if cnt > 100:
        return False
    pairing.append((student, index_to_name[partner_index]))
  return pairing



index_to_name = []
name_to_index = {}
# Check if there is already a data file present
try:
  data = open('data.csv', 'r', newline='')
except IOError:
  data = False

if len(argv) == 1 and not data:
  name = input("Please input name of your student (write done when finished): ")
  while name != "done":
    index_to_name.append(name.strip())
    name = input("Please input name of your student (write done when finished): ")
  matrix = [[False for i in range(len(index_to_name))] for j in range(len(index_to_name))]
else:
  if not data:
    data_file_name = argv[2]
    try:
      data = open(data_file_name, 'r', newline='')
    except IOError:
      print("That file name does not exist in the current directory")
      exit()
  data_output = reader(data)
  matrix = []
  row_num = 0
  for row in data_output:
    if row_num == 0:
      index_to_name = row
    else:
      matrix.append(list(map(lambda x: x == 'x', row)))
    row_num += 1
  for i in range(len(matrix)):
    if len(matrix) != len(matrix[i]):
      print("The given csv file is not square dimensions")
      exit()
    for j in range(len(matrix)):
      if matrix[i][j] != matrix[j][i]:
        print("The given csv file is not symmetrical at 0-based indices {}, {}".format(i, j))
        exit()

for i in range(len(index_to_name)):
  name_to_index[index_to_name[i]] = i

pairing = make_pairing()
cnt = 0
while not pairing and cnt < 10000:
  pairing = make_pairing()
  cnt += 1

if not pairing:
  print("We're afraid we were unable to make a pairing for new seats")
else:
  for pair in pairing:
    index1 = name_to_index[pair[0]]
    index2 = name_to_index[pair[1]]
    matrix[index1][index2] = matrix[index2][index1] = True
  print("This is the pairing we made:")
  for pair in pairing:
    print("{} is paired with {}".format(pair[0], pair[1]))

