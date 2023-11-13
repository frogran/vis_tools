# Pixelation

import cv2
import numpy as np


def read_write_video(inpath, outpath):
    cap = cv2.VideoCapture(inpath)

    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frm = cv2.VideoWriter_fourcc(*'mp4v')
    if outpath:
        vw = cv2.VideoWriter(outpath, frm, fps, (w,h), )
        return cap, vw
    return cap


def threshold_by_max(mask, mx = 255, threshold = cv2.THRESH_BINARY):
    m = np.max(mask)
    m *= 0.7
    r, res = cv2.threshold(mask, m, mx, threshold)
    res = np.uint8(res)
    return res


def gauss_comparison(curr, prev, blur_w = 9, blur_h = 9):
    g1 = cv2.GaussianBlur(curr, (blur_w, blur_h), 0)
    g2 = cv2.GaussianBlur(prev, (blur_w, blur_h), 0)
    return cv2.bitwise_xor(g1, g2)


def to_gray_gauss_comparison(curr, prev, blur_w = 9, blur_h = 9):
    gray1 = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    return gauss_comparison(gray1, gray2, blur_w, blur_h)
    

def color_gauss_comparison(curr, prev, blur_w = 9, blur_h = 9):
    burr = curr[:,:,0]
    brev = prev[:,:,0]
    bauss = gauss_comparison(burr, brev)

    gurr = curr[:,:,1]
    grev = prev[:,:,1]
    gauss = gauss_comparison(gurr, grev)

    rurr = curr[:,:,2]
    rrev = prev[:,:,2]
    rauss = gauss_comparison(rurr, rrev)

    new = np.zeros(curr.shape, curr.dtype)
    new[:,:,0] = bauss
    new[:,:,1] = gauss
    new[:,:,2] = rauss

    return new

def gauss_compare(curr, prev, blur_w = 9, blur_h = 9):
    diff = gauss_comparison(curr, prev, blur_w, blur_h)
    return threshold_by_max(diff)


def add_div_clip(img: np.ndarray, mask: np.ndarray, strength=0.8, decay=0.9):
    new_mat = img.astype(np.float64, order='K', copy=False)
    new_mat *= decay
    if not np.max(new_mat) == 0:
        new_mat /= np.max(new_mat)

    new_mat += (mask.astype(np.float64) * strength)
    np.clip(new_mat, 0.0, 255.0)

    result_mat = new_mat.astype(np.uint8, copy=False)
    return result_mat


def weigh_img_with_mask(curr, mask):
    pass


def next_memory(masked_img, memory_matrix):
    pass


def triple_gauss_comparison(curr, prev):
    #gauss = gauss_comparison()
    pass

def test_mask_strength():
    print('started color fading 20')
    cap, vw = read_write_video('noa_solo.mp4', '/Users/galgo/code/pixelation/noa_burning_memory6.MP4')
    t, curr = cap.read()
    y, x, c = curr.shape
    img_with_memories = np.zeros((y,x,c), dtype=curr.dtype)
    prev = curr
    t, curr = cap.read()
    while t:
        diff_weight = to_gray_gauss_comparison(curr, prev, 51, 51)
        # mask = gauss_comparison(curr, prev)
        # mem_matrix = add_div_clip(mem_matrix, diff_weight)

        # make matrix of images:
        # each img is added in weight to previous?
        # each img is multiplied by mask then added to memory matrix
        #curr = cv2.GaussianBlur(curr, (15, 15), 0)
        img_weighted_by_mask = cv2.bitwise_and(curr,curr, mask=diff_weight)
        # img_weighted_by_mask = weigh_img_with_mask(curr, diff_weight)
        img_with_memories = add_div_clip(img_with_memories, img_weighted_by_mask)
        cv2.imshow('show render', img_with_memories)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
        # color_matrix = cv2.cvtColor(mem_matrix, cv2.COLOR_GRAY2BGR)
        vw.write(img_with_memories)
        prev = curr
        t, curr = cap.read()
    print('finished loop')
    vw.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test_mask_strength()