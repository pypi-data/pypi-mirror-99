import cv2
import nudged
import numpy as np

# ShiTomasi corner detection
feature_params = dict(maxCorners = 30, 
                    qualityLevel = 0.6, 
                    minDistance = 30, 
                    blockSize = 100)

# Lucas Kanade optical flow
lk_params = dict(winSize = (20,20), 
               maxLevel = 15, 
               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 0.05))


def rot_matrix(theta, inv=False):
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    if inv:
        R = R.T
    return R


def affine_matrix(theta, tx, ty, scale=1, R_inv=False):
    R = rot_matrix(theta, R_inv)
    R_s = (scale * np.identity(2)) @ R
    T = np.array([tx, ty])
    A = np.hstack([R_s, T[None,:].T])
    return A


def estimate_params(p1, p2):
    trans = nudged.estimate(p1, p2)
    tx, ty = trans.get_translation()
    theta, scale = trans.get_rotation(), trans.get_scale()
    return theta, tx, ty, scale


def get_p3(p1, theta, tx, ty, scale=1):
    A = affine_matrix(theta, tx, ty, scale)
    p3 = np.array([A @ [x1, y1, 1] for (x1, y1) in p1])
    return p3


def get_r(p1, p2):
    x, y = (p1 - p2).T       
    r = np.sqrt(x**2 + y**2)
    return r


def get_mask_r(r, quantile=1.5):
    # median and standard deviation of distance population
    r_median, r_std = np.median(r), np.std(r)
    # cutoff used to filter far features points
    bound = max(1, quantile * r_std)
    # get mask for nearby points
    mask = r < r_median + bound
    return mask


def delete_far_points(p1, p2, p3=None, quantile=1.5):
    # distance amoung p1 and p2, or p2 and p3
    r = get_r(p1, p2) if p3 is None else get_r(p2, p3)
    # mask that filters outliers for a given quantile value
    mask = get_mask_r(r, quantile)
    # delete far points
    p1, p2 = p1[mask], p2[mask]
    return p1, p2


def estimate_matrix(p1, p2, quantile1=None, quantile2=None):
    # validate tracked features deletting outliers
    if quantile1 is not None:
        p1, p2 = delete_far_points(p1, p2, quantile=quantile1)

    # estimate matrix parameters and transformed features
    affine_params = estimate_params(p1, p2)
    p3 = get_p3(p1, *affine_params)

    # delete outliers considering transformed features
    if quantile2 is not None:
        p1, p2 = delete_far_points(p1, p2, p3, quantile=quantile2)
        affine_params = estimate_params(p1, p2)
        p3 = get_p3(p1, *affine_params)

    p = p1, p2, p3
    theta, tx, ty, scale = affine_params
    return p, affine_params


def get_mse(p2, p3):
    x, y = (p2 - p3).T
    r_2 = np.mean(x**2 + y**2)
    mse_r = np.sqrt(r_2)

    x_2, y_2 = np.mean(x**2), np.mean(y**2)
    mse_x, mse_y = np.sqrt(x_2), np.sqrt(y_2)
    
    return mse_r, mse_x, mse_y


def get_affine(img1, img2, region, mask=None):
    x0, xf, y0, yf = region
    err = None

    # get main regions
    img1_ = img1[y0:yf, x0:xf, :]
    img2_ = img2[y0:yf, x0:xf, :]

    if mask is not None:
        mask = mask[y0:yf, x0:xf]

    # convert to grayscale
    img1_gray = cv2.cvtColor(img1_, cv2.COLOR_BGR2GRAY)                    
    img2_gray = cv2.cvtColor(img2_, cv2.COLOR_BGR2GRAY)
   
    # equalize histograms to improve contrast
    img1_gray = cv2.equalizeHist(img1_gray)
    img2_gray = cv2.equalizeHist(img2_gray)

    # track good features
    p1_ = cv2.goodFeaturesToTrack(img1_gray, mask=mask, **feature_params)
    p2_, st, _ = cv2.calcOpticalFlowPyrLK(img1_gray, img2_gray, p1_, None, **lk_params)

    # change origin and select tracked points
    p1, p2 = p1_ + [x0, y0], p2_ + [x0, y0]
    p1_good, p2_good = p1[st==1], p2[st==1]

    # cancel estimation if no good points were found or tracked
    if p1_good.size == 0:
        print('[ERROR] No good points were found or sucessfully tracked.')
        return 3*(0,), 3*(0,), err
        
    # estimate points and matrix
    p_good, affine_params = estimate_matrix(p1_good, p2_good, quantile1=1.5, quantile2=1.5)
    p1_good, p2_good, p3_good = p_good

    # mean square error
    err, *_ = get_mse(p2_good, p3_good)

    return p_good, affine_params, err
