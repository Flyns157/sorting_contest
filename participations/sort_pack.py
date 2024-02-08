def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def quicksort_wr(arr):
    if len(arr) <= 1:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        low, high = stack.pop()
        if high - low < 1:
            continue
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        stack.append((low, i))
        stack.append((i + 2, high))
    return arr

# MergeSort in Python
def mergeSort(L):
    array=L[:]
    if len(array) > 1:
        #  r is the point where the array is divided into two subarrays
        r = len(array)//2
        L = array[:r]
        M = array[r:]
        # Sort the two halves
        L=mergeSort(L)
        M=mergeSort(M)
        i = j = k = 0
        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        while i < len(L) and j < len(M):
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1
        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1
        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1
    return array

def mergesort_wr(arr):
    def merge_wr(left, right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]
    left = mergesort_wr(left)
    right = mergesort_wr(right)
    return merge_wr(left, right)

def heapsort_wr(arr):
    def heapify_wr(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify_wr(arr, n, largest)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify_wr(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_wr(arr, i, 0)
    return arr

def heapsort(arr):
    def heapify(arr, n, i):
        j = i
        while True:
            left = 2 * j + 1
            right = 2 * j + 2
            if left >= n:
                break
            if right >= n:
                if arr[j] < arr[left]:
                    arr[j], arr[left] = arr[left], arr[j]
                break
            if arr[left] > arr[right]:
                if arr[j] < arr[left]:
                    arr[j], arr[left] = arr[left], arr[j]
                    j = left
                else:
                    break
            else:
                if arr[j] < arr[right]:
                    arr[j], arr[right] = arr[right], arr[j]
                    j = right
                else:
                    break
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        j = 0
        while True:
            left = 2 * j + 1
            right = 2 * j + 2
            if left >= i:
                break
            if right >= i:
                if arr[j] < arr[left]:
                    arr[j], arr[left] = arr[left], arr[j]
                break
            if arr[left] > arr[right]:
                if arr[j] < arr[left]:
                    arr[j], arr[left] = arr[left], arr[j]
                    j = left
                else:
                    break
            else:
                if arr[j] < arr[right]:
                    arr[j], arr[right] = arr[right], arr[j]
                    j = right
                else:
                    break
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    for i in range(len(arr)-1):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def bubble_sort(arr):
    n=len(arr)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if arr[i-1] > arr[i]:
                arr[i-1], arr[i] = arr[i], arr[i-1]
                swapped = True
        n -= 1
    return arr

# def smoothsort(arr):
#     def sift(p, n):
#         while p > 1:
#             if arr[p-2] <= arr[p-1]:
#                 p -= 1
#             else:
#                 arr[p-2], arr[p-1] = arr[p-1], arr[p-2]
#                 p = 2*p if p-1 <= n/2 else 2*(p-1)
#     # Build the initial Leonardo heap
#     q = []
#     p = 1
#     r = -1
#     t = 0
#     for i in range(len(arr)):
#         if (p & 3) == 3:
#             q.append(p)
#             q.append(p+1)
#             t += 1
#         elif (p & 1) == 1:
#             if i != 0:
#                 q.append(r)
#             r = p
#         p >>= 1
#     for i in reversed(q):
#         sift(i, len(arr))
#     # Perform the downward sifting phase
#     for i in range(len(arr)-1, 0, -1):
#         if q[t-1] == i:
#             t -= 1
#             sift(q[t], i)
#         else:
#             sift(1, i)
#         arr[0], arr[i] = arr[i], arr[0]

def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        end -= 1
        swapped = False
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr

def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while gap > 1 or swapped:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
        i = 0
        swapped = False
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
            i += 1
        if not swapped and gap == 1:
            break
    return arr

def odd_even_sort(arr):
    n = len(arr)
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted = False
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted = False
    return arr

def intercalary_sort2(L: list[int]) -> list[int]:
    sorted_list = [L[0]]
    for i in L[1:]:
        left = 0
        right = len(sorted_list) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_list[mid] < i:
                left = mid + 1
            else:
                right = mid - 1
        sorted_list.insert(left, i)
    return sorted_list

def intercalary_sort3(L: list[int]) -> list[int]:
    sorted_list = [L[0]]
    for i in range(1,len(L)):
        left = 0
        right = len(sorted_list) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_list[mid] < L[i]:
                left = mid + 1
            else:
                right = mid - 1
        sorted_list.insert(left, L[i])
    return sorted_list

def test(L):return L