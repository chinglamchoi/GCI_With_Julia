# This program uses Insertion Sort to sort numerical arrays

# Insertion Sort has a time complexity of O(n^2) (worst case = n*(n-1)/2 inversions) and is generally faster than quicksort and mergesort


function InsertionSort(a)
	for i in 1:length(a)
		b, c = a[i], i-1
		while c >= 1 && b < a[c]
			a[c+1] = a[c]
			c -= 1
		end
		a[c+1] = b
	end
	return a
end

a = readline()
a = split(a, " ")
a = [parse(Int64, i) for i in a]
sorted = InsertionSort(a)
println("Array sorted by Insertion Sort: ", sorted)
