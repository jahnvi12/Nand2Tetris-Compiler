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
        if kind == 'STATIC':
            self.class_scope[name] = (type, 'STATIC' , self.static_count)
            self.static_count += 1
        elif kind == 'FIELD':
            self.class_scope[name] = (type, 'FIELD' , self.field_count)
            self.field_count += 1
        elif kind == 'ARG':
            self.subroutine_scope[name] = (type, 'ARG' , self.arg_count)
            self.arg_count += 1
        elif kind == 'VAR':
            self.subroutine_scope[name] = (type, 'VAR' , self.var_count)
            self.var_count += 1

      def VarCount(self, kind):
        if kind == 'ARG':
            return self.arg_count
        elif kind == 'VAR':
            return self.var_count
        elif kind == 'STATIC':
            return self.static_count
        elif kind == 'FIELD':
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
