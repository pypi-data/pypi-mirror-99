from environment import BaseEnvironment

class GamblerEnvironment(BaseEnvironment):
    def __init__(self):
      pass

    def env_init(self, env_info={}):
      self.n = env_info.get("n",100)
      self.p_h = env_info.get("p_h",0.4)
      
      self.states = list(range(self.n+1))            
      self.terminal_states = [0,self.n]     
      self.actions = list(range(self.n//2+1))      
    
    def env_state_transition_two_args(self, s, a):
      
      if s in self.terminal_states:
        return [(s,0,1)]      
    
      #If the action is impossible, return 0 probability
      if a > s or a > self.n-s:
        return []
      
      if a+s >= self.n:
        r = 1
      else:
        r = 0    
      return [(s-a,0,1-self.p_h),(min(s+a,self.n), r, self.p_h)]
