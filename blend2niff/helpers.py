"""Helper methods."""


def correct_gamma(color):
    """Return gamma corrected rgb color. Keep alpha if any."""
    correct = [0.0]*len(color)

    # rgb
    correct[0] = pow(color[0], (1.0/2.2))
    correct[1] = pow(color[1], (1.0/2.2))
    correct[2] = pow(color[2], (1.0/2.2))

    # alpha
    if len(color) > 3:
        correct[3] = color[3]

    return correct
