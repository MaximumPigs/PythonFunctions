# Return a Prefix Sum List of an input List
def runningSum(self, nums: List[int]) -> List[int]:
    num_sum = 0
    out = []
    for num in nums:
        num_sum += num
        out.append(num_sum)
    return out