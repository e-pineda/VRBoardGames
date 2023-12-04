import cv2
import numpy as np
# from scipy.spatial import distance as dist

MAX_PIXEL_VALUE = 255


# openCV documention
def to_gray_scale(img):
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayscale_img, 127, MAX_PIXEL_VALUE, cv2.THRESH_BINARY)
    thresh = cv2.GaussianBlur(thresh, (7, 7), 0)
    return thresh


def find_board(board):
    board_img = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    _, board_thresh = cv2.threshold(board_img, 127, MAX_PIXEL_VALUE, cv2.THRESH_BINARY_INV)
    move_slot_coords = find_move_slot_coords(board_thresh)
    return board_img, board_thresh, move_slot_coords


# finds corners of tictactoe board
# openCV documention
def find_corners(img):
    corners = cv2.cornerHarris(img, 5, 3, 0.1)
    corners = cv2.dilate(corners, None)
    corners = cv2.threshold(corners, 0.01 * corners.max(), MAX_PIXEL_VALUE, 0)[1]
    corners = corners.astype(np.uint8)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(corners, connectivity=4)
    return stats[1:, :2] #first point is center, so drop 


# finds the playable board
def find_and_mark_board_boundary(frame, thresh):
    corner_coords = find_corners(thresh)
    sorted_corners = sort_corners(corner_coords)

    # Get top down view of board
    frame = perspective_transform(frame, sorted_corners) 
    frame = frame[10:-10, 10:-10]

    for c in sorted_corners:
        formatted_corner = tuple((int(c[0]), int(c[1])))
        cv2.circle(frame, formatted_corner, 2, (255, 0, 0), 2)

    return frame


def find_move_slot_coords(img):
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sorted_cntrs = sorted(contours, key=lambda contour: cv2.contourArea(contour))
    center_middle = cv2.boundingRect(sorted_cntrs[-2])
    center_x, center_y, width, height = center_middle

    left = center_x - width
    right = center_x + width
    top = center_y - height
    bottom = center_y + height

    top_left = (left, top, width, height)
    top_center = (center_x, top, width, height)
    top_right = (right, top, width, height)

    center_left = (left, center_y, width, height)
    center_right = (right, center_y, width, height)

    bottom_left = (left, bottom, width, height)
    bottom_center = (center_x, bottom, width, height)
    bottom_right = (right, bottom, width, height)

    # Grid's coordinates
    return [top_left, top_center, top_right,
            center_left, center_middle, center_right,
            bottom_left, bottom_center, bottom_right]


def sort_corners(corners):
	# initialize a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype="float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = corners.sum(axis=1)
	rect[0] = corners[np.argmin(s)]
	rect[2] = corners[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(corners, axis=1)
	rect[1] = corners[np.argmin(diff)]
	rect[3] = corners[np.argmax(diff)]
	# return the ordered coordinates
	return rect

# presents img in top-down perspective
def perspective_transform(img, corners):
    tl, tr, br, bl  = corners

    # get dimensons of new image
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)

    height = int(round(max(heightA, heightB)))
    width = int(round(max(widthA, widthB)))

    # get coordinates of transformed image
    new_corners = np.array([
        # top  1, top 2, bottom 1, bottom 2
        [0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32)
    
    # compute perspective transform and apply it
    M = cv2.getPerspectiveTransform(corners, new_corners)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped


def draw_shape(img, shape, coords):
    x, y, w, h = coords
    if shape == 'X':
        cv2.line(img, (x + 10, y + 8), (x + w - 10, y + h - 8),
                 (0, 0, 0), 2)
        cv2.line(img, (x + 10, y + h - 8), (x + w - 10, y + 8),
                 (0, 0, 0), 2)
    else:
        centroid = (x + int(w / 2), y + int(h / 2))
        cv2.circle(img, centroid, 10, (0, 0, 0), 2)
       
    return img


