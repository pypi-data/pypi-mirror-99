from replit import db
class Db():
  def __init__(self, name, data={}):
    self.name = name
    self.data = data
    
  def save(self, key_to_save):
    db[key_to_save] = self.data

  def __str__(self):
    toret = '\x1b[1m\x1b[4m' + self.name + '\n\x1b[0m'#.format('_'*len(self.name))
    for data in self.data:
      toret += str(data) + ': \n'
      for data2 in self.data[data]:
        toret += str(data2) + ': ' + str(self.data[data][data2]) + '; '
      toret += '\n--------\n'
    return toret
    
  def set(self, column, row, value):
    self.data[column][row] = value
    return self

  def delete_item(self, column, row):
    self.data[column][row] = None
    return self
  
  def delete_column(self, column):
    del self.data[column]

  def delete_row(self, row):
    for data in self.data:
      del self.data[data][row]

  def get_value(self, column, row):
    return self.data[column][row]

  def get_column(self, column):
    return self.data[column]

  def get_row(self, row):
    end = {}
    for info in self.data:
      end[info] = self.data[info][row]
    return end

  def add_column(self, name):
    self.data[name] = {}
    dat = self.data
    rownames = list(dat[list(dat.keys())[0]].keys())
    lstid = list(dat[list(dat.keys())[0]].values())[0]
    for i in rownames:
      if i == 'id':
        apndval = str(int(lstid)+1)
      else:
        apndval = ''
      self.data[name][i] = apndval
  
  def add_row(self, name):
    for iterr in self.data:
      self.data[iterr][name] = ''

  def __add__(self, value):
    new = self
    if type(value) != type(new):
      raise ValueError('Invalid operand(+) for types')
    for iter in value.data:
      new.data[iter] = value.data[iter]
    return new

  def __iter__(self):
    return iter(self.data)

  def __eq__(self, o):
    return self.__dict__ == o.__dict__

  def __bool__(self):
    return self.data != {}

  def __contains__(self, key):
    return key in self.data

  """def select(self, query=''):
    if query == '':
      return str(self)
    else:
      query = query.lower()
      for section in query.split('|'):
        if section.startswith('where'):
          params = section[6:]
          rlprms = eval(params)
          help(rlprms)"""

def make(name, column_names=[], row_names=[]):
  name = str(name)
  column_names = list(column_names)
  row_names = list(row_names)
  db_ = Db(name)
  db_.data = {}
  if row_names != []:
    row_names.insert(0, 'id')
  ids = 1
  for i in range(0, len(column_names)):
    j = column_names[i]
    db_.data[j] = ''
    rowws = {}
    for k in range(0, len(row_names)):
      m = row_names[k]
      if m == 'id':
        rowws[m] = str(ids)
      else:
        rowws[m] = ''
    ids += 1
    db_.data[j] = rowws
  return db_

def retrieve(name, key_saved):
  return Db(name, db[key_saved])