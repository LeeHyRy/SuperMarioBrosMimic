# 0번 레이어 - 배경
# 1번 레이어 - 캐릭터

objects = [[], [], []]


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


# 모든 객체 제거
def clear_objects():
    for singleObj in all_objects():
        del singleObj
    for groupObj in objects:
        groupObj.clear_object()


def destroy():
    clear_objects()
    objects.clear()


# 모든 오브젝트 호출(yield)
def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o
