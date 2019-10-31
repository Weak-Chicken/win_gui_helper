import numpy as np


def array_conv2d(array, kernel, stride):
    if kernel.shape[0] > array.shape[0] or kernel.shape[1] > array.shape[1]:
        return np.nan
    if stride[0] > array.shape[0] - kernel.shape[0] or stride[1] > array.shape[1] - kernel.shape[1]:
        return np.nan

    step_x, step_y = stride
    array = np.pad(array,
                   ((0, (array.shape[0] - kernel.shape[0]) % step_x), (0, (array.shape[1] - kernel.shape[1]) % step_y)),
                   'constant', constant_values=(0, 0))
    result = []

    for i in range(0, array.shape[0] - kernel.shape[0] + 1, step_x):
        temp_res = []
        for j in range(0, array.shape[1] - kernel.shape[1] + 1, step_y):
            temp_res.append(np.sum(array[i:kernel.shape[0] + i, j:kernel.shape[1] + j] \
                                                                   * kernel[:, :]))
        result.append(np.array(temp_res))
    result = np.array(result)
    return result


def array_pooling(array, kernel_size, stride, mode="max_pooling"):
    if kernel_size[0] > array.shape[0] or kernel_size[1] > array.shape[1]:
        return np.nan
    if stride[0] > array.shape[0] - kernel_size[0] or stride[1] > array.shape[1] - kernel_size[1]:
        return np.nan

    step_x, step_y = stride
    array = np.pad(array,
                   ((0, (array.shape[0] - kernel_size[0]) % step_x), (0, (array.shape[1] - kernel_size[1]) % step_y)),
                   'constant', constant_values=(0, 0))
    result = []

    for i in range(0, array.shape[0] - kernel_size[0] + 1, step_x):
        temp_res = []
        for j in range(0, array.shape[1] - kernel_size[1] + 1, step_y):
            if mode == "max_pooling":
                temp_res.append(np.max(array[i:kernel_size[0] + i, j:kernel_size[1] + j]))
            elif mode == "avg_pooling":
                temp_res.append(np.mean(array[i:kernel_size[0] + i, j:kernel_size[1] + j]))
            else:
                raise NameError("Selected pooling method is not supported")
        result.append(np.array(temp_res))
    result = np.array(result)
    return result


if __name__ == "__main__":
    test_arr = np.array([range(0, 5), range(5, 10), range(10, 15), range(15, 20), range(20, 25)])
    kernel = np.array([(6, 2), (3, 5)])
    print(array_conv2d(test_arr, kernel, (2, 2)))
    print(array_pooling(array_conv2d(test_arr, kernel, (2, 2)), (2, 2), (1, 1), "avg_pooling"))
