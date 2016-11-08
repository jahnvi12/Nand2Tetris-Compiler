class SymbolTable:
      def __init__(self):
        self.field_count = 0
        self.static_count = 0
        self.arg_count = 0
        self.var_count = 0
        self.subroutine_scope = {}
        self.class_scope = {}

      def startSubroutine(self):
        self.subroutine_scope = {}
        self.arg_count = 0
        self.var_count = 0

      def currClass(self):
        for key,values in self.class_scope.items():
          if 'class' in values:
            return key

      def Define(self, name, type, kind):
        if kind == 'static':
            self.class_scope[name] = (type, 'static' , self.static_count)
            self.static_count += 1
        elif kind == 'field':
            self.class_scope[name] = (type, 'field' , self.field_count)
            self.field_count += 1
        elif kind == 'class':
            self.class_scope[name] = (type, 'class' , 0)
        elif kind == 'argument':
            self.subroutine_scope[name] = (type, 'argument' , self.arg_count)
            self.arg_count += 1
        elif kind == 'local':
            self.subroutine_scope[name] = (type, 'local' , self.var_count)
            self.var_count += 1

      def VarCount(self, kind):
        if kind == 'argument':
            return self.arg_count
        elif kind == 'local':
            return self.var_count
        elif kind == 'static':
            return self.static_count
        elif kind == 'field':
            return self.field_count
        else:
            return None

      def KindOf(self, name):
        if name in self.subroutine_scope.keys():
          return self.subroutine_scope[name][1]
        elif name in self.class_scope.keys():
          return self.class_scope[name][1]
        else:
          return None

      def TypeOf(self, name):
        if name in self.subroutine_scope.keys():
          return self.subroutine_scope[name][0]
        elif name in self.class_scope.keys():
          return self.class_scope[name][0]
        else:
          return None

      def IndexOf(self, name):
        if name in self.subroutine_scope.keys():
          return self.subroutine_scope[name][2]
        elif name in self.class_scope.keys():
          return self.class_scope[name][2]
        else:
          return None
