from turtle import title
import cv2
import matplotlib.pyplot as plt
import numpy as np


def region_of_interest(img, vertices, channels):
    # Define a blank matrix that matches the image height/width.
    # Retrieve the number of color channels of the image.
    mask = np.zeros_like(img)
    # Create a match color with the same color channel counts.
    channel_count = channels
    match_mask_color = (255,) * channel_count

    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)

    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    # If there are no lines to draw, exit.
    if lines is None:
        return    # Make a copy of the original image.
    # Create a blank image that matches the original in size.
    img = np.copy(img)
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8,
    )    # Loop over all lines and draw them on the blank image.
    for line in lines:
        for x1, y1, x2, y2 in line:
            # Merge the image with the lines onto the original.
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    # Return the modified image.
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    return img


if __name__ == "__main__":
    image = cv2.imread("C:/Users/edwin/Documents/uni/fun/vision/5.png")
    # get dimensions of image
    dimensions = image.shape

    # height, width, number of channels in image
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]

    region_of_interest_vertices = [
        (0, 0),
        (0, 300),
        (1700, height),
        (2500, height),
    ]

    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plt.figure()
    plt.imshow(grey_image)

    cannyed_image = cv2.Canny(grey_image,
                              100,
                              200)
    plt.figure()
    plt.imshow(cannyed_image)
    plt.title("Canny")

    cropped_image = region_of_interest(
        cannyed_image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
        channels
    )

    plt.figure()
    plt.imshow(cropped_image)

    lines = cv2.HoughLinesP(
        cropped_image,
        rho=5,
        theta=np.pi / 40,
        threshold=220,
        lines=np.array([]),
        minLineLength=750,
        maxLineGap=250
    )

    line_image = draw_lines(image, lines)
    plt.figure()
    plt.imshow(line_image)
    plt.show()
