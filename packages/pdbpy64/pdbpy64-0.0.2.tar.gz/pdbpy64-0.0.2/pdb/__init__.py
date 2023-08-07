class pydatabase():
  module = {}
  def set_value(self, name, value):
    self.module[name] = value
  def get_all_values(self):
    return self.module
  def get_value(self, name):
    return self.module[name]
  def save(self, filename):
    open(filename, 'w').write(f'{self.module}')
  
class pydatabase_from_file():
  module = {}
  def set_value(self, name, value):
    self.module[name] = value
  def get_all_values(self):
    return self.module
  def get_value(self, name):
    return self.module[name]
  def save(self, filename):
    open(filename, 'w').write(f'{self.module}')
  def load(self, name):
    exec(f'self.module = {open(name).read()}')
    


