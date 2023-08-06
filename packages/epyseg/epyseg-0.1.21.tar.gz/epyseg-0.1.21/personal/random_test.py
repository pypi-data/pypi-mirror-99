# random test?
# always in same way
# test of that ???

# ça marche et c'est plus simple que ce que je faisais en fait --> utiliser ça pr éviter les pbs



import random


test = [1,2,3,4,5,6,7]

from datetime import datetime

seed = datetime.now()
random.seed(seed)

print(seed)
print(seed)

random.seed(seed)
print(random.choice(test))
random.seed(seed)
print(random.choice(test))


seed = datetime.now()
random.seed(seed)

random.seed(seed)
print(random.choice(test))
random.seed(seed)
print(random.choice(test))


# better idea --> no need to pass in the parameters and can really do the stuff anywhere then --> good idea