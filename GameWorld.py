import pickle


# 0번 레이어 - 배경
# 1번 레이어 - 캐릭터
# 2번 레이어 - 예비용
objects = [[], []]


def add_object(singleObj, layer):
    objects[layer].append(singleObj)


def add_objects(groupObj, layer):
    objects[layer] += groupObj

# 해당 객체 제거
def remove_object(singleObj):
    for i in range(len(objects)):
        if singleObj in objects[i]:
            objects[i].remove(singleObj)
            del singleObj
            break


# 해당 목록 제거
def delete_objects(groupObj):
    for i in range(len(objects)):
        for j in range(len(objects[i])):
            if groupObj == objects[i][j]:
                del objects[i][j]
                return


# 모든 객체 제거
def clear_objects():
    for singleObj in all_objects():
        del singleObj
    for groupObj in objects:
        groupObj.clear_object()

def destroy():
    clear_objects()
    objects.clear()

def erase_objects():
    global objects
    objects = [[], [], []]


# 모든 오브젝트 호출(yield)
def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def save():
    with open('game.sav', 'wb') as f:
        pickle.dump(objects, f)

def load():
    global objects
    with open('game.sav', 'rb') as f:
        objects = pickle.load(f)

