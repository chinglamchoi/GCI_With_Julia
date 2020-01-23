# This program aims to find all primes from 1 to n

# Instead of using recursion, I use the Sieve of Eratosthenes, an O(n(log n)(log log n)) time complexity algorithm for efficiency

# The Sieve of Eratosthenes iteratively marks the multiples of each prime number as composites, starting with the first prime number, 2.


function get_primes(a)
	result, loprime, p = Array{Int64}(undef, 1), fill(true, a+1), 2
	while p*p <= a
		if loprime[p] == true
			for i in p*p:a
				if i % p == 0
					# divisible = not prime
					loprime[i] = false
				end
			end
		end
		p += 1 #check next
	end
	for p in 2:a-1
		if loprime[p] # print primes (verified to be true)
			append!(result, p)
		end
	end
	return result
end

a = parse(Int64, readline())
result = get_primes(a)
print("Primes from 1 to 100 are: ", result[2:end])
