def removeDuplicates(nums):
    if not nums:
        return 0
    
    i = 0  # Slow pointer
    for j in range(1, len(nums)):  # j is the fast pointer
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]
            
    # The unique elements are now at nums[0...i]
    return nums[:i+1]

a = [1, 1, 2, 2, 3]
print(removeDuplicates(a)) # [1, 2, 3]