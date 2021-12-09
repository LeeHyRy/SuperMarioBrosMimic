def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    elif right_a < left_b: return False
    elif top_a < bottom_b: return False
    elif bottom_a > top_b: return False

    return True

# return값에 대하여
# 0         : 충돌하지 않음
# 1         : 상충돌
# 2         : 하충돌
# 3         : 좌충돌
# 4         : 우충돌
def collide_dir(norm, b):
    if not collide(norm, b): return 0

    left_n, bottom_n, right_n, top_n = norm.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    height = min(top_n, top_b) - max(bottom_n, bottom_b)
    if height < 2 * (top_b - bottom_b) / 5:
        if bottom_n < bottom_b: return 1
        else: return 2
    else:
        if left_n < left_b: return 4
        else: return 3
