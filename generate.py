import os
import random
import string
from collections import deque

import qrcode

random.seed(12333)

QR_DIR = 'qr'
IP = '51.250.1.88'
LEN = 8


def generate_image(text, filename):
    # img = qrcode.make(text)
    # if not os.path.exists(QR_DIR):
    #     os.makedirs(QR_DIR)
    # img.save(f"{QR_DIR}/{filename}.png")
    pass


def get_random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(LEN))


prev_id = 'entrypoint'
passed_ids = set()

# generate sequence first
for _ in range(316):
    new_id = get_random_id()
    generate_image(f'http://{IP}/{new_id}.png', prev_id)
    passed_ids.add(prev_id)
    prev_id = new_id

# now generate killer
new_id = get_random_id()
generate_image(f'ahhahha and here http://{IP}/{new_id}.png you script crashes lol', prev_id)
passed_ids.add(prev_id)
prev_id = new_id

# now walk a bit more
for _ in range(33):
    new_id = get_random_id()
    generate_image(f'http://{IP}/{new_id}.png', prev_id)
    passed_ids.add(prev_id)
    prev_id = new_id

LENGTH_LIMIT = 105

dead_ends = 0
middle = 0
split = 0
loops = 0

nodes = deque()

nodes.append((prev_id, 0))
iterations = 0

before_dead_end_nodes = []

while len(nodes) > 0 and iterations < 5000:
    r = random.random()
    node, idx = nodes.pop()
    print(iterations, idx)

    if idx > LENGTH_LIMIT or r > 0.99:
        # terminate
        dead_ends += 1
        before_dead_end_nodes.append(node)

    elif r < 0.1:
        # split
        next1 = get_random_id()
        next2 = get_random_id()
        generate_image(f'Beware it\'s a split, would you go /{next1}.png or /{next2}.png ?', node)
        nodes.append((next1, idx + 1))
        nodes.append((next2, idx + 1))
        split += 1

    elif r < 0.95:
        # straight
        next_point = get_random_id()
        generate_image(f'http://{IP}/{next_point}.png', node)
        nodes.append((next_point, idx + 1))
        middle += 1

    else:
        # make a loop
        next = random.choice(list(passed_ids))
        generate_image(f'http://{IP}/{next}.png', node)
        loops += 1

    iterations += 1

print(f'loops {loops}')
print(f'middle {middle}')
print(f'dead_ends {dead_ends}')
print(f'split {split}')
print(f'iterations {iterations}')
print(f'queue size {len(nodes)}')

random.shuffle(before_dead_end_nodes)
i = 0
code = get_random_id()
for node in before_dead_end_nodes:
    if i < LEN:
        generate_image(f'You\'ve find key [{i}], it\'s "{code[i]}", but what\'s next?', node)
    else:
        generate_image('Oh no, it\' a dead end!', node)
    i += 1

print(f'code is {code}')
# done ?
# add winnind slide
generate_image(f'http://{IP}/dooone.html', code)
