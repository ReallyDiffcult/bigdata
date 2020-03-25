from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    dict_num = {}
    for i in range(len(nums)):
        dict_num[nums[i]] = i
    for i in range(len(nums)):
        res = target - nums[i]
        if res in dict_num.keys() and i != dict_num[res]:
            return list([i, dict_num[res]])
if __name__ == '__main__':
    print(twoSum([3,3],6))
