import cv2
import numpy as np

from pixelation import read_write_video, to_gray_gauss_comparison


# new update memory matrix

# decay by const


def const_decay_memories(mat: np.ndarray, decay=-10):
    mat[np.where(mat < decay)] = 0
    mat[np.where(mat >= decay)] -= decay

    return mat


def add_weighted_at_mask(new_img: np.ndarray, memory_img: np.ndarray, mask: np.ndarray):
    # decay where mask and then add
    mask_not_zero_indices = mask[np.where(mask > 0)]

    decay_mask_location_with_right_shift(mask_not_zero_indices, memory_img)
    add_right_shifted_img(mask_not_zero_indices, memory_img, new_img)

    return memory_img


def decay_mask_location_with_right_shift(mask_not_zero_indices, memory_img):
    #right_shifted_mem = memory_img[mask_not_zero_indices] // 2
    #0print(right_shifted_mem)
    memory_img[mask_not_zero_indices] = memory_img[mask_not_zero_indices] // 2

# replace with addWeighted or other right_sight method. this method is too slow
def add_right_shifted_img(mask_not_zero_indices, memory_img, new_img):
    # right_shifted_img = new_img[mask_not_zero_indices] // 2
    #print(right_shifted_img)
    memory_img[mask_not_zero_indices] += new_img[mask_not_zero_indices] // 2


# add new photo with lowering by mask



def addition_memories(inpath, outpath):
    cap,vw = read_write_video(inpath, outpath)
    t, curr = cap.read()

    memory_img = np.zeros(curr.shape, dtype=curr.dtype)
    prev = curr
    t, curr = cap.read()
    print('starting')
    i = 0
    while t:
        if i % 4 == 0:
            print(i)
        i += 1
        mask_of_weight_diff = to_gray_gauss_comparison(curr, prev, 13, 13)
        memory_img = add_weighted_at_mask(curr, memory_img, mask_of_weight_diff)
        cv2.imshow('render window', memory_img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
        vw.write(memory_img)
        prev = curr
        t, curr = cap.read()
    print('loop ended')
    vw.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    addition_memories('/Users/galgo/code/pixelation/4G6A3120.MP4', '/Users/galgo/code/pixelation/4G6A3120_fade2.MP4')

